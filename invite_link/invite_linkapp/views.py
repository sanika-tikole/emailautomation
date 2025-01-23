'''from django.shortcuts import render
from django.http import JsonResponse
from .utils import send_student_email

def send_email_view(request):
    if request.method == 'POST':
        # Collect data from the POST request
        student_name = request.POST.get('student_name')
        student_email = request.POST.get('student_email')
        job_role = request.POST.get('job_role')
        zoom_link = request.POST.get('zoom_link')
        scheduled_time = request.POST.get('scheduled_time')

        # Send the email
        result = send_student_email(student_name, student_email, job_role, zoom_link, scheduled_time)
        return JsonResponse({"message": result})
    return render(request, 'invite_linkapp/send_email.html')'''
import re
import openpyxl
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.http import JsonResponse


def is_valid_email(email):
    """Validate email format using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def upload_excel_and_send_emails(request):
    if request.method == "POST":
        # Get the uploaded files and form data
        excel_file = request.FILES.get('excel_file')
        zoom_link = request.POST.get('zoom_link')
        interview_date = request.POST.get('interview_date')
        task_file = request.FILES.get('task_file')

        # Validate the form inputs
        if not excel_file or not zoom_link or not interview_date or not task_file:
            return JsonResponse({"error": "All fields are required."}, status=400)

        # Try to open and read the Excel file
        try:
            workbook = openpyxl.load_workbook(excel_file)
            sheet = workbook.active
        except Exception as e:
            return JsonResponse({"error": f"Error reading Excel file: {str(e)}"}, status=400)

        # Initialize counters and lists for tracking results
        invalid_emails = []
        failed_emails = []
        sent_emails = []

        # Iterate through rows and process
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
            # Log the row for debugging
            print(f"Processing row: {row}")

            # Extract required columns (first 3 columns)
            name = row[0] if len(row) > 0 else None
            email = row[1] if len(row) > 1 else None
            job_role = row[2] if len(row) > 2 else None

            # Skip rows with missing essential data
            if not name or not email or not job_role:
                print(f"Skipping row due to missing data: {row}")
                continue

            # Validate email and send
            if email and is_valid_email(email):
                try:
                    # Create the email content
                    subject = f"Interview Scheduled for {job_role}"
                    body = f"""
                    Hi {name},

                    Greetings!

                    You have been scheduled for an interview for the role of {job_role}.
                    Details:
                    - Zoom Meeting Link: {zoom_link}
                    - Interview Date: {interview_date}

                    Please find the attached task file for your reference.

                    Best regards,  
                    Your Company
                    """
                    # Send the email
                    email_message = EmailMessage(
                        subject=subject,
                        body=body,
                        from_email='your_email@gmail.com',
                        to=[email],
                    )
                    email_message.attach(task_file.name, task_file.read(), task_file.content_type)
                    email_message.send()
                    sent_emails.append(email)
                except Exception as e:
                    failed_emails.append(email)
                    print(f"Failed to send email to {email}: {str(e)}")
            else:
                invalid_emails.append(email)
                print(f"Invalid email: {email}")

        # Prepare a summary of the results
        result_summary = {
            "message": "Processing complete.",
            "sent_emails": sent_emails,
            "failed_emails": failed_emails,
            "invalid_emails": invalid_emails,
        }

        return JsonResponse(result_summary)

    # Render the file upload form
    return render(request, 'invite_linkapp/send_email.html')



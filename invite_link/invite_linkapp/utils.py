# # email_app/utils.py
# from django.core.mail import EmailMessage
# from django.conf import settings
# import os

# def send_student_email(student_name, student_email, job_role, zoom_link, scheduled_time):
#     # Email subject and body
#     subject = f"Interview Invitation for {job_role}"
#     body = f"""
#     Dear {student_name},

#     We are pleased to inform you that you have been shortlisted for an interview for the role of {job_role}.
#     Please find the meeting details below:

#     - Meeting Link: {zoom_link}
#     - Time: {scheduled_time}

#     Please join on time, and feel free to reach out if you have any questions.

#     Regards,
#     Team Name
#     """

#     # Define the file path for the attachment
#     excel_file_path = r"C:\Users\Admin\Desktop\screening\tableinfo.xlsx"  # Update the path as needed

#     # Send email
#     email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [student_email])
#     try:
#         # Attach file if it exists
#         if os.path.exists(excel_file_path):
#             email.attach_file(excel_file_path)
#         email.send()
#         return f"Email sent to {student_name} ({student_email})"
#     except Exception as e:
#         return f"Failed to send email to {student_name}. Error: {e}"

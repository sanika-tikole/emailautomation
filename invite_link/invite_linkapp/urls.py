from django.urls import path
# from .views import send_email_view

# urlpatterns = [
#     path('', send_email_view, name='send_email'),
# ]
from django.urls import path
from .views import upload_excel_and_send_emails

urlpatterns = [
    path('', upload_excel_and_send_emails, name='upload_excel_and_send_emails'),
]


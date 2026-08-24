from django.urls import path
from . import views

urlpatterns = [
    path('add-student/', views.add_student, name='add_student'),
    path('generate-qr/', views.generate_qr, name='generate_qr'),
    path('scan-attendance/', views.scan_attendance, name='scan_attendance'),
    path('send-alert/<int:student_id>/', views.send_alert, name='send_alert'),
    path('report/<int:teacher_id>/', views.download_monthly_report, name='report'),
    path('student/<str:student_code>/', views.student_quiz_gate, name='student_quiz_gate'),
    path('extra-info/<str:subject_name>/', views.extra_info_view, name='extra_info'),
]

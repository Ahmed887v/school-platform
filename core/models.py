from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models import Teacher, Student


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_subjects')

class Post(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_posts')
    content = models.TextField()
    attachment = models.FileField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(weeks=2))

class Quiz(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_quizzes')
    grade = models.CharField(max_length=50)
    group_number = models.IntegerField()
    questions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance')
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, default='Present')

class Alert(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_alerts')
    reason = models.TextField()
    alert_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

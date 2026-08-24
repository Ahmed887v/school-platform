from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models import Teacher, Student

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    # نضيف related_name مختلف لتجنب التعارض
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects_taught')  

class Post(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(weeks=2))

    def save(self, *args, **kwargs):
        if self.attachment and self.attachment.size > 10 * 1024 * 1024:
            raise ValueError("حجم المنشور يتجاوز 10 ميجا بايت")
        super().save(*args, **kwargs)

    @staticmethod
    def enforce_storage_limit():
        posts = Post.objects.all().order_by('created_at')
        total_size = sum(p.attachment.size for p in posts if p.attachment)
        while total_size > 60 * 1024 * 1024:
            oldest = posts.first()
            total_size -= oldest.attachment.size
            oldest.delete()

class Quiz(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.CharField(max_length=50)
    group_number = models.IntegerField()
    questions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, default='Present')

class Alert(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.TextField()
    alert_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


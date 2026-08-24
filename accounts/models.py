from django.db import models
from .utils.encryption import encrypt_data, decrypt_data

class Teacher(models.Model):
    teacher_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    national_id_encrypted = models.CharField(max_length=255, default='')
    phone_encrypted = models.CharField(max_length=255, default='')
    
    # غيرنا الاسم من subject إلى subject_name
    subject_name = models.CharField(max_length=100)  

    def save(self, *args, **kwargs):
        if not self.pk:  # عند الإنشاء فقط
            self.national_id_encrypted = encrypt_data(self.national_id_encrypted)
            self.phone_encrypted = encrypt_data(self.phone_encrypted)
        super().save(*args, **kwargs)

    def get_national_id(self):
        return decrypt_data(self.national_id_encrypted)

    def get_phone(self):
        return decrypt_data(self.phone_encrypted)

    def __str__(self):
        return self.name

class Student(models.Model):
    student_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    national_id_encrypted = models.CharField(max_length=255)
    group_number = models.IntegerField()
    phone_encrypted = models.CharField(max_length=255)
    father_phone_encrypted = models.CharField(max_length=255, blank=True)
    mother_phone_encrypted = models.CharField(max_length=255, blank=True)
    attendance_percentage = models.FloatField(default=100.0)
    warnings_count = models.IntegerField(default=0)
    accepted_rules = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.national_id_encrypted = encrypt_data(self.national_id_encrypted)
            self.phone_encrypted = encrypt_data(self.phone_encrypted)
            if self.father_phone_encrypted:
                self.father_phone_encrypted = encrypt_data(self.father_phone_encrypted)
            if self.mother_phone_encrypted:
                self.mother_phone_encrypted = encrypt_data(self.mother_phone_encrypted)
        super().save(*args, **kwargs)

    def get_phone(self):
        return decrypt_data(self.phone_encrypted)

    def __str__(self):
        return self.name

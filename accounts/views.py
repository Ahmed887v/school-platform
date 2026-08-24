from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Teacher, Student
from .utils.encryption import encrypt_data, decrypt_data
import uuid

# تسجيل دخول المعلم
def teacher_login(request):
    if request.method == 'POST':
        teacher_code = request.POST.get('teacher_code')
        teacher = Teacher.objects.filter(teacher_code=teacher_code).first()
        if teacher:
            # تسجيل دخول ناجح
            return redirect('admin_home', teacher_id=teacher.id)
        else:
            return render(request, 'login.html', {'error': 'كود المعلم غير صحيح'})
    return render(request, 'login.html')

# تسجيل دخول الطالب
def student_login(request):
    if request.method == 'POST':
        subject_code = request.POST.get('subject_code')
        student_code = request.POST.get('student_code')
        
        # التحقق من المادة والطالب
        student = Student.objects.filter(student_code=student_code).first()
        if student:
            # التحقق من أن هذه المادة تنتمي له (التحقق من الـ Subject Code)
            return redirect('student_quiz_gate', student_code=student.student_code)
        else:
            return render(request, 'login.html', {'error': 'كود الطالب غير صحيح'})
    return render(request, 'login.html')

# إنشاء حساب معلم جديد
def teacher_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        national_id = request.POST.get('national_id')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        
        # توليد كود فريد
        teacher_code = str(uuid.uuid4())[:8]
        
        Teacher.objects.create(
            name=name,
            national_id_encrypted=encrypt_data(national_id), # تشفير تلقائي
            phone_encrypted=encrypt_data(phone), # تشفير تلقائي
            subject=subject,
            teacher_code=teacher_code
        )
        # عرض الكود للمستخدم في رسالة
        return render(request, 'registration.html', {'success': f'تم إنشاء حسابك، كود المعلم هو: {teacher_code}'})
    
    return render(request, 'registration.html')

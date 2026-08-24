import qrcode
import json
import requests
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Post, Quiz, Attendance, Alert
from accounts.models import Student, Teacher

# دالة إضافة طالب
def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        grade = request.POST.get('grade')
        national_id = request.POST.get('national_id')
        group = request.POST.get('group')
        phone = request.POST.get('phone')

        # التحقق من وجود الطالب
        existing_student = Student.objects.filter(national_id_encrypted__iexact=encrypt_data(national_id)).first()
        if existing_student:
            # إرسال تنبيه للواجهة "الطالب مسجل سابقاً وكوده الفريد هو..."
            return JsonResponse({'status': 'exists', 'code': existing_student.student_code})

        # إنشاء كود فريد
        import uuid
        student_code = str(uuid.uuid4())[:8]
        Student.objects.create(
            name=name, grade=grade, national_id_encrypted=national_id,
            group_number=group, phone_encrypted=phone, student_code=student_code
        )
        return JsonResponse({'status': 'success', 'code': student_code})

# دالة إنشاء QR للحضور
def generate_qr(request):
    data = "ATTENDANCE_SESSION_#12345"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response['Content-Disposition'] = 'attachment; filename="attendance_qr.png"'
    return response

# تسجيل الحضور (عند مسح الطالب للرمز)
@csrf_exempt
def scan_attendance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_code = data.get('student_code')
        session_code = data.get('session_code')
        if session_code == "ATTENDANCE_SESSION_#12345":
            student = Student.objects.get(student_code=student_code)
            Attendance.objects.create(student=student, status='Present')
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

# إرسال تنبيه واتساب للطالب
def send_alert(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    reason = request.POST.get('reason')
    
    # حفظ التنبيه
    student.warnings_count += 1
    student.save()
    Alert.objects.create(student=student, reason=reason, alert_number=student.warnings_count)

    # إرسال واتساب (هنا يتم استدعاء API الخاصة بالواتساب)
    message = f"السلام عليكم، هذه الرسالة مرسله من الاستاذ {teacher.name} معلم مادة {teacher.subject} بشأن الطالب {student.name} حيث انه قد تم التنبيه عليه بشأن {reason} وهذا هو التنبيه رقم {student.warnings_count} وارجوا الا يتكرر الامر مرة اخري حتي لا يتم اتخاذ اجراء منع الطالب من الحضور مرة اخري,,,, شكرا"
    # (هنا يتم استدعاء API الخاصة بالواتساب مثل Twilio)
    requests.post("https://api.whatsapp.com/send?phone=..." , data={'text': message})
    
    return JsonResponse({'status': 'sent'})

# توليد التقرير الشهري PDF
def download_monthly_report(request, teacher_id):
    # تجميع البيانات
    attendance_percentage = 85.0
    warnings_count = 12
    quizzes_count = 5
    high_scores_percentage = 30
    total_profit = 15000
    net_profit = 12000
    profit_increase = 10.5

    # رسم بياني
    labels = ['Attendance', 'High Scores', 'Profit']
    values = [attendance_percentage, high_scores_percentage, net_profit]
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['green', 'blue', 'gold'])
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(100, 800, "Monthly Report")
    c.drawString(100, 750, f"Attendance: {attendance_percentage}%")
    c.drawString(100, 730, f"Warnings: {warnings_count}")
    c.drawString(100, 710, f"Net Profit: {net_profit} EGP")
    c.drawImage(img_buffer, 100, 400, width=300, height=200)
    c.showPage()
    c.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='monthly_report.pdf')

# دالة توجيه الطالب للاختبار قبل فتح أي حاجة
def student_quiz_gate(request, student_code):
    student = get_object_or_404(Student, student_code=student_code)
    active_quiz = Quiz.objects.filter(
        grade=student.grade,
        group=student.group_number,
        is_active=True
    ).first()
    
    if active_quiz:
        # منعه من أي حاجة، افتح الاختبار مباشرة
        return render(request, 'student/quiz_view.html', {'quiz': active_quiz})
    
    # لو مفيش اختبار، افتح الصفحة الرئيسية
    return render(request, 'student/student_home.html', {'student': student})

# (اختياري) دالة جلب معلومات إضافية (موجودة في ملف منفصل)
# من الأفضل استدعائها من هنا
def extra_info_view(request):
    return fetch_scientific_facts(request, "Physics") # مثال

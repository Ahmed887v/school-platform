import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_scientific_facts(request, subject_name):
    """
    (الميزة الإضافية): جلب معلومات علمية موثوقة كل يوم من الإنترنت.
    ملاحظة: البيانات لا تُحفظ في قاعدة البيانات، تُعرض للاطلاع العام فقط.
    """
    # 1. تحديد مصدر البيانات الموثوق (مثلاً ويكيبيديا أو موقع Nature أو NASA)
    # في هذا المثال، سنستخدم واجهة برمجية (API) عامة للمعلومات العلمية.
    url = f"https://api.api-ninjas.com/v1/facts?limit=3&subject={subject_name}"
    headers = {'X-Api-Key': 'YOUR_API_KEY'}  # يجب استبدال هذا بمفتاح حقيقي

    response = requests.get(url, headers=headers)
    
    facts = []
    if response.status_code == 200:
        data = response.json()
        # تحويل البيانات إلى قائمة نصوص
        for item in data:
            facts.append(item['fact'])
    else:
        # في حال فشل الاتصال، نعرض معلومات ثابتة عن المادة
        facts = ["المعلومات العلمية اليومية غير متاحة حالياً، حاول لاحقاً."]

    # 2. إرسال البيانات إلى القالب
    return render(request, 'student/extra_info.html', {
        'subject_name': subject_name,
        'facts': facts,
        'today': datetime.now().strftime("%A, %d %B %Y")
    })

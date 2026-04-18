# 🤖 اختبار API CVision AI System

ملف Python script لاختبار نظام مطابقة السير الذاتية مع الوظائف

## 📋 المتطلبات

```
pip install requests
```

## 🚀 كيفية الاستخدام

### 1️⃣ تشغيل الخادم أولاً

```
cd c:\Users\20100\Downloads\project
fastapi run code/app.py --port 8002 --host 127.0.0.1
```

### 2️⃣ تشغيل السكريبت (في terminal آخر)

```
cd c:\Users\20100\Downloads\project
python test_api.py
```

### 3️⃣ اختيار خيار من الخيارات التالية:

```
1. اختبار بنصوص مكتوبة مباشرة
   - اكتب نص السيرة الذاتية
   - اكتب وصف الوظيفة
   - اضغط Enter مرتين للإنهاء

2. اختبار برفع ملف CV
   - أدخل مسار ملف CV (PDF/DOCX)
   - أدخل نص وصف الوظيفة

3. اختبار بملفات نصية
   - أدخل مسار ملف السيرة الذاتية (txt)
   - أدخل مسار ملف وصف الوظيفة (txt)

4. خروج
```

## 📂 الملفات المرفقة

- `test_api.py` - السكريبت الرئيسي
- `sample_cv.txt` - نموذج سيرة ذاتية
- `sample_job.txt` - نموذج وصف وظيفة

## 🧪 اختبار سريع

استخدم الملفات المرفقة:

```bash
python test_api.py
# ثم اختر 3
# أدخل: sample_cv.txt
# أدخل: sample_job.txt
```

## 📊 النتيجة المتوقعة

```json
{
  "top_candidates": [
    {
      "Resume Index": 0,
      "Match Score": 85.5,
      "Level": "Senior",
      "Skill Score": 4,
      "Final Score": 77.35,
      "Strengths": ["Python", "SQL", "Machine Learning"],
      "Weaknesses": []
    }
  ]
}
```

## ⚙️ المعادلة المستخدمة

```
Final Score = (0.5 × Match Score) + (0.3 × Level Score) + (0.2 × Skill Score × 10)
```

- **Match Score** (50%): التشابه بين CV والوظيفة
- **Level Score** (30%): مستوى الخبرة (Senior=100, Mid=70, Junior=40)
- **Skill Score** (20%): عدد المهارات المطلوبة المتوفرة

## 🔍 المهارات المدقق عنها

- Python
- Java
- SQL
- Machine Learning
- Excel
- Power BI

## 📝 ملاحظات

- الخادم يجب أن يكون يعمل على `http://127.0.0.1:8002`
- يدعم ملفات PDF و DOCX و TXT
- يعيد أفضل 10 مرشحين
- الاختبار غير محدود - جرب عدة مرات

## 🆘 استكشاف الأخطاء

### خطأ: "لا يمكن الاتصال بالخادم"
```
تأكد من تشغيل:
fastapi run code/app.py --port 8002 --host 127.0.0.1
```

### خطأ: "الملف غير موجود"
```
تأكد من إدخال المسار الكامل للملف بشكل صحيح
مثال: C:\Users\20100\Downloads\project\sample_cv.txt
```

### خطأ: TimeoutError
```
تأكد من أن الخادم يعمل بشكل صحيح وجرب مرة أخرى
```

---

**تم إنشاؤه**: April 14, 2026
**Version**: 1.0

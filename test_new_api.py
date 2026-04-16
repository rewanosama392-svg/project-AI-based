"""
اختبار النسخة الجديدة من API
Test Script for New CVision API
"""

import requests
import json
import sys

API_URL = "http://127.0.0.1:8002"

def test_connection():
    """اختبار الاتصال"""
    try:
        response = requests.get(f"{API_URL}/", timeout=3)
        if response.status_code == 200:
            print("✅ الخادم يعمل!")
            return True
        else:
            print(f"❌ خطأ في الاتصال: {response.status_code}")
            return False
    except:
        print("❌ لا يمكن الاتصال بالخادم")
        print("تأكد من تشغيل: fastapi run code/app.py --port 8002 --host 127.0.0.1")
        return False

def analyze_text():
    """اختبار المطابقة بالنصوص"""
    print("\n" + "="*60)
    print("📝 اختبار المطابقة بالنصوص")
    print("="*60)
    
    cv = input("\n🎓 أدخل نص السيرة الذاتية: ").strip()
    job = input("💼 أدخل وصف الوظيفة: ").strip()
    
    if not cv or not job:
        print("❌ يجب إدخال النصوص!")
        return
    
    try:
        payload = {"cv_text": cv, "job_text": job}
        response = requests.post(f"{API_URL}/analyze", json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print_result(result)
        else:
            print(f"❌ خطأ: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ خطأ: {e}")

def analyze_file():
    """اختبار رفع ملف"""
    print("\n" + "="*60)
    print("📤 اختبار رفع الملف")
    print("="*60)
    
    file_path = input("\n📂 أدخل مسار ملف CV: ").strip()
    job = input("💼 أدخل وصف الوظيفة: ").strip()
    
    if not file_path or not job:
        print("❌ يجب إدخال البيانات!")
        return
    
    try:
        with open(file_path, 'rb') as f:
            files = {'cv_file': f}
            params = {'job_text': job}
            response = requests.post(
                f"{API_URL}/analyze-upload",
                files=files,
                params=params,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n📄 الملف: {result.get('filename')}\n")
            print_result(result.get('result', {}))
        else:
            print(f"❌ خطأ: {response.status_code}")
            print(response.text)
    except FileNotFoundError:
        print(f"❌ الملف غير موجود: {file_path}")
    except Exception as e:
        print(f"❌ خطأ: {e}")

def print_result(result):
    """طباعة النتائج بشكل منسق"""
    print("\n" + "="*60)
    print("🎯 النتائج")
    print("="*60)
    
    lexical = result.get('lexical_score', 0)
    semantic = result.get('semantic_score', 0)
    skills = result.get('skills_score', 0)
    final = result.get('final_score', 0)
    
    # عرض الدرجات
    print(f"\n📊 الدرجات:")
    print(f"  • Lexical Score (35%):  {lexical:>6.2f}%  {create_bar(lexical)}")
    print(f"  • Semantic Score (35%): {semantic:>6.2f}%  {create_bar(semantic)}")
    print(f"  • Skills Score (30%):   {skills:>6.2f}%  {create_bar(skills)}")
    print(f"\n  ✦ Final Score:          {final:>6.2f}%  {create_bar(final)}")
    
    # عرض المهارات
    matched = result.get('matched_skills', [])
    missing = result.get('missing_skills', [])
    
    print(f"\n🎯 المهارات:")
    if matched:
        print(f"  ✅ مطابقة: {', '.join(matched)}")
    if missing:
        print(f"  ❌ مفقودة: {', '.join(missing)}")
    
    # عرض التوصية
    rec = result.get('recommendation', 'Unknown')
    emoji = "✅" if final >= 70 else "⚠️" if final >= 50 else "❌"
    print(f"\n{emoji} التوصية: {rec}")
    print("\n" + "="*60)

def create_bar(score):
    """إنشاء بار بصري"""
    filled = int(score / 10)
    empty = 10 - filled
    return "[" + "█" * filled + "░" * empty + "]"

def test_samples():
    """اختبار مع عينات"""
    print("\n" + "="*60)
    print("🧪 اختبار مع عينات")
    print("="*60)
    
    samples = [
        {
            "name": "مطابقة ممتازة",
            "cv": "Flutter developer with 5 years experience in Firebase, BLOC, Clean Architecture and Dart",
            "job": "Senior Flutter Engineer needed. Required: Flutter, Dart, Firebase, MVVM architecture"
        },
        {
            "name": "مطابقة متوسطة",
            "cv": "Mobile developer with experience in cross-platform development",
            "job": "Flutter developer needed"
        },
        {
            "name": "مطابقة ضعيفة",
            "cv": "I am a frontend web developer with React and Vue experience",
            "job": "Looking for Senior Backend Python Developer"
        }
    ]
    
    for i, sample in enumerate(samples, 1):
        print(f"\n{i}. {sample['name']}")
        print(f"   CV: {sample['cv'][:50]}...")
        print(f"   Job: {sample['job'][:50]}...")
        
        try:
            payload = {"cv_text": sample['cv'], "job_text": sample['job']}
            response = requests.post(f"{API_URL}/analyze", json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ➜ Final Score: {result.get('final_score', 0):.2f}%")
                print(f"   ➜ Recommendation: {result.get('recommendation', 'Unknown')}")
            else:
                print(f"   ❌ خطأ: {response.status_code}")
        except Exception as e:
            print(f"   ❌ خطأ: {e}")

def main():
    """البرنامج الرئيسي"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "🤖 اختبار النسخة الجديدة من CVision" + " "*11 + "║")
    print("║" + " "*8 + "Advanced CV Matching System - API Tester" + " "*10 + "║")
    print("╚" + "="*58 + "╝")
    
    # اختبار الاتصال
    if not test_connection():
        print("\n⚠️  تأكد من تشغيل الخادم وحاول مرة أخرى.")
        return
    
    while True:
        print("\n" + "-"*60)
        print("🎯 اختر خياراً:")
        print("-"*60)
        print("1. اختبار بنصوص مكتوبة مباشرة")
        print("2. اختبار برفع ملف CV (PDF/DOCX)")
        print("3. اختبار مع عينات جاهزة")
        print("4. مشاهدة الوثائق (Swagger UI)")
        print("5. خروج")
        print("-"*60)
        
        choice = input("\n👉 اختر (1/2/3/4/5): ").strip()
        
        if choice == "1":
            analyze_text()
        elif choice == "2":
            analyze_file()
        elif choice == "3":
            test_samples()
        elif choice == "4":
            print("\n📖 الوثائق على: http://127.0.0.1:8002/docs")
            print("\nافتح الرابط في المتصفح للوثائق التفاعلية")
        elif choice == "5":
            print("\n👋 شكراً لاستخدامك النظام!")
            break
        else:
            print("❌ خيار غير صحيح!")

if __name__ == "__main__":
    main()

"""
اختبار الـ API - نظام مطابقة السير الذاتية مع الوظائف
Test Script for CVision AI System
"""

import requests
import json
from pathlib import Path

# ============================================
# الإعدادات
# ============================================
API_URL = "http://127.0.0.1:8002"
ENDPOINT_ANALYZE = f"{API_URL}/analyze"
ENDPOINT_UPLOAD = f"{API_URL}/analyze-upload"


# ============================================
# دالة قراءة ملف النص
# ============================================
def read_text_file(file_path):
    """قراءة ملف نصي"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ الملف غير موجود: {file_path}")
        return None
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {e}")
        return None


# ============================================
# دالة اختبار المطابقة بالنصوص
# ============================================
def test_text_matching(cv_text, job_text):
    """اختبار المطابقة باستخدام النصوص مباشرة"""
    print("\n" + "="*60)
    print("📊 اختبار المطابقة بالنصوص")
    print("="*60)
    
    payload = {
        "cv_text": cv_text,
        "job_text": job_text
    }
    
    try:
        print("\n🔄 جاري الإرسال إلى الـ API...")
        response = requests.post(ENDPOINT_ANALYZE, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ النتيجة:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # عرض أفضل مرشح
            if result.get("top_candidates"):
                top = result["top_candidates"][0]
                print("\n" + "="*60)
                print("🏆 أفضل مرشح:")
                print("="*60)
                print(f"  Resume Index: {top['Resume Index']}")
                print(f"  Match Score: {top['Match Score']}%")
                print(f"  Level: {top['Level']}")
                print(f"  Skill Score: {top['Skill Score']}")
                print(f"  Final Score: {top['Final Score']}")
                print(f"  Strengths: {', '.join(top['Strengths']) if top['Strengths'] else 'لا توجد'}")
                print(f"  Weaknesses: {', '.join(top['Weaknesses']) if top['Weaknesses'] else 'لا توجد'}")
            
            return result
        else:
            print(f"❌ خطأ: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return None


# ============================================
# دالة اختبار رفع ملف
# ============================================
def test_file_upload(file_path, job_text):
    """اختبار المطابقة برفع ملف"""
    print("\n" + "="*60)
    print("📤 اختبار رفع الملف")
    print("="*60)
    
    if not Path(file_path).exists():
        print(f"❌ الملف غير موجود: {file_path}")
        return None
    
    try:
        print(f"\n📄 الملف: {file_path}")
        print(f"📝 وصف الوظيفة: {job_text[:100]}...")
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'job_text': job_text}
            
            print("\n🔄 جاري الإرسال إلى الـ API...")
            response = requests.post(ENDPOINT_UPLOAD, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ النتيجة:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        else:
            print(f"❌ خطأ: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return None


# ============================================
# دالة اختبار التواصل مع الـ API
# ============================================
def test_connection():
    """اختبار الاتصال بالـ API"""
    print("\n" + "="*60)
    print("🔗 اختبار الاتصال بالـ API")
    print("="*60)
    
    try:
        print(f"\n🔄 جاري الاتصال بـ {API_URL}...")
        response = requests.get(f"{API_URL}/", timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ الخادم يعمل بنجاح!")
            print(f"   الرسالة: {result.get('message')}")
            print(f"   الحالة: {result.get('status')}")
            return True
        else:
            print(f"❌ خطأ: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ لا يمكن الاتصال بالخادم على {API_URL}")
        print("   تأكد من أن الخادم يعمل:")
        print("   fastapi run code/app.py --port 8002 --host 127.0.0.1")
        return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False


# ============================================
# البرنامج الرئيسي - الخيارات التفاعلية
# ============================================
def main():
    """البرنامج الرئيسي"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "🤖 اختبار نظام مطابقة السير الذاتية" + " "*13 + "║")
    print("║" + " "*8 + "CVision AI System - API Testing Script" + " "*11 + "║")
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
        print("2. اختبار برفع ملف CV")
        print("3. اختبار بملف CV ووصف وظيفة من ملفات")
        print("4. خروج")
        print("-"*60)
        
        choice = input("\n👉 اختر (1/2/3/4): ").strip()
        
        if choice == "1":
            print("\n" + "="*60)
            print("📝 أدخل نصوص المطابقة")
            print("="*60)
            
            print("\n🎓 أدخل نص السيرة الذاتية (CV):")
            print("(أو اترك فارغاً واضغط Enter مرتين لإنهاء)")
            cv_lines = []
            while True:
                line = input()
                if line == "":
                    if cv_lines:
                        break
                else:
                    cv_lines.append(line)
            
            cv_text = "\n".join(cv_lines)
            
            print("\n💼 أدخل نص وصف الوظيفة:")
            print("(أو اترك فارغاً واضغط Enter مرتين لإنهاء)")
            job_lines = []
            while True:
                line = input()
                if line == "":
                    if job_lines:
                        break
                else:
                    job_lines.append(line)
            
            job_text = "\n".join(job_lines)
            
            if cv_text and job_text:
                test_text_matching(cv_text, job_text)
            else:
                print("❌ يجب إدخال النصوص!")
        
        elif choice == "2":
            file_path = input("\n📂 أدخل مسار ملف CV (PDF أو DOCX): ").strip()
            job_text = input("💼 أدخل نص وصف الوظيفة: ").strip()
            
            if file_path and job_text:
                test_file_upload(file_path, job_text)
            else:
                print("❌ يجب إدخال البيانات!")
        
        elif choice == "3":
            cv_file = input("\n📂 أدخل مسار ملف السيرة الذاتية (txt): ").strip()
            job_file = input("📂 أدخل مسار ملف وصف الوظيفة (txt): ").strip()
            
            cv_text = read_text_file(cv_file)
            job_text = read_text_file(job_file)
            
            if cv_text and job_text:
                test_text_matching(cv_text, job_text)
            else:
                print("❌ خطأ في قراءة الملفات!")
        
        elif choice == "4":
            print("\n👋 شكراً لاستخدامك النظام!")
            break
        
        else:
            print("❌ خيار غير صحيح!")


if __name__ == "__main__":
    main()

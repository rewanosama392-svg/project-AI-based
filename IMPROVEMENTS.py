"""
تحسينات مقترحة لمحرك الـ API الجديد
Suggested Improvements for New API Engine
"""

# ============================================
# 1. إضافة مهارات جديدة
# ============================================
# في engine/skills.py، أضف المزيد من المهارات:

ENHANCED_SKILLS = {
    # Mobile Development
    "flutter": ["flutter", "flutter sdk", "flutter app"],
    "dart": ["dart", "dart language"],
    "swift": ["swift", "ios"],
    "kotlin": ["kotlin", "android"],
    "react native": ["react native", "react-native"],
    
    # Web Development
    "react": ["react", "reactjs", "react.js"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vuejs", "vue.js"],
    "nodejs": ["node", "nodejs", "node.js"],
    "express": ["express", "expressjs"],
    
    # Backend
    "python": ["python", "py"],
    "java": ["java"],
    "c#": ["c#", "csharp", "c sharp"],
    "go": ["go", "golang"],
    "rust": ["rust"],
    
    # Databases
    "sql": ["sql", "postgresql", "mysql", "oracle"],
    "mongodb": ["mongodb", "mongo"],
    "firebase": ["firebase", "firestore"],
    "realm": ["realm"],
    
    # Tools & Platforms
    "git": ["git", "github", "gitlab", "bitbucket"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],
    
    # Testing
    "junit": ["junit", "testing"],
    "espresso": ["espresso", "ui testing"],
    "xctest": ["xctest"],
    "pytest": ["pytest"],
    
    # Architecture
    "clean architecture": ["clean architecture", "clean code"],
    "mvvm": ["mvvm", "model view view model"],
    "mvc": ["mvc", "model view controller"],
    "mvp": ["mvp", "model view presenter"],
    "bloc": ["bloc", "blc", "business logic"],
    "oop": ["oop", "object oriented"],
}


# ============================================
# 2. تحسين Semantic Score باستخدام Word2Vec
# ============================================
# قم بتثبيت: pip install gensim

from gensim.models import Word2Vec
import numpy as np

def enhanced_semantic_score(resume_text: str, job_text: str) -> float:
    """
    استخدام Word2Vec لحساب التشابه الدلالي بشكل أفضل
    """
    resume_words = resume_text.split()
    job_words = job_text.split()
    
    if not resume_words or not job_words:
        return 0.0
    
    # تدريب نموذج بسيط (في الإنتاج، استخدم نموذج مدرب مسبقاً)
    try:
        model = Word2Vec([resume_words + job_words], vector_size=100, window=5, min_count=1)
        
        scores = []
        for job_word in job_words:
            if job_word in model.wv:
                max_sim = 0
                for resume_word in resume_words:
                    if resume_word in model.wv:
                        similarity = model.wv.similarity(job_word, resume_word)
                        max_sim = max(max_sim, similarity)
                scores.append(max_sim)
        
        return (sum(scores) / len(scores) * 100) if scores else 0.0
    except:
        # fallback إذا فشل النموذج
        resume_set = set(resume_words)
        job_set = set(job_words)
        overlap = len(resume_set & job_set)
        return (overlap / len(job_set)) * 100 if job_set else 0


# ============================================
# 3. وزن ديناميكي للمعادلة حسب نوع الوظيفة
# ============================================

def dynamic_weighted_score(
    lexical_score: float,
    semantic_score: float,
    skills_score: float,
    job_level: str = "mid"  # junior, mid, senior
) -> dict:
    """
    حساب النتيجة بناءً على نوع الوظيفة
    """
    if job_level == "junior":
        # التركيز على المهارات للوظائف الجديدة
        weights = {"lexical": 0.25, "semantic": 0.25, "skills": 0.50}
    elif job_level == "senior":
        # التركيز على الخبرة والدلالة للوظائف العليا
        weights = {"lexical": 0.40, "semantic": 0.40, "skills": 0.20}
    else:  # mid
        weights = {"lexical": 0.35, "semantic": 0.35, "skills": 0.30}
    
    final = (
        weights["lexical"] * lexical_score +
        weights["semantic"] * semantic_score +
        weights["skills"] * skills_score
    )
    
    return {
        "lexical_score": round(lexical_score, 2),
        "semantic_score": round(semantic_score, 2),
        "skills_score": round(skills_score, 2),
        "final_score": round(final, 2),
        "weights": weights,
    }


# ============================================
# 4. تحليل التطابق التفصيلي
# ============================================

def detailed_analysis(cv_text: str, job_text: str) -> dict:
    """
    إرجاع تحليل مفصل للتطابق
    """
    # استخراج الجمل الرئيسية
    cv_sentences = [s.strip() for s in cv_text.split('.') if s.strip()]
    job_sentences = [s.strip() for s in job_text.split('.') if s.strip()]
    
    # مطابقة الجمل
    matched_sentences = []
    for job_sent in job_sentences:
        for cv_sent in cv_sentences:
            overlap = len(set(job_sent.split()) & set(cv_sent.split()))
            if overlap >= len(job_sent.split()) * 0.6:  # 60% match
                matched_sentences.append({
                    "job_requirement": job_sent[:50] + "...",
                    "cv_statement": cv_sent[:50] + "...",
                    "match_ratio": overlap / len(job_sent.split())
                })
    
    return {
        "total_job_requirements": len(job_sentences),
        "matched_requirements": len(matched_sentences),
        "detailed_matches": matched_sentences[:5],  # أول 5 تطابقات
    }


# ============================================
# 5. توصيات ذكية
# ============================================

def generate_recommendations(cv_text: str, job_text: str, final_score: float) -> list:
    """
    إرجاع قائمة بالتوصيات لتحسين التطابق
    """
    recommendations = []
    
    if final_score < 50:
        recommendations.append("Consider updating your CV to include relevant keywords from the job description")
        recommendations.append("Your background seems quite different from this role")
    
    if "experience" in job_text.lower() and "experience" not in cv_text.lower():
        recommendations.append("Add your years of experience to your CV")
    
    if "certification" in job_text.lower() and "certification" not in cv_text.lower():
        recommendations.append("Include any relevant certifications in your CV")
    
    if "project" in job_text.lower() and "project" not in cv_text.lower():
        recommendations.append("Add examples of relevant projects you've worked on")
    
    if final_score > 80:
        recommendations = ["Great match! Consider applying for this position."]
    
    return recommendations


# ============================================
# استخدام التحسينات
# ============================================

if __name__ == "__main__":
    from engine.preprocessing import preprocess_text
    from engine.skills import extract_skills
    
    resume = "Flutter developer with 3 years experience in Firebase and Bloc architecture"
    job = "Senior Flutter Engineer needed. Required: Flutter, Dart, Firebase, MVVM, Git"
    
    # معالجة
    resume_clean = preprocess_text(resume)
    job_clean = preprocess_text(job)
    
    # استخراج المهارات
    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job)
    
    print(f"Detected Skills in CV: {resume_skills}")
    print(f"Detected Skills in Job: {job_skills}")
    
    # توصيات
    recs = generate_recommendations(resume, job, 75)
    print(f"Recommendations: {recs}")

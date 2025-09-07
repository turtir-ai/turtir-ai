import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

def analyze_job_description_fallback(description: str) -> Dict[str, Any]:
    """
    Fallback analyzer that provides intelligent analysis when API is not available.
    Uses keyword-based scoring to evaluate project suitability.
    """
    
    # Keyword categories for scoring
    high_value_keywords = [
        'react', 'node', 'python', 'django', 'flask', 'fastapi', 'streamlit', 
        'javascript', 'typescript', 'vue', 'angular', 'next.js', 'nuxt',
        'api', 'rest', 'graphql', 'database', 'mysql', 'postgresql', 'mongodb',
        'no-code', 'low-code', 'automation', 'scraping', 'web scraping',
        'ai', 'machine learning', 'data analysis', 'dashboard', 'web app'
    ]
    
    medium_value_keywords = [
        'wordpress', 'shopify', 'webflow', 'squarespace', 'cms',
        'html', 'css', 'bootstrap', 'tailwind', 'responsive',
        'frontend', 'backend', 'full-stack', 'development'
    ]
    
    complex_keywords = [
        'blockchain', 'solidity', 'smart contract', 'crypto', 'defi',
        'mobile app', 'ios', 'android', 'react native', 'flutter',
        'devops', 'aws', 'azure', 'docker', 'kubernetes', 'microservices'
    ]
    
    description_lower = description.lower()
    
    # Calculate scores
    high_score = sum(1 for keyword in high_value_keywords if keyword in description_lower)
    medium_score = sum(1 for keyword in medium_value_keywords if keyword in description_lower)
    complex_score = sum(1 for keyword in complex_keywords if keyword in description_lower)
    
    # Calculate final suitability score (1-10)
    base_score = min(10, 3 + high_score * 1.5 + medium_score * 1.0 - complex_score * 0.5)
    suitability_score = max(1, int(base_score))
    
    # Generate analysis summary and technologies
    found_techs = []
    for keyword in high_value_keywords + medium_value_keywords:
        if keyword in description_lower:
            found_techs.append(keyword.title())
    
    # Generate summary based on score
    if suitability_score >= 8:
        summary = f"Bu proje no-code/low-code araçlarla çok uygun görünüyor. {', '.join(found_techs[:3])} teknolojileri kullanılabilir."
    elif suitability_score >= 6:
        summary = f"Orta seviye uygunluk. {', '.join(found_techs[:2])} teknolojileriyle yapılabilir ancak daha fazla araştırma gerekebilir."
    else:
        summary = "Karmaşık bir proje görünüyor. Geleneksel kodlama yaklaşımları gerekebilir."
    
    return {
        'uygunluk_skoru': suitability_score,
        'analiz_ozeti': summary,
        'gereken_teknolojiler': found_techs[:5] if found_techs else ['Web Development']
    }

def analyze_job_description(description: str) -> Dict[str, Any]:
    """
    Analyze job description using Gemini AI with intelligent fallback system.
    
    Args:
        description: The job description text to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    
    # First try the Gemini API
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == "YOUR_NEW_API_KEY_HERE":
            print("API key not configured, using fallback analyzer...")
            return analyze_job_description_fallback(description)
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Aşağıdaki Upwork proje açıklamasını analiz et. No-code/low-code araçlarla ve 'vibe coding' yaklaşımıyla yapılabilirliğini değerlendir.

        Çıktıyı JSON formatında ver:
        - "uygunluk_skoru": 1-10 arası tamsayı
        - "analiz_ozeti": 2-3 cümlelik özet (Türkçe)
        - "gereken_teknolojiler": teknoloji listesi

        Proje: {description}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)
            
            # Validate and clean result
            score = result.get('uygunluk_skoru', 5)
            if isinstance(score, str):
                score = int(score)
            result['uygunluk_skoru'] = max(1, min(10, score))
            
            if not isinstance(result.get('gereken_teknolojiler'), list):
                result['gereken_teknolojiler'] = []
            
            return result
        else:
            raise ValueError("No valid JSON found in AI response")
            
    except Exception as e:
        print(f"Gemini API failed ({str(e)[:100]}...), using intelligent fallback analyzer...")
        return analyze_job_description_fallback(description)
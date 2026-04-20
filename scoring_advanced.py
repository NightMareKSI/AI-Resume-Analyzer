"""
Advanced ATS Scoring System
Implements production-level weighted scoring with multiple factors
"""

import re
from collections import Counter
from typing import Dict, List, Tuple


class ATSScorer:
    """Production-grade ATS scoring system with weighted components"""
    
    def __init__(self):
        # Scoring weights for production-level evaluation
        self.weights = {
            'semantic_match': 0.30,      # Job description semantic alignment
            'skill_match': 0.25,          # Skills matching job requirements
            'keyword_optimization': 0.15, # Keyword frequency and density
            'experience_relevance': 0.15, # Years and relevance of experience
            'education_relevance': 0.10,  # Education alignment
            'formatting_structure': 0.05  # resume completeness and structure
        }
        
        # Key sections every resume should have
        self.required_sections = [
            'contact', 'summary', 'experience', 
            'education', 'skills', 'projects'
        ]
        
        # Critical keywords for different sections
        self.critical_keywords = {
            'experience': ['developed', 'designed', 'implemented', 'managed', 'led', 'architect', 'engineered', 'optimized'],
            'achievement': ['improved', 'increased', 'reduced', 'accelerated', 'enhanced', 'delivered'],
            'tech': ['api', 'database', 'framework', 'algorithm', 'architecture', 'deployment']
        }
    
    def calculate_overall_score(
        self,
        semantic_score: float,
        skill_score: float,
        keyword_score: float,
        experience_relevance: float,
        education_relevance: float,
        formatting_score: float
    ) -> Tuple[float, Dict]:
        """
        Calculate weighted overall ATS score
        Returns: (overall_score, component_scores_dict)
        """
        components = {
            'semantic_match': semantic_score,
            'skill_match': skill_score,
            'keyword_optimization': keyword_score,
            'experience_relevance': experience_relevance,
            'education_relevance': education_relevance,
            'formatting_structure': formatting_score
        }
        
        overall = sum(
            components[key] * self.weights[key]
            for key in components
        )
        
        return round(overall, 2), components
    
    def calculate_keyword_density_score(
        self,
        resume_text: str,
        job_description: str
    ) -> float:
        """
        Analyze keyword frequency and density
        Keywords appearing in both texts get higher scores
        """
        # Extract keywords (words > 4 chars, not common words)
        common_words = {'the', 'have', 'from', 'with', 'this', 'that', 'your', 'their', 'which', 'where'}
        
        def extract_keywords(text):
            words = re.findall(r'\b\w+\b', text.lower())
            keywords = [w for w in words if len(w) > 4 and w not in common_words]
            return keywords
        
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(job_description)
        
        if not jd_keywords:
            return 0
        
        # Count keyword occurrences
        resume_counter = Counter(resume_keywords)
        jd_counter = Counter(jd_keywords)
        
        # Calculate keyword match ratio
        matched_keywords = set(resume_counter.keys()).intersection(set(jd_counter.keys()))
        
        if not matched_keywords:
            return 0
        
        # Calculate average frequency ratio
        frequency_scores = []
        for keyword in matched_keywords:
            resume_freq = resume_counter[keyword]
            jd_freq = jd_counter[keyword]
            # Score based on how well resume matches JD frequency
            freq_ratio = min(resume_freq / max(jd_freq, 1), 2) / 2
            frequency_scores.append(freq_ratio)
        
        avg_frequency = sum(frequency_scores) / len(frequency_scores) if frequency_scores else 0
        
        # Keyword coverage
        coverage = len(matched_keywords) / len(set(jd_keywords))
        
        # Combined score: 60% coverage, 40% frequency
        keyword_score = (coverage * 0.6 + avg_frequency * 0.4) * 100
        
        return round(min(keyword_score, 100), 2)
    
    def calculate_experience_relevance(
        self,
        resume_text: str,
        years_required: float = None
    ) -> float:
        """
        Evaluate experience relevance and depth
        Looks for achievement metrics and action verbs
        """
        text_lower = resume_text.lower()
        
        # Count action verbs (sign of strong experience description)
        action_verb_count = 0
        for verb in self.critical_keywords['experience']:
            action_verb_count += text_lower.count(verb)
        
        # Count achievement indicators
        achievement_count = 0
        for achievement in self.critical_keywords['achievement']:
            achievement_count += text_lower.count(achievement)
        
        # Count metrics (numbers, percentages, etc.)
        metric_pattern = r'\d+(%|x|year|month|project|team|user|customer)?'
        metrics = re.findall(metric_pattern, text_lower)
        metric_count = len(metrics)
        
        # Score calculation
        action_verb_score = min(action_verb_count * 5, 40)  # Up to 40 points
        achievement_score = min(achievement_count * 3, 35)  # Up to 35 points
        quantification_score = min(metric_count * 5, 25)    # Up to 25 points
        
        experience_score = (action_verb_score + achievement_score + quantification_score) / 100 * 100
        
        return round(min(experience_score, 100), 2)
    
    def calculate_education_relevance(
        self,
        resume_text: str,
        job_description: str
    ) -> float:
        """
        Evaluate education section relevance
        """
        text_lower = resume_text.lower()
        jd_lower = job_description.lower()
        
        # Look for degree levels
        degree_patterns = {
            'Ph.D': ['phd', 'ph.d', 'doctorate'],
            'Masters': ['masters', 'msc', 'm.s', 'm.sc', 'master'],
            'Bachelors': ['bachelors', 'ba', 'bs', 'btech', 'b.tech', 'bachelor'],
            'Bootcamp': ['bootcamp']
        }
        
        found_degrees = {}
        for degree_type, patterns in degree_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    found_degrees[degree_type] = True
        
        # Check for relevant fields in Education
        relevant_fields = []
        keywords = ['computer science', 'engineering', 'it', 'information technology', 
                   'software', 'data science', 'artificial intelligence', 'machine learning']
        
        for keyword in keywords:
            if keyword in text_lower:
                relevant_fields.append(keyword)
        
        # Score: 50% for having degree, 50% for relevant field
        degree_score = 40 if found_degrees else 0
        field_score = 30 if relevant_fields else 10
        
        education_score = degree_score + field_score
        
        return round(min(education_score, 100), 2)
    
    def calculate_formatting_score(self, resume_text: str) -> float:
        """
        Evaluate resume structure and formatting completeness
        """
        text_lower = resume_text.lower()
        
        # Check for required sections
        section_scores = {}
        section_keywords = {
            'contact': ['email', '@', 'phone', 'linkedin'],
            'summary': ['profile', 'summary', 'objective', 'about'],
            'experience': ['experience', 'employment', 'worked at', 'position'],
            'education': ['education', 'university', 'college', 'degree', 'graduated'],
            'skills': ['skills', 'technical', 'programming', 'languages'],
            'projects': ['project', 'portfolio', 'built', 'developed', 'github']
        }
        
        for section, keywords in section_keywords.items():
            section_scores[section] = any(kw in text_lower for kw in keywords)
        
        # Length check (resume should be substantial)
        text_length = len(resume_text.split())
        length_score = 20 if text_length > 300 else 10 if text_length > 150 else 0
        
        # Section completeness (0-80 points)
        sections_found = sum(section_scores.values())
        section_score = (sections_found / len(section_keywords)) * 80
        
        formatting_score = section_score + length_score
        
        return round(min(formatting_score, 100), 2)
    

    def calculate_skill_match_score(self, resume_skills: List[str], jd_skills: List[str]) -> float:
        if len(jd_skills) == 0:
            return 0
    
        matched_skills = set(resume_skills).intersection(set(jd_skills))
        score = (len(matched_skills) / len(jd_skills)) * 100
    
        return round(score, 2)

    
    def generate_detailed_feedback(self, components: Dict, scores: Dict) -> Dict:
        """
        Generate detailed feedback based on component scores
        """
        feedback = {
            'strengths': [],
            'weaknesses': [],
            'improvements': [],
            'score_breakdown': components
        }
        
        # Analyze each component
        thresholds = {
            'excellent': 80,
            'good': 70,
            'average': 50,
            'poor': 0
        }
        
        for component, score in components.items():
            if score >= thresholds['excellent']:
                feedback['strengths'].append(
                    f"{component}: Excellent ({score}%)"
                )
            elif score < thresholds['average']:
                feedback['weaknesses'].append(
                    f"{component}: Needs improvement ({score}%)"
                )
                
                # Add specific improvement suggestions
                if component == 'keyword_optimization':
                    feedback['improvements'].append(
                        "→ Include more job description keywords"
                    )
                elif component == 'experience_relevance':
                    feedback['improvements'].append(
                        "→ Use action verbs and add quantifiable achievements"
                    )
                elif component == 'formatting_structure':
                    feedback['improvements'].append(
                        "→ Ensure all resume sections are present"
                    )
                elif component == 'skill_match':
                    feedback['improvements'].append(
                        "→ Add missing required skills"
                    )
        
        return feedback


# Maintain backward compatibility

def calculate_overall_score(semantic_score: float, skill_score: float) -> float:
    """Legacy function - basic weighted score"""
    semantic_weight = 0.6
    skill_weight = 0.4
    overall = (semantic_score * semantic_weight + skill_score * skill_weight)
    
    return round(overall, 2)

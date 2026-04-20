"""
Resume Section Analysis Module
Analyzes individual sections of resume with detailed feedback
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class SectionScore:
    """Represents a section score"""
    section_name: str
    score: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]


class ResumeSectionAnalyzer:
    """Analyzes resume sections individually"""
    
    SECTION_PATTERNS = {
        'contact': r'(email|phone|linkedin|github|portfolio|contact)',
        'summary': r'(professional summary|objective|profile|about)',
        'experience': r'(experience|employment|work experience|career history)',
        'education': r'(education|academic|university|college|degree)',
        'skills': r'(skills|technical skills|core competencies|expertise)',
        'projects': r'(projects|portfolio|github|building|side project)',
        'certifications': r'(certification|certified|credential|license)'
    }
    
    ACTION_VERBS = [
        'achieved', 'addressed', 'administered', 'anchored', 'anticipated',
        'architected', 'authored', 'budgeted', 'built', 'calculated',
        'captured', 'championed', 'clarified', 'coached', 'collaborated',
        'compiled', 'completed', 'conceived', 'conceptualized', 'constructed',
        'consulted', 'coordinated', 'created', 'cultivated', 'customized',
        'debugged', 'decreased', 'decorated', 'defined', 'delegated',
        'delivered', 'demonstrated', 'deployed', 'designed', 'developed',
        'diagnosed', 'directed', 'discovered', 'displayed', 'distributed',
        'documented', 'drove', 'edited', 'educated', 'elevated',
        'enabled', 'encouraged', 'engineered', 'enhanced', 'ensured',
        'established', 'estimated', 'evaluated', 'examined', 'executed',
        'exercised', 'expanded', 'expedited', 'experienced', 'experimented',
        'explained', 'explored', 'fabricated', 'facilitated', 'fashioned',
        'focused', 'forecasted', 'formulated', 'fostered', 'founded',
        'generated', 'governed', 'guided', 'handled', 'headed',
        'heightened', 'helped', 'identified', 'illustrated', 'implemented',
        'improved', 'increased', 'influenced', 'informed', 'initiated',
        'innovated', 'installed', 'instituted', 'instructed', 'integrated',
        'intended', 'interpreted', 'interviewed', 'introduced', 'invented',
        'investigated', 'invited', 'involved', 'isolated', 'issued',
        'judged', 'justified', 'kept', 'launched', 'led', 'leveled'
    ]
    
    ACHIEVEMENT_KEYWORDS = {
        'improvement': ['improved', 'enhanced', 'optimized', 'better', 'streamlined'],
        'growth': ['increased', 'grew', 'expanded', 'scaled', 'accelerated'],
        'reduction': ['reduced', 'decreased', 'cut', 'minimized', 'eliminated'],
        'leadership': ['led', 'managed', 'directed', 'headed', 'championed'],
        'innovation': ['developed', 'created', 'designed', 'invented', 'pioneered']
    }
    
    @staticmethod
    def extract_section(resume_text: str, section_type: str) -> str:
        """
        Extract a specific section from resume text
        """
        pattern = ResumeSectionAnalyzer.SECTION_PATTERNS.get(section_type, '')
        if not pattern:
            return ""
        
        lines = resume_text.split('\n')
        section_content = []
        capturing = False
        
        for line in lines:
            if re.search(pattern, line, re.IGNORECASE):
                capturing = True
                continue
            
            if capturing:
                # Stop if we hit another section
                if any(re.search(ResumeSectionAnalyzer.SECTION_PATTERNS[s], line, re.IGNORECASE)
                       for s in ResumeSectionAnalyzer.SECTION_PATTERNS if s != section_type):
                    break
                
                section_content.append(line)
        
        return '\n'.join(section_content).strip()
    
    @staticmethod
    def analyze_contact_section(resume_text: str) -> SectionScore:
        """Analyze Contact Information section"""
        section_text = ResumeSectionAnalyzer.extract_section(resume_text, 'contact')
        
        score = 100
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Check for required contact elements
        has_email = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            section_text or resume_text,
            re.IGNORECASE
        )
        has_phone = re.search(r'[\+]?[\d\s\-\(\)]{10,}', section_text or resume_text)
        has_linkedin = re.search(r'linkedin', resume_text, re.IGNORECASE)
        has_address = re.search(r'(city|state|country|address)', resume_text, re.IGNORECASE)
        
        if has_email:
            strengths.append("Email address provided")
        else:
            weaknesses.append("Missing email address")
            score -= 20
        
        if has_phone:
            strengths.append("Phone number included")
        else:
            weaknesses.append("Phone number not visible")
            score -= 10
        
        if has_linkedin:
            strengths.append("LinkedIn profile linked")
        else:
            suggestions.append("Add LinkedIn profile link")
        
        if has_address:
            strengths.append("Location information included")
        else:
            suggestions.append("Consider adding location (City, State)")
        
        return SectionScore('Contact Information', max(score, 0), strengths, weaknesses, suggestions)
    
    @staticmethod
    def analyze_summary_section(resume_text: str, job_description: str = "") -> SectionScore:
        """Analyze Professional Summary section"""
        section_text = ResumeSectionAnalyzer.extract_section(resume_text, 'summary')
        
        if not section_text:
            section_text = resume_text[:500]  # Use beginning of resume
        
        score = 0
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Check length (should be 2-4 lines, 50-150 words)
        word_count = len(section_text.split())
        
        if 50 < word_count < 150:
            score += 30
            strengths.append(f"Good length ({word_count} words)")
        else:
            weaknesses.append(f"Summary too {'short' if word_count < 50 else 'long'} ({word_count} words)")
            score += 15
        
        # Check for action verbs
        action_verb_count = sum(1 for verb in ResumeSectionAnalyzer.ACTION_VERBS if verb in section_text.lower())
        if action_verb_count > 0:
            score += 20
            strengths.append(f"Contains action verbs ({action_verb_count} found)")
        else:
            weaknesses.append("Missing action verbs")
        
        # Check for keywords matching job description
        if job_description:
            jd_words = set(job_description.lower().split())
            summary_words = set(section_text.lower().split())
            keyword_matches = len(jd_words.intersection(summary_words))
            
            if keyword_matches > 5:
                score += 25
                strengths.append(f"Aligns with job description")
            else:
                suggestions.append("Incorporate more job description keywords")
        else:
            score += 25
        
        # Check for specific skills/achievements
        if any(keyword in section_text.lower() for keywords in ResumeSectionAnalyzer.ACHIEVEMENT_KEYWORDS.values() for keyword in keywords):
            score += 15
            strengths.append("Includes achievements and metrics")
        else:
            suggestions.append("Add quantifiable achievements (e.g., 'increased by 25%')")
        
        if not section_text:
            weaknesses.append("Professional summary missing")
            score = 10
        
        return SectionScore('Professional Summary', min(score, 100), strengths, weaknesses, suggestions)
    
    @staticmethod
    def analyze_experience_section(resume_text: str) -> SectionScore:
        """Analyze Work Experience section"""
        section_text = ResumeSectionAnalyzer.extract_section(resume_text, 'experience')
        
        score = 0
        strengths = []
        weaknesses = []
        suggestions = []
        
        if not section_text:
            return SectionScore('Work Experience', 0, [], ['No work experience section found'], 
                               ['Add work experience details'])
        
        # Check for job titles and companies
        lines = section_text.split('\n')
        job_count = len([l for l in lines if l.strip()])
        
        if job_count > 0:
            score += 10 * min(job_count, 5)
            strengths.append(f"Multiple positions listed ({job_count} entries)")
        
        # Check for action verbs
        action_verb_count = sum(1 for verb in ResumeSectionAnalyzer.ACTION_VERBS if verb in section_text.lower())
        if action_verb_count > 5:
            score += 30
            strengths.append(f"Strong action verbs used ({action_verb_count} instances)")
        elif action_verb_count > 0:
            score += 15
            suggestions.append("Use more action verbs to describe achievements")
        else:
            weaknesses.append("Lacks action verbs in descriptions")
        
        # Check for metrics and quantifiable achievements
        metrics = re.findall(r'[\d\.]+(%|x|increase|improvement|growth)', section_text, re.IGNORECASE)
        if metrics:
            score += 25
            strengths.append(f"Includes quantifiable metrics ({len(metrics)} found)")
        else:
            suggestions.append("Add metrics and numbers (revenue growth, efficiency gains, etc.)")
        
        # Check for technologies mentioned
        tech_keywords = ['python', 'java', 'sql', 'aws', 'docker', 'kubernetes', 'javascript', 'react', 'nodejs']
        tech_found = [t for t in tech_keywords if t in section_text.lower()]
        if tech_found:
            score += 15
            strengths.append(f"Technical skills highlighted ({len(tech_found)} technologies)")
        else:
            suggestions.append("Mention specific technologies and tools used")
        
        # Check for length
        if len(section_text) > 300:
            score += 10
            strengths.append("Comprehensive experience description")
        else:
            suggestions.append("Expand experience descriptions with more details")
        
        return SectionScore('Work Experience', min(score, 100), strengths, weaknesses, suggestions)
    
    @staticmethod
    def analyze_skills_section(resume_text: str, job_description: str = "") -> Tuple[SectionScore, List[str], List[str]]:
        """Analyze Skills section and return matched vs missing skills"""
        section_text = ResumeSectionAnalyzer.extract_section(resume_text, 'skills')
        
        score = 0
        strengths = []
        weaknesses = []
        suggestions = []
        
        if not section_text:
            weaknesses.append("No dedicated skills section")
            score = 20
        else:
            score += 25
            strengths.append("Dedicated skills section present")
        
        # Parse skills (assuming comma-separated or bullet points)
        skills_list = re.split(r'[,\n•\-\*]', section_text + resume_text)
        skills_list = [s.strip().lower() for s in skills_list if s.strip() and len(s.strip()) > 2]
        skills_list = list(set(skills_list))  # Remove duplicates
        
        matched_skills = []
        missing_skills = []
        
        if job_description:
            jd_keywords = set(job_description.lower().split())
            
            for skill in skills_list[:20]:  # Check top 20 skills
                if skill in jd_keywords or any(skill in kw for kw in jd_keywords):
                    matched_skills.append(skill)
                    score += 2
            
            # Find missing required skills from JD
            tech_keywords = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes',
                            'git', 'react', 'nodejs', 'machine learning', 'ai', 'data science']
            
            for keyword in tech_keywords:
                if keyword in jd_keywords and keyword not in [s.lower() for s in skills_list]:
                    missing_skills.append(keyword)
        
        if len(skills_list) > 10:
            score += 20
            strengths.append(f"Comprehensive skills list ({len(skills_list)} skills)")
        elif len(skills_list) > 5:
            score += 10
            suggestions.append("Add more relevant technical skills")
        else:
            weaknesses.append("Limited skills listed")
        
        # Check for skill categories
        categories = {'languages': ['python', 'java', 'javascript', 'c++'],
                     'databases': ['sql', 'mongodb', 'postgresql'],
                     'frameworks': ['react', 'django', 'spring', 'nodejs'],
                     'cloud': ['aws', 'gcp', 'azure']}
        
        found_categories = sum(1 for cat, keywords in categories.items()
                              if any(kw in section_text.lower() for kw in keywords))
        if found_categories > 2:
            score += 15
            strengths.append("Skills organized by category")
        
        return SectionScore('Skills', min(score, 100), strengths, weaknesses, suggestions), matched_skills, missing_skills
    
    @staticmethod
    def analyze_education_section(resume_text: str) -> SectionScore:
        """Analyze Education section"""
        section_text = ResumeSectionAnalyzer.extract_section(resume_text, 'education')
        
        if not section_text:
            section_text = resume_text
        
        score = 0
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Check for degree types
        degree_patterns = {
            'phd': r'(phd|ph\.d|doctorate)',
            'masters': r'(master|m\.?s\.?c?|msc)',
            'bachelors': r'(bachelor|b\.?[a-z]\.?|bs|ba)',
            'bootcamp': r'bootcamp'
        }
        
        found_degrees = {}
        for degree_type, pattern in degree_patterns.items():
            if re.search(pattern, section_text, re.IGNORECASE):
                found_degrees[degree_type] = True
        
        if not found_degrees:
            weaknesses.append("No clear degree information")
            score += 20
        else:
            score += 40
            strengths.append(f"Degree(s) clearly stated")
        
        # Check for university names
        if re.search(r'(university|college|institute)', section_text, re.IGNORECASE):
            score += 20
            strengths.append("Institution clearly named")
        else:
            suggestions.append("Include university/college name clearly")
        
        # Check for graduation date
        if re.search(r'\d{4}|graduating', section_text, re.IGNORECASE):
            score += 15
            strengths.append("Graduation date included")
        else:
            suggestions.append("Add graduation year or expected graduation date")
        
        # Check for CGPA or honors
        if re.search(r'(cgpa|gpa|honors|summa|magna|cum laude)', section_text, re.IGNORECASE):
            score += 15
            strengths.append("Academic achievements noted")
        else:
            suggestions.append("Include GPA if 3.5 or higher, or academic honors")
        
        # Check for relevant field
        relevant_fields = ['computer science', 'engineering', 'it', 'information technology',
                          'software', 'data science', 'machine learning', 'artificial intelligence']
        if any(field in section_text.lower() for field in relevant_fields):
            score += 10
            strengths.append("Relevant field of study")
        
        return SectionScore('Education', min(score, 100), strengths, weaknesses, suggestions)
    
    @staticmethod
    def analyze_projects_section(resume_text: str, job_description: str = "") -> SectionScore:
        """Analyze Projects section"""
        section_text = ResumeSectionAnalyzer.extract_section(resume_text, 'projects')
        
        score = 0
        strengths = []
        weaknesses = []
        suggestions = []
        
        if not section_text:
            weaknesses.append("No projects section found")
            score = 10
            suggestions.append("Add a Projects section with portfolio/GitHub links")
            return SectionScore('Projects', score, strengths, weaknesses, suggestions)
        
        score += 25
        strengths.append("Projects section included")
        
        # Check for project descriptions
        projects = len([l for l in section_text.split('\n') if l.strip()])
        if projects > 1:
            score += 20
            strengths.append(f"Multiple projects listed ({projects})")
        
        # Check for technical details
        if any(keyword in section_text.lower() for keyword in ['github', 'gitlab', 'link', 'demo', 'deployed']):
            score += 20
            strengths.append("Project links/URLs included")
        else:
            suggestions.append("Include GitHub/GitLab links or project URLs")
        
        # Check for technologies
        tech_keywords = ['python', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 'api']
        tech_found = sum(1 for t in tech_keywords if t in section_text.lower())
        if tech_found > 1:
            score += 15
            strengths.append("Technologies mentioned")
        
        # Check for impact/achievements
        if any(keyword in section_text.lower() for keywords in ResumeSectionAnalyzer.ACHIEVEMENT_KEYWORDS.values() for keyword in keywords):
            score += 10
            strengths.append("Project impact described")
        else:
            suggestions.append("Describe the impact and outcome of each project")
        
        return SectionScore('Projects', min(score, 100), strengths, weaknesses, suggestions)
    
    @staticmethod
    def analyze_all_sections(resume_text: str, job_description: str = "") -> Dict[str, SectionScore]:
        """Analyze all resume sections"""
        analyses = {
            'contact': ResumeSectionAnalyzer.analyze_contact_section(resume_text),
            'summary': ResumeSectionAnalyzer.analyze_summary_section(resume_text, job_description),
            'experience': ResumeSectionAnalyzer.analyze_experience_section(resume_text),
            'education': ResumeSectionAnalyzer.analyze_education_section(resume_text),
            'projects': ResumeSectionAnalyzer.analyze_projects_section(resume_text, job_description),
        }
        
        # Add skills analysis
        skills_analysis, matched, missing = ResumeSectionAnalyzer.analyze_skills_section(resume_text, job_description)
        analyses['skills'] = skills_analysis
        
        return analyses

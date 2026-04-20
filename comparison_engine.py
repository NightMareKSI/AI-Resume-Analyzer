"""
Multi-Resume Comparison Module
Enables users to compare multiple resumes side-by-side
"""

from typing import List, Dict, Tuple
import pandas as pd
from dataclasses import dataclass


@dataclass
class ResumeComparison:
    """Represents a comparison of multiple resumes"""
    resume_names: List[str]
    overall_scores: List[float]
    component_scores: Dict[str, List[float]]
    strengths: Dict[str, List[str]]
    weaknesses: Dict[str, List[str]]
    recommendations: Dict[str, List[str]]


class ResumeComparisonEngine:
    """Compares multiple resumes for ranking and analysis"""
    
    @staticmethod
    def compare_resumes(analyses: List[Dict]) -> ResumeComparison:
        """
        Compare multiple resume analyses
        
        Args:
            analyses: List of analysis dictionaries with scores
        
        Returns:
            ResumeComparison object with detailed comparison
        """
        if len(analyses) < 2:
            raise ValueError("At least 2 resumes required for comparison")
        
        resume_names = [analysis.get('name', f'Resume {i+1}') for i, analysis in enumerate(analyses)]
        
        overall_scores = [analysis.get('overall_score', 0) for analysis in analyses]
        
        # Extract component scores
        component_keys = ['semantic_match', 'skill_match', 'keyword_optimization',
                         'experience_relevance', 'education_relevance', 'formatting_structure']
        
        component_scores = {}
        for component in component_keys:
            component_scores[component] = [
                analysis.get('components', {}).get(component, 0)
                for analysis in analyses
            ]
        
        # Extract strengths, weaknesses, recommendations
        strengths = {name: analysis.get('strengths', []) for name, analysis in zip(resume_names, analyses)}
        weaknesses = {name: analysis.get('weaknesses', []) for name, analysis in zip(resume_names, analyses)}
        recommendations = {name: analysis.get('improvements', []) for name, analysis in zip(resume_names, analyses)}
        
        return ResumeComparison(
            resume_names=resume_names,
            overall_scores=overall_scores,
            component_scores=component_scores,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
    
    @staticmethod
    def rank_resumes(analyses: List[Dict]) -> List[Tuple[str, float, int]]:
        """
        Rank resumes by overall score
        
        Returns:
            List of (resume_name, overall_score, rank)
        """
        resumes = []
        
        for i, analysis in enumerate(analyses):
            name = analysis.get('name', f'Resume {i+1}')
            score = analysis.get('overall_score', 0)
            resumes.append((name, score, i))
        
        # Sort by score descending
        resumes.sort(key=lambda x: x[1], reverse=True)
        
        # Add rank
        ranked = [(name, score, rank+1) for rank, (name, score, _) in enumerate(resumes)]
        
        return ranked
    
    @staticmethod
    def generate_comparison_dataframe(comparison: ResumeComparison) -> pd.DataFrame:
        """
        Generate a DataFrame for comparison display
        """
        data = {
            'Resume': comparison.resume_names,
            'Overall Score': comparison.overall_scores,
            'Semantic Match': comparison.component_scores.get('semantic_match', []),
            'Skill Match': comparison.component_scores.get('skill_match', []),
            'Keyword Optimization': comparison.component_scores.get('keyword_optimization', []),
            'Experience': comparison.component_scores.get('experience_relevance', []),
            'Education': comparison.component_scores.get('education_relevance', []),
            'Formatting': comparison.component_scores.get('formatting_structure', [])
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def get_best_resume(comparison: ResumeComparison) -> Tuple[str, float]:
        """Get the best performing resume"""
        max_idx = comparison.overall_scores.index(max(comparison.overall_scores))
        return comparison.resume_names[max_idx], comparison.overall_scores[max_idx]
    
    @staticmethod
    def get_improvement_gaps(comparison: ResumeComparison) -> Dict[str, Dict[str, float]]:
        """
        Calculate improvement gaps between resumes
        Shows how much each resume needs to improve to match the best one
        """
        best_score = max(comparison.overall_scores)
        gaps = {}
        
        for i, name in enumerate(comparison.resume_names):
            gap_to_best = best_score - comparison.overall_scores[i]
            
            component_gaps = {}
            for component, scores in comparison.component_scores.items():
                best_component = max(scores)
                component_gaps[component] = best_component - scores[i]
            
            gaps[name] = {
                'total_gap': gap_to_best,
                'component_gaps': component_gaps
            }
        
        return gaps
    
    @staticmethod
    def generate_improvement_plan(comparison: ResumeComparison, target_resume: str) -> Dict:
        """
        Generate personalized improvement plan for a resume to match another
        """
        target_idx = comparison.resume_names.index(target_resume)
        target_scores = {
            component: scores[target_idx]
            for component, scores in comparison.component_scores.items()
        }
        
        plan = {
            'target_resume': target_resume,
            'focus_areas': [],
            'priority': []
        }
        
        # Identify weakest areas compared to target
        for component, scores in comparison.component_scores.items():
            avg_score = sum(scores) / len(scores)
            improvement_needed = target_scores[component] - avg_score
            
            if improvement_needed > 0:
                plan['focus_areas'].append({
                    'component': component,
                    'current_avg': round(avg_score, 2),
                    'target': round(target_scores[component], 2),
                    'improvement_needed': round(improvement_needed, 2)
                })
        
        # Sort by improvement needed (descending)
        plan['priority'] = sorted(
            plan['focus_areas'],
            key=lambda x: x['improvement_needed'],
            reverse=True
        )
        
        return plan
    
    @staticmethod
    def compare_against_job_description(
        resumes: List[Dict],
        job_description: str
    ) -> Dict[str, Dict]:
        """
        Compare how well each resume matches a job description
        """
        comparison_results = {}
        
        from section_analyzer import ResumeSectionAnalyzer
        
        for resume_data in resumes:
            resume_name = resume_data.get('name', 'Resume')
            resume_text = resume_data.get('resume_text', '')
            
            # Analyze skills match
            skills_analysis, matched, missing = ResumeSectionAnalyzer.analyze_skills_section(
                resume_text,
                job_description
            )
            
            # Calculate match percentage
            total_required = len(matched) + len(missing)
            match_percentage = (len(matched) / total_required * 100) if total_required > 0 else 0
            
            comparison_results[resume_name] = {
                'matched_skills': matched,
                'missing_skills': missing,
                'match_percentage': round(match_percentage, 2),
                'match_count': len(matched),
                'missing_count': len(missing),
                'recommendation': ResumeComparisonEngine._get_match_recommendation(match_percentage)
            }
        
        return comparison_results
    
    @staticmethod
    def _get_match_recommendation(match_percentage: float) -> str:
        """Get recommendation based on match percentage"""
        if match_percentage >= 80:
            return "Excellent match - Apply now!"
        elif match_percentage >= 60:
            return "Good match - Consider applying with cover letter"
        elif match_percentage >= 40:
            return "Partial match - Add missing skills mentioned in job description"
        else:
            return "Poor match - Consider customizing resume for this position"


def Tuple(*args):
    """Placeholder for typing annotations"""
    pass

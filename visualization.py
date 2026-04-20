"""
Advanced Visualization Module
Creates professional, production-grade visualizations for ATS analysis
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


class VisualizationEngine:
    """Handles all professional visualizations for the resume analyzer"""
    
    # Professional color scheme (SaaS-standard)
    COLOR_SCHEME = {
        'excellent': '#10B981',  # Green
        'good': '#3B82F6',       # Blue
        'average': '#F59E0B',    # Amber/Yellow
        'poor': '#EF4444'        # Red
    }
    
    # Score level classifications
    SCORE_LEVELS = {
        (0, 40): ('Poor', '#EF4444'),
        (40, 70): ('Average', '#F59E0B'),
        (70, 100): ('Excellent', '#10B981')
    }
    
    @staticmethod
    def get_score_level(score: float) -> Tuple[str, str]:
        """Get score level name and color"""
        for (min_score, max_score), (level, color) in VisualizationEngine.SCORE_LEVELS.items():
            if min_score <= score < max_score:
                return level, color
        return 'Excellent', '#10B981'
    
    @staticmethod
    def create_gauge_chart(score: float, metric_name: str = "ATS Score") -> go.Figure:
        """
        Create a professional gauge chart for score visualization
        """
        level_name, level_color = VisualizationEngine.get_score_level(score)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            title={'text': metric_name},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100], 'tickfont': {'size': 14}},
                'bar': {'color': level_color, 'thickness': 0.7},
                'steps': [
                    {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.1)"},
                    {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.1)"},
                    {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.1)"}
                ],
                'threshold': {
                    'line': {'color': level_color, 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            },
            number={'font': {'size': 48, 'color': level_color}},
            delta={'reference': 80, 'valueformat': '.0f', 'suffix': ' vs target'},
        ))
        
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=70, b=20),
            font=dict(family="Poppins", size=14),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_radar_chart(components: Dict[str, float]) -> go.Figure:
        """
        Create radar chart for multi-factor ATS scoring
        """
        categories = list(components.keys())
        values = list(components.values())
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='ATS Scores',
            line=dict(color='#3B82F6', width=2),
            fillcolor='rgba(59, 130, 246, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=11),
                ),
                angularaxis=dict(
                    tickfont=dict(size=11)
                ),
                bgcolor='rgba(242,245,250,0.5)'
            ),
            height=450,
            showlegend=True,
            title="ATS Component Score Breakdown",
            font=dict(family="Arial, sans-serif", size=11),
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=80, r=80, t=60, b=60)
        )
        
        return fig
    
    @staticmethod
    def create_donut_chart(data: Dict[str, float], title: str = "Score Distribution") -> go.Figure:
        """
        Create donut chart for score composition visualization
        """
        labels = list(data.keys())
        values = list(data.values())
        
        # Assign colors based on contribution
        colors = [
            '#3B82F6',
            '#10B981',
            '#F59E0B',
            '#8B5CF6',
            '#EC4899',
            '#06B6D4'
        ]
        colors = colors[:len(labels)]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Score: %{value:.1f}<br>%{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=title,
            height=400,
            font=dict(family="Arial, sans-serif", size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    @staticmethod
    def create_comparison_bar_chart(
        resume_scores: List[float],
        resume_names: List[str]
    ) -> go.Figure:
        """
        Create bar chart for comparing multiple resumes
        """
        colors = [VisualizationEngine.get_score_level(score)[1] for score in resume_scores]
        
        fig = go.Figure(data=[
            go.Bar(
                x=resume_names,
                y=resume_scores,
                marker=dict(color=colors, line=dict(color='white', width=2)),
                text=[f"{score:.1f}" for score in resume_scores],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Score: %{y:.2f}%<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="Resume Comparison",
            xaxis_title="Resume",
            yaxis_title="ATS Score (%)",
            height=400,
            showlegend=False,
            yaxis=dict(range=[0, 100]),
            font=dict(family="Arial, sans-serif", size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(242,245,250,0.5)',
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_progress_bars(scores: Dict[str, float], show_percentage: bool = True) -> None:
        """
        Create styled progress bars with labels and values
        """
        for metric, score in scores.items():
            level, color = VisualizationEngine.get_score_level(score)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.progress(min(score / 100, 1.0))
            
            with col2:
                st.metric(metric, f"{score:.1f}%")
            
            with col3:
                st.markdown(
                    f'<span style="color: {color}; font-weight: bold;">{level}</span>',
                    unsafe_allow_html=True
                )
    
    @staticmethod
    def create_section_score_card(
        section_name: str,
        score: float,
        feedback: str = "",
        icon: str = "📊"
    ) -> None:
        """
        Create a professional card for section scores
        """
        level, color = VisualizationEngine.get_score_level(score)
        
        html_card = f"""
        <div style="
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-left: 5px solid {color};
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #1f2937;">{icon} {section_name}</h4>
                    <p style="margin: 8px 0 0 0; color: #6b7280; font-size: 14px;">{feedback}</p>
                </div>
                <div style="text-align: center;">
                    <h2 style="margin: 0; color: {color};">{score:.0f}</h2>
                    <p style="margin: 4px 0 0 0; color: {color}; font-size: 12px; font-weight: bold;">{level}</p>
                </div>
            </div>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)
    
    @staticmethod
    def create_skills_visualization(
        matched_skills: List[str],
        missing_skills: List[str],
        total_jd_skills: int
    ) -> None:
        """
        Create professional visualization of skill matching
        """
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Matched Skills",
                len(matched_skills),
                f"{(len(matched_skills)/max(total_jd_skills, 1)*100):.0f}%"
            )
        
        with col2:
            st.metric(
                "Missing Skills",
                len(missing_skills),
                f"-{(len(missing_skills)/max(total_jd_skills, 1)*100):.0f}%"
            )
        
        with col3:
            st.metric(
                "Requirement Coverage",
                f"{total_jd_skills}",
                "Total skills in JD"
            )
        
        # Visualize skill breakdown
        skill_data = {
            'Matched': len(matched_skills),
            'Missing': len(missing_skills)
        }
        
        fig = px.pie(
            values=skill_data.values(),
            names=skill_data.keys(),
            hole=0.3,
            color_discrete_map={'Matched': '#10B981', 'Missing': '#EF4444'},
            title="Skill Match Breakdown"
        )
        
        fig.update_layout(
            height=300,
            font=dict(family="Arial, sans-serif", size=11),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_improvement_checklist(improvements: List[str]) -> None:
        """
        Create a visual checklist of improvements
        """
        st.subheader("📋 Suggested Improvements")
        
        for i, improvement in enumerate(improvements, 1):
            col1, col2 = st.columns([1, 20])
            
            with col1:
                st.write("✓")
            
            with col2:
                st.write(improvement)
    
    @staticmethod
    def create_score_timeline(history_data: List[Dict]) -> go.Figure:
        """
        Create timeline of scores over time
        """
        if not history_data:
            return None
        
        df = pd.DataFrame(history_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['score'],
            mode='lines+markers',
            name='ATS Score',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        
        fig.update_layout(
            title="Your Score Improvement Over Time",
            xaxis_title="Date",
            yaxis_title="ATS Score (%)",
            yaxis=dict(range=[0, 100]),
            height=350,
            font=dict(family="Arial, sans-serif", size=11),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(242,245,250,0.5)',
            hovermode='x unified'
        )
        
        return fig


def render_score_summary(overall_score: float, components: Dict[str, float]) -> None:
    """
    Render main ATS score summary with gauge and breakdown
    """
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig_gauge = VisualizationEngine.create_gauge_chart(overall_score, "Overall ATS Score")
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        fig_radar = VisualizationEngine.create_radar_chart(components)
        st.plotly_chart(fig_radar, use_container_width=True)


def render_score_breakdown(components: Dict[str, float]) -> None:
    """
    Render detailed component breakdown
    """
    st.subheader("📊 Score Component Breakdown")
    
    # Calculate overall from components
    weights = {'semantic_match': 0.30, 'skill_match': 0.25, 'keyword_optimization': 0.15,
               'experience_relevance': 0.15, 'education_relevance': 0.10, 'formatting_structure': 0.05}
    
    cols = st.columns(3)
    
    for idx, (component, score) in enumerate(components.items()):
        with cols[idx % 3]:
            VisualizationEngine.create_section_score_card(
                component.replace('_', ' ').title(),
                score,
                f"Weight: {weights.get(component, 0)*100:.0f}%",
                "📈"
            )

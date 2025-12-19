"""
Results Page - DPDPA Compliance Dashboard
Display assessment results with metrics and downloadable report
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.assessment.business_profiler import get_business_profile
from src.assessment.requirement_matcher import match_requirements
from src.assessment.gap_analyzer import analyze_gaps
from src.assessment.report_generator import export_to_excel

def show():
    """Render results page"""
    
    st.title("Compliance Report")
    
    # Check if we have assessment data
    if 'current_assessment' in st.session_state:
        data = st.session_state['current_assessment']
        business_id = data['business_id']
        answers = data['answers']
        analysis = data['analysis']
    elif 'selected_business_id' in st.session_state:
        # Load from database
        business_id = st.session_state['selected_business_id']
        try:
            profile = get_business_profile(business_id)
            answers = profile
            if 'extended_data' in profile:
                answers.update(profile['extended_data'])
            
            # Re-run analysis with answers
            applicable_ids = match_requirements(answers)
            analysis = analyze_gaps(business_id, applicable_ids, answers)
        except Exception as e:
            st.error(f"Error loading assessment: {e}")
            return
    else:
        st.warning("No assessment data found. Please complete an assessment first.")
        if st.button("Start New Assessment"):
            st.query_params["page"] = "assessment"
            st.rerun()
        return
    
    # Business info header
    st.markdown(f"### {answers.get('business_name', 'N/A')}")
    st.caption(f"{answers.get('entity_type', 'N/A').title()} | {answers.get('user_count', 0):,} users")
    
    st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = analysis['compliance_score']
        st.metric(
            label="Compliance Score",
            value=f"{score:.1f}%",
            delta=f"{analysis['completed']}/{analysis['total_requirements']} complete"
        )
    
    with col2:
        max_penalty_cr = analysis['max_penalty_exposure'] / 10_000_000
        st.metric(
            label="Max Single Penalty",
            value=f"Rs. {max_penalty_cr:.0f} Cr",
            delta="Security breach"
        )
    
    with col3:
        total_exposure_cr = analysis['total_penalty_exposure'] / 10_000_000
        st.metric(
            label="Total Exposure",
            value=f"Rs. {total_exposure_cr:,.0f} Cr",
            delta=f"{len(analysis['gaps'])} gaps"
        )
    
    with col4:
        deadline = datetime(2027, 5, 13)
        days_left = (deadline - datetime.now()).days
        st.metric(
            label="Days to Deadline",
            value=days_left,
            delta="May 13, 2027"
        )
    
    st.markdown("---")
    
    # Illegal activity warning (if applicable)
    if answers.get('processes_children_data'):
        if answers.get('tracks_behavior') or answers.get('targeted_advertising'):
            violations = []
            if answers.get('tracks_behavior'):
                violations.append("Behavioral tracking of children")
            if answers.get('targeted_advertising'):
                violations.append("Targeted advertising to children")
                
            st.error(f"""
            ### CRITICAL LEGAL VIOLATION
            
            You are currently violating **DPDP Act Section 9(3)**:
            
            {chr(10).join('- ' + v for v in violations)}
            
            **PENALTY: Rs. 200 CRORE PER VIOLATION**
            
            **Action required: IMMEDIATELY cease these activities!**
            """)
    
    # Requirements breakdown with visualizations
    st.subheader("Requirements Breakdown")
    
    # Check dark mode
    is_dark = st.session_state.get('dark_mode', False)
    bg_color = '#1a1a1a' if is_dark else 'white'
    text_color = '#e0e0e0' if is_dark else '#262730'
    grid_color = '#404040' if is_dark else '#e0e0e0'
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pie chart of requirements by type
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=[t.title() for t in analysis['by_type'].keys()],
            values=list(analysis['by_type'].values()),
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textfont=dict(family='Arial', size=11, color=text_color)
        )])
        
        fig_pie.update_layout(
            title=dict(
                text="Requirements Distribution",
                font=dict(family='Arial', size=16, color=text_color)
            ),
            showlegend=True,
            legend=dict(
                orientation="v",
                font=dict(family='Arial', size=10, color=text_color)
            ),
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(family='Arial', color=text_color),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Compliance progress gauge
        score = analysis['compliance_score']
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Compliance Score", 'font': {'family': 'Arial', 'size': 18, 'color': text_color}},
            number={'suffix': "%", 'font': {'size': 40, 'color': text_color}},
            gauge={
                'axis': {'range': [None, 100], 'tickfont': {'family': 'Arial', 'color': text_color}},
                'bar': {'color': "#667eea"},
                'bgcolor': bg_color,
                'borderwidth': 2,
                'bordercolor': grid_color,
                'steps': [
                    {'range': [0, 33], 'color': '#ffebee' if not is_dark else '#4a1a1a'},
                    {'range': [33, 66], 'color': '#fff9c4' if not is_dark else '#4a4a1a'},
                    {'range': [66, 100], 'color': '#e8f5e9' if not is_dark else '#1a4a1a'}
                ],
                'threshold': {
                    'line': {'color': "#43e97b", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=50, b=20),
            font={'family': 'Arial', 'size': 14, 'color': text_color},
            paper_bgcolor=bg_color
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Statistics summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Requirements",
            analysis['total_requirements'],
            help="Total applicable requirements for your business"
        )
    
    with col2:
        st.metric(
            "Completed",
            analysis['completed'],
            delta=f"{analysis['compliance_score']:.1f}%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Pending",
            len(analysis['gaps']),
            delta=f"-{100-analysis['compliance_score']:.1f}%",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Penalty exposure bar chart
    st.subheader("Penalty Exposure Analysis")
    
    # Create penalty breakdown
    penalty_breakdown = {}
    for req in analysis['gaps']:
        penalty_cat = req.get('penalty_category', 'Unknown')
        penalty_amt = req.get('penalty_amount', 0)
        oblig_type = req.get('obligation_type', 'general')
        
        if oblig_type not in penalty_breakdown:
            penalty_breakdown[oblig_type] = {
                'count': 0,
                'total_exposure': 0,
                'max_penalty': 0
            }
        
        penalty_breakdown[oblig_type]['count'] += 1
        penalty_breakdown[oblig_type]['total_exposure'] += penalty_amt
        penalty_breakdown[oblig_type]['max_penalty'] = max(
            penalty_breakdown[oblig_type]['max_penalty'], 
            penalty_amt
        )
    
    if penalty_breakdown:
        # Create bar chart data
        categories = []
        counts = []
        exposures = []
        colors_bar = []
        
        color_map = {
            'security': '#667eea',
            'breach': '#764ba2',
            'children': '#f093fb',
            'notice': '#4facfe',
            'rights': '#00f2fe',
            'retention': '#43e97b',
            'sdf': '#f6d365',
            'general': '#fda085'
        }
        
        for oblig_type, data in sorted(penalty_breakdown.items(), key=lambda x: x[1]['total_exposure'], reverse=True):
            categories.append(oblig_type.title())
            counts.append(data['count'])
            exposures.append(data['total_exposure'] / 10_000_000)  # Convert to crores
            colors_bar.append(color_map.get(oblig_type, '#667eea'))
        
        fig_bar = go.Figure()
        
        # Add exposure bars
        fig_bar.add_trace(go.Bar(
            x=categories,
            y=exposures,
            name='Total Exposure (Rs. Cr)',
            marker=dict(color=colors_bar, line=dict(color=text_color, width=1)),
            text=[f"Rs. {e:.0f} Cr" for e in exposures],
            textposition='auto',
            textfont=dict(family='Arial', size=11, color=text_color),
            hovertemplate='<b>%{x}</b><br>Exposure: Rs. %{y:.0f} Cr<br><extra></extra>'
        ))
        
        fig_bar.update_layout(
            title=dict(
                text="Penalty Exposure by Requirement Type",
                font=dict(family='Arial', size=16, color=text_color)
            ),
            xaxis=dict(
                title=dict(
                    text="Requirement Type",
                    font=dict(color=text_color)
                ),
                tickangle=-45,
                tickfont=dict(family='Arial', size=11, color=text_color),
                gridcolor=grid_color
            ),
            yaxis=dict(
                title=dict(
                    text="Total Penalty Exposure (Rs. Crore)",
                    font=dict(color=text_color)
                ),
                tickfont=dict(family='Arial', color=text_color),
                gridcolor=grid_color
            ),
            height=400,
            margin=dict(l=50, r=50, t=60, b=100),
            font=dict(family='Arial', color=text_color),
            showlegend=False,
            hovermode='x unified',
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # Top priorities
    st.subheader("Top 10 Priority Requirements")
    
    priorities_data = []
    for req in analysis['priority_requirements'][:10]:
        priorities_data.append({
            'Priority': f"{req['priority_score']:.1f}/100",
            'Rule': req['rule_number'],
            'Type': req['obligation_type'].title(),
            'Penalty': f"Rs. {req['penalty_amount'] / 10_000_000:.0f} Cr",
            'Days Left': req['days_remaining'],
            'Description': req['requirement_text'][:80] + "..."
        })
    
    df_priorities = pd.DataFrame(priorities_data)
    st.dataframe(df_priorities, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export to Excel
        if st.button("Download Excel Report", use_container_width=True):
            try:
                # Generate Excel
                output_dir = project_root / "data" / "processed" / "assessment_results"
                output_dir.mkdir(parents=True, exist_ok=True)
                
                business_name_clean = answers['business_name'].replace(' ', '_').replace('/', '_')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"assessment_{business_id}_{business_name_clean}_{timestamp}.xlsx"
                filepath = output_dir / filename
                
                # Get full profile
                profile = get_business_profile(business_id)
                profile.update(answers)
                
                export_to_excel(profile, analysis, str(filepath))
                
                # Provide download
                with open(filepath, 'rb') as f:
                    st.download_button(
                        label="Save Excel File",
                        data=f,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"Error generating Excel: {e}")
    
    with col2:
        if st.button("New Assessment", use_container_width=True):
            # Clear session state
            if 'current_assessment' in st.session_state:
                del st.session_state['current_assessment']
            if 'selected_business_id' in st.session_state:
                del st.session_state['selected_business_id']
            st.query_params["page"] = "assessment"
            st.rerun()
    
    with col3:
        if st.button("Back to Home", use_container_width=True):
            # Clear selected business ID
            if 'selected_business_id' in st.session_state:
                del st.session_state['selected_business_id']
            st.query_params["page"] = "home"
            st.rerun()
    
    st.markdown("---")
    
    # Next steps
    st.subheader("Next Steps")
    
    st.markdown("""
    1. **Review Priority Requirements** - Focus on high-penalty items first
    2. **Implement Security Measures** - Rule 6 (Rs. 250 crore penalty)
    3. **Setup Breach Response** - Rule 7 (Rs. 200 crore penalty, 72-hour timeline)
    4. **Children's Data Compliance** - Rule 10 (Rs. 200 crore penalty if applicable)
    5. **Track Progress** - Update compliance status as you implement
    
    **Need Help?**
    - Download the Excel report for detailed analysis
    - Consult a data protection lawyer for legal advice
    - Monitor MEITY website for updates and guidance
    """)

if __name__ == "__main__":
    show()
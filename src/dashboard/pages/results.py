"""
Results Page - DPDPA Compliance Dashboard
Display assessment results with metrics and downloadable report
ENHANCED: Dynamic "Next Steps" based on actual gaps
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
        oblig_type = req.get('obligation_type', 'general')
        penalty_amt = req.get('penalty_amount', 0)
        
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
            exposures.append(data['total_exposure'] / 10_000_000)  # Convert to crores
            colors_bar.append(color_map.get(oblig_type, '#667eea'))
        
        fig_bar = go.Figure()
        
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
    
    # Dynamic Next Steps - Personalized to Actual Gaps
    st.subheader("Your Personalized Action Plan")
    
    # Analyze gaps to generate tailored recommendations
    top_gaps = analysis['priority_requirements'][:5]
    
    if not top_gaps:
        # Perfect or near-perfect compliance
        st.success("""
        ### Congratulations! You have excellent compliance.
        
        **To Maintain Your Status:**
        1. Document all your compliance measures for audit purposes
        2. Schedule regular audits (quarterly recommended)
        3. Monitor MEITY website for regulatory updates
        4. Train your team on DPDP requirements
        5. Update your privacy notices annually
        
        **Keep up the great work!**
        """)
    else:
        # Generate personalized steps based on gap types
        gap_types = {}
        for gap in top_gaps:
            gtype = gap['obligation_type']
            if gtype not in gap_types:
                gap_types[gtype] = []
            gap_types[gtype].append(gap)
        
        step_num = 1
        
        # Security gaps (highest penalty - always prioritize)
        if 'security' in gap_types:
            security_gaps = gap_types['security']
            penalty_total = sum(g['penalty_amount'] for g in security_gaps) / 10_000_000
            st.error(f"""
### {step_num}. CRITICAL: Implement Security Safeguards (Rule 6)

**Penalty Exposure:** Rs. {penalty_total:.0f} crore  
**Missing:** {len(security_gaps)} security requirement(s)

**Required Actions:**
- Implement data encryption (in transit and at rest)
- Setup access control mechanisms (role-based permissions)
- Enable comprehensive logging (retain for 1 year minimum)
- Implement backup and recovery procedures

**Timeline:** Start immediately - this is your highest priority  
**Estimated Effort:** 4-8 weeks depending on current infrastructure
            """)
            step_num += 1
        
        # Breach notification gaps
        if 'breach' in gap_types:
            breach_gaps = gap_types['breach']
            penalty_total = sum(g['penalty_amount'] for g in breach_gaps) / 10_000_000
            st.warning(f"""
### {step_num}. HIGH PRIORITY: Setup Breach Response Plan (Rule 7)

**Penalty Exposure:** Rs. {penalty_total:.0f} crore  
**Missing:** {len(breach_gaps)} breach notification requirement(s)

**Required Actions:**
- Create documented breach response procedures
- Setup 72-hour notification process to Data Protection Board
- Create breach notification templates for Data Principals
- Designate breach response team with clear roles

**Timeline:** Complete within 2-4 weeks  
**Estimated Effort:** 2-3 weeks (documentation + testing)
            """)
            step_num += 1
        
        # Children's data gaps
        if 'children' in gap_types:
            children_gaps = gap_types['children']
            penalty_total = sum(g['penalty_amount'] for g in children_gaps) / 10_000_000
            st.error(f"""
### {step_num}. HIGH PRIORITY: Children's Data Protection (Rule 10)

**Penalty Exposure:** Rs. {penalty_total:.0f} crore  
**Missing:** {len(children_gaps)} children data requirement(s)

**Required Actions:**
- Implement verifiable parental consent mechanism
- IMMEDIATELY disable behavioral tracking of children
- IMMEDIATELY disable targeted advertising to children
- Add age verification at registration

**Timeline:** Immediate action required - legal compliance critical  
**Estimated Effort:** 1-2 weeks (urgent implementation)
            """)
            step_num += 1
        
        # Notice/Consent gaps
        if 'notice' in gap_types:
            notice_gaps = gap_types['notice']
            penalty_total = sum(g['penalty_amount'] for g in notice_gaps) / 10_000_000
            st.info(f"""
### {step_num}. IMPORTANT: Update Privacy Notice (Rule 3)

**Penalty Exposure:** Rs. {penalty_total:.0f} crore  
**Missing:** {len(notice_gaps)} notice requirement(s)

**Required Actions:**
- Draft compliant privacy notice in clear, plain language
- Implement consent mechanism (must be as easy to withdraw as to give)
- Add links to exercise Data Principal rights
- Publish prominently on website and mobile app

**Timeline:** 2-3 weeks  
**Estimated Effort:** 1-2 weeks (legal review recommended)
            """)
            step_num += 1
        
        # Rights/Grievance gaps
        if 'rights' in gap_types:
            rights_gaps = gap_types['rights']
            penalty_total = sum(g['penalty_amount'] for g in rights_gaps) / 10_000_000
            st.info(f"""
### {step_num}. IMPORTANT: Data Principal Rights System (Rule 14)

**Penalty Exposure:** Rs. {penalty_total:.0f} crore  
**Missing:** {len(rights_gaps)} rights requirement(s)

**Required Actions:**
- Setup grievance redressal system (90-day response timeline)
- Enable data access, correction, and erasure requests
- Publish contact information for rights requests
- Create tracking system for request handling

**Timeline:** 1-2 months  
**Estimated Effort:** 3-4 weeks (portal setup + testing)
            """)
            step_num += 1
        
        # Retention gaps
        if 'retention' in gap_types:
            retention_gaps = gap_types['retention']
            penalty_total = sum(g['penalty_amount'] for g in retention_gaps) / 10_000_000
            st.info(f"""
### {step_num}. Data Retention Policy (Rule 8)

**Penalty Exposure:** Rs. {penalty_total:.0f} crore  
**Missing:** {len(retention_gaps)} retention requirement(s)

**Required Actions:**
- Document data retention schedules per purpose
- Implement automated data erasure procedures
- Add 48-hour warning before data deletion
- Create retention policy documentation

**Timeline:** 1-2 months  
**Estimated Effort:** 2-3 weeks (policy + automation)
            """)
            step_num += 1
        
        # SDF gaps (if applicable)
        if 'sdf' in gap_types:
            sdf_gaps = gap_types['sdf']
            penalty_total = sum(g['penalty_amount'] for g in sdf_gaps) / 10_000_000
            st.warning(f"""
### {step_num}. SDF Obligations (Rule 13) *(if designated)*

**Penalty Exposure:** Rs. {penalty_total:.0f} crore  
**Missing:** {len(sdf_gaps)} SDF requirement(s)

**Required Actions:**
- Conduct annual Data Protection Impact Assessment (DPIA)
- Appoint Data Protection Officer (DPO) based in India
- Conduct annual independent audit
- Perform algorithmic due diligence (if using AI)

**Timeline:** 3-6 months (complex requirements)  
**Estimated Effort:** Ongoing (annual obligations)

**Note:** SDF designation is pending government notification
            """)
            step_num += 1
        
        # Generic final steps
        st.info(f"""
### {step_num}. Track Your Progress

**Recommended Actions:**
- Download the Excel report above for detailed implementation roadmap
- Re-run this assessment as you complete requirements
- Document all compliance measures for audit trail
- Set calendar reminders for deadline milestones

**Progress Tracking:**
- Every 30 days: Review and update implementation status
- Every 90 days: Re-assess compliance score
- 6 months before deadline: Final review and gap closure
        """)
        step_num += 1
        
        st.success(f"""
### {step_num}. Get Professional Help

**When to Consult Experts:**
- Legal advisor: For compliance strategy and implementation guidance
- Compliance consultant: For complex technical requirements
- Industry peers: Join DPDP compliance communities for support

**Remember:** This tool provides guidance, but professional legal advice is recommended for critical decisions.
        """)
    
    # Deadline-based urgency warning
    days_left = (datetime(2027, 5, 13) - datetime.now()).days
    
    st.markdown("---")
    
    if days_left < 180:
        st.error(f"""
        ### URGENT: Only {days_left} days until May 13, 2027 deadline!
        
        **You are in the final 6 months.** You should be:
        - Completing final implementations
        - Conducting internal audits
        - Training all team members
        - Finalizing documentation
        
        **Prioritize high-penalty gaps (Rules 6, 7, 10) immediately!**
        """)
    elif days_left < 365:
        st.warning(f"""
        ### {days_left} days remaining until May 13, 2027 deadline
        
        **You are in the final 12 months.** You should be:
        - Actively implementing compliance measures
        - Completing technical requirements (Rules 6, 7)
        - Finalizing policies and documentation
        - Beginning team training
        
        **Stay on track - focus on the action plan above!**
        """)
    else:
        st.info(f"""
        ### {days_left} days until May 13, 2027 deadline
        
        **Good timing to start compliance!** You have sufficient time to:
        - Plan your implementation strategy
        - Budget for compliance requirements
        - Build your compliance team
        - Implement measures systematically
        
        **Follow the priority order above for optimal results.**
        """)
# ============================================================================
# DOCUMENT GENERATION SECTION
# ============================================================================

st.markdown("---")
st.subheader("Generate Required Documents")

st.info("""
Based on your compliance gaps, generate DPDP-compliant legal document templates.

**IMPORTANT:** Generated documents are templates requiring legal review before deployment.
Yellow-highlighted sections need manual completion.
""")

try:
    from src.document_generator import DocumentGenerator, DocumentGenerationError
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Universal Documents (All Businesses)**")
        
        doc_configs = {
            'Privacy Notice (Rule 3)': ('privacy_notice', 'generate_privacy_notice'),
            'Consent Form (Section 6)': ('consent_form', 'generate_consent_form'),
            'Grievance Procedure (Rule 14)': ('grievance_procedure', 'generate_grievance_procedure'),
            'Retention Schedule (Rule 8)': ('retention_schedule', 'generate_retention_schedule')
        }
        
        for label, (file_prefix, method_name) in doc_configs.items():
            if st.button(label, key=f"btn_{file_prefix}", use_container_width=True):
                try:
                    with st.spinner(f"Generating {label}..."):
                        generator = DocumentGenerator(answers, analysis)
                        doc = getattr(generator, method_name)()
                        
                        filepath = generator.export_to_docx(
                            doc, 
                            f"{file_prefix}_{business_id}.docx"
                        )
                        
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                f"Download {label}",
                                data=f,
                                file_name=f"{file_prefix}_{answers['business_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key=f"dl_{file_prefix}"
                            )
                        
                        st.success(f"{label} generated. Review yellow-highlighted sections before use.")
                
                except DocumentGenerationError as e:
                    st.error(f"Generation failed: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
    
    with col2:
        st.markdown("**Pre-Crisis Templates**")
        
        if st.button("Breach Notification Templates (Rule 7)", use_container_width=True, key="btn_breach"):
            try:
                with st.spinner("Generating breach templates..."):
                    generator = DocumentGenerator(answers, analysis)
                    doc_dpb, doc_users = generator.generate_breach_notification_templates()
                    
                    path_dpb = generator.export_to_docx(doc_dpb, f"breach_dpb_{business_id}.docx")
                    path_users = generator.export_to_docx(doc_users, f"breach_users_{business_id}.docx")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        with open(path_dpb, 'rb') as f:
                            st.download_button(
                                "DPB Notification",
                                data=f,
                                file_name=f"breach_dpb_{answers['business_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="dl_breach_dpb"
                            )
                    with col_b:
                        with open(path_users, 'rb') as f:
                            st.download_button(
                                "User Notification",
                                data=f,
                                file_name=f"breach_users_{answers['business_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="dl_breach_users"
                            )
                    
                    st.success("Breach templates generated. Store with incident response plan.")
            
            except Exception as e:
                st.error(f"Generation failed: {e}")
        
        st.markdown("**Conditional Documents**")
        
        if answers.get('processes_children_data'):
            if st.button("Parental Consent Form (Rule 10)", use_container_width=True, key="btn_parental"):
                try:
                    with st.spinner("Generating parental consent form..."):
                        generator = DocumentGenerator(answers, analysis)
                        doc = generator.generate_parental_consent_form()
                        
                        if doc:
                            filepath = generator.export_to_docx(doc, f"parental_consent_{business_id}.docx")
                            
                            with open(filepath, 'rb') as f:
                                st.download_button(
                                    "Download Parental Consent Form",
                                    data=f,
                                    file_name=f"parental_consent_{answers['business_name']}.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    key="dl_parental"
                                )
                            
                            st.success("Parental consent form generated.")
                
                except Exception as e:
                    st.error(f"Generation failed: {e}")
        
        if answers.get('has_processors'):
            if st.button("Processor Agreement Checklist (Rule 6)", use_container_width=True, key="btn_processor"):
                st.warning("**Note:** This generates a CHECKLIST, not a full legal agreement.")
                
                try:
                    with st.spinner("Generating processor checklist..."):
                        generator = DocumentGenerator(answers, analysis)
                        doc = generator.generate_processor_agreement_checklist()
                        
                        if doc:
                            filepath = generator.export_to_docx(doc, f"processor_checklist_{business_id}.docx")
                            
                            with open(filepath, 'rb') as f:
                                st.download_button(
                                    "Download Processor Checklist",
                                    data=f,
                                    file_name=f"processor_checklist_{answers['business_name']}.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    key="dl_processor"
                                )
                            
                            st.success("Processor agreement checklist generated.")
                
                except Exception as e:
                    st.error(f"Generation failed: {e}")
    
    st.markdown("---")
    
    # Bulk generation
    if st.button("Generate All Required Documents (ZIP)", use_container_width=True, type="primary", key="btn_bulk"):
        try:
            with st.spinner("Generating all documents..."):
                generator = DocumentGenerator(answers, analysis)
                documents = generator.generate_all_required_documents()
                
                zip_path = generator.export_all_to_zip(
                    documents, 
                    f"DPDP_Documents_{business_id}.zip"
                )
                
                with open(zip_path, 'rb') as f:
                    st.download_button(
                        "Download All Documents (ZIP)",
                        data=f,
                        file_name=f"DPDP_Documents_{answers['business_name']}.zip",
                        mime="application/zip",
                        key="dl_bulk"
                    )
                
                st.success(f"""
                Generated {len(documents)} documents. Review all yellow-highlighted sections.
                
                Have a lawyer review before deployment.
                """)
        
        except Exception as e:
            st.error(f"Bulk generation failed: {e}")
            st.exception(e)

except ImportError:
    st.error("Document generator module not found. Ensure src/document_generator is installed.")
if __name__ == "__main__":
    show()
"""
Documents Page - DPDPA Compliance Dashboard
Generate DPDP-compliant legal document templates
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.assessment.business_profiler import get_business_profile
from src.assessment.requirement_matcher import match_requirements
from src.assessment.gap_analyzer import analyze_gaps

def show():
    """Render documents generation page"""
    
    st.title("Legal Document Generation")
    
    st.markdown("""
    Generate DPDP-compliant legal document templates pre-filled with your business information.
    All documents require legal review before deployment.
    """)
    
    # Check if we have assessment data
    if 'current_assessment' in st.session_state:
        data = st.session_state['current_assessment']
        business_id = data['business_id']
        answers = data['answers']
        analysis = data['analysis']
    elif 'selected_business_id' in st.session_state:
        business_id = st.session_state['selected_business_id']
        try:
            profile = get_business_profile(business_id)
            answers = profile
            if 'extended_data' in profile:
                answers.update(profile['extended_data'])
            
            applicable_ids = match_requirements(answers)
            analysis = analyze_gaps(business_id, applicable_ids, answers)
        except Exception as e:
            st.error(f"Error loading assessment: {e}")
            st.info("Please complete an assessment first to generate documents.")
            if st.button("Start New Assessment", type="primary"):
                st.query_params["page"] = "assessment"
                st.rerun()
            return
    else:
        st.warning("No assessment data found. Complete an assessment to generate documents.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start New Assessment", use_container_width=True, type="primary"):
                st.query_params["page"] = "assessment"
                st.rerun()
        return
    
    # Business info bar
    st.markdown(f"""
    <div style='padding: 0.75rem 1rem; background-color: #f8f9fa; border-left: 4px solid #2c5282; 
                margin-bottom: 1.5rem; font-family: Arial, sans-serif;'>
        <strong>Business:</strong> {answers.get('business_name', 'N/A')} &nbsp;|&nbsp; 
        <strong>Type:</strong> {answers.get('entity_type', 'N/A').title()} &nbsp;|&nbsp; 
        <strong>Users:</strong> {answers.get('user_count', 0):,}
    </div>
    """, unsafe_allow_html=True)
    
    # Important disclaimers
    st.markdown("""
    <div style='padding: 1rem; background-color: #fff3cd; border-left: 4px solid #856404; 
                margin-bottom: 1.5rem; font-family: Arial, sans-serif;'>
        <strong>LEGAL DISCLAIMER</strong><br>
        Generated documents are templates only. They require review by qualified legal counsel 
        before deployment. Yellow-highlighted sections need manual completion. Developer assumes 
        no liability for use of these templates.
    </div>
    """, unsafe_allow_html=True)
    
    # Cost information
    st.markdown("""
    <div style='padding: 1rem; background-color: #d4edda; border-left: 4px solid #155724; 
                margin-bottom: 1.5rem; font-family: Arial, sans-serif;'>
        <strong>COST SAVINGS:</strong> Law firms typically charge Rs. 1,15,000 - 2,10,000 for these documents.
        Generate instantly here (legal review still required).
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Document Generation Module
    try:
        from src.document_generator import DocumentGenerator, DocumentGenerationError
        
        generator = DocumentGenerator(answers, analysis)
        
        # Universal Documents
        st.markdown("### Universal Documents")
        st.caption("Required for all businesses under DPDP Act 2023")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2x2 Grid
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        
        # Privacy Notice
        with row1_col1:
            st.markdown("""
            <div style='border: 1px solid #2c5282; padding: 1.25rem; margin-bottom: 1rem; 
                        background-color: #ffffff;'>
                <div style='border-bottom: 2px solid #2c5282; padding-bottom: 0.5rem; margin-bottom: 0.75rem;'>
                    <h4 style='margin: 0; color: #2c5282; font-size: 1.1rem;'>Privacy Notice</h4>
                </div>
                <p style='margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #495057;'>
                    <strong>Rule 3</strong> | Penalty: Rs. 50 Crore
                </p>
                <p style='margin: 0 0 0.75rem 0; font-size: 0.85rem; color: #6c757d; line-height: 1.4;'>
                    Disclosure of data collection practices, purposes, and Data Principal rights. 
                    Must be in clear, plain language.
                </p>
                <p style='margin: 0; font-size: 0.8rem; color: #868e96;'>
                    2 pages | 30 seconds generation time
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Generate Privacy Notice", key="btn_privacy", use_container_width=True):
                try:
                    with st.spinner("Generating Privacy Notice..."):
                        doc = generator.generate_privacy_notice()
                        filepath = generator.export_to_docx(doc, f"privacy_notice_{business_id}.docx")
                        
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                "Download Privacy Notice",
                                data=f,
                                file_name=f"Privacy_Notice_{answers['business_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="dl_privacy",
                                use_container_width=True
                            )
                        
                        st.success("Privacy Notice generated. Review yellow-highlighted sections before deployment.")
                
                except DocumentGenerationError as e:
                    st.error(f"Generation failed: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
        
        # Consent Form
        with row1_col2:
            st.markdown("""
            <div style='border: 1px solid #2c5282; padding: 1.25rem; margin-bottom: 1rem; 
                        background-color: #ffffff;'>
                <div style='border-bottom: 2px solid #2c5282; padding-bottom: 0.5rem; margin-bottom: 0.75rem;'>
                    <h4 style='margin: 0; color: #2c5282; font-size: 1.1rem;'>Consent Form</h4>
                </div>
                <p style='margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #495057;'>
                    <strong>Section 6</strong> | Penalty: Rs. 50 Crore
                </p>
                <p style='margin: 0 0 0.75rem 0; font-size: 0.85rem; color: #6c757d; line-height: 1.4;'>
                    Template for obtaining free, specific, informed, and unambiguous user consent 
                    as required by DPDP Act.
                </p>
                <p style='margin: 0; font-size: 0.8rem; color: #868e96;'>
                    2 pages | 30 seconds generation time
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Generate Consent Form", key="btn_consent", use_container_width=True):
                try:
                    with st.spinner("Generating Consent Form..."):
                        doc = generator.generate_consent_form()
                        filepath = generator.export_to_docx(doc, f"consent_form_{business_id}.docx")
                        
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                "Download Consent Form",
                                data=f,
                                file_name=f"Consent_Form_{answers['business_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="dl_consent",
                                use_container_width=True
                            )
                        
                        st.success("Consent Form generated. Review yellow-highlighted sections before deployment.")
                
                except DocumentGenerationError as e:
                    st.error(f"Generation failed: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
        
        # Grievance Procedure
        with row2_col1:
            st.markdown("""
            <div style='border: 1px solid #2c5282; padding: 1.25rem; margin-bottom: 1rem; 
                        background-color: #ffffff;'>
                <div style='border-bottom: 2px solid #2c5282; padding-bottom: 0.5rem; margin-bottom: 0.75rem;'>
                    <h4 style='margin: 0; color: #2c5282; font-size: 1.1rem;'>Grievance Redressal Procedure</h4>
                </div>
                <p style='margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #495057;'>
                    <strong>Rule 14</strong> | Penalty: Rs. 50 Crore
                </p>
                <p style='margin: 0 0 0.75rem 0; font-size: 0.85rem; color: #6c757d; line-height: 1.4;'>
                    Documented process for handling Data Principal complaints. 
                    90-day response timeline mandated.
                </p>
                <p style='margin: 0; font-size: 0.8rem; color: #868e96;'>
                    3 pages | 45 seconds generation time
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Generate Grievance Procedure", key="btn_grievance", use_container_width=True):
                try:
                    with st.spinner("Generating Grievance Redressal Procedure..."):
                        doc = generator.generate_grievance_procedure()
                        filepath = generator.export_to_docx(doc, f"grievance_procedure_{business_id}.docx")
                        
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                "Download Grievance Procedure",
                                data=f,
                                file_name=f"Grievance_Procedure_{answers['business_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="dl_grievance",
                                use_container_width=True
                            )
                        
                        st.success("Grievance Procedure generated. Review yellow-highlighted sections before deployment.")
                
                except DocumentGenerationError as e:
                    st.error(f"Generation failed: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
        
        # Retention Schedule
        with row2_col2:
            st.markdown("""
            <div style='border: 1px solid #2c5282; padding: 1.25rem; margin-bottom: 1rem; 
                        background-color: #ffffff;'>
                <div style='border-bottom: 2px solid #2c5282; padding-bottom: 0.5rem; margin-bottom: 0.75rem;'>
                    <h4 style='margin: 0; color: #2c5282; font-size: 1.1rem;'>Data Retention Schedule</h4>
                </div>
                <p style='margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #495057;'>
                    <strong>Rule 8</strong> | Penalty: Rs. 50 Crore
                </p>
                <p style='margin: 0 0 0.75rem 0; font-size: 0.85rem; color: #6c757d; line-height: 1.4;'>
                    Data retention periods by category with legal basis. 
                    Includes 48-hour warning mechanism before deletion.
                </p>
                <p style='margin: 0; font-size: 0.8rem; color: #868e96;'>
                    2 pages | 30 seconds generation time
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Generate Retention Schedule", key="btn_retention", use_container_width=True):
                try:
                    with st.spinner("Generating Data Retention Schedule..."):
                        doc = generator.generate_retention_schedule()
                        filepath = generator.export_to_docx(doc, f"retention_schedule_{business_id}.docx")
                        
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                "Download Retention Schedule",
                                data=f,
                                file_name=f"Retention_Schedule_{answers['business_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="dl_retention",
                                use_container_width=True
                            )
                        
                        st.success("Retention Schedule generated. Review yellow-highlighted sections before deployment.")
                
                except DocumentGenerationError as e:
                    st.error(f"Generation failed: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
        
        st.markdown("---")
        
        # Pre-Crisis Templates
        st.markdown("### Pre-Crisis Templates")
        st.caption("Store these with your incident response plan. Use only when data breach occurs.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='border: 1px solid #721c24; padding: 1.25rem; margin-bottom: 1rem; 
                    background-color: #ffffff;'>
            <div style='border-bottom: 2px solid #721c24; padding-bottom: 0.5rem; margin-bottom: 0.75rem;'>
                <h4 style='margin: 0; color: #721c24; font-size: 1.1rem;'>Breach Notification Templates</h4>
            </div>
            <p style='margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #495057;'>
                <strong>Rule 7</strong> | Penalty: Rs. 200 Crore
            </p>
            <p style='margin: 0 0 0.75rem 0; font-size: 0.85rem; color: #6c757d; line-height: 1.4;'>
                Two templates: (1) Notification to Data Protection Board (72-hour deadline), 
                (2) Notification to affected users (clear language requirement).
                <strong>DO NOT FILE THESE NOW.</strong> Pre-prepared for crisis preparedness only.
            </p>
            <p style='margin: 0; font-size: 0.8rem; color: #868e96;'>
                7 pages total | 60 seconds generation time
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate Breach Notification Templates", key="btn_breach", use_container_width=True):
            try:
                with st.spinner("Generating breach notification templates..."):
                    doc_dpb, doc_users = generator.generate_breach_notification_templates()
                    
                    path_dpb = generator.export_to_docx(doc_dpb, f"breach_dpb_{business_id}.docx")
                    path_users = generator.export_to_docx(doc_users, f"breach_users_{business_id}.docx")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        with open(path_dpb, 'rb') as f:
                            st.download_button(
                                "Download DPB Notification",
                                data=f,
                                file_name=f"Breach_DPB_{answers['business_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="dl_breach_dpb",
                                use_container_width=True
                            )
                    with col_b:
                        with open(path_users, 'rb') as f:
                            st.download_button(
                                "Download User Notification",
                                data=f,
                                file_name=f"Breach_Users_{answers['business_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="dl_breach_users",
                                use_container_width=True
                            )
                    
                    st.success("Breach notification templates generated. Store with incident response plan. Use only when breach occurs.")
            
            except Exception as e:
                st.error(f"Generation failed: {e}")
        
        st.markdown("---")
        
        # Conditional Documents
        st.markdown("### Conditional Documents")
        st.caption("Required only if applicable to your business operations")
        st.markdown("<br>", unsafe_allow_html=True)
        
        conditional_col1, conditional_col2 = st.columns(2)
        
        # Parental Consent
        with conditional_col1:
            if answers.get('processes_children_data'):
                st.markdown("""
                <div style='border: 1px solid #2c5282; padding: 1.25rem; margin-bottom: 1rem; 
                            background-color: #ffffff;'>
                    <div style='border-bottom: 2px solid #2c5282; padding-bottom: 0.5rem; margin-bottom: 0.75rem;'>
                        <h4 style='margin: 0; color: #2c5282; font-size: 1.1rem;'>Parental Consent Form</h4>
                    </div>
                    <p style='margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #495057;'>
                        <strong>Rule 10</strong> | Penalty: Rs. 200 Crore
                    </p>
                    <p style='margin: 0 0 0.75rem 0; font-size: 0.85rem; color: #6c757d; line-height: 1.4;'>
                        Verifiable parental consent mechanism for processing data of children under 18 years.
                    </p>
                    <p style='margin: 0; font-size: 0.8rem; color: #868e96;'>
                        3 pages | 45 seconds generation time
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Generate Parental Consent Form", key="btn_parental", use_container_width=True):
                    try:
                        with st.spinner("Generating parental consent form..."):
                            doc = generator.generate_parental_consent_form()
                            
                            if doc:
                                filepath = generator.export_to_docx(doc, f"parental_consent_{business_id}.docx")
                                
                                with open(filepath, 'rb') as f:
                                    st.download_button(
                                        "Download Parental Consent Form",
                                        data=f,
                                        file_name=f"Parental_Consent_{answers['business_name']}.docx",
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        key="dl_parental",
                                        use_container_width=True
                                    )
                                
                                st.success("Parental consent form generated. Review yellow-highlighted sections before deployment.")
                    
                    except Exception as e:
                        st.error(f"Generation failed: {e}")
            else:
                st.markdown("""
                <div style='border: 1px solid #d1d3d4; padding: 1.25rem; margin-bottom: 1rem; 
                            background-color: #f8f9fa;'>
                    <h4 style='margin: 0 0 0.5rem 0; color: #6c757d; font-size: 1.1rem;'>Parental Consent Form</h4>
                    <p style='margin: 0; font-size: 0.85rem; color: #868e96;'>
                        Not applicable - Your business does not process children's data.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Processor Checklist
        with conditional_col2:
            if answers.get('has_processors'):
                st.markdown("""
                <div style='border: 1px solid #2c5282; padding: 1.25rem; margin-bottom: 1rem; 
                            background-color: #ffffff;'>
                    <div style='border-bottom: 2px solid #2c5282; padding-bottom: 0.5rem; margin-bottom: 0.75rem;'>
                        <h4 style='margin: 0; color: #2c5282; font-size: 1.1rem;'>Data Processor Agreement Checklist</h4>
                    </div>
                    <p style='margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #495057;'>
                        <strong>Rule 6</strong> | Penalty: Rs. 250 Crore
                    </p>
                    <p style='margin: 0 0 0.75rem 0; font-size: 0.85rem; color: #6c757d; line-height: 1.4;'>
                        Checklist of required contractual clauses for data processor agreements. 
                        <strong>Note:</strong> This is a checklist, not a complete legal agreement.
                    </p>
                    <p style='margin: 0; font-size: 0.8rem; color: #868e96;'>
                        2 pages | 30 seconds generation time
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Generate Processor Agreement Checklist", key="btn_processor", use_container_width=True):
                    try:
                        with st.spinner("Generating data processor agreement checklist..."):
                            doc = generator.generate_processor_agreement_checklist()
                            
                            if doc:
                                filepath = generator.export_to_docx(doc, f"processor_checklist_{business_id}.docx")
                                
                                with open(filepath, 'rb') as f:
                                    st.download_button(
                                        "Download Processor Checklist",
                                        data=f,
                                        file_name=f"Processor_Checklist_{answers['business_name']}.docx",
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        key="dl_processor",
                                        use_container_width=True
                                    )
                                
                                st.success("Processor agreement checklist generated. Full legal agreement requires legal counsel.")
                    
                    except Exception as e:
                        st.error(f"Generation failed: {e}")
            else:
                st.markdown("""
                <div style='border: 1px solid #d1d3d4; padding: 1.25rem; margin-bottom: 1rem; 
                            background-color: #f8f9fa;'>
                    <h4 style='margin: 0 0 0.5rem 0; color: #6c757d; font-size: 1.1rem;'>Data Processor Agreement Checklist</h4>
                    <p style='margin: 0; font-size: 0.85rem; color: #868e96;'>
                        Not applicable - Your business does not use data processors.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Bulk Generation
        st.markdown("### Bulk Document Generation")
        st.caption("Generate all required documents in a single ZIP file")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("Generate All Required Documents (ZIP)", use_container_width=True, type="primary"):
                try:
                    with st.spinner("Generating all required documents..."):
                        documents = generator.generate_all_required_documents()
                        
                        zip_path = generator.export_all_to_zip(
                            documents, 
                            f"DPDP_Documents_{business_id}.zip"
                        )
                        
                        with open(zip_path, 'rb') as f:
                            st.download_button(
                                "Download Complete Document Package (ZIP)",
                                data=f,
                                file_name=f"DPDP_Documents_{answers['business_name']}.zip",
                                mime="application/zip",
                                key="dl_bulk",
                                use_container_width=True
                            )
                        
                        st.success(f"Successfully generated {len(documents)} documents.")
                        
                        st.info("""
                        **Next Steps:**
                        1. Review all yellow-highlighted sections in each document
                        2. Complete manual fields marked with [INSERT]
                        3. Have documents reviewed by qualified legal counsel
                        4. Deploy on website/application after legal approval
                        5. Update documents annually or when business operations change
                        """)
                
                except Exception as e:
                    st.error(f"Bulk generation failed: {e}")
                    st.exception(e)
    
    except ImportError:
        st.error("Document generator module not found. Ensure python-docx is installed.")
        st.code("pip install python-docx", language="bash")
    
    st.markdown("---")
    
    # Navigation footer
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Back to Results", use_container_width=True):
            st.query_params["page"] = "results"
            st.rerun()
    
    with col2:
        if st.button("Return to Home", use_container_width=True):
            if 'selected_business_id' in st.session_state:
                del st.session_state['selected_business_id']
            st.query_params["page"] = "home"
            st.rerun()
    
    with col3:
        if st.button("New Assessment", use_container_width=True):
            if 'current_assessment' in st.session_state:
                del st.session_state['current_assessment']
            if 'selected_business_id' in st.session_state:
                del st.session_state['selected_business_id']
            st.query_params["page"] = "assessment"
            st.rerun()

if __name__ == "__main__":
    show()
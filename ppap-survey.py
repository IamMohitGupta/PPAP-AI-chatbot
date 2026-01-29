"""
Medtronic PPAP Document Review - Eligibility Survey
UI Prototype for Capstone Project

Survey page to determine if PPAP case is suitable for the AI review system
Scope: FAIR, OQ, PQ workflows for new injection-molded plastic parts only
Internal use only - Runs on Medtronic secure network with internal LLM
"""

import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="PPAP Eligibility Survey - Medtronic",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
def init_survey_state():
    """Initialize survey-related session state variables"""

    if 'survey_page' not in st.session_state:
        st.session_state.survey_page = "WELCOME"  # WELCOME, Q1, Q2, Q3, Q4, RESULT

    if 'survey_responses' not in st.session_state:
        st.session_state.survey_responses = {
            'q1_molding_surgical': None,
            'q2_new_product': None,
            'q3_process_verified': None,
            'q4_fixed_setpoints': None
        }

    if 'survey_eligible' not in st.session_state:
        st.session_state.survey_eligible = None

    if 'survey_completion_date' not in st.session_state:
        st.session_state.survey_completion_date = None

def reset_survey():
    """Reset survey to start over"""
    st.session_state.survey_page = "WELCOME"
    st.session_state.survey_responses = {
        'q1_molding_surgical': None,
        'q2_new_product': None,
        'q3_process_verified': None,
        'q4_fixed_setpoints': None
    }
    st.session_state.survey_eligible = None
    st.session_state.survey_completion_date = None

def check_eligibility():
    """Check if user is eligible based on survey responses"""
    responses = st.session_state.survey_responses

    # If Q1 or Q2 is No -> Not eligible
    if responses['q1_molding_surgical'] == 'No' or responses['q2_new_product'] == 'No':
        return False

    # If Q4 is Yes -> Not eligible
    if responses['q4_fixed_setpoints'] == 'Yes':
        return False

    # Otherwise eligible
    return True

def get_ineligibility_reason():
    """Get reason for ineligibility with explanation"""
    responses = st.session_state.survey_responses

    reasons = []

    if responses['q1_molding_surgical'] == 'No':
        reasons.append({
            'question': 'PPAP Process Type',
            'response': 'Not molding plastic processes under Surgical Operation Unit',
            'explanation': 'This system is specifically designed for PPAPs associated with **injection-molded plastic parts** within the **Surgical Operation Unit**. Other processes or business units are not currently supported by this tool.'
        })

    if responses['q2_new_product'] == 'No':
        reasons.append({
            'question': 'Product Type',
            'response': 'Not a new product part',
            'explanation': 'This system currently focuses on **new product parts only**. Legacy products may have different PPAP requirements and workflows. For legacy products, we would need to check for previously approved PPAP tickets and potentially combine documentation, which requires a different review process.'
        })

    if responses['q4_fixed_setpoints'] == 'Yes':
        reasons.append({
            'question': 'Process Parameters',
            'response': 'Process will be run at fixed set points without parameter ranges',
            'explanation': 'Manufacturing processes should have defined **parameter ranges** rather than single fixed setpoints. Parameter ranges allow for normal process variation while maintaining quality. Fixed setpoints without ranges indicate insufficient process understanding or validation, which does not meet PPAP requirements for robust manufacturing processes.'
        })

    return reasons

# Initialize state
init_survey_state()

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Center the content
left_space, center_col, right_space = st.columns([1, 3, 1])

with center_col:
    # Header section
    st.title("PPAP Eligibility Survey")
    st.markdown("### Medtronic PPAP Document Review System")

    with st.container(border=True):
        st.image("images.png", width=120)
        st.markdown("### 🔒 Internal Use Only")
        st.caption("Medtronic • Secure Network • Internal LLM")

    st.markdown("---")

    # ========================================================================
    # WELCOME PAGE
    # ========================================================================
    if st.session_state.survey_page == "WELCOME":
        st.markdown("""
        ## Welcome to the PPAP Review System

        This tool automates the review of PPAP (Production Part Approval Process) documentation
        for **injection-molded plastic parts** within the **Surgical Operation Unit**.

        Before creating a PPAP case, please complete a brief eligibility survey to ensure
        this system is appropriate for your specific PPAP requirements.

        ### What You'll Need to Know:
        - Process type and business unit
        - Product classification (new vs. legacy)
        - Process verification status
        - Process parameter specifications

        The survey takes approximately **1-2 minutes** to complete.
        """)

        st.markdown("---")

        if st.button("Begin Eligibility Survey", type="primary", use_container_width=True):
            st.session_state.survey_page = "Q1"
            st.rerun()

    # ========================================================================
    # QUESTION 1: Molding Plastic Process - Surgical Operation Unit
    # ========================================================================
    elif st.session_state.survey_page == "Q1":
        # Progress indicator
        st.progress(0.25)
        st.caption("Question 1 of 4")
        st.markdown("---")

        st.markdown("""
        ## Question 1: Process Type and Business Unit

        Is this PPAP associated with **molding plastic processes** under the **Surgical Operation Unit**?
        """)

        with st.container(border=True):
            st.info("""
            **What this means:**
            - **Molding plastic processes:** Injection molding or similar plastic manufacturing processes
            - **Surgical Operation Unit:** Business unit responsible for surgical devices and components

            This system is specifically designed for plastic molding processes within the Surgical Operation Unit.
            """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Yes", use_container_width=True, type="primary"):
                st.session_state.survey_responses['q1_molding_surgical'] = 'Yes'
                st.session_state.survey_page = "Q2"
                st.rerun()

        with col2:
            if st.button("❌ No", use_container_width=True):
                st.session_state.survey_responses['q1_molding_surgical'] = 'No'
                st.session_state.survey_page = "RESULT"
                st.rerun()

        st.markdown("---")

        if st.button("⬅ Back to Welcome"):
            st.session_state.survey_page = "WELCOME"
            st.rerun()

    # ========================================================================
    # QUESTION 2: New Product Part
    # ========================================================================
    elif st.session_state.survey_page == "Q2":
        # Progress indicator
        st.progress(0.50)
        st.caption("Question 2 of 4")
        st.markdown("---")

        st.markdown("""
        ## Question 2: Product Classification

        Is this PPAP associated with a **new product part**?
        """)

        with st.container(border=True):
            st.info("""
            **What this means:**
            - **New product part:** A part that has not been previously manufactured or approved
            - **Not a new product part:** Legacy products, existing parts with revisions, or previously approved parts

            This system currently supports new product parts only. Legacy products require different workflows
            (such as checking for previously approved PPAP tickets and combining documentation).
            """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Yes", use_container_width=True, type="primary"):
                st.session_state.survey_responses['q2_new_product'] = 'Yes'
                st.session_state.survey_page = "Q3"
                st.rerun()

        with col2:
            if st.button("❌ No", use_container_width=True):
                st.session_state.survey_responses['q2_new_product'] = 'No'
                st.session_state.survey_page = "RESULT"
                st.rerun()

        st.markdown("---")

        if st.button("⬅ Back to Question 1"):
            st.session_state.survey_page = "Q1"
            st.rerun()

    # ========================================================================
    # QUESTION 3: Process Output Verification
    # ========================================================================
    elif st.session_state.survey_page == "Q3":
        # Progress indicator
        st.progress(0.75)
        st.caption("Question 3 of 4")
        st.markdown("---")

        st.markdown("""
        ## Question 3: Process Verification Status

        Is the **process output fully verified**?
        """)

        with st.container(border=True):
            st.info("""
            **What this means:**
            - **Fully verified:** The manufacturing process has been validated and produces consistent,
              specification-compliant parts
            - Process capability studies (Cpk) have been completed
            - First article inspection has been performed
            - Production runs demonstrate consistent output

            Full process verification is essential for PPAP approval and ensures manufacturing readiness.
            """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Yes", use_container_width=True, type="primary"):
                st.session_state.survey_responses['q3_process_verified'] = 'Yes'
                st.session_state.survey_page = "Q4"
                st.rerun()

        with col2:
            if st.button("❌ No", use_container_width=True):
                st.session_state.survey_responses['q3_process_verified'] = 'No'
                st.session_state.survey_page = "Q4"
                st.rerun()

        st.markdown("---")

        if st.button("⬅ Back to Question 2"):
            st.session_state.survey_page = "Q2"
            st.rerun()

    # ========================================================================
    # QUESTION 4: Process Parameters - Fixed Setpoints vs Ranges
    # ========================================================================
    elif st.session_state.survey_page == "Q4":
        # Progress indicator
        st.progress(1.0)
        st.caption("Question 4 of 4")
        st.markdown("---")

        st.markdown("""
        ## Question 4: Process Parameter Specification

        Will the process be run at **fixed set points** without a range of process limits or parameters?
        """)

        with st.container(border=True):
            st.info("""
            **What this means:**
            - **Fixed setpoints (NOT recommended):** Process parameters are specified as exact single values
              (e.g., Temperature = 280°C, Pressure = 1200 bar)
            - **Parameter ranges (RECOMMENDED):** Process parameters are specified with acceptable ranges
              (e.g., Temperature = 280°C ± 5°C, Pressure = 1200 bar ± 50 bar)

            **Why ranges are required:**
            - Manufacturing processes naturally have variation
            - Parameter ranges demonstrate process understanding and robustness
            - Fixed setpoints without ranges do not meet PPAP requirements for production readiness
            """)

        st.warning("""
        **Note:** If your process uses fixed setpoints without ranges, it may not be ready for PPAP approval.
        Robust manufacturing processes should define acceptable parameter ranges.
        """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes - Fixed setpoints only", use_container_width=True):
                st.session_state.survey_responses['q4_fixed_setpoints'] = 'Yes'
                st.session_state.survey_page = "RESULT"
                st.rerun()

        with col2:
            if st.button("✅ No - Has parameter ranges", use_container_width=True, type="primary"):
                st.session_state.survey_responses['q4_fixed_setpoints'] = 'No'
                st.session_state.survey_page = "RESULT"
                st.rerun()

        st.markdown("---")

        if st.button("⬅ Back to Question 3"):
            st.session_state.survey_page = "Q3"
            st.rerun()

    # ========================================================================
    # RESULT PAGE
    # ========================================================================
    elif st.session_state.survey_page == "RESULT":
        st.markdown("---")

        # Determine eligibility
        is_eligible = check_eligibility()
        st.session_state.survey_eligible = is_eligible
        st.session_state.survey_completion_date = datetime.now()

        # Display survey summary
        st.markdown("## Survey Summary")

        with st.container(border=True):
            st.markdown("### Your Responses:")
            st.markdown(f"""
            1. **Molding plastic processes under Surgical Operation Unit?** {st.session_state.survey_responses['q1_molding_surgical']}
            2. **New product part?** {st.session_state.survey_responses['q2_new_product']}
            3. **Process output fully verified?** {st.session_state.survey_responses['q3_process_verified']}
            4. **Fixed setpoints without parameter ranges?** {st.session_state.survey_responses['q4_fixed_setpoints']}
            """)

        st.markdown("---")

        # ========================================================================
        # ELIGIBLE RESULT
        # ========================================================================
        if is_eligible:
            st.success("""
            ## ✅ System Suitable for Your PPAP

            Based on your responses, this PPAP AI Review System is appropriate for your use case.
            """)

            st.markdown("""
            ### Next Steps:
            1. Click "Proceed to PPAP Case Setup" below
            2. Create a new PPAP case with part details
            3. Upload required documents (FAIR, OQ, PQ)
            4. Use AI-powered analysis for document review

            ### System Capabilities:
            - Automated PPAP checklist generation
            - Dimensional analysis from FAIR documents
            - Equipment qualification validation (OQ)
            - Statistical process control analysis (PQ)
            - Gap detection and recommendations
            - Comprehensive report generation
            """)

            # Additional notes based on Q3
            if st.session_state.survey_responses['q3_process_verified'] == 'No':
                st.warning("""
                **Note:** You indicated the process output is not fully verified. While you can proceed with
                the PPAP documentation review, please ensure process verification is completed before final
                PPAP approval. The system will flag any missing verification documentation.
                """)

            st.markdown("---")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Proceed to PPAP Case Setup", type="primary", use_container_width=True):
                    # In integrated version, this would navigate to CASE_SETUP page
                    st.success("✅ Survey completed! Ready to create PPAP case.")
                    st.info("**Integration Note:** This would navigate to the PPAP Case Setup page in the integrated application.")

                st.markdown("---")

                if st.button("🔄 Restart Survey", use_container_width=True):
                    reset_survey()
                    st.rerun()

        # ========================================================================
        # INELIGIBLE RESULT
        # ========================================================================
        else:
            st.error("""
            ## ⚠️ System Not Suitable for This PPAP

            Based on your responses, this PPAP AI Review System may not be appropriate for your use case.
            """)

            st.markdown("### Reasons for Incompatibility:")

            reasons = get_ineligibility_reason()

            for i, reason in enumerate(reasons, 1):
                with st.container(border=True):
                    st.markdown(f"#### {i}. {reason['question']}")
                    st.markdown(f"**Your Response:** {reason['response']}")
                    st.markdown(f"**Explanation:** {reason['explanation']}")

            st.markdown("---")

            st.markdown("""
            ### Recommended Actions:

            **For Non-Molding or Non-Surgical Unit PPAPs:**
            - Contact your business unit's PPAP coordinator for appropriate review processes
            - Different processes may have specialized requirements not covered by this system

            **For Legacy Product Parts:**
            - Check for existing PPAP tickets for the product
            - Coordinate with Quality Engineering to determine if documentation should be combined with previous approvals
            - Legacy product PPAPs may require a different workflow (to be added in future system updates)

            **For Fixed Setpoint Processes:**
            - Work with Process Engineering to establish acceptable parameter ranges
            - Complete process capability studies to determine appropriate tolerances
            - Ensure process robustness before proceeding with PPAP
            - Parameter ranges are essential for FDA compliance and manufacturing reliability

            ### Need Help?
            If you believe your PPAP should be eligible or have questions about these requirements,
            please contact the PPAP Support Team or your Quality Engineering representative.
            """)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔄 Restart Survey", use_container_width=True, type="primary"):
                    reset_survey()
                    st.rerun()

            with col2:
                if st.button("📧 Contact Support (Demo)", use_container_width=True):
                    st.info("In production, this would open a support ticket or contact form.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption("Medtronic PPAP Document Review System • Capstone Project Prototype • Version 1.0")

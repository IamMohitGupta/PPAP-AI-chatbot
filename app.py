"""
Medtronic PPAP Document Review - Generative AI Tool
UI Prototype for Capstone Project

Scope: FAIR, OQ, PQ workflows for new injection-molded plastic parts only
Internal use only - Runs on Medtronic secure network with internal LLM
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io
import random

# Page configuration
st.set_page_config(
    page_title="Medtronic PPAP Review",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""

    if 'ppap_cases' not in st.session_state:
        st.session_state.ppap_cases = {}

    if 'current_case_id' not in st.session_state:
        st.session_state.current_case_id = None

    if 'activity_log' not in st.session_state:
        st.session_state.activity_log = {}

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = {}
    
    if "active_chat_context" not in st.session_state:
        # (case_id, doc_type, version)
        st.session_state.active_chat_context = None

def add_activity_log(case_id, activity_type, description):
    """Add entry to activity log for a PPAP case"""
    if case_id not in st.session_state.activity_log:
        st.session_state.activity_log[case_id] = []

    st.session_state.activity_log[case_id].append({
        'timestamp': datetime.now(),
        'type': activity_type,
        'description': description
    })

def create_new_case(part_number, revision, supplier, qil, pc, ctf):
    """Create a new PPAP case"""
    case_id = f"{part_number}_{revision}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    st.session_state.ppap_cases[case_id] = {
        'part_number': part_number,
        'revision': revision,
        'supplier': supplier,
        'process': 'Injection Molding - Plastic',
        'qil': qil,
        'pc': pc,
        'ctf': ctf,
        'created_date': datetime.now(),
        'documents': {
            'FAIR': [],
            'OQ': [],
            'PQ': [],
            'Drawing': [],
            'Measurements': []
        },
        'checklist': None,
        'fair_analysis': None,
        'oq_analysis': None,
        'pq_analysis': None
    }

    st.session_state.current_case_id = case_id
    add_activity_log(case_id, 'CASE_CREATED', f'PPAP case created for {part_number} Rev {revision}')

    return case_id

def get_current_case():
    """Get the currently selected PPAP case"""
    if st.session_state.current_case_id:
        return st.session_state.ppap_cases.get(st.session_state.current_case_id)
    return None

def mock_ai_checklist_generation():
    """Mock AI-generated PPAP checklist"""
    return {
        'total_items': 24,
        'satisfied': 18,
        'missing': 6,
        'items': [
            {'category': 'FAIR', 'requirement': 'Part dimensional report with all critical dimensions', 'status': 'Satisfied', 'evidence': 'FAIR_v2.pdf'},
            {'category': 'FAIR', 'requirement': 'Material certification and compliance', 'status': 'Satisfied', 'evidence': 'FAIR_v2.pdf'},
            {'category': 'FAIR', 'requirement': 'Process capability study (Cpk ≥ 1.33)', 'status': 'Missing', 'evidence': None},
            {'category': 'OQ', 'requirement': 'Equipment qualification documentation', 'status': 'Satisfied', 'evidence': 'OQ_v1.pdf'},
            {'category': 'OQ', 'requirement': 'Process parameter validation', 'status': 'Satisfied', 'evidence': 'OQ_v1.pdf'},
            {'category': 'OQ', 'requirement': 'Maintenance and calibration records', 'status': 'Missing', 'evidence': None},
            {'category': 'PQ', 'requirement': 'Production run data (30+ consecutive units)', 'status': 'Satisfied', 'evidence': 'PQ_v1.pdf'},
            {'category': 'PQ', 'requirement': 'Statistical process control charts', 'status': 'Missing', 'evidence': None},
            {'category': 'Drawing', 'requirement': 'Ballooned engineering drawing with GD&T', 'status': 'Satisfied', 'evidence': 'Drawing_v3.pdf'},
            {'category': 'Measurements', 'requirement': 'Complete measurement data for all dimensions', 'status': 'Satisfied', 'evidence': 'Measurements_v2.xlsx'}
        ]
    }

def mock_fair_analysis():
    """Mock FAIR document analysis results"""
    return {
        'dimensions_extracted': 47,
        'critical_dimensions': 12,
        'dimensions': pd.DataFrame({
            'Balloon_ID': ['1', '2', '3', '4', '5', '6', '7', '8'],
            'Dimension': ['Overall Length', 'Inner Diameter', 'Wall Thickness', 'Boss Height', 'Hole Diameter', 'Surface Finish', 'Thread Depth', 'Concentricity'],
            'Nominal': [125.0, 25.4, 2.5, 8.0, 6.35, 0.8, 5.0, 0.05],
            'USL': [125.5, 25.6, 2.6, 8.2, 6.40, 1.2, 5.2, 0.10],
            'LSL': [124.5, 25.2, 2.4, 7.8, 6.30, 0.4, 4.8, 0.00],
            'Measured': [125.1, 25.42, 2.51, 8.05, 6.36, 0.75, 5.03, 0.03],
            'Tolerance_Used_%': [20, 40, 20, 25, 20, 37.5, 15, 30],
            'Status': ['Pass', 'Pass', 'Pass', 'Pass', 'Pass', 'Pass', 'Pass', 'Pass']
        }),
        'material': 'Polycarbonate (PC) - Medical Grade',
        'supplier_cert': 'ISO 13485 Certified',
        'traceability': 'Lot# PCM-2024-8891'
    }

def mock_oq_analysis():
    """Mock OQ document analysis results"""
    return {
        'sections_found': ['Equipment List', 'Process Parameters', 'Qualification Protocol', 'Test Results'],
        'sections_missing': ['Maintenance Schedule', 'Calibration Certificates'],
        'equipment': pd.DataFrame({
            'Equipment': ['Injection Molding Machine', 'Temperature Controller', 'Mold Assembly', 'Material Dryer'],
            'Model': ['Engel Victory 200', 'Mold-Masters Summit', 'Custom Mold #8891', 'Motan Luxor'],
            'Serial_Number': ['ENG-200-4478', 'MM-SUM-9921', 'MM-8891', 'MLX-3344'],
            'Calibration_Status': ['Valid until 06/2026', 'Valid until 08/2026', 'N/A', 'Valid until 12/2025'],
            'Status': ['Qualified', 'Qualified', 'Qualified', 'Qualified']
        }),
        'process_params': {
            'Injection Pressure': '1200 bar ± 50',
            'Melt Temperature': '280°C ± 5°C',
            'Mold Temperature': '80°C ± 3°C',
            'Cooling Time': '25s ± 2s',
            'Cycle Time': '45s ± 3s'
        },
        'validation_status': 'Partially Complete'
    }

def mock_pq_analysis():
    """Mock PQ document analysis results"""
    return {
        'production_run_size': 50,
        'required_run_size': 30,
        'run_status': 'Sufficient',
        'spc_data': pd.DataFrame({
            'Parameter': ['Overall Length', 'Inner Diameter', 'Wall Thickness', 'Boss Height'],
            'Mean': [125.08, 25.41, 2.502, 8.03],
            'StdDev': [0.08, 0.06, 0.015, 0.04],
            'Cp': [2.08, 1.67, 2.22, 2.50],
            'Cpk': [1.87, 1.50, 1.93, 2.25],
            'Status': ['Pass (Cpk>1.33)', 'Pass (Cpk>1.33)', 'Pass (Cpk>1.33)', 'Pass (Cpk>1.33)']
        }),
        'defect_rate': '0.02% (1 reject in 50 parts)',
        'first_pass_yield': '98%',
        'validation_notes': 'Production process demonstrated adequate capability for all critical dimensions.'
    }

def render_dimension_grid(prefix, count, step=0.01):
    """
    Renders numeric inputs in a 3-column grid.
    Returns a list of entered values.
    """
    values = []

    for i in range(0, count, 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < count:
                with cols[j]:
                    val = st.number_input(
                        f"{prefix} Dimension {idx + 1}",
                        key=f"{prefix.lower()}_dim_{idx}",
                        step=step
                    )
                    values.append(val)

    return values


# Initialize session state
init_session_state()

# ============================================================================
# SIDEBAR - PPAP Case Workspace
# ============================================================================

with st.sidebar:
    st.image("assets/images.png", width=150)
    st.markdown("### 🔒 Internal Use Only")
    st.caption("Medtronic • Secure Network • Internal LLM")
    st.divider()

    st.header("PPAP Case Workspace")

    # Case selection or creation
    if len(st.session_state.ppap_cases) > 0:
        case_options = {
            case_id: f"{case['part_number']} Rev {case['revision']}"
            for case_id, case in st.session_state.ppap_cases.items()
        }

        selected_case = st.selectbox(
            "Select PPAP Case",
            options=['Create New Case'] + list(case_options.keys()),
            format_func=lambda x: x if x == 'Create New Case' else case_options[x]
        )

        if selected_case != 'Create New Case':
            st.session_state.current_case_id = selected_case
    else:
        selected_case = 'Create New Case'

    # Create new case form
    if selected_case == 'Create New Case':
        st.subheader("Create New PPAP Case")
        with st.form("new_case_form"):
            part_number = st.text_input("Part Number", placeholder="e.g., MED-12345")
            revision = st.text_input("Revision", placeholder="e.g., A, B, C")
            supplier = st.text_input("Supplier", placeholder="e.g., Supplier XYZ")

            # col1, col2 = st.columns(2)
            # with col1:
                # Display labels (bold 3 & 4), but map to numeric values
            qil_options = {
                "1": 1,
                "2": 2,
                "**3 (In Scope)**": 3,
                "**4 (In Scope)**": 4,
                "5": 5,
                "6": 6,
                "7": 7,
            }

            qil_label = st.selectbox(
                "QIL (Quality Impact Level)",
                options=list(qil_options.keys()),
                help="QIL 3 & 4 are within project scope"
            )
            qil = qil_options[qil_label]

            pc_count = st.number_input(
            "PC (Number of Dimensions)",
            min_value=0,
            step=1
            )

            ctf_count = st.number_input(
                "CTF (Number of Dimensions)",
                min_value=0,
                step=1
            )
            
            
            pc_dimensions = []
            if pc_count > 0:
                st.markdown("**PC Dimensions**")
                pc_dimensions = render_dimension_grid("PC", pc_count)


            ctf_dimensions = []
            if ctf_count > 0:
                st.markdown("**CTF Dimensions**")
                ctf_dimensions = render_dimension_grid("CTF", ctf_count)

            submitted = st.form_submit_button("Create Case")

            if submitted:
                if part_number and revision and supplier:
                    case_id = create_new_case(part_number, revision, supplier, qil, pc, ctf)
                    st.success(f"Created case: {case_id}")
                    st.rerun()
                else:
                    st.error("Please fill all required fields")

    # Display current case metadata
    current_case = get_current_case()
    if current_case:
        st.divider()
        st.subheader("Current Case")
        st.markdown(f"**Part Number:** {current_case['part_number']}")
        st.markdown(f"**Revision:** {current_case['revision']}")
        st.markdown(f"**Supplier:** {current_case['supplier']}")
        st.markdown(f"**Process:** {current_case['process']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("QIL", current_case['qil'])
        with col2:
            st.metric("PC", current_case['pc'])
        with col3:
            st.metric("CTF", current_case['ctf'])

        st.caption(f"Created: {current_case['created_date'].strftime('%Y-%m-%d %H:%M')}")

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

if not current_case:
    st.title("Generative AI Tool for PPAP Document Review")
    st.markdown("### Medtronic Capstone Project")
    st.info("👈 Please create or select a PPAP case from the sidebar to begin.")

    st.markdown("---")
    st.markdown("### System Overview")
    st.markdown("""
    This tool automates the review of PPAP (Production Part Approval Process) documentation
    for **new injection-molded plastic parts only**.

    **Scope:**
    - ✅ FAIR (First Article Inspection Report)
    - ✅ OQ (Operational Qualification)
    - ✅ PQ (Performance Qualification)
    - ✅ Ballooned Engineering Drawings
    - ✅ Measurement Data (Excel/Minitab)

    **Security:**
    - 🔒 Runs exclusively on Medtronic secure internal network
    - 🔒 Uses internal Medtronic GPT (no external APIs)
    - 🔒 No cloud storage - all data remains on-premises
    """)
else:

    st.title(f"PPAP Review: {current_case['part_number']} Rev {current_case['revision']}")

    st.divider()


    # Tab navigation
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📁 Ingestion & Revision",
        "✅ Checklist & Gaps",
        "📏 FAIR Review",
        "⚙️ OQ Review",
        "📊 PQ Review",
        "📄 Reports",
        "💬 PPAP Coaching Chat"
    ])

    # ========================================================================
    # TAB 1: Ingestion & Revision Management
    # ========================================================================
    with tab1:
        st.header("Document Ingestion & Revision Management")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Upload Documents")

            doc_type = st.selectbox(
                "Document Type",
                ["FAIR", "OQ", "PQ", "Drawing (Ballooned)", "Measurements (Excel/Minitab)"]
            )

            uploaded_file = st.file_uploader(
                "Choose file(s)",
                type=['pdf', 'xlsx', 'xls', 'csv'],
                help="Upload PPAP documentation. System will detect if document already exists and create new version."
            )

            if uploaded_file:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    version_notes = st.text_input("Version Notes (optional)", placeholder="e.g., Updated per engineering change notice ECN-1234")
                with col_b:
                    if st.button("Upload & Process", type="primary"):
                        # Mock document processing
                        doc_type_key = doc_type.split()[0]  # Extract key part

                        version_id = f"v{len(current_case['documents'][doc_type_key]) + 1}"

                        current_case['documents'][doc_type_key].append({
                            'filename': uploaded_file.name,
                            'version': version_id,
                            'upload_date': datetime.now(),
                            'size_kb': uploaded_file.size / 1024,
                            'notes': version_notes,
                            'status': 'Processing...'
                        })

                        add_activity_log(
                            st.session_state.current_case_id,
                            'DOCUMENT_UPLOAD',
                            f"Uploaded {doc_type} - {uploaded_file.name} ({version_id})"
                        )

                        st.success(f"✅ Uploaded {uploaded_file.name} as {version_id}")
                        st.info("🤖 AI processing started... (mocked)")

                        # Mock AI processing complete
                        current_case['documents'][doc_type_key][-1]['status'] = 'Processed'
                        add_activity_log(
                            st.session_state.current_case_id,
                            'AI_PROCESSING',
                            f"AI completed analysis of {doc_type} {version_id}"
                        )

                        st.rerun()

        with col2:
            st.subheader("Quick Stats")
            total_docs = sum(len(docs) for docs in current_case['documents'].values())
            st.metric("Total Documents", total_docs)
            st.metric("Latest Version", f"v{max([len(docs) for docs in current_case['documents'].values()], default=0)}")

        st.divider()

        # Document version history
        st.subheader("Document Version History")

        for doc_type_key, documents in current_case['documents'].items():
            if documents:
                with st.expander(f"📁 {doc_type_key} ({len(documents)} versions)", expanded=True):
                    # Display each version as a clean card instead of dataframe
                    for doc in reversed(documents):  # Show newest first
                        with st.container(border=True):
                            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
                            with col1:
                                st.markdown(f"**{doc['version']}**")
                            with col2:
                                st.markdown(f"📄 {doc['filename']}")
                            with col3:
                                st.markdown(f"🕒 {doc['upload_date'].strftime('%Y-%m-%d %H:%M:%S')}")
                            with col4:
                                status_emoji = "✅" if doc['status'] == 'Processed' else "⏳"
                                st.markdown(f"{status_emoji} {doc['status']}")
                            with col5:
                                if st.button(
                                    "💬 Chat",
                                    key=f"chat_{doc_type_key}_{doc['version']}"
                                ):
                                    st.session_state.active_chat_context = (
                                        st.session_state.current_case_id,
                                        doc_type_key,
                                        doc['version']
                                    )
                                    st.rerun()
                            if doc['notes']:
                                st.caption(f"📝 {doc['notes']}")
                            st.caption(f"Size: {doc['size_kb']:.2f} KB")

                    if len(documents) > 1:
                        st.info(f"ℹ️ Version change detection: {documents[-1]['version']} vs {documents[-2]['version']} - [Click to view diff] (mocked)")

    # ========================================================================
    # TAB 2: PPAP Checklist & Gap Analysis
    # ========================================================================
    with tab2:
        st.header("PPAP Checklist & Gap Analysis")

        if st.button("🤖 Generate Checklist with AI", type="primary"):
            current_case['checklist'] = mock_ai_checklist_generation()
            add_activity_log(
                st.session_state.current_case_id,
                'AI_ANALYSIS',
                'Generated PPAP checklist and gap analysis'
            )
            st.rerun()

        if current_case['checklist']:
            checklist = current_case['checklist']

            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Requirements", checklist['total_items'])
            with col2:
                st.metric("Satisfied", checklist['satisfied'], delta=f"{(checklist['satisfied']/checklist['total_items']*100):.0f}%")
            with col3:
                st.metric("Missing", checklist['missing'], delta=f"-{(checklist['missing']/checklist['total_items']*100):.0f}%", delta_color="inverse")
            with col4:
                completion = (checklist['satisfied'] / checklist['total_items']) * 100
                st.metric("Completion", f"{completion:.0f}%")

            st.divider()

            # Detailed checklist
            st.subheader("Detailed Requirements")

            df_checklist = pd.DataFrame(checklist['items'])

            # Filter options
            col1, col2 = st.columns([1, 1])
            with col1:
                filter_category = st.multiselect("Filter by Category", options=df_checklist['category'].unique(), default=df_checklist['category'].unique())
            with col2:
                filter_status = st.multiselect("Filter by Status", options=['Satisfied', 'Missing'], default=['Satisfied', 'Missing'])

            filtered_df = df_checklist[
                (df_checklist['category'].isin(filter_category)) &
                (df_checklist['status'].isin(filter_status))
            ]

            # Style the dataframe
            def highlight_status(row):
                if row['status'] == 'Missing':
                    return ['background-color: #ffebee'] * len(row)
                else:
                    return ['background-color: #e8f5e9'] * len(row)

            styled_df = filtered_df.style.apply(highlight_status, axis=1)

            st.dataframe(styled_df, use_container_width=True, hide_index=True)

            # Gap summary
            st.divider()
            st.subheader("⚠️ Gaps Requiring Attention")

            missing_items = df_checklist[df_checklist['status'] == 'Missing']
            for idx, item in missing_items.iterrows():
                st.warning(f"**{item['category']}:** {item['requirement']}")
        else:
            st.info("Click 'Generate Checklist with AI' to analyze uploaded documents and create PPAP checklist.")

    # ========================================================================
    # TAB 3: FAIR Review
    # ========================================================================
    with tab3:
        st.header("FAIR (First Article Inspection Report) Review")

        if not current_case['documents']['FAIR']:
            st.warning("⚠️ No FAIR documents uploaded yet. Please upload a FAIR document in the Ingestion tab.")
        else:
            if st.button("🤖 Analyze FAIR Document", type="primary"):
                current_case['fair_analysis'] = mock_fair_analysis()
                add_activity_log(
                    st.session_state.current_case_id,
                    'AI_ANALYSIS',
                    'Completed FAIR document analysis'
                )
                st.rerun()

            if current_case['fair_analysis']:
                fair = current_case['fair_analysis']

                # Summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Dimensions Extracted", fair['dimensions_extracted'])
                with col2:
                    st.metric("Critical Dimensions", fair['critical_dimensions'])
                with col3:
                    passing = (fair['dimensions']['Status'] == 'Pass').sum()
                    st.metric("Passing", f"{passing}/{len(fair['dimensions'])}")

                st.divider()

                # Material info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Material:** {fair['material']}")
                with col2:
                    st.markdown(f"**Supplier Cert:** {fair['supplier_cert']}")
                with col3:
                    st.markdown(f"**Traceability:** {fair['traceability']}")

                st.divider()

                # Dimensional analysis table
                st.subheader("Dimensional Analysis")

                def highlight_tolerance(row):
                    colors = []
                    for col in row.index:
                        if col == 'Tolerance_Used_%':
                            val = row[col]
                            if val > 80:
                                colors.append('background-color: #ffebee')
                            elif val > 60:
                                colors.append('background-color: #fff3e0')
                            else:
                                colors.append('background-color: #e8f5e9')
                        else:
                            colors.append('')
                    return colors

                styled_dims = fair['dimensions'].style.apply(highlight_tolerance, axis=1)
                st.dataframe(styled_dims, use_container_width=True, hide_index=True)

                st.caption("🟢 Green: <60% tolerance used | 🟡 Orange: 60-80% | 🔴 Red: >80%")

                # AI insights
                st.divider()
                st.subheader("🤖 AI Insights")
                st.info("""
                **Key Findings:**
                - ✅ All measured dimensions are within specification limits
                - ✅ Material certification is valid and compliant with medical grade requirements
                - ⚠️ Balloon ID #2 (Inner Diameter) is using 40% of tolerance - monitor in production
                - ✅ Traceability documentation is complete
                - ℹ️ Recommend additional sampling for Inner Diameter to verify process stability
                """)
            else:
                st.info("Latest FAIR document uploaded. Click 'Analyze FAIR Document' to extract dimensions and validate measurements.")

    # ========================================================================
    # TAB 4: OQ Review
    # ========================================================================
    with tab4:
        st.header("OQ (Operational Qualification) Review")

        if not current_case['documents']['OQ']:
            st.warning("⚠️ No OQ documents uploaded yet. Please upload an OQ document in the Ingestion tab.")
        else:
            if st.button("🤖 Analyze OQ Document", type="primary"):
                current_case['oq_analysis'] = mock_oq_analysis()
                add_activity_log(
                    st.session_state.current_case_id,
                    'AI_ANALYSIS',
                    'Completed OQ document analysis'
                )
                st.rerun()

            if current_case['oq_analysis']:
                oq = current_case['oq_analysis']

                # Validation status
                status_color = "🟡" if oq['validation_status'] == 'Partially Complete' else "🟢"
                st.markdown(f"### {status_color} Validation Status: {oq['validation_status']}")

                st.divider()

                # Sections analysis
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("✅ Sections Found")
                    for section in oq['sections_found']:
                        st.success(f"✓ {section}")

                with col2:
                    st.subheader("⚠️ Sections Missing")
                    for section in oq['sections_missing']:
                        st.error(f"✗ {section}")

                st.divider()

                # Equipment qualification
                st.subheader("Equipment Qualification Status")
                st.dataframe(oq['equipment'], use_container_width=True, hide_index=True)

                st.divider()

                # Process parameters
                st.subheader("Validated Process Parameters")

                params_df = pd.DataFrame({
                    'Parameter': list(oq['process_params'].keys()),
                    'Specification': list(oq['process_params'].values())
                })

                st.dataframe(params_df, use_container_width=True, hide_index=True)

                # AI insights
                st.divider()
                st.subheader("🤖 AI Insights")
                st.warning("""
                **Key Findings:**
                - ✅ All critical equipment is qualified and calibrated
                - ✅ Process parameters are well-defined with appropriate tolerances
                - ⚠️ **MISSING:** Maintenance schedule documentation required
                - ⚠️ **MISSING:** Calibration certificates for temperature controller
                - ℹ️ Recommend completing missing sections before final PPAP approval
                """)
            else:
                st.info("Latest OQ document uploaded. Click 'Analyze OQ Document' to validate equipment and process qualification.")

    # ========================================================================
    # TAB 5: PQ Review
    # ========================================================================
    with tab5:
        st.header("PQ (Performance Qualification) Review")

        if not current_case['documents']['PQ']:
            st.warning("⚠️ No PQ documents uploaded yet. Please upload a PQ document in the Ingestion tab.")
        else:
            if st.button("🤖 Analyze PQ Document", type="primary"):
                current_case['pq_analysis'] = mock_pq_analysis()
                add_activity_log(
                    st.session_state.current_case_id,
                    'AI_ANALYSIS',
                    'Completed PQ document analysis'
                )
                st.rerun()

            if current_case['pq_analysis']:
                pq = current_case['pq_analysis']

                # Production run summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Production Run Size", pq['production_run_size'], delta=f"{pq['production_run_size'] - pq['required_run_size']} above minimum")
                with col2:
                    st.metric("Required Minimum", pq['required_run_size'])
                with col3:
                    st.metric("Defect Rate", pq['defect_rate'])
                with col4:
                    st.metric("First Pass Yield", pq['first_pass_yield'])

                run_status = "✅" if pq['run_status'] == 'Sufficient' else "⚠️"
                st.markdown(f"### {run_status} Run Status: {pq['run_status']}")

                st.divider()

                # SPC data
                st.subheader("Statistical Process Control (SPC) Analysis")

                def highlight_cpk(row):
                    colors = []
                    for col in row.index:
                        if col == 'Cpk':
                            val = row[col]
                            if val >= 1.67:
                                colors.append('background-color: #e8f5e9')
                            elif val >= 1.33:
                                colors.append('background-color: #fff3e0')
                            else:
                                colors.append('background-color: #ffebee')
                        else:
                            colors.append('')
                    return colors

                styled_spc = pq['spc_data'].style.apply(highlight_cpk, axis=1)
                st.dataframe(styled_spc, use_container_width=True, hide_index=True)

                st.caption("🟢 Cpk ≥ 1.67: Excellent | 🟡 Cpk ≥ 1.33: Acceptable | 🔴 Cpk < 1.33: Unacceptable")

                # Validation notes
                st.divider()
                st.subheader("📋 Validation Summary")
                st.markdown(f"**Notes:** {pq['validation_notes']}")

                # AI insights
                st.divider()
                st.subheader("🤖 AI Insights")
                st.success("""
                **Key Findings:**
                - ✅ Production run size exceeds minimum requirement (50 vs 30 required)
                - ✅ All critical dimensions demonstrate Cpk > 1.33 (process capability acceptable)
                - ✅ Inner Diameter Cpk = 1.50 (acceptable, but monitor for drift)
                - ✅ First pass yield of 98% exceeds typical medical device requirements
                - ✅ Defect rate of 0.02% is well within acceptable limits
                - ℹ️ Recommend establishing ongoing SPC monitoring for Inner Diameter
                """)
            else:
                st.info("Latest PQ document uploaded. Click 'Analyze PQ Document' to validate production performance.")

    # ========================================================================
    # TAB 6: Reports
    # ========================================================================
    with tab6:
        st.header("PPAP Summary Reports")

        st.markdown("Generate comprehensive PPAP review reports for submission and archival.")

        # Report generation options
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Report Options")

            include_fair = st.checkbox("Include FAIR Analysis", value=True)
            include_oq = st.checkbox("Include OQ Review", value=True)
            include_pq = st.checkbox("Include PQ Review", value=True)
            include_checklist = st.checkbox("Include PPAP Checklist", value=True)
            include_audit = st.checkbox("Include Audit Trail", value=True)

            report_format = st.radio("Report Format", ["PDF", "Word (DOCX)"])

        with col2:
            st.subheader("Report Preview")

            with st.container(border=True):
                st.markdown("#### PPAP Summary Report")
                st.markdown(f"**Part Number:** {current_case['part_number']}")
                st.markdown(f"**Revision:** {current_case['revision']}")
                st.markdown(f"**Supplier:** {current_case['supplier']}")
                st.markdown(f"**Process:** {current_case['process']}")
                st.markdown("---")
                st.markdown("**Document Status:**")
                for doc_type, docs in current_case['documents'].items():
                    if docs:
                        st.markdown(f"- {doc_type}: v{len(docs)} uploaded")
                    else:
                        st.markdown(f"- {doc_type}: Not uploaded")

        st.divider()

        # Generate report button
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if st.button("🤖 Generate Report", type="primary", use_container_width=True):
                with st.spinner("Generating PPAP summary report..."):
                    # Mock report generation
                    add_activity_log(
                        st.session_state.current_case_id,
                        'REPORT_GENERATED',
                        f'Generated PPAP summary report ({report_format})'
                    )
                    st.success("✅ Report generated successfully!")

        with col2:
            # Mock download button
            mock_report_content = f"""
            PPAP Summary Report
            Part Number: {current_case['part_number']}
            Revision: {current_case['revision']}
            Supplier: {current_case['supplier']}

            This is a mock report for demonstration purposes.
            """

            st.download_button(
                label=f"⬇️ Download {report_format}",
                data=mock_report_content,
                file_name=f"PPAP_Report_{current_case['part_number']}_{current_case['revision']}.{'pdf' if report_format == 'PDF' else 'docx'}",
                mime="application/pdf" if report_format == "PDF" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        st.divider()

        # Report history
        st.subheader("Report Generation History")

        # Mock report history
        report_history = pd.DataFrame({
            'Generated Date': ['2026-01-17 10:30:00', '2026-01-15 14:22:00'],
            'Format': ['PDF', 'Word'],
            'Sections': ['All', 'FAIR, OQ, PQ'],
            'Generated By': ['AI System', 'AI System'],
            'Status': ['Available', 'Available']
        })

        st.dataframe(report_history, use_container_width=True, hide_index=True)

    # ========================================================================
    # TAB 7: PPAP Coaching Chat
    # ========================================================================
    with tab7:
        st.header("💬 PPAP Coaching Chat")

        # Split layout: left = documents, right = chat
        left_col, right_col = st.columns([1, 2])

        # --------------------------------------------------
        # LEFT: Document Version Selector
        # --------------------------------------------------
        with left_col:
            st.subheader("📁 Documents")

            for doc_type_key, documents in current_case['documents'].items():
                if not documents:
                    continue

                with st.expander(f"{doc_type_key}", expanded=True):
                    for doc in reversed(documents):
                        is_active = (
                            st.session_state.active_chat_context ==
                            (st.session_state.current_case_id, doc_type_key, doc['version'])
                        )

                        button_label = "💬 Active" if is_active else "💬 Chat"

                        if st.button(
                            f"{doc['version']} – {doc['filename']}",
                            key=f"chat_select_{doc_type_key}_{doc['version']}",
                            use_container_width=True
                        ):
                            st.session_state.active_chat_context = (
                                st.session_state.current_case_id,
                                doc_type_key,
                                doc['version']
                            )
                            st.rerun()

        # --------------------------------------------------
        # RIGHT: Chat Window
        # --------------------------------------------------
        with right_col:
            if not st.session_state.active_chat_context:
                st.info("👈 Select a document version to start chatting.")
                st.stop()

            case_id, doc_type, version = st.session_state.active_chat_context
            chat_key = f"{case_id}:{doc_type}:{version}"

            st.markdown(f"""
            **Context**
            - Part: `{current_case['part_number']}` Rev `{current_case['revision']}`
            - Document: **{doc_type}**
            - Version: **{version}**
            """)

            if chat_key not in st.session_state.chat_history:
                st.session_state.chat_history[chat_key] = []

            messages = st.session_state.chat_history[chat_key]

            chat_container = st.container(height=420)
            with chat_container:
                for msg in messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            user_input = st.chat_input(f"Ask about {doc_type} {version}...")

            if user_input:
                messages.append({"role": "user", "content": user_input})

                ai_response = (
                    f"This response is scoped to **{doc_type} {version}**.\n\n"
                    "Only this document version is considered. "
                    "Other PPAP documents or versions are excluded."
                )

                messages.append({"role": "assistant", "content": ai_response})

                add_activity_log(
                    case_id,
                    "CHAT_INTERACTION",
                    f"Chat on {doc_type} {version}: {user_input[:60]}"
                )

                st.rerun()


    # ========================================================================
    # AUDIT TRAIL (shown at bottom of all tabs)
    # ========================================================================
    st.divider()

    with st.expander("📋 Audit Trail / Activity Log", expanded=False):
        if case_id in st.session_state.activity_log and st.session_state.activity_log[case_id]:
            # Display audit log entries in reverse chronological order with clean formatting
            audit_entries = reversed(st.session_state.activity_log[case_id])

            for entry in audit_entries:
                # Choose icon based on activity type
                icon_map = {
                    'CASE_CREATED': '📋',
                    'DOCUMENT_UPLOAD': '📤',
                    'AI_PROCESSING': '🤖',
                    'AI_ANALYSIS': '🔍',
                    'REPORT_GENERATED': '📄',
                    'CHAT_INTERACTION': '💬'
                }
                icon = icon_map.get(entry['type'], '📌')

                # Format activity type for display
                activity_display = entry['type'].replace('_', ' ').title()

                with st.container(border=True):
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{entry['timestamp'].strftime('%H:%M:%S')}**")
                        st.caption(entry['timestamp'].strftime('%Y-%m-%d'))
                    with col2:
                        st.markdown(f"{icon} **{activity_display}**")
                        st.markdown(entry['description'])
        else:
            st.info("No activity recorded yet for this PPAP case.")
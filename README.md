# Generative AI Tool for PPAP Document Review

## Medtronic Capstone Project - UI Prototype

### Project Overview

This is a Streamlit-based UI prototype for automating the review of PPAP (Production Part Approval Process) documentation for **new injection-molded plastic parts only**. The system is designed to run on Medtronic's secure internal network using an internal LLM (Medtronic GPT).

**Important Notes:**
- This is a **UI-only prototype** - no backend or database implementation yet
- All logic is mocked using Streamlit session state
- Designed for internal use only - no external APIs or cloud storage
- Scope limited to new parts only (no legacy or changed parts)
- **Eligibility Survey:** Users must complete a survey to verify their PPAP is suitable for the system before accessing case creation

---

## Project Scope

### Covered Workflows
- ✅ **FAIR** (First Article Inspection Report)
- ✅ **OQ** (Operational Qualification)
- ✅ **PQ** (Performance Qualification)
- ✅ Ballooned Engineering Drawings (PDF)
- ✅ Measurement Files (Excel/Minitab)

### Part Requirements
- **Process:** Injection Molding - Plastic Parts Only
- **Type:** New parts only (no legacy or changed parts)
- **Metadata:** QIL, PC, CTF tracking

---

## Application Flow

### 1. Eligibility Survey (ppap-survey.py)

Before accessing the PPAP case creation system, users must complete an eligibility survey to ensure their PPAP is suitable for this automated review system.

#### Survey Questions (Sequential)

**Question 1: Process Type and Business Unit**
- "Is the PPAP associated with molding plastic processes under the Surgical Operation Unit?"
- **If No:** System not suitable → Show explanation and suggest alternative

**Question 2: Product Classification**
- "Is the PPAP associated with a new product part?"
- **If No:** System not suitable → Explain legacy product workflows are different

**Question 3: Process Verification Status**
- "Is the process output fully verified?"
- **If No:** Can proceed with warning → Flag that verification must be completed before final approval

**Question 4: Process Parameters**
- "Will the process be run at fixed set points without a range of process limits or parameters?"
- **If Yes:** System not suitable → Explain that parameter ranges are required for robust manufacturing

#### Eligibility Logic

**User is ELIGIBLE if:**
- Q1 = Yes (Molding plastic + Surgical Operation Unit)
- Q2 = Yes (New product part)
- Q4 = No (Has parameter ranges, not fixed setpoints)

**User is INELIGIBLE if:**
- Q1 = No (Different process or business unit)
- Q2 = No (Legacy product - requires different workflow)
- Q4 = Yes (Fixed setpoints - insufficient process definition)

#### Survey Features

- **Progress indicator:** Shows "Question X of 4" with progress bar
- **Contextual help:** Each question includes explanations of terms and requirements
- **Sequential navigation:** Questions appear one at a time
- **Eligibility determination:** Automatic evaluation based on responses
- **Detailed explanations:** Ineligible users receive specific reasons and recommended actions
- **Survey restart:** Users can restart the survey at any time

#### Ineligibility Explanations

When a user is deemed ineligible, the system provides:
1. **Specific reasons** explaining which responses caused ineligibility
2. **Context** on why those criteria matter for PPAP review
3. **Recommended actions** for next steps (e.g., contact coordinators, establish parameter ranges)
4. **Support options** to get help or clarification

### 2. PPAP Case Setup (app-current.py)

After passing the eligibility survey, users can create PPAP cases and access the full workspace.

---

## Features Implemented

### 1. PPAP Case Workspace (Sidebar)
- Create new PPAP cases with metadata:
  - Part Number
  - Revision
  - Supplier
  - Process Type (fixed: Injection Molding - Plastic)
  - QIL/PC/CTF flags
- Switch between multiple PPAP cases
- Display current case summary and metadata

### 2. Tab-Based Interface

#### 📁 Ingestion & Revision Management
- Upload documents by type (FAIR, OQ, PQ, Drawing, Measurements)
- Version tracking with timestamps and version IDs
- Document history display with clean, readable cards
- File size and status tracking
- Version comparison placeholders ("what changed" detection)
- Upload notes for each version

#### ✅ PPAP Checklist & Gap Analysis
- AI-generated PPAP checklist (mocked)
- Summary metrics: Total items, Satisfied, Missing, Completion %
- Detailed requirements table with filtering by category and status
- Color-coded status indicators (green for satisfied, red for missing)
- Gap summary with actionable items

#### 📏 FAIR Review
- Dimensional analysis with extracted dimensions table
- USL/LSL and % tolerance used display
- Color-coded tolerance usage (green <60%, orange 60-80%, red >80%)
- Material certification and traceability information
- AI insights on dimensional compliance and recommendations

#### ⚙️ OQ Review
- Equipment qualification status table
- Process parameters validation
- Sections found vs missing analysis
- Calibration status tracking
- AI insights on missing documentation

#### 📊 PQ Review
- Production run size validation
- Statistical Process Control (SPC) data
- Cp/Cpk capability metrics with color coding
- Defect rate and first pass yield tracking
- AI insights on process capability

#### 📄 Reports
- Generate comprehensive PPAP summary reports
- Report format options (PDF/Word)
- Configurable sections (FAIR, OQ, PQ, Checklist, Audit Trail)
- Report preview and download (mocked)
- Report generation history

#### 💬 PPAP Coaching Chat
- Interactive chat interface scoped to selected PPAP case
- Context-aware responses based on uploaded documents
- Quick question buttons for common queries
- Chat history per PPAP case
- Mocked AI responses for demonstration

### 3. Audit Trail / Activity Log
- Comprehensive activity tracking per PPAP case
- Clean, readable display with icons and timestamps
- Activity types tracked:
  - Case creation
  - Document uploads
  - AI processing events
  - AI analysis completion
  - Report generation
  - Chat interactions
- Reverse chronological order (newest first)
- Expandable section at bottom of each tab

### 4. Security & Compliance Features
- Clear "Internal Use Only" labeling throughout UI
- Emphasis on secure network and internal LLM usage
- No external API integration
- No cloud storage references
- Medical device compliance considerations

---

## Technical Implementation

### Technology Stack
- **Framework:** Streamlit
- **Language:** Python 3.x
- **Data Management:** Pandas (for mock data display)
- **State Management:** Streamlit session state

### Session State Structure
```python
st.session_state = {
    'ppap_cases': {},           # Dictionary of all PPAP cases
    'current_case_id': None,    # Currently selected case
    'activity_log': {},         # Activity logs per case
    'chat_history': {}          # Chat history per case
}
```

### Mock Data
All AI outputs, parsing, and analysis are currently mocked:
- Checklist generation
- FAIR dimensional analysis
- OQ equipment validation
- PQ statistical analysis
- Version comparison
- AI chat responses

---

## Installation & Setup

### Prerequisites
```bash
pip install streamlit pandas
```

### Running the Applications

**Option 1: Eligibility Survey (Standalone)**
```bash
cd PPAP-AI-chatbot
streamlit run ppap-survey.py
```

**Option 2: Main PPAP Workspace**
```bash
cd PPAP-AI-chatbot
streamlit run app-current.py
```

**Option 3: Original Prototype**
```bash
cd UI
streamlit run ppap_review_app.py
```

The app will open in your default browser at `http://localhost:8501` (or `8502` if port is in use).

**Note:** Currently, the survey and main workspace are separate applications. They will be integrated in a future update to provide a seamless user flow from eligibility survey to PPAP case creation.

---

## Usage Guide

### Step 1: Complete Eligibility Survey (ppap-survey.py)

**Purpose:** Verify that your PPAP is suitable for the automated review system

1. Click "Begin Eligibility Survey" on the welcome page
2. Answer 4 sequential questions:
   - Process type and business unit
   - Product classification (new vs. legacy)
   - Process verification status
   - Process parameter specification
3. Review your eligibility result:
   - **If Eligible:** Proceed to PPAP Case Setup
   - **If Ineligible:** Review explanations and recommended actions

**Eligibility Criteria:**
- Must be molding plastic processes under Surgical Operation Unit
- Must be a new product part (not legacy)
- Must use process parameter ranges (not fixed setpoints)

### Step 2: Creating a PPAP Case (app-current.py)

**Note:** In the integrated version, this will be accessible only after passing the survey

1. On the case setup page, fill out the "Create New PPAP Case" form
2. Enter Part Number, Revision, and Supplier
3. Select QIL level and enter PC/CTF counts
4. Click "Create Case"

### Uploading Documents
1. Navigate to the "Ingestion & Revision" tab
2. Select document type from dropdown
3. Upload file (PDF, Excel, CSV)
4. Add optional version notes
5. Click "Upload & Process"

### Reviewing Documents
1. Navigate to respective tabs (FAIR, OQ, PQ)
2. Click "Analyze [Document Type] Document" button
3. Review generated analysis and metrics
4. Check AI insights for recommendations

### Generating Reports
1. Go to "Reports" tab
2. Select report sections to include
3. Choose format (PDF or Word)
4. Click "Generate Report"
5. Download generated report

### Using PPAP Coaching Chat
1. Navigate to "PPAP Coaching Chat" tab
2. Select a document version from the left panel
3. Type questions in chat input scoped to that specific document version
4. Chat maintains context per document version

---

## Survey Design Details

### Question Flow and Logic

The eligibility survey uses a **sequential question flow** where each question appears one at a time. This design:
- Reduces cognitive load on users
- Provides focused context for each question
- Allows early exit if user is clearly ineligible
- Creates a more guided, conversational experience

### Eligibility Decision Tree

```
Q1: Molding plastic + Surgical Unit?
├─ No → INELIGIBLE (Wrong process/unit)
└─ Yes → Continue to Q2

Q2: New product part?
├─ No → INELIGIBLE (Legacy product - different workflow)
└─ Yes → Continue to Q3

Q3: Process output verified?
├─ No → Continue with WARNING (verification needed before approval)
└─ Yes → Continue to Q4

Q4: Fixed setpoints only (no ranges)?
├─ Yes → INELIGIBLE (Insufficient process definition)
└─ No → ELIGIBLE ✅
```

### Session State Management

The survey uses dedicated session state variables:
```python
survey_page: str              # Current page: WELCOME, Q1, Q2, Q3, Q4, RESULT
survey_responses: dict        # User answers to all 4 questions
survey_eligible: bool         # Final eligibility determination
survey_completion_date: datetime  # When survey was completed
```

### Integration Considerations

When integrating with the main application:
1. Survey should be the first page users see
2. Survey eligibility should gate access to case creation
3. Survey responses should be stored with PPAP case metadata
4. Users should be able to review their survey responses later
5. Admin users might bypass survey (future feature)

---

## Recent Updates

### Latest Improvements (2026-01-28)
- **Added Eligibility Survey Page:** New standalone survey to screen PPAPs before case creation
  - 4 sequential questions to determine system suitability
  - Detailed eligibility logic based on process type, product classification, and process parameters
  - Comprehensive explanations for ineligible users with recommended actions
  - Survey state management and restart capability
- **Updated documentation:** README now includes survey workflow and eligibility criteria

### Previous Updates (2026-01-17)
- **Fixed audit log and version history display:** Replaced monospace/code-styled dataframe with clean, readable card-based layouts
- **Enhanced version history:** Each document version now displays as a bordered card with proper formatting
- **Improved audit trail:** Activity log now uses icons, better spacing, and readable fonts
- **Better visual hierarchy:** Timestamps, activity types, and descriptions are now clearly separated

---

## Future Enhancements (Backend Implementation)

### Immediate Next Steps
- **Integrate survey with main application:** Combine `ppap-survey.py` and `app-current.py` into unified flow
  - Survey page as initial entry point
  - Navigate to case setup only after passing eligibility screening
  - Store survey responses with PPAP case data
- **Expand eligibility rules:** Support for legacy products with ticket lookup functionality
- **Survey response validation:** Add checkboxes or additional context fields for ambiguous cases

### Planned Features
- Real AI integration with Medtronic GPT
- Database implementation for persistent storage
- Actual PDF parsing and dimension extraction
- Real version comparison and diff detection
- Document storage and retrieval system
- User authentication and role management
- Advanced analytics and reporting
- Integration with existing Medtronic systems
- **Legacy product support:** Auto-detection of existing PPAP tickets and documentation merging

### AI Capabilities to Implement
- Natural language processing for document parsing
- Automated dimension extraction from drawings
- Intelligent gap detection
- Contextual chat responses using RAG
- Automated report generation
- Version comparison and change detection

---

## Project Structure

```
Medtronic/
├── PPAP-AI-chatbot/
│   ├── ppap-survey.py         # Eligibility survey page (standalone)
│   ├── app-current.py         # Main PPAP workspace application
│   └── README.md              # This file
└── UI/
    └── ppap_review_app.py     # Original prototype
```

**Note:** The application is being modularized:
- `ppap-survey.py`: Standalone survey page for eligibility screening
- `app-current.py`: Main PPAP case workspace with document review features
- These will be integrated into a single application in future updates

---

## Security Considerations

### Current Implementation
- No external network calls
- No data persistence (session-only)
- No authentication (prototype only)

### Production Requirements
- Deploy on Medtronic secure internal network only
- Use Medtronic GPT (internal LLM) for AI features
- Implement proper authentication and authorization
- Add audit logging to secure database
- Ensure HIPAA/FDA compliance
- Implement data encryption at rest and in transit
- Add role-based access control (RBAC)

---

## Known Limitations

1. **UI Prototype Only:** All AI functionality is mocked
2. **No Persistence:** Data is lost when session ends
3. **No Real PDF Parsing:** Document analysis is simulated
4. **No Backend:** No API layer or database
5. **Limited Error Handling:** Basic validation only
6. **No User Management:** Single-user session-based prototype

---

## Contact & Support

This is a capstone project prototype for Medtronic. For questions or issues:
- Review the code in `UI/ppap_review_app.py`
- Check Streamlit documentation: https://docs.streamlit.io
- Refer to PPAP standards documentation

---

## License

Internal Medtronic project - Proprietary and Confidential

# Generative AI Tool for PPAP Document Review

## Medtronic Capstone Project - UI Prototype

### Project Overview

This is a Streamlit-based UI prototype for automating the review of PPAP (Production Part Approval Process) documentation for **new injection-molded plastic parts only**. The system is designed to run on Medtronic's secure internal network using an internal LLM (Medtronic GPT).

**Important Notes:**
- This is a **UI-only prototype** - no backend or database implementation yet
- All logic is mocked using Streamlit session state
- Designed for internal use only - no external APIs or cloud storage
- Scope limited to new parts only (no legacy or changed parts)

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

### Running the Application
```bash
cd UI
streamlit run ppap_review_app.py
```

The app will open in your default browser at `http://localhost:8501` (or `8502` if port is in use).

---

## Usage Guide

### Creating a PPAP Case
1. In the sidebar, fill out the "Create New PPAP Case" form
2. Enter Part Number, Revision, and Supplier
3. Select QIL, PC, and CTF flags
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
2. Type questions in chat input
3. Use quick question buttons for common queries
4. Chat maintains context of current PPAP case

---

## Recent Updates

### Latest Improvements (2026-01-17)
- **Fixed audit log and version history display:** Replaced monospace/code-styled dataframe with clean, readable card-based layouts
- **Enhanced version history:** Each document version now displays as a bordered card with proper formatting
- **Improved audit trail:** Activity log now uses icons, better spacing, and readable fonts
- **Better visual hierarchy:** Timestamps, activity types, and descriptions are now clearly separated

---

## Future Enhancements (Backend Implementation)

### Planned Features
- Real AI integration with Medtronic GPT
- Database implementation for persistent storage
- Actual PDF parsing and dimension extraction
- Real version comparison and diff detection
- Document storage and retrieval system
- User authentication and role management
- Advanced analytics and reporting
- Integration with existing Medtronic systems

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
├── UI/
│   └── ppap_review_app.py    # Main Streamlit application
└── README.md                  # This file
```

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

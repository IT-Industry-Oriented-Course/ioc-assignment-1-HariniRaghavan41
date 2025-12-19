# Clinical Workflow Automation Agent 🏥

**IOC Assignment 1 - Harini Raghavan**

An intelligent, function-calling LLM agent designed to orchestrate clinical workflows. This agent interprets natural language requests from clinicians to schedule appointments, check insurance eligibility, and find available slots, all while enforcing safety and validation protocols.

---

## 🚀 Features

- **Intelligent Orchestration**: Uses an LLM to decide which tools to call based on natural language input.
- **Deterministic Tools**:
    - `search_patient`: Fuzzy search for patient records.
    - `check_insurance_eligibility`: Real-time (mocked) insurance validation.
    - `find_available_slots`: Smart slot discovery excluding booked times.
    - `book_appointment`: Transactional booking logic.
- **FHIR-Aligned Models**: Data schemas (`Patient`, `Appointment`, `Coverage`) inspired by HL7 FHIR standards.
- **Safety First**:
    - Validates patient existence before booking.
    - Refuses to provide medical diagnoses or advice.
    - Operates within a strictly defined scope.

## 🛠️ Prerequisites

- **Python 3.9+**
- **Hugging Face API Token** (or OpenAI API Key)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/IT-Industry-Oriented-Course/ioc-assignment-1-HariniRaghavan41.git
   cd ioc-assignment-1-HariniRaghavan41
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory and add your API token:
   ```env
   HUGGINGFACEHUB_API_TOKEN=hf_YourTokenHere
   # OR
   OPENAI_API_KEY=sk-YourKeyHere
   ```
   *Get your HF Token [here](https://huggingface.co/settings/tokens).*

## 💻 Usage

### Interactive CLI
Run the agent in interactive mode:
```bash
python src/main.py
```

**Example Session:**
```text
Enter Request: Check eligibility for Ravi Kumar
[AGENT] Searching for patient 'Ravi Kumar'...
[AGENT] Checking insurance...
[RESPONSE] Ravi Kumar is eligible (MediCare Plus, Active).
```

### Supported Queries
- *"Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility"*
- *"Find vacant slots for General Practice this Friday"*
- *"Book an appointment for Linda Chen for Dermatology"*

## 📂 Project Structure

```
ioc-assignment-1/
├── src/
│   ├── agent.py       # Core agent logic & LLM binding
│   ├── tools.py       # Implementation of clinical tools
│   ├── models.py      # Pydantic data models (FHIR-like)
│   ├── mock_db.py     # In-memory database (Patients/Appts)
│   └── main.py        # CLI Entry point
├── tests/
│   └── test_tools.py  # Unit tests for tools
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

## 🧪 Testing

Run the automated test suite to verify tool functionality:
```bash
python tests/test_tools.py
```

---
*Built for the Clinical Workflow Automation Assignment.*

from datetime import date, datetime, timedelta
from typing import Dict, List
import uuid
from src.models import Patient, Appointment, InsuranceCoverage, AppointmentStatus, InsuranceStatus

# Mock In-Memory Database

# 1. Patients
patients_db: Dict[str, Patient] = {
    "P001": Patient(id="P001", name="Ravi Kumar", dob=date(1985, 6, 15), gender="Male", phone="555-0101"),
    "P002": Patient(id="P002", name="Linda Chen", dob=date(1992, 11, 20), gender="Female", phone="555-0102"),
    "P003": Patient(id="P003", name="Marcus Johnson", dob=date(1978, 3, 10), gender="Male", phone="555-0103"),
    "P004": Patient(id="P004", name="Sarah Jones", dob=date(1990, 7, 22), gender="Female", phone="555-0104"),
    "P005": Patient(id="P005", name="Mike Ross", dob=date(1982, 1, 15), gender="Male", phone="555-0105"),
    "P006": Patient(id="P006", name="Rachel Zane", dob=date(1988, 8, 12), gender="Female", phone="555-0106"),
    "P007": Patient(id="P007", name="Harvey Specter", dob=date(1972, 5, 1), gender="Male", phone="555-0107"),
    "P008": Patient(id="P008", name="Jessica Pearson", dob=date(1975, 9, 30), gender="Female", phone="555-0108"),
}

# 2. Insurance Coverage
coverage_db: Dict[str, List[InsuranceCoverage]] = {
    "P001": [InsuranceCoverage(id="C001", patient_id="P001", payer_name="MediCare Plus", policy_number="MC-998877", status=InsuranceStatus.ACTIVE)],
    "P002": [InsuranceCoverage(id="C002", patient_id="P002", payer_name="Global Health", policy_number="GH-112233", status=InsuranceStatus.ACTIVE)],
    "P004": [InsuranceCoverage(id="C003", patient_id="P004", payer_name="Aetna", policy_number="AE-445566", status=InsuranceStatus.ACTIVE)],
    "P005": [InsuranceCoverage(id="C004", patient_id="P005", payer_name="Blue Cross", policy_number="BC-778899", status=InsuranceStatus.PENDING)], # Pending coverage
    "P007": [InsuranceCoverage(id="C005", patient_id="P007", payer_name="Pearson Health", policy_number="PH-001001", status=InsuranceStatus.ACTIVE)],
    "P008": [InsuranceCoverage(id="C006", patient_id="P008", payer_name="Pearson Health", policy_number="PH-001002", status=InsuranceStatus.DRAFT)], # Draft coverage
    # P003, P006 have no coverage
}

# 3. Appointments
# Helper to get dynamic dates
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

appointments_db: Dict[str, Appointment] = {
    "A001": Appointment(
        id="A001", 
        patient_id="P001", 
        provider_id="Dr. Smith (Cardiology)", 
        start_time=today - timedelta(days=30, hours=-10), 
        end_time=today - timedelta(days=30, hours=-11), 
        status=AppointmentStatus.FULFILLED, 
        reason="Initial Consultation"
    ),
    # Pending / Future Appointments
    "A002": Appointment(
        id="A002",
        patient_id="P004",
        provider_id="Dr. Mock (General Practice)",
        start_time=today + timedelta(days=1, hours=10), # Tomorrow 10 AM
        end_time=today + timedelta(days=1, hours=11),
        status=AppointmentStatus.PENDING, # Pending slot
        reason="Routine Checkup"
    ),
    "A003": Appointment(
        id="A003",
        patient_id="P005",
        provider_id="Dr. Mock (Cardiology)",
        start_time=today + timedelta(days=2, hours=14), # Day after tomorrow 2 PM
        end_time=today + timedelta(days=2, hours=15),
        status=AppointmentStatus.BOOKED,
        reason="Follow-up: High BP"
    ),
    "A004": Appointment(
        id="A004",
        patient_id="P002",
        provider_id="Dr. Mock (Dermatology)",
        start_time=today + timedelta(days=3, hours=9), 
        end_time=today + timedelta(days=3, hours=10),
        status=AppointmentStatus.PROPOSED,
        reason="Skin Rash"
    ),
    "A005": Appointment(
        id="A005",
        patient_id="P007",
        provider_id="Dr. Mock (Neurology)",
        start_time=today + timedelta(days=1, hours=11), 
        end_time=today + timedelta(days=1, hours=12),
        status=AppointmentStatus.BOOKED,
        reason="Migraine"
    )
}

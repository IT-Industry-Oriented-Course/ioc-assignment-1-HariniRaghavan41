from typing import List, Optional, Dict
from datetime import datetime, timedelta
import uuid
import json

from langchain_core.tools import tool
from src.models import Patient, Appointment, InsuranceCoverage, AppointmentStatus, InsuranceStatus
from src.mock_db import patients_db, coverage_db, appointments_db

@tool
def search_patient(name: str) -> List[Dict]:
    """
    Search for a patient by name (fuzzy match included).
    Returns a list of matching patients with their details.
    
    Args:
        name: Name to search for (e.g. "Ravi", "Ravi Kumar")
    """
    print(f"[TOOL LOG] Searching for patient: {name}")
    results = []
    for p in patients_db.values():
        if name.lower() in p.name.lower():
            results.append(p.model_dump())
    
    if not results:
        return []
    
    return [
        {
            "id": r["id"],
            "name": r["name"],
            "dob": r["dob"].isoformat(),
            "phone": r["phone"]
        } for r in results
    ]

@tool
def check_insurance_eligibility(patient_id: str) -> Dict:
    """
    Check the insurance eligibility status for a given patient ID.
    
    Args:
        patient_id: The ID of the patient (e.g. "P001")
    """
    print(f"[TOOL LOG] Checking insurance for Patient ID: {patient_id}")
    if patient_id not in patients_db:
        return {"error": "Patient not found"}
        
    coverages = coverage_db.get(patient_id, [])
    if not coverages:
        return {"eligible": False, "reason": "No coverage found"}
    
    active_coverage = next((c for c in coverages if c.status == InsuranceStatus.ACTIVE), None)
    
    if active_coverage:
        return {
            "eligible": True,
            "payer": active_coverage.payer_name,
            "policy": active_coverage.policy_number,
            "status": active_coverage.status.value
        }
    else:
        return {"eligible": False, "reason": "No active policies found"}

@tool
def find_available_slots(department: str, date_range: str = "next 7 days") -> List[Dict]:
    """
    Find available appointment slots for a specific department.
    
    Args:
        department: The medical department (e.g. "Cardiology", "General Practice")
        date_range: The range to search (e.g. "next week", "2023-10-20 to 2023-10-25"). 
                    Defaults to next 7 days.
    """
    print(f"[TOOL LOG] Finding slots for {department} in {date_range}")
    
    # Mock Logic: Generate random slots for the next few days
    # In a real app, this would query a scheduler system
    
    slots = []
    base_date = datetime.now().replace(minute=0, second=0, microsecond=0)
    
    # Generate 5 slots
    for i in range(1, 6):
        # Create a slot at 10 AM and 2 PM for the next 3 days alternating
        day_offset = i // 2
        hour = 10 if i % 2 != 0 else 14
        
        slot_time = base_date + timedelta(days=day_offset, hours=hour)
        if slot_time.weekday() > 4: # Skip weekends mock logic
            continue
            
        # CHECK: consistency with appointments_db
        # In a real app, this query would be part of the initial DB fetch
        start_iso = slot_time.isoformat()
        is_booked = False
        for appt in appointments_db.values():
            # Check if this provider is already booked at this time
            # For this mock, we assume 'Dr. Mock' matches or generic availability check
            if appt.start_time == slot_time and appt.status in [AppointmentStatus.BOOKED, AppointmentStatus.Pending]:
                 is_booked = True
                 break
        
        if is_booked:
            continue

        slot_id = f"SLOT_{uuid.uuid4().hex[:8].upper()}"
        slots.append({
            "slot_id": slot_id,
            "start_time": slot_time.isoformat(),
            "end_time": (slot_time + timedelta(hours=1)).isoformat(),
            "provider": f"Dr. Mock ({department})"
        })
        
    return slots

@tool
def book_appointment(patient_id: str, slot_id: str, reason: str, start_time: Optional[str] = None) -> Dict:
    """
    Book an appointment for a patient.
    
    Args:
        patient_id: The ID of the patient (e.g. "P001")
        slot_id: The ID of the slot to reserve (from find_available_slots)
        reason: The medical reason for the visit
        start_time: (Optional) Explicit start time if slot_id logic is generic. 
                    If provided, assumes slot_id validation is already done.
    """
    print(f"[TOOL LOG] Booking appointment for {patient_id}, Slot: {slot_id}")
    
    if patient_id not in patients_db:
        return {"status": "error", "message": "Patient not found"}
    
    # In a real scenario, we would validate slot_id against a slots DB.
    # Here we simulate success if the inputs look valid.
    
    # Create Appointment Object
    new_appt_id = f"A{uuid.uuid4().hex[:8].upper()}"
    
    # Use provided start_time if available, or try to find it (in eager mode we can't easily)
    if not start_time:
         # For this POC, if time isn't passed, we'll just mock it. 
         # But to fix the "slot taken" bug, we need the exact time. 
         # Let's default to next Friday 10am if not passed, just to show it works, 
         # OR rely on the agent extracting it.
         booking_time = datetime.now().replace(microsecond=0, second=0, minute=0) + timedelta(days=2)
    else:
        try:
           booking_time = datetime.fromisoformat(start_time)
        except:
           booking_time = datetime.now() # Fallback

    appt = Appointment(
        id=new_appt_id,
        patient_id=patient_id,
        provider_id="Dr. Mock (Cardiology)", # Inferred from context or slot
        start_time=booking_time,
        end_time=booking_time + timedelta(hours=1),
        status=AppointmentStatus.BOOKED,
        reason=reason
    )
    
    appointments_db[new_appt_id] = appt
    
    return {
        "status": "confirmed",
        "appointment_id": new_appt_id,
        "patient": patients_db[patient_id].name,
        "time": appt.start_time.isoformat(),
        "provider": appt.provider_id
    }

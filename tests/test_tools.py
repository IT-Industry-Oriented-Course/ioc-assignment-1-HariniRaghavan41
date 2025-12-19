import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools import search_patient, check_insurance_eligibility, find_available_slots, book_appointment

class TestClinicalTools(unittest.TestCase):
    
    def test_search_patient_found(self):
        # Test searching for "Ravi"
        result = search_patient.invoke({"name": "Ravi"})
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]["name"], "Ravi Kumar")
        self.assertEqual(result[0]["id"], "P001")

    def test_search_patient_not_found(self):
        result = search_patient.invoke({"name": "NonExistent"})
        self.assertEqual(result, [])

    def test_check_insurance_eligible(self):
        # P001 has active coverage
        result = check_insurance_eligibility.invoke({"patient_id": "P001"})
        self.assertTrue(result["eligible"])
        self.assertEqual(result["payer"], "MediCare Plus")

    def test_check_insurance_ineligible(self):
        # P003 has no coverage
        result = check_insurance_eligibility.invoke({"patient_id": "P003"})
        self.assertFalse(result["eligible"])

    def test_find_slots(self):
        result = find_available_slots.invoke({"department": "Cardiology"})
        self.assertTrue(len(result) > 0)
        self.assertIn("slot_id", result[0])
        print(f"\nExample Slot: {result[0]}")

    def test_book_appointment(self):
        # 1. Find a slot
        slots = find_available_slots.invoke({"department": "Cardiology"})
        slot_id = slots[0]["slot_id"]
        start_time = slots[0]["start_time"]
        
        # 2. Book it
        result = book_appointment.invoke({
            "patient_id": "P001",
            "slot_id": slot_id,
            "reason": "Chest pain",
            "start_time": start_time
        })
        
        self.assertEqual(result["status"], "confirmed")
        self.assertEqual(result["patient"], "Ravi Kumar")
        
if __name__ == '__main__':
    unittest.main()

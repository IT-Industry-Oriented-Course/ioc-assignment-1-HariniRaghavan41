from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import date, datetime

class Patient(BaseModel):
    """Schema for Patient data, inspired by FHIR Patient resource."""
    id: str = Field(..., description="Unique identifier for the patient")
    name: str = Field(..., description="Full name of the patient")
    dob: date = Field(..., description="Date of birth")
    gender: str = Field(..., description="Gender of the patient")
    phone: str = Field(..., description="Contact phone number")

class AppointmentStatus(str, Enum):
    PROPOSED = "proposed"
    PENDING = "pending"
    BOOKED = "booked"
    ARRIVED = "arrived"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"

class Appointment(BaseModel):
    """Schema for Appointment data, inspired by FHIR Appointment resource."""
    id: str = Field(..., description="Unique identifier for the appointment")
    patient_id: str = Field(..., description="Reference to the patient")
    provider_id: str = Field(..., description="Reference to the provider or department")
    start_time: datetime = Field(..., description="Start time of the appointment")
    end_time: datetime = Field(..., description="End time of the appointment")
    status: AppointmentStatus = Field(default=AppointmentStatus.PROPOSED, description="Current status")
    reason: str = Field(..., description="Reason for the appointment")

class InsuranceStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    DRAFT = "draft"
    PENDING = "pending"
    ENTERED_IN_ERROR = "entered-in-error"

class InsuranceCoverage(BaseModel):
    """Schema for Insurance Coverage, inspired by FHIR Coverage resource."""
    id: str = Field(..., description="Unique identifier for the coverage")
    patient_id: str = Field(..., description="Reference to the patient")
    payer_name: str = Field(..., description="Name of the insurance company")
    policy_number: str = Field(..., description="Policy number")
    status: InsuranceStatus = Field(..., description="Status of the coverage")

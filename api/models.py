"""
API response models.
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AccountResponse(BaseModel):
    """Account response model."""
    model_config = ConfigDict(from_attributes=True)
    
    account_id: str
    account_type: str
    currency: str
    status: str
    opened_date: datetime
    closed_date: Optional[datetime] = None


class TransactionResponse(BaseModel):
    """Transaction response model."""
    model_config = ConfigDict(from_attributes=True)
    
    transaction_id: str
    account_id: str
    transaction_type: str
    amount: Decimal
    currency: str
    timestamp: datetime
    counterparty: Optional[str] = None
    description: Optional[str] = None


class CustomerResponse(BaseModel):
    """Customer response model."""
    model_config = ConfigDict(from_attributes=True)
    
    customer_id: str
    name: str
    risk_rating: str
    country: str
    created_at: datetime
    accounts: List[AccountResponse]


class AlertEventResponse(BaseModel):
    """Alert event response model."""
    model_config = ConfigDict(from_attributes=True)
    
    event_type: str
    timestamp: datetime
    user_id: Optional[str] = None
    notes: Optional[str] = None


class AlertResponse(BaseModel):
    """Alert response model."""
    model_config = ConfigDict(from_attributes=True)
    
    alert_id: str
    alert_type: str
    risk_score: float
    status: str
    created_at: datetime
    description: str
    customer: CustomerResponse
    transaction: Optional[TransactionResponse] = None
    events: List[AlertEventResponse]


class TransactionSummary(BaseModel):
    """Transaction summary model."""
    total_count: int
    total_amount: Decimal
    average_amount: Decimal
    currency: str
    by_type: dict[str, int]  # Transaction type -> count

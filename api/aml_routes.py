"""AML routes for the FastAPI application."""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Query, Path
from pydantic import BaseModel
from decimal import Decimal
from . import dummy_data

class CustomerResponse(BaseModel):
    customer_id: str
    name: str
    risk_rating: str
    country: str
    accounts: list

class TransactionResponse(BaseModel):
    transaction_id: str
    transaction_type: str
    amount: Decimal
    currency: str
    date: datetime

class AlertTransactionsResponse(BaseModel):
    alert_id: str
    alert_type: str
    triggering_transactions: List[TransactionResponse]
    related_transactions: List[TransactionResponse]
    total_transaction_count: int
    total_transaction_amount: Decimal
    time_period: str

router = APIRouter(prefix="/api/v1")

@router.get("/customers/{customer_id}/documents")
async def get_customer_documents(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Retrieve all documents attached to a specific customer.
    """
    return dummy_data.generate_documents(customer_id)

@router.get("/customers/{customer_id}/documents/summary")
async def get_document_summary(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get a summary of customer documents from an AML perspective.
    """
    return dummy_data.generate_document_summary(customer_id)

@router.get("/customers/{customer_id}/transactions")
async def get_transaction_summary(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    start_date: datetime = Query(..., description="Start date for the transaction period"),
    end_date: datetime = Query(..., description="End date for the transaction period")
):
    """
    Get customer transactions summarized by type over a specified period.
    """
    return dummy_data.generate_transaction_summary(customer_id, start_date, end_date)

@router.get("/customers/{customer_id}/alerts")
async def get_customer_alerts(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all historical alerts that have resulted in a case.
    """
    return dummy_data.generate_alerts(customer_id)

@router.get("/customers/{customer_id}/relationships")
async def get_customer_relationships(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all relationships attached to a particular customer.
    """
    return dummy_data.generate_relationships(customer_id)

@router.get("/customers/{customer_id}/counterparties")
async def get_customer_counterparties(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    months: int = Query(6, description="Number of months to look back")
):
    """
    Get all counterparties a customer has interacted with over a period.
    """
    return dummy_data.generate_counterparties(customer_id, months)

@router.get("/customers/{customer_id}/touchpoints")
async def get_customer_touchpoints(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    months: int = Query(6, description="Number of months to look back")
):
    """
    Get all bank touchpoints for a customer over a period.
    """
    return dummy_data.generate_touchpoints(customer_id, months)

@router.get("/customers/{customer_id}/business-locations")
async def get_business_locations(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all places where the customer conducts business.
    """
    return dummy_data.generate_business_locations(customer_id)

@router.get("/countries/{country_code}/risk-assessment")
async def get_country_risk(
    country_code: str = Path(..., description="The country code to assess")
):
    """
    Check if a country is rated high risk.
    """
    return dummy_data.generate_country_risk(country_code)

@router.get("/customers/{customer_id}/pep-counterparties")
async def get_pep_counterparties(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get politically exposed counterparties for a customer.
    """
    return dummy_data.generate_pep_counterparties(customer_id)

@router.get("/customers/{customer_id}/subsidiaries")
async def get_customer_subsidiaries(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all subsidiaries and their transactions for a customer.
    """
    return dummy_data.generate_subsidiary_info(customer_id)

@router.get("/customers/{customer_id}/alert-scenarios")
async def get_customer_alert_scenarios(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all scenarios used to generate alerts for a customer.
    """
    return dummy_data.generate_alert_scenarios(customer_id)

@router.get("/counterparties/{counterparty_id}/related-customers")
async def get_related_customers(
    counterparty_id: str = Path(..., description="The unique identifier of the counterparty")
):
    """
    Get all bank customers who have interacted with a counterparty.
    """
    return dummy_data.generate_related_customers(counterparty_id)

@router.get("/scenarios/{scenario_id}")
async def get_scenario_details(
    scenario_id: str = Path(..., description="The unique identifier of the scenario")
):
    """
    Get detailed description and parameters for a money laundering scenario.
    """
    return dummy_data.generate_scenario_details(scenario_id)

@router.get("/scenarios/{scenario_id}/thresholds")
async def get_scenario_thresholds(
    scenario_id: str = Path(..., description="The unique identifier of the scenario")
):
    """
    Get all thresholds for an AML scenario.
    """
    return dummy_data.generate_scenario_thresholds(scenario_id)

@router.get("/alerts/{alert_id}/transactions", response_model=AlertTransactionsResponse)
async def get_alert_transactions_detail(
    alert_id: str = Path(..., description="The unique identifier of the alert"),
    include_related: bool = Query(True, description="Include related transactions in the response")
):
    """
    Get all transactions linked to a specific alert.
    
    This endpoint returns:
    - Transactions that triggered the alert
    - Related transactions from the same customer
    - Transaction statistics and summary
    
    Parameters:
    - alert_id: Unique identifier of the alert
    - include_related: If true, includes related transactions from the same time period
    """
    return dummy_data.generate_alert_transactions_detail(alert_id, include_related)

@router.get("/alerts/{alert_id}/customer", response_model=CustomerResponse)
async def get_alert_customer_details(
    alert_id: str = Path(..., description="The unique identifier of the alert")
):
    """
    Get detailed customer information and all their accounts for a given alert ID.
    
    This endpoint returns:
    - Customer details (ID, name, risk rating, country)
    - All accounts associated with the customer
    - Account details (type, status, currency, dates)
    """
    return dummy_data.generate_alert_customer_details(alert_id)

@router.get("/transactions/{transaction_id}/outlier-analysis")
async def get_transaction_outlier_analysis(
    transaction_id: str = Path(..., description="The unique identifier of the transaction"),
    analysis_type: str = Query(
        ...,
        description="Type of analysis to perform",
        enum=["customer_6month", "customer_daily", "same_day_transfers"]
    )
):
    """
    Analyze if a transaction is an outlier based on different criteria.
    """
    return dummy_data.generate_outlier_analysis(transaction_id, analysis_type)

@router.get("/counterparties/risk-assessment")
async def get_counterparties_risk_assessment(
    customer_id: str = Query(None, description="Filter counterparties for a specific customer"),
    risk_level: str = Query(None, description="Filter by risk level (HIGH, MEDIUM, LOW)"),
    is_pep: bool = Query(None, description="Filter politically exposed persons")
):
    """
    Get risk assessment for all counterparties including PEP status.
    
    This endpoint provides:
    - Comprehensive risk assessment for each counterparty
    - PEP status and details if applicable
    - Transaction history and patterns
    - Risk factors and scores
    
    Parameters:
    - customer_id: Optional filter for a specific customer's counterparties
    - risk_level: Optional filter by risk level
    - is_pep: Optional filter for politically exposed persons
    """
    return dummy_data.generate_counterparties_risk_assessment(customer_id, risk_level, is_pep)

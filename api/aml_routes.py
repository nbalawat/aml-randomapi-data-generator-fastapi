"""AML routes for the FastAPI application."""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Query, Path
from pydantic import BaseModel
from decimal import Decimal
from . import data_generator as data

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

class CustomerDocument(BaseModel):
    id: str
    type: str
    date_created: datetime
    content: str

class JurisdictionDetail(BaseModel):
    country_code: str
    country_name: str
    risk_level: str
    risk_factors: List[str]

class TransactionDetail(BaseModel):
    customer_id: str
    transaction_id: str
    transaction_amount: Decimal
    source_of_funds_jurisdiction: JurisdictionDetail
    date: Optional[datetime] = None

class ScenarioDetail(BaseModel):
    """Details about an AML scenario."""
    id: str
    name: str
    description: str
    threshold: float
    time_window_days: int

class AlertTransactionsResponse(BaseModel):
    """Response model for alert-triggering transactions."""
    scenario: ScenarioDetail
    alert_id: str
    transactions: List[TransactionDetail]

router = APIRouter()

@router.get("/api/v1/customers/{customer_id}/documents")
async def get_customer_documents(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Retrieve all documents attached to a specific customer.
    """
    return data.generate_documents(customer_id)

@router.get("/api/v1/customers/{customer_id}/documents/summary")
async def get_document_summary(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get a summary of customer documents from an AML perspective.
    """
    return data.generate_document_summary(customer_id)

@router.get("/api/v1/customers/{customer_id}/transactions")
async def get_customer_transactions(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    start_date: Optional[datetime] = Query(None, description="Start date for the transaction period"),
    end_date: Optional[datetime] = Query(None, description="End date for the transaction period"),
    months: Optional[int] = Query(None, description="Number of months of history to return (max 36)")
) -> List[TransactionDetail]:
    """
    Get transaction details for a specific customer.
    
    Parameters:
    - start_date/end_date: Optional date range filter
    - months: Optional number of months of history to return (max 36)
    
    Returns a list of transactions with the following characteristics:
    - 3-5 transactions per month
    - Mix of jurisdictions (70% low risk, 20% medium risk, 10% high risk)
    - Outlier transactions in random months (large amounts from high-risk jurisdictions)
    """
    # Generate historical transactions
    transactions = data.generate_historical_transactions(customer_id, min(months or 36, 36))
    
    # Filter by date range if provided
    if start_date and end_date:
        transactions = [
            t for t in transactions 
            if start_date <= datetime.fromisoformat(t["date"]) <= end_date
        ]
    
    # Convert to TransactionDetail objects
    return [
        TransactionDetail(
            customer_id=t["customer_id"],
            transaction_id=t["transaction_id"],
            transaction_amount=Decimal(t["transaction_amount"]),
            source_of_funds_jurisdiction=t["source_of_funds_jurisdiction"],
            date=datetime.fromisoformat(t["date"])
        )
        for t in transactions
    ]

@router.get("/api/v1/customers/{customer_id}/incorporation-documents")
async def get_customer_incorporation_documents(
    customer_id: str = Path(..., description="The unique identifier of the customer")
) -> List[CustomerDocument]:
    """
    Get incorporation documents for a specific customer.
    """
    # Mock data based on screenshot example
    if customer_id == "1234":
        return [
            CustomerDocument(
                id="89fb5e08-843b-4877-8244-326ae678067f",
                type="ARTICLES_OF_INCORPORATION",
                date_created=datetime.fromisoformat("2024-07-25T17:08:06.018284"),
                content="The name of the corporation is Advancement in Education (AIE). The corporation is organized for promoting access to education and improving outcomes, and obtains its funding through monthly donations. It qualifies as tax exempt under section 501(c)(3) of the IRC. Each January AIE holds a fundraising event which provides the majority of the corporation's yearly funding."
            ),
            CustomerDocument(
                id="89fb5e08-843b-4877-8244-326ae678067f",
                type="BYLAWS",
                date_created=datetime.fromisoformat("2024-07-25T17:08:06.018284"),
                content="Advancement in Education (AIE) operates in the United States of America. AIE supports school programs for children in need."
            )
        ]
    elif customer_id == "1235":
        return [
            CustomerDocument(
                id="89fb5e08-843b-4877-8244-326ae678067f",
                type="ARTICLES_OF_INCORPORATION",
                date_created=datetime.fromisoformat("2024-07-25T17:08:06.018284"),
                content="The name of the corporation is Better Energy Advocates (BEA). The corporation is organized for energy policy development and educational purposes, along with non-substantial lobbying activity and obtains its funding through monthly donations. It qualifies as tax exempt under section 501(c)(3) of the IRC."
            ),
            CustomerDocument(
                id="89fb5e08-843b-4877-8244-326ae678067f",
                type="BYLAWS",
                date_created=datetime.fromisoformat("2024-07-25T17:08:06.018284"),
                content="Better Energy Advocates (BEA) operates in the United States of America. BEA Advocates supports development, education, and limited influencing of legislation at the federal level."
            )
        ]
    return []

@router.get("/api/v1/customers/{customer_id}/alerts")
async def get_customer_alerts(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all historical alerts that have resulted in a case.
    """
    return data.generate_alerts(customer_id)

@router.get("/api/v1/customers/{customer_id}/relationships")
async def get_customer_relationships(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all relationships attached to a particular customer.
    """
    return data.generate_relationships(customer_id)

@router.get("/api/v1/customers/{customer_id}/counterparties")
async def get_customer_counterparties(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    months: int = Query(6, description="Number of months to look back")
):
    """
    Get all counterparties a customer has interacted with over a period.
    """
    return data.generate_counterparties(customer_id, months)

@router.get("/api/v1/customers/{customer_id}/touchpoints")
async def get_customer_touchpoints(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    months: int = Query(6, description="Number of months to look back")
):
    """
    Get all bank touchpoints for a customer over a period.
    """
    return data.generate_touchpoints(customer_id, months)

@router.get("/api/v1/customers/{customer_id}/business-locations")
async def get_business_locations(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all places where the customer conducts business.
    """
    return data.generate_business_locations(customer_id)

@router.get("/api/v1/countries/{country_code}/risk-assessment")
async def get_country_risk(
    country_code: str = Path(..., description="The country code to assess")
):
    """
    Check if a country is rated high risk.
    """
    return data.generate_country_risk(country_code)

@router.get("/api/v1/customers/{customer_id}/pep-counterparties")
async def get_pep_counterparties(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get politically exposed counterparties for a customer.
    """
    return data.generate_pep_counterparties(customer_id)

@router.get("/api/v1/customers/{customer_id}/subsidiaries")
async def get_customer_subsidiaries(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all subsidiaries and their transactions for a customer.
    """
    return data.generate_subsidiary_info(customer_id)

@router.get("/api/v1/customers/{customer_id}/alert-scenarios")
async def get_customer_alert_scenarios(
    customer_id: str = Path(..., description="The unique identifier of the customer")
):
    """
    Get all scenarios used to generate alerts for a customer.
    """
    return data.generate_alert_scenarios(customer_id)

@router.get("/api/v1/counterparties/{counterparty_id}/related-customers")
async def get_related_customers(
    counterparty_id: str = Path(..., description="The unique identifier of the counterparty")
):
    """
    Get all bank customers who have interacted with a counterparty.
    """
    return data.generate_related_customers(counterparty_id)

@router.get("/api/v1/scenarios/{scenario_id}")
async def get_scenario_details(
    scenario_id: str = Path(..., description="The unique identifier of the scenario")
):
    """
    Get detailed description and parameters for a money laundering scenario.
    """
    return data.generate_scenario_details(scenario_id)

@router.get("/api/v1/scenarios/{scenario_id}/thresholds")
async def get_scenario_thresholds(
    scenario_id: str = Path(..., description="The unique identifier of the scenario")
):
    """
    Get all thresholds for an AML scenario.
    """
    return data.generate_scenario_thresholds(scenario_id)

@router.get("/api/v1/alerts/{alert_id}/transactions", response_model=AlertTransactionsResponse)
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
    return data.generate_alert_transactions_detail(alert_id, include_related)

@router.get("/api/v1/alerts/{alert_id}/customer", response_model=CustomerResponse)
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
    return data.generate_alert_customer_details(alert_id)

@router.get("/api/v1/transactions/{transaction_id}/outlier-analysis")
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
    return data.generate_outlier_analysis(transaction_id, analysis_type)

@router.get("/api/v1/counterparties/risk-assessment")
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
    return data.generate_counterparties_risk_assessment(customer_id, risk_level, is_pep)

@router.get("/api/v1/customers/{customer_id}/transaction-metrics")
async def get_transaction_metrics(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    months: int = Query(6, description="Number of months to analyze")
):
    """
    Get comprehensive transaction metrics for a customer.
    """
    return data.generate_transaction_metrics(customer_id, months)

@router.get("/api/v1/customers/{customer_id}/high-risk-metrics")
async def get_high_risk_metrics(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    months: int = Query(6, description="Number of months to analyze", ge=3, le=6)
):
    """
    Get metrics related to high-risk transactions.
    """
    return data.generate_high_risk_metrics(customer_id, months)

@router.get("/api/v1/customers/{customer_id}/transaction-patterns")
async def get_transaction_patterns(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    months: int = Query(6, description="Number of months to analyze")
):
    """
    Get analysis of transaction patterns and behaviors.
    """
    return data.generate_transaction_patterns(customer_id, months)

@router.get("/api/v1/customers/{customer_id}/transaction-analysis")
async def get_transaction_analysis(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    months: int = Query(6, description="Number of months to analyze")
):
    """
    Get detailed analysis of transaction characteristics.
    """
    return data.generate_transaction_analysis(customer_id, months)

@router.get("/api/v1/customers/{customer_id}/alert-transactions")
async def get_alert_triggering_transactions(
    customer_id: str = Path(..., description="The unique identifier of the customer"),
    scenario_type: Optional[str] = Query(
        None,
        description="Specific scenario type to generate (STRUCTURING, RAPID_MOVEMENT, HIGH_RISK_FLOW, UNUSUAL_PATTERN, ROUND_NUMBERS)"
    )
) -> AlertTransactionsResponse:
    """
    Get transactions that would trigger an AML alert for a specific customer.
    
    Parameters:
    - customer_id: Customer identifier
    - scenario_type: Optional specific scenario to generate (if not provided, a random scenario is chosen)
    
    Returns transactions that would trigger an AML alert based on various scenarios:
    - STRUCTURING: Multiple transactions just below reporting threshold
    - RAPID_MOVEMENT: Large amounts moved quickly through accounts
    - HIGH_RISK_FLOW: Large transfers involving high-risk jurisdictions
    - UNUSUAL_PATTERN: Sudden change in transaction behavior
    - ROUND_NUMBERS: Multiple large round-number transactions
    """
    result = data.generate_alert_triggering_transactions(customer_id, scenario_type)
    
    # Convert transactions to TransactionDetail objects
    transactions = [
        TransactionDetail(
            customer_id=t["customer_id"],
            transaction_id=t["transaction_id"],
            transaction_amount=Decimal(t["transaction_amount"]),
            source_of_funds_jurisdiction=t["source_of_funds_jurisdiction"],
            date=datetime.fromisoformat(t["date"])
        )
        for t in result["transactions"]
    ]
    
    return AlertTransactionsResponse(
        scenario=ScenarioDetail(**result["scenario"]),
        alert_id=result["alert_id"],
        transactions=transactions
    )

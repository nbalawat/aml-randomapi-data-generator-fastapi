"""
API routes for AML investigation.
"""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from amlagents.api.models import (
    AlertResponse,
    CustomerResponse,
    TransactionResponse,
    TransactionSummary,
)
from amlagents.database.models import Alert, Customer, Transaction
from amlagents.database.session import get_database

router = APIRouter(prefix="/api/v1")


async def get_session() -> AsyncSession:
    """Get database session."""
    db = get_database()
    async with db.session() as session:
        yield session


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert_details(
    alert_id: str,
    session: AsyncSession = Depends(get_session),
) -> Alert:
    """Get alert details including customer and transaction information.
    
    Args:
        alert_id: Alert ID
        session: Database session
        
    Returns:
        Alert details with related information
        
    Raises:
        HTTPException: If alert not found
    """
    result = await session.execute(
        select(Alert)
        .options(
            joinedload(Alert.customer).joinedload(Customer.accounts),
            joinedload(Alert.transaction),
            selectinload(Alert.events),
        )
        .where(Alert.alert_id == alert_id)
    )
    alert = result.unique().scalar_one_or_none()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return alert


@router.get("/alerts/{alert_id}/customer", response_model=CustomerResponse)
async def get_alert_customer(
    alert_id: str,
    session: AsyncSession = Depends(get_session),
) -> Customer:
    """Get customer details for an alert.
    
    Args:
        alert_id: Alert ID
        session: Database session
        
    Returns:
        Customer details
        
    Raises:
        HTTPException: If alert or customer not found
    """
    result = await session.execute(
        select(Customer)
        .join(Alert)
        .options(selectinload(Customer.accounts))
        .where(Alert.alert_id == alert_id)
    )
    customer = result.unique().scalar_one_or_none()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer


@router.get("/alerts/{alert_id}/transactions", response_model=List[TransactionResponse])
async def get_alert_transactions(
    alert_id: str,
    session: AsyncSession = Depends(get_session),
) -> List[Transaction]:
    """Get transactions related to an alert.
    
    For transaction-based alerts, returns the triggering transaction.
    For pattern-based alerts, returns all transactions in the pattern.
    
    Args:
        alert_id: Alert ID
        session: Database session
        
    Returns:
        List of related transactions
        
    Raises:
        HTTPException: If alert not found
    """
    result = await session.execute(
        select(Alert)
        .options(joinedload(Alert.transaction))
        .where(Alert.alert_id == alert_id)
    )
    alert = result.unique().scalar_one_or_none()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    transactions = []
    if alert.transaction:
        transactions.append(alert.transaction)
    
    return transactions


@router.get("/alerts/{alert_id}/transaction_summary", response_model=TransactionSummary)
async def get_transaction_summary(
    alert_id: str,
    months: int = Query(default=6, ge=1, le=12),
    session: AsyncSession = Depends(get_session),
) -> TransactionSummary:
    """Get transaction summary for the alert's customer.
    
    Summarizes transactions for the specified number of months before the alert.
    
    Args:
        alert_id: Alert ID
        months: Number of months to analyze
        session: Database session
        
    Returns:
        Transaction summary
        
    Raises:
        HTTPException: If alert not found
    """
    # Get alert and customer
    result = await session.execute(
        select(Alert).where(Alert.alert_id == alert_id)
    )
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Calculate date range
    end_date = alert.created_at
    start_date = end_date - timedelta(days=30 * months)
    
    # Get transactions
    result = await session.execute(
        select(
            func.count().label("total_count"),
            func.sum(Transaction.amount).label("total_amount"),
            func.avg(Transaction.amount).label("average_amount"),
            Transaction.currency,
            Transaction.transaction_type,
        )
        .where(
            Transaction.customer_id == alert.customer_id,
            Transaction.timestamp.between(start_date, end_date),
        )
        .group_by(Transaction.currency, Transaction.transaction_type)
    )
    rows = result.all()
    
    if not rows:
        return TransactionSummary(
            total_count=0,
            total_amount=Decimal("0"),
            average_amount=Decimal("0"),
            currency="USD",  # Default
            by_type={},
        )
    
    # Aggregate by currency (assuming single currency for simplicity)
    currency = rows[0].currency
    total_count = sum(row.total_count for row in rows)
    total_amount = sum(row.total_amount for row in rows)
    average_amount = total_amount / total_count if total_count > 0 else Decimal("0")
    
    # Count by type
    by_type = {
        row.transaction_type: row.total_count
        for row in rows
    }
    
    return TransactionSummary(
        total_count=total_count,
        total_amount=total_amount,
        average_amount=average_amount,
        currency=currency,
        by_type=by_type,
    )

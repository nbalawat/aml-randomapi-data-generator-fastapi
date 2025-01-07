"""Data generation module for AML API."""
import random
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any, Optional
import uuid
import statistics

# Business names and industries
COMPANY_TYPES = ['LLC', 'Inc.', 'Corp', 'Ltd']
INDUSTRIES = [
    'Technology', 'Financial Services', 'Manufacturing', 'Healthcare',
    'Real Estate', 'Retail', 'Energy', 'Transportation', 'Construction'
]

BUSINESS_NAMES_FIRST = [
    'Global', 'Premier', 'Advanced', 'Strategic', 'Innovative',
    'United', 'Integrated', 'Digital', 'Pacific', 'Atlantic'
]

BUSINESS_NAMES_SECOND = [
    'Solutions', 'Systems', 'Technologies', 'Enterprises', 'Industries',
    'Partners', 'Group', 'Holdings', 'Capital', 'Ventures'
]

# Transaction types
TRANSACTION_TYPES = [
    'Wire Transfer', 'ACH Credit', 'ACH Debit', 'Check Deposit',
    'International Wire', 'Merchant Payment', 'Loan Payment', 'Payroll'
]

# Countries with risk ratings
COUNTRIES = {
    'US': 'LOW',
    'UK': 'LOW',
    'CA': 'LOW',
    'DE': 'LOW',
    'FR': 'LOW',
    'SG': 'MEDIUM',
    'AE': 'MEDIUM',
    'RU': 'HIGH',
    'IR': 'HIGH',
    'KP': 'HIGH'
}

def generate_business_name() -> str:
    """Generate a realistic business name."""
    return f"{random.choice(BUSINESS_NAMES_FIRST)} {random.choice(BUSINESS_NAMES_SECOND)} {random.choice(COMPANY_TYPES)}"

def generate_customer(customer_id: str) -> Dict[str, Any]:
    """Generate realistic customer data."""
    country = random.choice(list(COUNTRIES.keys()))
    return {
        "customer_id": customer_id,
        "name": generate_business_name(),
        "industry": random.choice(INDUSTRIES),
        "risk_rating": COUNTRIES[country],
        "country": country,
        "incorporation_date": (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime("%Y-%m-%d"),
        "accounts": generate_accounts()
    }

def generate_accounts() -> List[Dict[str, Any]]:
    """Generate realistic account data."""
    num_accounts = random.randint(1, 4)
    account_types = ['Operating', 'Payroll', 'Savings', 'Investment']
    currencies = ['USD', 'EUR', 'GBP']
    
    return [{
        "account_id": f"ACC{random.randint(100000, 999999)}",
        "type": account_types[i] if i < len(account_types) else random.choice(account_types),
        "currency": random.choice(currencies),
        "status": "Active",
        "balance": round(Decimal(random.uniform(10000, 1000000)), 2)
    } for i in range(num_accounts)]

def generate_transaction(transaction_id: str) -> Dict[str, Any]:
    """Generate realistic transaction data."""
    amount = round(Decimal(random.uniform(1000, 100000)), 2)
    return {
        "transaction_id": transaction_id,
        "transaction_type": random.choice(TRANSACTION_TYPES),
        "amount": amount,
        "currency": "USD",
        "date": (datetime.now() - timedelta(days=random.randint(0, 180))).isoformat()
    }

def generate_alerts(customer_id: str) -> List[Dict[str, Any]]:
    """Generate realistic alert data."""
    alert_types = [
        'Unusual Transaction Pattern',
        'Large Cash Transaction',
        'High-Risk Country Transfer',
        'Structured Transactions',
        'Multiple SAR Filing'
    ]
    
    num_alerts = random.randint(1, 5)
    return [{
        "alert_id": f"ALT{random.randint(100000, 999999)}",
        "customer_id": customer_id,
        "alert_type": random.choice(alert_types),
        "status": random.choice(['Open', 'Closed', 'Under Investigation']),
        "risk_score": random.randint(60, 95),
        "date_generated": (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat()
    } for _ in range(num_alerts)]

def generate_relationships(customer_id: str) -> List[Dict[str, Any]]:
    """Generate realistic business relationship data."""
    relationship_types = [
        'Parent Company',
        'Subsidiary',
        'Sister Company',
        'Joint Venture',
        'Business Partner'
    ]
    
    num_relationships = random.randint(1, 4)
    return [{
        "relationship_id": f"REL{random.randint(100000, 999999)}",
        "entity_name": generate_business_name(),
        "relationship_type": random.choice(relationship_types),
        "ownership_percentage": random.randint(10, 100) if "Subsidiary" in relationship_types else None,
        "country": random.choice(list(COUNTRIES.keys()))
    } for _ in range(num_relationships)]

def generate_documents(customer_id: str) -> List[Dict[str, Any]]:
    """Generate realistic document data."""
    document_types = [
        'Certificate of Incorporation',
        'Business License',
        'Tax Returns',
        'Financial Statements',
        'Beneficial Ownership Declaration'
    ]
    
    return [{
        "document_id": f"DOC{random.randint(100000, 999999)}",
        "document_type": doc_type,
        "status": "Verified",
        "expiry_date": (datetime.now() + timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d"),
        "last_updated": (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d")
    } for doc_type in random.sample(document_types, random.randint(2, len(document_types)))]

def generate_counterparties(customer_id: str, months: int) -> List[Dict[str, Any]]:
    """Generate realistic counterparty data."""
    num_counterparties = random.randint(3, 8)
    return [{
        "counterparty_id": f"CPT{random.randint(100000, 999999)}",
        "name": generate_business_name(),
        "country": random.choice(list(COUNTRIES.keys())),
        "transaction_count": random.randint(5, 50),
        "total_value": round(Decimal(random.uniform(10000, 1000000)), 2),
        "risk_score": random.randint(20, 90)
    } for _ in range(num_counterparties)]

def generate_touchpoints(customer_id: str, months: int) -> List[Dict[str, Any]]:
    """Generate realistic customer touchpoint data."""
    touchpoint_types = [
        'Account Review',
        'Document Update',
        'Risk Assessment',
        'Customer Interview',
        'Site Visit'
    ]
    
    num_touchpoints = random.randint(2, 6)
    return [{
        "touchpoint_id": f"TP{random.randint(100000, 999999)}",
        "type": random.choice(touchpoint_types),
        "date": (datetime.now() - timedelta(days=random.randint(0, months * 30))).strftime("%Y-%m-%d"),
        "outcome": random.choice(['Satisfactory', 'Needs Follow-up', 'Escalated']),
        "conducted_by": f"RM{random.randint(1000, 9999)}"
    } for _ in range(num_touchpoints)]

def generate_business_locations(customer_id: str) -> List[Dict[str, Any]]:
    """Generate realistic business location data."""
    locations = [
        {'city': 'New York', 'country': 'US', 'type': 'Headquarters'},
        {'city': 'London', 'country': 'UK', 'type': 'Branch Office'},
        {'city': 'Singapore', 'country': 'SG', 'type': 'Regional Office'},
        {'city': 'Dubai', 'country': 'AE', 'type': 'Sales Office'}
    ]
    return random.sample(locations, random.randint(1, len(locations)))

def generate_document_summary(customer_id: str) -> Dict[str, Any]:
    """Generate document summary from an AML perspective."""
    risk_levels = ["LOW", "MEDIUM", "HIGH"]
    findings = [
        "Multiple address changes in short period",
        "Incomplete documentation",
        "Unusual business structure",
        "High-risk jurisdiction connections"
    ]
    recommendations = [
        "Request additional identification documents",
        "Conduct enhanced due diligence",
        "Schedule customer interview",
        "Review transaction patterns"
    ]
    
    base_summary = {
        "risk_level": random.choice(risk_levels),
        "key_findings": random.sample(findings, k=random.randint(1, len(findings))),
        "recommendations": random.sample(recommendations, k=random.randint(1, len(recommendations)))
    }
    
    # Add the metrics from our previous implementation
    base_summary.update({
        "total_documents": random.randint(5, 15),
        "verified_documents": random.randint(3, 10),
        "expired_documents": random.randint(0, 2),
        "missing_critical_documents": random.randint(0, 1),
        "last_verification_date": (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d"),
        "next_review_date": (datetime.now() + timedelta(days=random.randint(30, 180))).strftime("%Y-%m-%d")
    })
    
    return base_summary

def generate_transaction_summary(customer_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Generate transaction summary with both statistical and categorical breakdowns."""
    # Get the base summary from our previous implementation
    base_summary = {
        "total_transactions": random.randint(50, 200),
        "total_value": round(Decimal(random.uniform(100000, 5000000)), 2),
        "average_transaction_size": round(Decimal(random.uniform(5000, 50000)), 2),
        "high_risk_transactions": random.randint(0, 5),
        "by_type": {
            "Wire Transfer": random.randint(10, 50),
            "ACH Credit": random.randint(20, 80),
            "ACH Debit": random.randint(20, 80),
            "Check Deposit": random.randint(5, 20)
        },
        "by_country": {
            "US": random.randint(30, 100),
            "UK": random.randint(10, 30),
            "SG": random.randint(5, 15),
            "AE": random.randint(0, 10)
        }
    }
    
    # Add period information
    base_summary.update({
        "period_start": start_date.date().isoformat(),
        "period_end": end_date.date().isoformat(),
    })
    
    return base_summary

def generate_alert(customer_id: str) -> Dict[str, Any]:
    """Generate a single alert."""
    alert_types = ["SUSPICIOUS_ACTIVITY", "LARGE_TRANSACTION", "PATTERN_DEVIATION"]
    statuses = ["OPEN", "CLOSED", "UNDER_REVIEW"]
    
    return {
        "id": str(uuid.uuid4()),
        "date_created": (datetime.now() - timedelta(days=random.randint(1, 180))).isoformat(),
        "type": random.choice(alert_types),
        "status": random.choice(statuses),
        "risk_score": round(random.uniform(0, 100), 2),
        "case_id": str(uuid.uuid4()) if random.random() > 0.3 else None
    }

def generate_alerts(customer_id: str, count: int = 3) -> List[Dict[str, Any]]:
    """Generate multiple alerts."""
    return [generate_alert(customer_id) for _ in range(count)]

def generate_document(customer_id: str) -> Dict[str, Any]:
    """Generate a single document."""
    doc_types = ["ID_VERIFICATION", "PROOF_OF_ADDRESS", "BANK_STATEMENT", "TAX_RETURN"]
    return {
        "id": str(uuid.uuid4()),
        "type": random.choice(doc_types),
        "date_created": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
        "content": f"Sample document content for customer {customer_id}"
    }

def generate_documents(customer_id: str, count: int = 5) -> List[Dict[str, Any]]:
    """Generate multiple documents."""
    return [generate_document(customer_id) for _ in range(count)]

def generate_transaction(customer_id: str, date: Optional[datetime] = None) -> Dict[str, Any]:
    """Generate a single transaction with more realistic data."""
    if date is None:
        date = datetime.now() - timedelta(days=random.randint(0, 180))
    
    amount = round(Decimal(random.uniform(1000, 1000000)), 2)
    
    return {
        "id": str(uuid.uuid4()),
        "date": date.isoformat(),
        "amount": amount,
        "currency": random.choice(["USD", "EUR", "GBP"]),
        "type": random.choice(TRANSACTION_TYPES),
        "status": random.choice(["COMPLETED", "PENDING", "FAILED"]),
        "counterparty": {
            "id": str(uuid.uuid4()),
            "name": generate_business_name(),
            "country": random.choice(list(COUNTRIES.keys()))
        }
    }

def generate_outlier_analysis(transaction_id: str, analysis_type: str) -> Dict[str, Any]:
    """Generate transaction outlier analysis with statistical calculations."""
    amounts = [random.uniform(1000, 100000) for _ in range(100)]
    target_amount = random.uniform(1000, 100000)
    
    mean = statistics.mean(amounts)
    std_dev = statistics.stdev(amounts)
    z_score = (target_amount - mean) / std_dev
    is_outlier = abs(z_score) > 2
    
    factors = [
        "Amount significantly higher than average",
        "Unusual timing of transaction",
        "Multiple transactions in short period",
        "Unusual counterparty location"
    ]
    
    return {
        "transaction_id": transaction_id,
        "is_outlier": is_outlier,
        "confidence_score": round(random.uniform(0.5, 1.0), 2),
        "analysis_type": analysis_type,
        "factors": random.sample(factors, k=random.randint(1, len(factors))) if is_outlier else [],
        "statistics": {
            "mean": round(mean, 2),
            "std_dev": round(std_dev, 2),
            "z_score": round(z_score, 2)
        },
        "comparison_metrics": {
            "average_amount": round(Decimal(mean), 2),
            "standard_deviation": round(Decimal(std_dev), 2),
            "z_score": round(z_score, 2)
        },
        "similar_transactions_count": random.randint(5, 50)
    }

def generate_alert_transactions_detail(alert_id: str, include_related: bool = True) -> Dict[str, Any]:
    """Generate detailed transaction data for an alert with both triggering and related transactions."""
    base_date = datetime.now() - timedelta(days=7)
    
    # Transactions that triggered the alert
    triggering_transactions = [
        {
            "transaction_id": f"TXN_TRIG_1_{alert_id[-8:]}",
            "transaction_type": "WIRE_TRANSFER",
            "amount": Decimal("50000.00"),
            "currency": "USD",
            "date": base_date
        },
        {
            "transaction_id": f"TXN_TRIG_2_{alert_id[-8:]}",
            "transaction_type": "WIRE_TRANSFER",
            "amount": Decimal("45000.00"),
            "currency": "USD",
            "date": base_date + timedelta(hours=2)
        }
    ]
    
    # Related transactions from the same time period
    related_transactions = []
    if include_related:
        related_transactions = [
            {
                "transaction_id": f"TXN_REL_1_{alert_id[-8:]}",
                "transaction_type": "CASH_DEPOSIT",
                "amount": Decimal("15000.00"),
                "currency": "USD",
                "date": base_date - timedelta(days=1)
            },
            {
                "transaction_id": f"TXN_REL_2_{alert_id[-8:]}",
                "transaction_type": "WIRE_TRANSFER",
                "amount": Decimal("30000.00"),
                "currency": "USD",
                "date": base_date + timedelta(days=1)
            }
        ]
    
    total_amount = sum(Decimal(str(t["amount"])) for t in triggering_transactions + related_transactions)
    
    return {
        "alert_id": alert_id,
        "alert_type": "Suspicious Transaction Pattern",
        "triggering_transactions": triggering_transactions,
        "related_transactions": related_transactions,
        "total_transaction_count": len(triggering_transactions) + len(related_transactions),
        "total_transaction_amount": round(total_amount, 2),
        "time_period": "Last 30 days"
    }

def generate_scenario_details(scenario_id: str) -> Dict[str, Any]:
    """Generate detailed scenario information with parameters."""
    parameter_types = ["AMOUNT", "COUNT", "DURATION", "PERCENTAGE"]
    
    parameters = []
    for _ in range(random.randint(2, 5)):
        parameters.append({
            "name": f"Parameter_{uuid.uuid4().hex[:8]}",
            "type": random.choice(parameter_types),
            "description": "Parameter description",
            "default_value": str(random.randint(1, 1000))
        })
    
    scenarios = {
        "SCN001": {
            "name": "Large Cash Deposits",
            "description": "Multiple cash deposits just below reporting threshold",
            "risk_level": "HIGH",
            "parameters": {"threshold": 10000, "period": "7 days", "transaction_count": 3}
        },
        "SCN002": {
            "name": "International Wire Transfers",
            "description": "Large wire transfers to high-risk countries",
            "risk_level": "HIGH",
            "parameters": {"threshold": 50000, "countries": list(COUNTRIES.keys())}
        }
    }
    
    base_scenario = scenarios.get(scenario_id, scenarios["SCN001"])
    base_scenario["parameters"].update({"additional_params": parameters})
    
    return base_scenario

def generate_country_risk(country_code: str) -> Dict[str, Any]:
    """Generate country risk assessment."""
    risk_factors = [
        'Regulatory Environment',
        'AML Framework',
        'Political Stability',
        'Economic Sanctions',
        'Tax Haven Status'
    ]
    
    return {
        "country_code": country_code,
        "risk_rating": COUNTRIES.get(country_code, "HIGH"),
        "risk_factors": random.sample(risk_factors, random.randint(1, len(risk_factors))),
        "last_assessment_date": (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d"),
        "next_review_date": (datetime.now() + timedelta(days=random.randint(30, 180))).strftime("%Y-%m-%d")
    }

def generate_pep_counterparties(customer_id: str) -> List[Dict[str, Any]]:
    """Generate politically exposed person counterparty data."""
    pep_positions = [
        'Government Official',
        'Senior Politician',
        'Military Officer',
        'State Enterprise Executive',
        'Diplomatic Representative'
    ]
    
    num_peps = random.randint(0, 3)
    return [{
        "counterparty_id": f"PEP{random.randint(100000, 999999)}",
        "name": generate_business_name(),
        "position": random.choice(pep_positions),
        "country": random.choice(list(COUNTRIES.keys())),
        "risk_score": random.randint(70, 95),
        "transaction_count": random.randint(1, 10)
    } for _ in range(num_peps)]

def generate_subsidiary_info(customer_id: str) -> List[Dict[str, Any]]:
    """Generate subsidiary information."""
    num_subsidiaries = random.randint(1, 5)
    return [{
        "subsidiary_id": f"SUB{random.randint(100000, 999999)}",
        "name": generate_business_name(),
        "ownership_percentage": random.randint(51, 100),
        "country": random.choice(list(COUNTRIES.keys())),
        "annual_revenue": round(Decimal(random.uniform(1000000, 50000000)), 2),
        "employee_count": random.randint(10, 1000),
        "risk_score": random.randint(20, 80)
    } for _ in range(num_subsidiaries)]

def generate_alert_scenarios(customer_id: str) -> List[Dict[str, Any]]:
    """Generate alert scenario data."""
    scenarios = [
        {
            "name": "Large Cash Deposits",
            "threshold": 10000,
            "lookback_period": "7 days"
        },
        {
            "name": "Multiple International Wires",
            "threshold": 50000,
            "lookback_period": "30 days"
        },
        {
            "name": "Structured Transactions",
            "threshold": 9000,
            "lookback_period": "3 days"
        },
        {
            "name": "High-Risk Country Transfers",
            "threshold": 25000,
            "lookback_period": "immediate"
        }
    ]
    return random.sample(scenarios, random.randint(2, len(scenarios)))

def generate_related_customers(counterparty_id: str) -> List[Dict[str, Any]]:
    """Generate related customer data."""
    num_customers = random.randint(2, 6)
    return [{
        "customer_id": f"CUS{random.randint(100000, 999999)}",
        "name": generate_business_name(),
        "relationship_type": random.choice(['Vendor', 'Client', 'Partner']),
        "transaction_count": random.randint(5, 50),
        "total_value": round(Decimal(random.uniform(10000, 1000000)), 2),
        "last_transaction_date": (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d")
    } for _ in range(num_customers)]

def generate_scenario_details(scenario_id: str) -> Dict[str, Any]:
    """Generate scenario details."""
    scenarios = {
        "SCN001": {
            "name": "Large Cash Deposits",
            "description": "Multiple cash deposits just below reporting threshold",
            "risk_level": "HIGH",
            "parameters": {"threshold": 10000, "period": "7 days", "transaction_count": 3}
        },
        "SCN002": {
            "name": "International Wire Transfers",
            "description": "Large wire transfers to high-risk countries",
            "risk_level": "HIGH",
            "parameters": {"threshold": 50000, "countries": list(COUNTRIES.keys())}
        }
    }
    return scenarios.get(scenario_id, scenarios["SCN001"])

def generate_scenario_thresholds(scenario_id: str) -> Dict[str, Any]:
    """Generate scenario threshold data."""
    return {
        "threshold_settings": {
            "amount": round(Decimal(random.uniform(9000, 50000)), 2),
            "frequency": random.randint(3, 10),
            "time_window": f"{random.randint(1, 30)} days"
        },
        "last_updated": (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d"),
        "updated_by": f"ANALYST{random.randint(1000, 9999)}"
    }

def generate_alert_transactions_detail(alert_id: str, include_related: bool) -> Dict[str, Any]:
    """Generate detailed transaction data for an alert."""
    num_triggering = random.randint(1, 3)
    num_related = random.randint(2, 5) if include_related else 0
    
    triggering_transactions = [generate_transaction(f"TRX{random.randint(100000, 999999)}") for _ in range(num_triggering)]
    related_transactions = [generate_transaction(f"TRX{random.randint(100000, 999999)}") for _ in range(num_related)]
    
    total_amount = sum(Decimal(str(t["amount"])) for t in triggering_transactions + related_transactions)
    
    return {
        "alert_id": alert_id,
        "alert_type": "Suspicious Transaction Pattern",
        "triggering_transactions": triggering_transactions,
        "related_transactions": related_transactions,
        "total_transaction_count": len(triggering_transactions) + len(related_transactions),
        "total_transaction_amount": round(total_amount, 2),
        "time_period": "Last 30 days"
    }

def generate_alert_customer_details(alert_id: str) -> Dict[str, Any]:
    """Generate customer details for an alert."""
    return generate_customer(f"CUS{random.randint(100000, 999999)}")

def generate_outlier_analysis(transaction_id: str, analysis_type: str) -> Dict[str, Any]:
    """Generate transaction outlier analysis."""
    return {
        "transaction_id": transaction_id,
        "is_outlier": random.choice([True, False]),
        "confidence_score": random.randint(60, 99),
        "analysis_type": analysis_type,
        "comparison_metrics": {
            "average_amount": round(Decimal(random.uniform(5000, 50000)), 2),
            "standard_deviation": round(Decimal(random.uniform(1000, 10000)), 2),
            "z_score": round(random.uniform(1.5, 4.0), 2)
        },
        "similar_transactions_count": random.randint(5, 50)
    }

def generate_counterparties_risk_assessment(
    customer_id: Optional[str] = None,
    risk_level: Optional[str] = None,
    is_pep: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """Generate counterparty risk assessment data."""
    num_counterparties = random.randint(3, 8)
    risk_levels = ['HIGH', 'MEDIUM', 'LOW']
    
    def generate_counterparty():
        generated_risk = random.choice(risk_levels) if not risk_level else risk_level
        generated_pep = random.choice([True, False]) if is_pep is None else is_pep
        
        return {
            "counterparty_id": f"CPT{random.randint(100000, 999999)}",
            "name": generate_business_name(),
            "risk_level": generated_risk,
            "is_pep": generated_pep,
            "risk_factors": random.sample([
                "High-Risk Country",
                "Complex Ownership Structure",
                "Political Exposure",
                "Negative News",
                "Unusual Transaction Patterns"
            ], random.randint(1, 3)),
            "risk_score": random.randint(20, 95),
            "last_review_date": (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d")
        }
    
    counterparties = [generate_counterparty() for _ in range(num_counterparties)]
    return counterparties

def generate_transaction_metrics(customer_id: str, months: int = 6) -> dict:
    """Generate comprehensive transaction metrics."""
    return {
        "total_debits": 150,
        "total_credits": 75,
        "debit_metrics": {
            "average": 5000.00,
            "std_dev": 1200.00,
            "velocity_per_day": 0.82
        },
        "credit_metrics": {
            "average": 4800.00,
            "std_dev": 950.00,
            "velocity_per_day": 0.41
        },
        "growth_rate": {
            "month_over_month": 0.15,
            "transaction_volume": 0.08
        }
    }

def generate_high_risk_metrics(customer_id: str, months: int = 6) -> dict:
    """Generate metrics for high-risk transactions."""
    return {
        "high_risk_geography_transactions": {
            "count": 45,
            "total_value": 250000.00,
            "average": 5555.56,
            "std_dev": 1200.00
        },
        "high_risk_institution_transfers": {
            "count": 30,
            "total_value": 180000.00,
            "average": 6000.00,
            "std_dev": 1500.00
        }
    }

def generate_transaction_patterns(customer_id: str, months: int = 6) -> dict:
    """Generate analysis of transaction patterns."""
    return {
        "top_channels": [
            {"channel": "WIRE", "count": 45, "total_value": 225000.00},
            {"channel": "ACH", "count": 30, "total_value": 150000.00}
        ],
        "status_distribution": {
            "COMPLETED": 85,
            "PENDING": 10,
            "FAILED": 5
        },
        "peak_activity": {
            "day_of_week": "WEDNESDAY",
            "hour_of_day": 14
        },
        "recurring_patterns": {
            "weekly_transfers": 3,
            "monthly_payments": 2
        },
        "avg_time_between_transactions": "3.5 days"
    }

def generate_transaction_analysis(customer_id: str, months: int = 6) -> dict:
    """Generate detailed transaction analysis."""
    return {
        "geographic_distribution": {
            "domestic": {
                "count": 120,
                "total_value": 600000.00
            },
            "international": {
                "count": 30,
                "total_value": 150000.00
            }
        },
        "fees": {
            "total": 2500.00,
            "average": 16.67,
            "by_type": {
                "WIRE": 1800.00,
                "ACH": 700.00
            }
        },
        "failed_transactions": {
            "count": 5,
            "total_value": 25000.00,
            "reasons": {
                "INSUFFICIENT_FUNDS": 3,
                "INVALID_ACCOUNT": 2
            }
        },
        "highest_transactions": [
            {
                "id": "TXN_123",
                "amount": 50000.00,
                "date": "2024-01-01T10:00:00Z"
            }
        ]
    }

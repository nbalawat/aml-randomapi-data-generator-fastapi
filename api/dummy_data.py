from datetime import datetime, timedelta
import random
import uuid
from typing import List, Dict, Any, Optional
import statistics
from decimal import Decimal

def generate_document(customer_id: str) -> Dict[str, Any]:
    doc_types = ["ID_VERIFICATION", "PROOF_OF_ADDRESS", "BANK_STATEMENT", "TAX_RETURN"]
    return {
        "id": str(uuid.uuid4()),
        "type": random.choice(doc_types),
        "date_created": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
        "content": f"Sample document content for customer {customer_id}"
    }

def generate_documents(customer_id: str, count: int = 5) -> List[Dict[str, Any]]:
    return [generate_document(customer_id) for _ in range(count)]

def generate_document_summary(customer_id: str) -> Dict[str, Any]:
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
    
    return {
        "risk_level": random.choice(risk_levels),
        "key_findings": random.sample(findings, k=random.randint(1, len(findings))),
        "recommendations": random.sample(recommendations, k=random.randint(1, len(recommendations)))
    }

def generate_transaction(customer_id: str, date: Optional[datetime] = None) -> Dict[str, Any]:
    if date is None:
        date = datetime.now() - timedelta(days=random.randint(0, 180))
    
    return {
        "id": str(uuid.uuid4()),
        "date": date.isoformat(),
        "amount": round(random.uniform(100, 1000000), 2),
        "currency": random.choice(["USD", "EUR", "GBP"]),
        "type": random.choice(["WIRE", "ACH", "CHECK", "CASH"]),
        "status": random.choice(["COMPLETED", "PENDING", "FAILED"]),
        "counterparty": {
            "id": str(uuid.uuid4()),
            "name": f"Company_{uuid.uuid4().hex[:8]}",
            "country": random.choice(["US", "GB", "DE", "FR", "JP"])
        }
    }

def generate_transaction_summary(
    customer_id: str,
    start_date: datetime,
    end_date: datetime
) -> Dict[str, Any]:
    transaction_types = ["WIRE", "ACH", "CHECK", "CASH"]
    currencies = ["USD", "EUR", "GBP"]
    
    summaries = []
    for tx_type in transaction_types:
        summaries.append({
            "type": tx_type,
            "count": random.randint(5, 100),
            "total_amount": round(random.uniform(1000, 1000000), 2),
            "currency": random.choice(currencies)
        })
    
    return {
        "period_start": start_date.date().isoformat(),
        "period_end": end_date.date().isoformat(),
        "summaries": summaries
    }

def generate_alert(customer_id: str) -> Dict[str, Any]:
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
    return [generate_alert(customer_id) for _ in range(count)]

def generate_relationship(customer_id: str) -> Dict[str, Any]:
    relationship_types = ["OWNER", "DIRECTOR", "BENEFICIAL_OWNER", "AUTHORIZED_SIGNER"]
    entity_types = ["INDIVIDUAL", "CORPORATION", "PARTNERSHIP"]
    strengths = ["WEAK", "MODERATE", "STRONG"]
    
    return {
        "id": str(uuid.uuid4()),
        "type": random.choice(relationship_types),
        "related_entity": {
            "id": str(uuid.uuid4()),
            "name": f"Entity_{uuid.uuid4().hex[:8]}",
            "type": random.choice(entity_types)
        },
        "relationship_strength": random.choice(strengths)
    }

def generate_relationships(customer_id: str, count: int = 5) -> List[Dict[str, Any]]:
    return [generate_relationship(customer_id) for _ in range(count)]

def generate_counterparties(customer_id: str, months: int = 6) -> List[Dict[str, Any]]:
    counterparties = []
    for _ in range(random.randint(3, 10)):
        counterparties.append({
            "id": str(uuid.uuid4()),
            "name": f"Company_{uuid.uuid4().hex[:8]}",
            "country": random.choice(["US", "GB", "DE", "FR", "JP"]),
            "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "transaction_count": random.randint(1, 100),
            "total_amount": round(random.uniform(10000, 1000000), 2),
            "currency": random.choice(["USD", "EUR", "GBP"])
        })
    return counterparties

def generate_touchpoints(customer_id: str, months: int = 6) -> List[Dict[str, Any]]:
    touchpoint_types = ["BRANCH_VISIT", "PHONE_CALL", "EMAIL", "ONLINE_BANKING"]
    channels = ["IN_PERSON", "PHONE", "DIGITAL", "ATM"]
    locations = ["NEW_YORK", "LONDON", "TOKYO", "SINGAPORE"]
    
    touchpoints = []
    for _ in range(random.randint(5, 15)):
        touchpoints.append({
            "id": str(uuid.uuid4()),
            "date": (datetime.now() - timedelta(days=random.randint(1, months * 30))).isoformat(),
            "type": random.choice(touchpoint_types),
            "channel": random.choice(channels),
            "description": "Customer interaction details",
            "location": random.choice(locations)
        })
    return touchpoints

def generate_business_locations(customer_id: str) -> List[Dict[str, Any]]:
    countries = ["US", "GB", "DE", "FR", "JP", "SG", "HK"]
    cities = ["New York", "London", "Tokyo", "Singapore", "Hong Kong"]
    activity_types = ["RETAIL", "WHOLESALE", "MANUFACTURING", "SERVICES"]
    
    locations = []
    for _ in range(random.randint(1, 5)):
        locations.append({
            "country": random.choice(countries),
            "city": random.choice(cities),
            "activity_type": random.choice(activity_types),
            "transaction_volume": round(random.uniform(100000, 10000000), 2),
            "risk_score": round(random.uniform(0, 100), 2)
        })
    return locations

def generate_country_risk(country_code: str) -> Dict[str, Any]:
    risk_factors = [
        "Weak AML regulations",
        "High corruption index",
        "Limited regulatory oversight",
        "Significant informal economy",
        "Known tax haven"
    ]
    
    return {
        "country_code": country_code,
        "risk_rating": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "factors": random.sample(risk_factors, k=random.randint(1, len(risk_factors))),
        "last_updated": (datetime.now() - timedelta(days=random.randint(1, 30))).date().isoformat()
    }

def generate_pep_counterparties(customer_id: str) -> List[Dict[str, Any]]:
    pep_types = ["POLITICIAN", "DIPLOMAT", "MILITARY", "STATE_OWNED_ENTITY"]
    jurisdictions = ["US", "GB", "EU", "UN"]
    
    counterparties = []
    for _ in range(random.randint(0, 5)):
        counterparties.append({
            "id": str(uuid.uuid4()),
            "name": f"PEP_{uuid.uuid4().hex[:8]}",
            "pep_type": random.choice(pep_types),
            "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "relationship": random.choice(["DIRECT", "INDIRECT"]),
            "jurisdiction": random.choice(jurisdictions)
        })
    return counterparties

def generate_subsidiary_info(customer_id: str) -> List[Dict[str, Any]]:
    subsidiaries = []
    for _ in range(random.randint(1, 5)):
        transactions = [generate_transaction(customer_id) for _ in range(random.randint(3, 10))]
        subsidiaries.append({
            "id": str(uuid.uuid4()),
            "name": f"Subsidiary_{uuid.uuid4().hex[:8]}",
            "ownership_percentage": round(random.uniform(51, 100), 2),
            "transactions": transactions
        })
    return subsidiaries

def generate_alert_scenarios(customer_id: str) -> List[Dict[str, Any]]:
    scenario_names = [
        "Large Cash Deposits",
        "Rapid Movement of Funds",
        "Multiple Small Transactions",
        "High-Risk Country Transfers"
    ]
    
    scenarios = []
    for name in scenario_names:
        scenarios.append({
            "id": str(uuid.uuid4()),
            "name": name,
            "description": f"Scenario to detect {name.lower()}",
            "risk_category": random.choice(["HIGH", "MEDIUM", "LOW"]),
            "threshold_count": random.randint(1, 5),
            "enabled": random.choice([True, False])
        })
    return scenarios

def generate_related_customers(counterparty_id: str) -> List[Dict[str, Any]]:
    customers = []
    for _ in range(random.randint(1, 10)):
        customers.append({
            "id": str(uuid.uuid4()),
            "name": f"Customer_{uuid.uuid4().hex[:8]}",
            "relationship_type": random.choice(["DIRECT", "INDIRECT"]),
            "transaction_count": random.randint(1, 100),
            "last_transaction_date": (datetime.now() - timedelta(days=random.randint(1, 180))).date().isoformat()
        })
    return customers

def generate_scenario_details(scenario_id: str) -> Dict[str, Any]:
    parameter_types = ["AMOUNT", "COUNT", "DURATION", "PERCENTAGE"]
    
    parameters = []
    for _ in range(random.randint(2, 5)):
        parameters.append({
            "name": f"Parameter_{uuid.uuid4().hex[:8]}",
            "type": random.choice(parameter_types),
            "description": "Parameter description",
            "default_value": str(random.randint(1, 1000))
        })
    
    return {
        "id": scenario_id,
        "name": f"Scenario_{scenario_id}",
        "description": "Detailed scenario description",
        "parameters": parameters
    }

def generate_scenario_thresholds(scenario_id: str) -> List[Dict[str, Any]]:
    units = ["USD", "COUNT", "DAYS", "PERCENTAGE"]
    
    thresholds = []
    for _ in range(random.randint(2, 5)):
        thresholds.append({
            "id": str(uuid.uuid4()),
            "name": f"Threshold_{uuid.uuid4().hex[:8]}",
            "value": round(random.uniform(100, 1000000), 2),
            "unit": random.choice(units),
            "description": "Threshold description",
            "last_updated": (datetime.now() - timedelta(days=random.randint(1, 30))).date().isoformat()
        })
    return thresholds

def generate_alert_transactions(alert_id: str) -> Dict[str, Any]:
    alert_txns = [generate_transaction("") for _ in range(random.randint(1, 5))]
    historical_txns = [generate_transaction("") for _ in range(random.randint(5, 20))]
    
    return {
        "alert_id": alert_id,
        "alert_transactions": alert_txns,
        "historical_transactions": historical_txns
    }

def generate_outlier_analysis(
    transaction_id: str,
    analysis_type: str
) -> Dict[str, Any]:
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
        }
    }

def generate_alert_customer_details(alert_id: str) -> dict:
    """Generate dummy customer details and accounts for a given alert ID."""
    # In a real implementation, we would:
    # 1. Look up the alert by alert_id
    # 2. Get the associated customer_id
    # 3. Fetch customer details and all their accounts
    
    return {
        "customer_id": f"CUST_{alert_id[-8:]}",
        "name": "John Smith",
        "risk_rating": "HIGH",
        "country": "US",
        "created_at": datetime.now(),
        "accounts": [
            {
                "account_id": f"ACC_1_{alert_id[-8:]}",
                "account_type": "CHECKING",
                "currency": "USD",
                "status": "ACTIVE",
                "opened_date": datetime.now() - timedelta(days=365),
                "closed_date": None
            },
            {
                "account_id": f"ACC_2_{alert_id[-8:]}",
                "account_type": "SAVINGS",
                "currency": "USD",
                "status": "ACTIVE",
                "opened_date": datetime.now() - timedelta(days=180),
                "closed_date": None
            },
            {
                "account_id": f"ACC_3_{alert_id[-8:]}",
                "account_type": "INVESTMENT",
                "currency": "EUR",
                "status": "CLOSED",
                "opened_date": datetime.now() - timedelta(days=730),
                "closed_date": datetime.now() - timedelta(days=30)
            }
        ]
    }

def generate_alert_transactions_detail(alert_id: str, include_related: bool = True) -> dict:
    """Generate dummy alert transactions data."""
    # In a real implementation, we would:
    # 1. Look up the alert by alert_id
    # 2. Get the triggering transactions
    # 3. Find related transactions from the same time period
    # 4. Calculate transaction statistics
    
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
                "amount": Decimal("25000.00"),
                "currency": "USD",
                "date": base_date - timedelta(days=2)
            },
            {
                "transaction_id": f"TXN_REL_3_{alert_id[-8:]}",
                "transaction_type": "ACH_CREDIT",
                "amount": Decimal("10000.00"),
                "currency": "USD",
                "date": base_date + timedelta(days=1)
            }
        ]
    
    # Calculate totals
    all_transactions = triggering_transactions + related_transactions
    total_amount = sum(Decimal(str(t["amount"])) for t in all_transactions)
    
    return {
        "alert_id": alert_id,
        "alert_type": "STRUCTURED_TRANSACTIONS",
        "triggering_transactions": triggering_transactions,
        "related_transactions": related_transactions,
        "total_transaction_count": len(all_transactions),
        "total_transaction_amount": total_amount,
        "time_period": f"{min(t['date'] for t in all_transactions).date()} to {max(t['date'] for t in all_transactions).date()}"
    }

def generate_counterparties_risk_assessment(
    customer_id: Optional[str] = None,
    risk_level: Optional[str] = None,
    is_pep: Optional[bool] = None
) -> dict:
    """Generate dummy risk assessment data for counterparties."""
    risk_levels = ["HIGH", "MEDIUM", "LOW"]
    business_types = ["CORPORATION", "INDIVIDUAL", "GOVERNMENT", "NGO"]
    countries = ["US", "UK", "FR", "DE", "CN", "RU"]
    pep_positions = [
        "Senior Government Official",
        "Diplomat",
        "Military Officer",
        "State Enterprise Executive",
        None
    ]
    
    counterparties = []
    for i in range(10):  # Generate 10 sample counterparties
        # Generate base counterparty data
        cp_risk_level = random.choice(risk_levels)
        cp_is_pep = random.random() < 0.3  # 30% chance of being PEP
        
        # Apply filters
        if risk_level and cp_risk_level != risk_level:
            continue
        if is_pep is not None and cp_is_pep != is_pep:
            continue
            
        counterparty = {
            "counterparty_id": f"CP_{i:03d}",
            "name": f"Counterparty {i}",
            "business_type": random.choice(business_types),
            "country": random.choice(countries),
            "risk_assessment": {
                "overall_risk_level": cp_risk_level,
                "risk_factors": {
                    "country_risk": random.uniform(0, 1),
                    "business_type_risk": random.uniform(0, 1),
                    "transaction_pattern_risk": random.uniform(0, 1),
                    "adverse_media_risk": random.uniform(0, 1)
                }
            },
            "pep_information": {
                "is_pep": cp_is_pep,
                "position": random.choice(pep_positions) if cp_is_pep else None,
                "jurisdiction": random.choice(countries) if cp_is_pep else None,
                "screening_date": datetime.now().isoformat() if cp_is_pep else None
            },
            "transaction_summary": {
                "total_transactions": random.randint(10, 100),
                "total_amount": round(random.uniform(10000, 1000000), 2),
                "last_transaction_date": datetime.now() - timedelta(days=random.randint(1, 30))
            },
            "last_review": {
                "date": datetime.now() - timedelta(days=random.randint(1, 90)),
                "reviewed_by": "John Doe",
                "next_review_date": datetime.now() + timedelta(days=random.randint(30, 180))
            }
        }
        
        # Add customer-specific data if customer_id is provided
        if customer_id:
            counterparty["customer_relationship"] = {
                "customer_id": customer_id,
                "relationship_type": random.choice(["VENDOR", "CLIENT", "PARTNER"]),
                "relationship_start_date": datetime.now() - timedelta(days=random.randint(100, 1000))
            }
        
        counterparties.append(counterparty)
    
    return {
        "total_count": len(counterparties),
        "filters_applied": {
            "customer_id": customer_id,
            "risk_level": risk_level,
            "is_pep": is_pep
        },
        "counterparties": counterparties
    }

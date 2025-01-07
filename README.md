# AML Analysis API

## Overview
The AML Analysis API is a FastAPI-based service that provides endpoints for Anti-Money Laundering (AML) analysis and data retrieval. It offers comprehensive functionality for analyzing customer documents, transactions, and generating AML-related insights.

## Features
- Document analysis and retrieval
- Transaction monitoring and outlier detection
- Customer risk assessment
- PEP (Politically Exposed Person) screening
- Relationship mapping
- Alert management and investigation

## Tech Stack
- FastAPI: Modern, fast web framework for building APIs
- Pydantic: Data validation using Python type annotations
- UV: Fast Python package installer and resolver
- SQLAlchemy: SQL toolkit and ORM

## Getting Started

### Installation and Setup
1. Sync dependencies using UV:
```bash
uv sync
```

2. Run the FastAPI application:
```bash
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://0.0.0.0:8000`. Access the interactive API documentation at `http://0.0.0.0:8000/docs`.

### API Endpoints

### Documents
- `GET /api/v1/documents/{customer_id}`: Retrieve customer documents
- `GET /api/v1/documents/{document_id}/summary`: Get document summary

### Transactions
- `GET /api/v1/transactions/{customer_id}`: Get customer transactions
- `GET /api/v1/transactions/outliers/{customer_id}`: Get transaction outlier analysis

### Alerts
- `GET /api/v1/alerts/{customer_id}`: Retrieve customer alerts
- `GET /api/v1/alerts/{alert_id}/details`: Get detailed alert information

### Alert Investigation Endpoints

#### Get Alert Customer Details
```http
GET /api/v1/alerts/{alert_id}/customer
```
Returns comprehensive customer information and all associated accounts for a given alert. This endpoint is useful for:
- Quick access to customer profile during alert investigation
- Understanding customer's account portfolio
- Assessing overall customer risk profile

**Response includes:**
- Customer identification and risk information
- All accounts (active and closed)
- Account types, currencies, and status
- Account opening/closing dates

#### Get Alert Transactions
```http
GET /api/v1/alerts/{alert_id}/transactions
```
Retrieves all transactions related to an alert, including both triggering and related transactions. This endpoint helps in:
- Understanding the full context of suspicious activity
- Identifying transaction patterns
- Analyzing related transactions in the same time period

**Query Parameters:**
- `include_related` (boolean): Include additional related transactions

**Response includes:**
- Transactions that triggered the alert
- Related transactions from the same time period
- Transaction statistics and summary
- Total transaction count and amounts
- Time period covered

### Risk Assessment
- `GET /api/v1/risk/{customer_id}`: Get customer risk assessment
- `GET /api/v1/risk/country/{country_code}`: Get country risk information

### Relationships
- `GET /api/v1/relationships/{customer_id}`: Get customer relationships
- `GET /api/v1/relationships/graph/{customer_id}`: Get relationship graph data

## Authentication
The API uses Bearer token authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Error Handling
The API uses standard HTTP status codes and returns detailed error messages in JSON format:
```json
{
    "error": "string",
    "detail": "string",
    "status_code": 400
}
```

## Rate Limiting
API requests are rate-limited to ensure fair usage. The current limits are:
- 100 requests per minute per IP address
- 1000 requests per hour per API key

## Development

### Development Setup

For development, you'll want to install additional dependencies:

```bash
uv pip install -e ".[dev]"
```

This will install development tools like:
- pytest for testing
- black for code formatting
- isort for import sorting
- mypy for type checking
- ruff for linting

### Running Tests

```bash
uv run pytest
```

### Code Quality

Format your code:
```bash
uv run black .
uv run isort .
```

Run type checking:
```bash
uv run mypy .
```

Run linting:
```bash
uv run ruff .
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support
For support and questions, please open an issue in the repository.

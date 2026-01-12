# CardFolio 🃏

_A Magic: The Gathering collection & investment tracker_

CardFolio is a **work-in-progress backend-focused web application** built with Django to track, manage, and analyze Magic: The Gathering card collections as **financial assets**.

This project is part of my **personal portfolio** and learning journey as a backend / full-stack developer.  
Its purpose is not just to work, but to demonstrate **correct domain modeling**, **data integrity**, **testing practices**, and **real-world backend patterns** such as data pipelines and batch processing.

---

## 🚧 Project Status

⚠️ **Deployed - In active development**

[Cardfolio](cardfolio.ap-southeast-2.elasticbeanstalk.com) / cardfolio.ap-southeast-2.elasticbeanstalk.com

Core functionality is implemented and stable, but the project is still evolving.  
Expect refactors, new features, and architectural improvements as the system grows.

This is intentional — the repository reflects how real projects evolve over time.

---

## ✨ Current Features

- User authentication
- Add cards by **exact printing** (set code + collector number)
- **Foil and Non-Foil** modeled as separate entities
- Integration with the **Scryfall API**
- User collections with quantities
- Buy & Sell transactions (historical record)
- Portfolio metrics:
  - Total invested
  - Total earned
  - Current portfolio value
  - Unrealized profit / loss
  - ROI
- Pagination and search
- Dashboard with financial insights

---

## 🔄 Data Pipeline – Price Synchronization

CardFolio includes a **custom data pipeline** to keep card prices up to date using **Scryfall bulk data**.

Instead of making API calls per card (slow, rate-limited, and inefficient), the application:

- Fetches Scryfall bulk metadata
- Downloads the `default_cards` JSON file
- Processes data in memory
- Updates **only the cards that exist in the local database**

This mirrors real-world backend ingestion patterns.

### Why bulk data?

- Avoids API rate limits
- Reduces network overhead
- Scales efficiently
- Matches production-grade data ingestion workflows

### Pipeline steps

1. Fetch bulk metadata from Scryfall
2. Download the bulk JSON file
3. Index cards by `scryfall_id` for **O(1)** lookups
4. Update local prices (foil / non-foil aware)
5. Apply changes atomically using database transactions

### Orchestration

The pipeline is executed via a **custom Django management command**:

```bash
python manage.py sync_scryfall_prices
```

This allows the pipeline to be:

- Run manually
- Scheduled (cron, ECS task, CI job)
- Executed independently of web traffic
- This mirrors real backend batch job orchestration.

## Key Backend Concepts Applied

- Batch processing
- In-memory indexing for O(1) lookups
- Atomic database transactions
- Separation of concerns
- Fail-safe execution

## Testing Strategy

This project uses pytest with a clear separation between unit tests and integration tests.

Unit tests

- Test pure business logic
- Minimal database usage (validation-level only)
- No external services
- External dependencies are mocked

Integration tests

- Use the real database
- Validate ORM behavior and constraints
- Test transactional behavior
- External APIs are mocked (never called)

Fixtures & factories

- Reusable fixtures live in conftest.py, including:
- Users
- Cards
- Fake Scryfall payloads

This keeps tests:

- readable
- maintainable
- expressive
- fast

Run all tests:

```bash
pytest
```

## Tech Stack

- Python
- Django
- PostgreSQL
- Django ORM
- Django Templates
- Pytest
- Scryfall API
- Git & GitHub

## Environment Variables

Create a .env file in the project root:

- DB_NAME=""
- DB_USER=""
- DB_PASSWORD=""
- DB_HOST="localhost"
- DB_PORT="5432"

- SECRET_KEY="any-secret-key"

- APP_HOST="127.0.0.1"
- IS_DEVELOPMENT="TRUE"

## What I Learned Building This Project

This project helped me deeply understand:

- Backend fundamentals
- Domain modeling beyond CRUD
- Data integrity with constraints
- Transactions and atomic operations
- Separation of concerns
- Data engineering concepts
- Batch data ingestion
- Bulk file processing
- In-memory indexing for performance
- Avoiding N+1 and per-record API calls
- Thinking in pipelines, not requests
- Testing mindset
- Writing tests that expose design flaws
- Using tests to guide refactors
- Differentiating unit vs integration tests
- Treating tests as executable documentation
- Real-world engineering thinking
- Modeling financial transactions correctly
- Avoiding lossy updates
- Designing systems that evolve safely
- Understanding trade-offs, not just syntax

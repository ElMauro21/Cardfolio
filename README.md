# CardFolio 🃏

_A personal Magic: The Gathering collection tracker built with Django_

CardFolio is a **work-in-progress web application** designed to help Magic: The Gathering players **track, manage, and analyze** their card collections.

This project is part of my personal portfolio and learning journey as a backend / full-stack developer.  
The goal is not only to build a functional app, but to model the domain correctly (prints, finishes, prices, ownership) and apply real-world backend practices.

---

## 🚧 Project Status

⚠️ **In active development**

Core features are working, but the project is still evolving.  
Expect breaking changes, refactors, and new functionality.

---

## ✨ Current Features

- User authentication
- Add cards by **exact printing** (set code + collector number)
- Support for **Foil and Non-Foil** versions as distinct cards
- Integration with the **Scryfall API**
- Store purchase price and market price
- User collections with quantities
- Pagination and search
- Basic collection insights (e.g. most expensive card)

---

## 🧠 Design Philosophy

- **One Card = One exact printing**
- Foil and Non-Foil are modeled as **separate entities**
- Data integrity enforced with database constraints
- External API logic isolated from business logic
- Simple UI, focus on backend correctness first

This project prioritizes **correct domain modeling** over shortcuts.

---

## 🛠 Tech Stack

- **Python**
- **Django**
- **PostgreSQL**
- Django Templates
- Git & GitHub
- Scryfall API

---

## 🔐 Environment Variables

CardFolio uses environment variables for configuration.  
Create a `.env` file in the project root with the following values:

```env
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_HOST="localhost"
DB_PORT="5432"

SECRET_KEY="" -> Up to you

APP_HOST="127.0.0.1"
IS_DEVELOPMENT="TRUE"
```

---

## 🧪 Testing

This project uses **pytest** with a clear separation between **unit tests** and **integration tests**, following backend best practices.

---

### 🔹 Test types

**Unit tests**

- Test pure functions and business logic in isolation
- No database
- No external services
- External dependencies are mocked

**Integration tests**

- Test real interaction between business logic and the database
- Django ORM and constraints are used for real
- External APIs are mocked (e.g. Scryfall)

---

### 🏭 Factories & fixtures

Reusable test data is provided via **pytest fixtures** defined in `conftest.py`.

Examples:

- `fake_scryfall_card_data` generates minimal valid Scryfall-like payloads
- Tests override only the fields relevant to each scenario

This approach keeps tests:

- readable
- maintainable
- free of duplicated setup code

---

### ▶️ Running tests

Run **all tests**:

```bash
pytest
```

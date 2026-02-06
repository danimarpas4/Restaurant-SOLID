# 🏛️ Decentralized Restaurant Ledger Architecture (PoC)

> **Architectural Proof of Concept** demonstrating SOLID principles, Atomic State Transitions, and Immutable Audit Trails using Python & SQLAlchemy.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)]()

## 📋 Abstract

This repository implements a modular backend system for managing transactional assets (Orders) and inventory states (Products). Unlike traditional CRUD applications, this project treats data changes as **state transitions**, ensuring data integrity through atomic commits and enforcing strict separation of concerns (SoC).

Designed with scalability in mind, the system mimics the reliability of distributed ledger technologies by implementing:
* **Immutable Reporting:** PDF generation acting as off-chain snapshots.
* **Atomic Transactions:** All-or-nothing database commits to prevent state inconsistencies.
* **Governance Logic:** Decoupled business rules (e.g., Discounts) applied as external state modifiers.

## 🏗️ Technical Architecture

The codebase strictly adheres to **SOLID Principles** to ensure maintainability and extensibility.

| Module | Responsibility (The "Why") | Architectural Pattern |
| :--- | :--- | :--- |
| `producto.py` | **Asset Definition**. Defines the schema and immutable properties of system assets. | *Domain Model / ORM* |
| `pedido.py` | **Transaction Layer**. Manages state aggregation and relational integrity between entities. | *Aggregates* |
| `api.py` | **Gateway Interface**. Exposes system state to external consumers via read-only endpoints. | *Facade / DTO* |
| `reporte.py` | **Audit Trail**. Generates immutable artifacts (PDFs) verifying system history. | *Adapter* |
| `main.py` | **Orchestrator**. Manages the lifecycle of the application and dependency injection. | *Composition Root* |

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* MySQL Server (Local or Cloud instance)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/danimarpas4/restaurant-ledger-architecture.git](https://github.com/danimarpas4/restaurant-ledger-architecture.git)
    cd restaurant-ledger-architecture
    ```

2.  **Initialize Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install sqlalchemy pymysql reportlab python-dotenv cryptography
    ```

4.  **Environment Configuration:**
    Create a `.env` file in the root directory to secure your credentials:
    ```env
    DB_PASSWORD=your_secure_password
    ```

### Execution

Run the main node entry point to simulate the transaction flow:

```bash
python main.py
```

*The system will perform a genesis block simulation (creating initial assets), process a transaction batch, and generate an audit report.*

## 🧩 Key Features Implementation

### Atomic State Management
We utilize SQLAlchemy's `session` scope to ensure atomicity. Operations are staged and committed only when the full transaction context is valid.

```python
# Atomic Commit Pattern
try:
    session.add(order)
    order.calculate_total() # State aggregation
    session.commit()        # Persistence
except Exception:
    session.rollback()      # Revert to previous consistent state
```

### Immutable Audit (PDF Generation)
The `reporte.py` module generates a cryptographically verifiable-style document (PDF) representing the state of the ledger at a specific block height (time).

## 🤝 Contribution

Contributions are welcome. Please ensure any Pull Request adheres to the existing **SOLID** structure and includes appropriate unit tests.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/SmartContractLogic`)
3.  Commit your Changes (`git commit -m 'Add: New governance rule'`)
4.  Push to the Branch (`git push origin feature/SmartContractLogic`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed by Daniel Martínez Pascual- Junior Software Engineer specialized in High-Integrity Systems.*

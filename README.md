# 🚀 Async SQLAlchemy Learning Repository

This repository is a self-learning and educational resource for working with **SQLAlchemy** in **asynchronous Python** environments. It covers all major parts of SQLAlchemy including **Core**, **ORM**, **Async engine**, and **Alembic** for migrations. It also demonstrates how to **test async database code** using **pytest**.

---

## 📚 What You'll Learn

### ✅ SQLAlchemy Async Fundamentals
- Setting up **AsyncEngine** with `asyncpg`
- Connecting and querying using **Core** syntax
- Using the **ORM** with async sessions and models
- Executing queries using both **Core** and **ORM** in an async context

### 🧠 Query Examples
Each query is implemented **both in Core and ORM** styles:
- `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- Filtering, ordering, and pagination
- Transactions and session management
- **Aggregate functions** like `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`

> ❗ Note: This repo **does not cover many-to-many relationships**.

### 🧪 Testing Async SQLAlchemy
- Using `pytest` with `pytest-asyncio`
- Creating a `conftest.py` to manage test DB sessions
- One working async test included as an example

### 📦 Alembic Migrations
- Alembic initialized and configured for async SQLAlchemy
- Commands to autogenerate and apply migrations
- Versioned migrations for schema tracking

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **SQLAlchemy 2.x (with async support)**
- **PostgreSQL** (or any compatible async-supported DB)
- **asyncpg** (DB driver)
- **Alembic**
- **Pytest** + **pytest-asyncio**

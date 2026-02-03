# M-PESA Prototype

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Proprietary-red)
![Version](https://img.shields.io/badge/Version-1.0.0-green)

## Project Overview
This is a high-fidelity simulation of the M-PESA ecosystem. The project replicates core banking, crypto, and utility services while introducing advanced security layers and high-resolution data logging.

**Purpose:** Building a "Better M-Pesa"

---

## Key Features

### 1. Financial Services Engine
- **Cross-Platform Transfers:** Seamless funds movement between M-PESA, major Kenyan banks (KCB, Equity, etc.), and Crypto Wallets.
- **Dynamic Asset Valuation:** Real-time (simulated) crypto rates for BTC/ETH/USDT with automated unit calculation.
- **Lipa na M-PESA:** Support for Paybill, Till Numbers, and Pochi la Biashara.

### 2. Logic & Safety Guardrails
- **The "Fat-Finger" Block:** Hard transaction limit of 500,000 KES to prevent data outliers and entry errors.
- **Overdraft Protection:** Atomic balance checks for all assets to prevent negative ledger entries.

### 3. Security Framework
- **Session Lifecycle Management:** Automated 120-second inactivity timeout with memory cleanup (RAM wiping).
- **Masked PIN Entry:** Secure terminal input using `stdiomask` with custom bullet masking.
- **Encrypted Secrets:** Local storage of credentials in `secret.json` (excluded from version control).

### 4. 2026 Analytics Dashboard
- **Dynamic Monthly Reporting:** Automated financial summaries that pivot based on the current system date (e.g., February 2026).
- **Category Tagging:** Every transaction is tagged (Food, Rent, Savings, etc.) for high-resolution forecasting.

---

## 5. Forecasting Readiness (Data Pipeline)
The engine is architected to ensure **high-resolution temporal data** for ML model training:
- **Timestamp Precision:** All transactions are logged with ISO 8601 timestamps to support time-series analysis (ARIMA/LSTM).
- **Feature Diversity:** Captured features include transaction type, volume, frequency, and merchant categories.
- **Data Integrity:** A `file_integrity.hash` ensures that the simulation logic generating the data remains unchanged between experiments.

---

## Tech Stack
- **Language:** Python 3.x
- **Storage:** JSON (State management), CSV (Transaction Logs)
- **Security:** `stdiomask`, `getpass`
- **Architecture:** Modular OOP (Models, Engine, Security, Dashboard)

---

## Proprietary Notice
**Copyright (c) 2026 Eugene.**
This software and its underlying logic are **proprietary**. No part of this repository—including the transaction logging architecture or the 2026 forecasting integration—may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author.

---

## Project Structure
```text
├── main.py              # App Entry Point & Menu Logic
├── engine.py            # Core Financial Logic & Smart Guardrails
├── models.py            # User & Account Class Definitions
├── security.py          # Auth, Session Wiping & Masking logic
├── dashboard.py         # 2026 Analytics & Dynamic Reporting
├── data_logger.py       # ML-Ready CSV Transaction Recording
├── statement_service.py # Dynamic Mpesa Full Statment in PDF Generation (Non-hardcoded)
├── sync_rates.py        # Real-time Crypto Rate Integration
├── setup.py             # Package Configuration & Metadata
├── requirements.txt     # Pinned Dependencies for Reproducibility
├── .gitignore           # Security: Prevents leak of secrets/data
├── file_integrity.hash  # SHA-256 Checksums for Logic Verification
├── README.md            # Project Vision & Documentation
├── hakikisha.json       # (Ignored) Identity Cache: Name-Lookup Verification
└── secret.json          # (Ignored) Local Dev Credentials & PINs

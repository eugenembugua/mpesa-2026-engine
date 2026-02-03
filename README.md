# M-PESA Financial Engine & 2026 Forecasting Prototype

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Proprietary-red)
![Version](https://img.shields.io/badge/Version-1.0.0-green)

## Project Overview
This is a high-fidelity simulation of the M-PESA ecosystem, designed as a data-generation engine for **predictive financial forecasting**. The project replicates the core banking, crypto, and utility services of M-PESA while introducing advanced security layers and data-logging mechanisms.

**Purpose:** To generate a clean, structured dataset (`mpesa_data_2026.csv`) to train machine learning models to predict liquidity trends and spending habits in the Kenyan market for the year 2026.

---

## Key Features

### 1. Financial Services Engine
- **Cross-Platform Transfers:** Seamlessly move funds between M-PESA, major Kenyan banks (KCB, Equity, etc.), and Crypto Wallets.
- **Dynamic Asset Valuation:** Real-time (simulated) crypto rates for BTC/ETH/USDT with automated unit calculation.
- **Lipa na M-PESA:** Support for Paybill, Till Numbers, and Pochi la Biashara.

### 2. Logic & Safety Guardrails
- **The "Fat-Finger" Block:** Hard transaction limit of 500,000 KES to prevent data outliers and entry errors.
- **Overdraft Protection:** Atomic balance checks for all assets (Bank, Crypto, and M-PESA) to prevent negative ledger entries.

### 3. Security Framework
- **Session Lifecycle Management:** Automated 120-second inactivity timeout with memory cleanup (RAM wiping).
- **Masked PIN Entry:** Secure terminal input using `stdiomask` with custom bullet masking.
- **Encrypted Secrets:** Local storage of credentials in `secret.json` (excluded from version control).

### 4. 2026 Analytics Dashboard
- **Dynamic Monthly Reporting:** Automated financial summaries that pivot based on the current system date (e.g., February 2026).
- **Category Tagging:** Every transaction is tagged (Food, Rent, Savings, etc.) for high-resolution forecasting.

---

##  Tech Stack
- **Language:** Python 3.x
- **Storage:** JSON (State management), CSV (Transaction Logs)
- **Security:** stdiomask, getpass
- **Architecture:** Modular OOP (Models, Engine, Security, Dashboard)

---

## Proprietary Notice
**Copyright (c) 2026 Eugene.**
This software and its underlying logic are **proprietary**. No part of this repository—including the transaction logging architecture or the 2026 forecasting integration—may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author.

---

## Project Structure
```text
├── main.py           # App Entry Point & Menu Logic
├── engine.py         # Core Financial Logic & Balance Checks
├── models.py         # User & Account Class Definitions
├── security.py       # Auth & Session Management
├── dashboard.py      # Analytics & Monthly Reporting
├── data_logger.py    # CSV Transaction Recording
└── secret.json       # (Ignored) User Secrets & PINs
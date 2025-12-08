# 🤖 Tech Giants Quant Dashboard

A minimalist Quantitative Finance Dashboard built with **Streamlit**. It optimizes a portfolio of "Tech Giant" stocks using **Hierarchical Risk Parity (HRP)** and compares its performance against the S&P 500 (SPY).

## 🚀 Features

*   **Quantitative Engine**: Uses `PyPortfolioOpt` to perform HRP optimization.
*   **Live Data**: Fetches 2-year historical data using `yfinance` (with caching).
*   **Interactive Viz**: Plotly charts for Asset Allocation, Cluster Dendrograms, and Cumulative Returns.
*   **Lightweight**: Designed to run on minimal resources (e.g., free tier VPS with 1GB RAM).

## 🛠️ Stack

*   **Python 3.10+**
*   **Streamlit**: UI Framework.
*   **yfinance**: Market Data.
*   **PyPortfolioOpt**: Portfolio Optimization.
*   **Plotly**: Visualization.

## 📦 Deployment Instructions

### 1. VPS Setup (Debian/Ubuntu)
Update your system and install Python/Pip.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
```

### 🤖 Tech Giants HRP Portfolio Dashboard

A full-stack quantitative finance dashboard that constructs a **Hierarchical Risk Parity (HRP)** portfolio of top Tech stocks. It features a **FastAPI** backend for robust calculation and a **React (Vite)** frontend for a modern, responsive UI.

## 🚀 Key Features

*   **HRP Optimization**: Uses `PyPortfolioOpt` to build a risk-parity portfolio, robust to market noise.
*   **Modern Interactive UI**: React + Recharts + TailwindCSS.
*   **Automated Updates**: Dedicated scheduler service keeps market data fresh daily (Rolling Window).
*   **Persistence**: SQLite database (`data/portfolio.db`) stores history and allocations.
*   **Dockerized**: One-command deployment for the entire stack.

## 🛠️ Tech Stack

*   **Frontend**: React, TypeScript, Vite, TailwindCSS, Recharts.
*   **Backend**: Python, FastAPI, Pandas, PyPortfolioOpt, yfinance.
*   **Database**: SQLite (persisted via Docker volumes).
*   **DevOps**: Docker & Docker Compose.

## 📂 Project Structure

```
├── backend/            # FastAPI App & Worker
│   ├── main.py         # API Entrypoint
│   ├── scheduler.py    # Background Updater
│   ├── logic.py        # Core Quant Logic
│   └── database.py     # SQLite Handler
├── frontend/           # React App
│   ├── src/            # Components & Pages
│   └── Dockerfile      # Multi-stage Nginx build
├── data/               # Persistent Data Storage
├── compose.yml         # Full Stack Orchestration
└── analysis.ipynb      # Research Notebook (Backtesting)
```

## 🌍 Deployment

The application is designed to be deployed on a VPS using Docker.

### 1. Prerequisites
*   Docker & Docker Compose installed.

### 2. Quick Start
Clone the repository and launch the stack:

```bash
# 1. Clone
git clone https://github.com/achillekrtf/HRP_Optimizer.git
cd HRP_Optimizer

# 2. Launch
docker compose up -d --build
```

### 3. Access
*   **Dashboard**: `http://<YOUR_VPS_IP>` (Port 80)
*   **API**: `http://<YOUR_VPS_IP>:8000`
*   **Scheduler**: Runs automatically in the background (Updates daily at 22:00 UTC).

## 🔬 Research & Backtesting
For a deep dive into the algorithm and a rolling backtest of the strategy:
*   Open `analysis.ipynb` (Jupyter Notebook).
*   Includes Dendrograms, Correlation Matrices, and Equity Curves comparing HRP vs SPY.

## 🔄 Development
To run locally:
```bash
docker compose up
```
Or run services individually (requires python 3.11 and node 18+).

#### Rolling Window Logic
*   **Data Update**: Fetches the last 2 years of data for all tickers daily.
*   **Rebalancing**: Checks if the last allocation is older than 7 days. If yes, it re-runs HRP optimization and saves the new weights.

# HRP_Optimizer

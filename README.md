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

### 2. Installation

Clone your repository (or upload files) and set up the environment.

#### Option A: Using Standard Pip
```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using uv (Faster & Recommended)
If `uv` is available:
```bash
uv pip install -r requirements.txt
```

### 3. Running the App

Run the dashboard in the background (using `nohup` or `tmux` is recommended for persistent sessions).

```bash
# Simple run
streamlit run app.py

# Run on specific port (e.g., 80)
streamlit run app.py --server.port 80
```

**Access the dashboard at:** `http://<YOUR_VPS_IP>:8501`

## 💻 Local Development

1.  Clone repo.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Run: `streamlit run app.py`.

## 📂 Project Structure

### 4. Persistence & Automation (V2)

The application now uses a SQLite database (`portfolio.db`) to store market data and allocations. This allows it to run efficiently and maintain state.

#### Automatic Updates (Cron)
To ensure your portfolio is updated daily and rebalanced weekly, set up a cron job.

1.  Make sure `updater.py` is executable or run via python.
2.  Edit crontab:
    ```bash
    crontab -e
    ```
3.  Add the following line (runs every weekday at 10:00 PM):
    ```cron
    0 22 * * 1-5 cd /path/to/project && /path/to/venv/bin/python updater.py >> updater.log 2>&1
    ```

#### Rolling Window Logic
*   **Data Update**: Fetches the last 2 years of data for all tickers daily.
*   **Rebalancing**: Checks if the last allocation is older than 7 days. If yes, it re-runs HRP optimization and saves the new weights.


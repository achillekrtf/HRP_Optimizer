import sqlite3
import pandas as pd
import json
from datetime import datetime

DB_NAME = "portfolio.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Market Data Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            date TEXT,
            ticker TEXT,
            adj_close REAL,
            PRIMARY KEY (date, ticker)
        )
    ''')
    
    # Portfolio Allocations Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS allocations (
            date TEXT PRIMARY KEY,
            weights_json TEXT,
            metrics_json TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_prices(df):
    """
    Expects a DataFrame with Index=Date and Columns=Tickers.
    MELT it nicely for SQL storage.
    """
    conn = sqlite3.connect(DB_NAME)
    
    # Reset index to make Date a column
    reset_df = df.reset_index()
    
    # Melt: Date, Ticker, Price
    melted = reset_df.melt(id_vars=reset_df.columns[0], var_name='ticker', value_name='adj_close')
    melted.columns = ['date', 'ticker', 'adj_close']
    
    # Ensure date format is string YYYY-MM-DD
    melted['date'] = melted['date'].astype(str).str[:10]
    
    # Bulk Insert / Ignore duplicates
    data = list(melted.itertuples(index=False, name=None))
    
    c = conn.cursor()
    c.executemany('INSERT OR IGNORE INTO prices (date, ticker, adj_close) VALUES (?, ?, ?)', data)
    
    conn.commit()
    conn.close()

def get_prices(start_date=None):
    """
    Returns DF: Index=Date, Columns=Tickers
    """
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT date, ticker, adj_close FROM prices"
    if start_date:
        query += f" WHERE date >= '{start_date}'"
        
    query += " ORDER BY date ASC"
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    if df.empty:
        return pd.DataFrame()
        
    # Pivot back to wide format
    pivot = df.pivot(index='date', columns='ticker', values='adj_close')
    pivot.index = pd.to_datetime(pivot.index)
    return pivot

def save_allocation(weights, metrics):
    conn = sqlite3.connect(DB_NAME)
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    weights_json = json.dumps(weights)
    metrics_json = json.dumps(metrics)
    
    # Insert or Replace today's allocation
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO allocations (date, weights_json, metrics_json) VALUES (?, ?, ?)', 
              (date_str, weights_json, metrics_json))
    
    conn.commit()
    conn.close()

def get_latest_allocation():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT date, weights_json, metrics_json FROM allocations ORDER BY date DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'date': row[0],
            'weights': json.loads(row[1]),
            'metrics': json.loads(row[2])
        }
    return None

def get_all_allocations():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM allocations ORDER BY date ASC", conn)
    conn.close()
    return df

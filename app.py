import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from scipy.cluster.hierarchy import linkage
import database
import logic

# --- Configuration ---
st.set_page_config(
    page_title="Tech Giants Quant Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- Main App ---
st.title("🤖 Tech Giants HRP Portfolio Dashboard")

# 1. Load Data from DB
start_date = (pd.Timestamp.now() - pd.DateOffset(years=2)).strftime('%Y-%m-%d')
df_prices = database.get_prices(start_date=start_date)

if df_prices.empty:
    st.warning("⚠️ No data in database. Attempting partial update...")
    with st.spinner('First run initialization...'):
        database.init_db()
        logic.update_market_data()
        logic.rebalance_portfolio_if_needed()
        df_prices = database.get_prices(start_date=start_date)
        if df_prices.empty:
            st.error("Failed to initialize data. Please check connection.")
            st.stop()
    st.success("Initialization complete! Refreshing...")
    st.rerun()

# 2. Load Latest Allocation
allocation = database.get_latest_allocation()

if not allocation:
    st.warning("No allocation found. Running optimization...")
    logic.rebalance_portfolio_if_needed()
    st.rerun()

# Extract Data
weights = allocation['weights']
metrics = allocation['metrics']
alloc_date = allocation['date']

st.markdown(f"**Status**: Data from Database | **Last Rebalance**: {alloc_date}")

# 3. Metrics Display
col1, col2, col3 = st.columns(3)
col1.metric("Expected Annual Return", f"{metrics['expected_return']*100:.2f}%")
col2.metric("Annual Volatility", f"{metrics['volatility']*100:.2f}%")
col3.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")

# 4. Visualizations

# Row 1: Allocation & Dendrogram
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Asset Allocation (HRP)")
    df_weights = pd.DataFrame.from_dict(weights, orient='index', columns=['Weight'])
    df_weights = df_weights.reset_index().rename(columns={'index': 'Ticker'})
    
    fig_pie = px.pie(df_weights, values='Weight', names='Ticker', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with row1_col2:
    st.subheader("Cluster Dendrogram")
    # Reconstruct correlation from recent prices
    # Exclude SPY from dendrogram of portfolio
    port_tickers = [t for t in df_weights['Ticker']]
    
    if len(port_tickers) > 1:
        port_prices = df_prices[port_tickers].dropna()
        returns = port_prices.pct_change().dropna()
        corr = returns.corr()
        
        fig_dendro = ff.create_dendrogram(corr, labels=corr.columns)
        fig_dendro.update_layout(width=800, height=500) # Fix for Streamlit OverflowError
        st.plotly_chart(fig_dendro, use_container_width=True)
    else:
        st.info("Not enough assets for dendrogram.")

# Row 2: Performance Comparison
st.subheader("Performance vs Benchmark (Base 100)")

# Prices
# Benchmark
if "SPY" in df_prices:
    bench_prices = df_prices["SPY"].dropna()
    bench_rets = bench_prices.pct_change().dropna()
    bench_cum_returns = (1 + bench_rets).cumprod() * 100
else:
    bench_cum_returns = pd.Series()

# Portfolio
# Note: This is a simplified cumulative return assuming constant current weights over the history.
# For true rolling performance, we'd need historical weights.
# Given MVP, we project current weights backward to see "How this portfolio would have performed".
portfolio_prices = df_prices[port_tickers].dropna()
port_rets = portfolio_prices.pct_change().dropna()
port_cum_returns = (1 + port_rets @ pd.Series(weights)).cumprod() * 100

# Align
common_index = port_cum_returns.index.intersection(bench_cum_returns.index)
comparison_df = pd.DataFrame({
    "HRP Portfolio (Current Weights)": port_cum_returns.loc[common_index],
    "SPY Benchmark": bench_cum_returns.loc[common_index]
})

fig_perf = px.line(comparison_df)
st.plotly_chart(fig_perf, use_container_width=True)

# Footer
st.caption("Note: Performance chart projects current weights historically (Backtest).")

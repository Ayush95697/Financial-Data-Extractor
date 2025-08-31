import streamlit as st
import pandas as pd
from data_extractor import extract
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Financial Data Extractor",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 Financial Data Extractor</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for additional options
with st.sidebar:
    st.header("⚙️ Settings")
    show_comparison = st.checkbox("Show comparison chart", value=True)
    show_variance = st.checkbox("Show variance analysis", value=True)
    decimal_places = st.selectbox("Decimal places", [0, 1, 2, 3, 4], index=2)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Input Financial Data")
    
    # Sample text for demonstration
    sample_text = """Apple Inc. reported quarterly revenue of $94.8 billion, exceeding analyst estimates of $92.5 billion. 
The company's earnings per share came in at $1.52, compared to the expected $1.43 per share."""
    
    # Input area with example
    if st.button("📋 Load Sample Text"):
        st.session_state.sample_loaded = True
    
    paragraph = st.text_area(
        "Enter or paste financial paragraph:",
        value=sample_text if st.session_state.get('sample_loaded', False) else "",
        height=150,
        placeholder="Enter financial data here... (e.g., earnings reports, analyst expectations, etc.)"
    )
    
    # Clear button
    if st.button("🗑️ Clear Text"):
        st.session_state.sample_loaded = False
        st.rerun()

with col2:
    st.subheader("ℹ️ Instructions")
    st.info("""
    **How to use:**
    1. Paste financial text containing revenue and EPS data
    2. Click 'Extract Data' to process
    3. View results in table and charts below
    
    **Supported formats:**
    - Earnings reports
    - Analyst estimates vs actuals
    - Financial news articles
    """)

st.markdown("---")

# Extract button with better styling
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    extract_button = st.button("🔍 Extract Financial Data", type="primary", use_container_width=True)

# Processing and results
if extract_button:
    if paragraph.strip():
        try:
            with st.spinner("🔄 Extracting financial data..."):
                extracted_data = extract(paragraph)
            
            # Check if extraction was successful
            if extracted_data and any(extracted_data.values()):
                st.markdown('<div class="success-box">✅ <strong>Data extraction completed successfully!</strong></div>', unsafe_allow_html=True)
                
                # Helper function to format currency values
                def format_currency(value, prefix="$"):
                    if value is None or value == 'N/A' or (isinstance(value, str) and value.strip() == ''):
                        return 'N/A'
                    try:
                        num_value = float(value)
                        return f"{prefix}{num_value:,.{decimal_places}f}"
                    except (ValueError, TypeError):
                        return str(value)
                
                # Prepare enhanced table data
                data = {
                    'Metric': ['Revenue', 'EPS'],
                    'Expected': [
                        format_currency(extracted_data.get('revenue_expected'), "$"),
                        format_currency(extracted_data.get('eps_expected'), "$")
                    ],
                    'Actual': [
                        format_currency(extracted_data.get('revenue_actual'), "$"),
                        format_currency(extracted_data.get('eps_actual'), "$")
                    ]
                }
                
                # Calculate variances if both values exist
                if show_variance:
                    variances = []
                    for metric in ['revenue', 'eps']:
                        expected = extracted_data.get(f'{metric}_expected')
                        actual = extracted_data.get(f'{metric}_actual')
                        
                        # Convert to float if they're strings
                        try:
                            if expected and actual:
                                expected_val = float(expected) if not isinstance(expected, (int, float)) else expected
                                actual_val = float(actual) if not isinstance(actual, (int, float)) else actual
                                
                                if expected_val != 0:
                                    variance = ((actual_val - expected_val) / expected_val) * 100
                                    variances.append(f"{variance:+.1f}%")
                                else:
                                    variances.append('N/A')
                            else:
                                variances.append('N/A')
                        except (ValueError, TypeError):
                            variances.append('N/A')
                    
                    data['Variance (%)'] = variances
                
                # Display results in columns
                col_table, col_chart = st.columns([1, 1])
                
                with col_table:
                    st.subheader("📋 Extracted Data")
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="financial_data.csv",
                        mime="text/csv"
                    )
                
                # Comparison chart
                if show_comparison and col_chart:
                    with col_chart:
                        st.subheader("📊 Expected vs Actual")
                        
                        chart_data = []
                        for metric in ['Revenue', 'EPS']:
                            metric_lower = metric.lower()
                            expected = extracted_data.get(f'{metric_lower}_expected')
                            actual = extracted_data.get(f'{metric_lower}_actual')
                            
                            if expected and actual:
                                chart_data.extend([
                                    {'Metric': metric, 'Type': 'Expected', 'Value': expected},
                                    {'Metric': metric, 'Type': 'Actual', 'Value': actual}
                                ])
                        
                        if chart_data:
                            chart_df = pd.DataFrame(chart_data)
                            fig = px.bar(
                                chart_df, 
                                x='Metric', 
                                y='Value', 
                                color='Type',
                                barmode='group',
                                title="Expected vs Actual Performance",
                                color_discrete_map={'Expected': '#ff7f0e', 'Actual': '#1f77b4'}
                            )
                            fig.update_layout(height=400, showlegend=True)
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("📊 Chart will appear when numerical data is available.")
                
                # Metrics display with safe conversion
                revenue_expected = extracted_data.get('revenue_expected')
                revenue_actual = extracted_data.get('revenue_actual')
                
                if revenue_expected and revenue_actual:
                    st.subheader("📈 Key Metrics")
                    col_rev, col_eps = st.columns(2)
                    
                    with col_rev:
                        try:
                            rev_exp = float(revenue_expected)
                            rev_act = float(revenue_actual)
                            revenue_diff = rev_act - rev_exp
                            revenue_pct = (revenue_diff / rev_exp) * 100 if rev_exp != 0 else 0
                            st.metric(
                                label="Revenue Performance",
                                value=f"${rev_act:,.{decimal_places}f}B",
                                delta=f"{revenue_pct:+.1f}% vs estimate"
                            )
                        except (ValueError, TypeError):
                            st.metric(
                                label="Revenue Performance",
                                value=str(revenue_actual),
                                delta="Unable to calculate"
                            )
                    
                    with col_eps:
                        eps_expected = extracted_data.get('eps_expected')
                        eps_actual = extracted_data.get('eps_actual')
                        if eps_expected and eps_actual:
                            try:
                                eps_exp = float(eps_expected)
                                eps_act = float(eps_actual)
                                eps_diff = eps_act - eps_exp
                                eps_pct = (eps_diff / eps_exp) * 100 if eps_exp != 0 else 0
                                st.metric(
                                    label="EPS Performance",
                                    value=f"${eps_act:,.{decimal_places}f}",
                                    delta=f"{eps_pct:+.1f}% vs estimate"
                                )
                            except (ValueError, TypeError):
                                st.metric(
                                    label="EPS Performance",
                                    value=str(eps_actual),
                                    delta="Unable to calculate"
                                )
            
            else:
                st.error("❌ No financial data could be extracted from the provided text. Please check the format and try again.")
                
        except Exception as e:
            st.error(f"❌ An error occurred during extraction: {str(e)}")
            st.info("💡 **Tip:** Make sure your text contains clear financial metrics like revenue and EPS data.")
    
    else:
        st.warning("⚠️ Please enter some financial text to extract data from.")

# Footer with additional information
st.markdown("---")
with st.expander("🔍 About This Tool"):
    st.markdown("""
    **Financial Data Extractor** helps you quickly parse financial information from text sources like:
    - Earnings reports
    - Financial news articles
    - Analyst notes
    - Press releases
    
    The tool extracts key metrics including revenue and earnings per share (EPS), 
    comparing expected vs actual values when available.
    
    **Features:**
    - Automatic data extraction
    - Visual comparisons
    - Variance analysis
    - CSV export capability
    - Customizable precision
    """)

# Sample data section
with st.expander("📚 Sample Financial Texts"):
    st.markdown("""
    **Example 1 (Tech Company):**
    ```
    Microsoft Corporation reported fiscal Q4 revenue of $56.2 billion, surpassing analyst expectations of $55.5 billion. 
    Earnings per share reached $2.95, beating estimates of $2.75.
    ```
    
    **Example 2 (Retail Company):**
    ```
    Walmart Inc. announced quarterly revenue of $161.5 billion versus consensus estimates of $159.8 billion. 
    The retailer posted EPS of $1.78, compared to analyst projections of $1.72 per share.
    ```
    """)

import streamlit as str_lit
import pandas as pd
import plotly.express as px

# Page Configuration
str_lit.set_page_config(
    page_title="Sellers Performance Dashboard",
    layout="wide"
)

# Load Data 
@str_lit.cache_data
def load_data():
    # Read the Excel file
    df = pd.read_excel("sellers.xlsx", sheet_name="gc_QRO.PM3000.5.1813.18212_full")
    return df

df = load_data()

# Main Title
str_lit.title("Sellers Performance Dashboard")
str_lit.markdown("Explore vendor metrics, filter records by region, and inspect individual performance.")

# Filters
str_lit.sidebar.header("Filters")

# Region Filter
available_regions = df["REGION"].unique().tolist()
selected_regions = str_lit.sidebar.multiselect(
    "Select Region(s):",
    options=available_regions,
    default=available_regions
)

# Filter the DataFrame based on user selection and create FULL_NAME for charts
filtered_df = df[df["REGION"].isin(selected_regions)].copy()
filtered_df["FULL_NAME"] = filtered_df["NAME"] + " " + filtered_df["LASTNAME"]

# Regional Sales Overview
with str_lit.container():
    str_lit.subheader("Regional Sales Overview")
    
    # Display quick summary metrics
    col1, col2 = str_lit.columns(2)
    col1.metric("Total Sellers Displayed", len(filtered_df))
    col2.metric("Total Units Sold", f"{filtered_df['SOLD UNITS'].sum():,}")

    # Display the interactive table
    str_lit.dataframe(
        filtered_df.drop(columns=["FULL_NAME"]),
        use_container_width=True,
        hide_index=True
    )

str_lit.divider()

# Performance Graphs (Units Sold, Total Sales, Average Sales)
with str_lit.container():
    str_lit.subheader("Regional Performance Analytics")
    
    # color palette
    professional_colors = {
        "NORTE": "#1E3A8A",  
        "SUR": "#0369A1",    
        "ESTE": "#374151",   
        "OESTE": "#B45309"}
    
    # Create tabs for each required metric graph
    tab1, tab2, tab3 = str_lit.tabs([
        "Units Sold", 
        "Total Sales", 
        "Average Sales"
    ])

    with tab1:
        str_lit.markdown("### Units Sold per Vendor")
        fig_units = px.bar(
            filtered_df.sort_values("SOLD UNITS", ascending=True),
            x="SOLD UNITS",
            y="FULL_NAME",
            color="REGION",
            orientation="h",
            color_discrete_map=professional_colors,
            labels={"FULL_NAME": "Vendor", "SOLD UNITS": "Units Sold", "REGION": "Region"}
        )
        fig_units.update_layout(
            template="plotly_white",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=900
        )
        str_lit.plotly_chart(fig_units, use_container_width=True)

    with tab2:
        str_lit.markdown("### Total Sales per Vendor")
        fig_sales = px.bar(
            filtered_df.sort_values("TOTAL SALES", ascending=True),
            x="TOTAL SALES",
            y="FULL_NAME",
            color="REGION",
            orientation="h",
            color_discrete_map=professional_colors,
            labels={"FULL_NAME": "Vendor", "TOTAL SALES": "Total Sales", "REGION": "Region"}
        )
        fig_sales.update_layout(
            template="plotly_white",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=900
        )
        str_lit.plotly_chart(fig_sales, use_container_width=True)

    with tab3:
        str_lit.markdown("### Sales Average per Vendor")
        fig_avg = px.bar(
            filtered_df.sort_values("SALES AVERAGE", ascending=True),
            x="SALES AVERAGE",
            y="FULL_NAME",
            color="REGION",
            orientation="h",
            color_discrete_map=professional_colors,
            labels={"FULL_NAME": "Vendor", "SALES AVERAGE": "Sales Average", "REGION": "Region"}
        )
        fig_avg.update_layout(
            template="plotly_white",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=900
        )
        str_lit.plotly_chart(fig_avg, use_container_width=True)

str_lit.divider()

# Specific Vendor Data
with str_lit.container():
    str_lit.subheader("Specific Vendor Lookup")
    
    # selectbox to pick a vendor from the dataset
    all_vendors = df.copy()
    all_vendors["FULL_NAME"] = all_vendors["NAME"] + " " + all_vendors["LASTNAME"]
    
    selected_vendor_name = str_lit.selectbox(
        "Select a Vendor:",
        options=all_vendors["FULL_NAME"].sort_values().unique()
    )
    
    # Retrieve data for the selected vendor
    vendor_data = all_vendors[all_vendors["FULL_NAME"] == selected_vendor_name].iloc[0]
    
    # Display vendor profile inside a container
    with str_lit.expander(f"Profile Details: {selected_vendor_name}", expanded=True):
        col_info1, col_info2, col_info3 = str_lit.columns(3)
        col_info1.write(f"**Vendor ID:** {vendor_data['ID']}")
        col_info2.write(f"**Region:** {vendor_data['REGION']}")
        col_info3.write(f"**Income:** ${vendor_data['INCOME']:,.2f}")
        
        str_lit.markdown("---")
        
        col_m1, col_m2, col_m3 = str_lit.columns(3)
        
        # Calculate differences against general averages for context
        diff_units = vendor_data["SOLD UNITS"] - df["SOLD UNITS"].mean()
        diff_sales = vendor_data["TOTAL SALES"] - df["TOTAL SALES"].mean()
        diff_avg = vendor_data["SALES AVERAGE"] - df["SALES AVERAGE"].mean()
        
        col_m1.metric(
            "Units Sold", 
            int(vendor_data["SOLD UNITS"]), 
            f"{diff_units:+.1f} vs average"
        )
        col_m2.metric(
            "Total Sales", 
            f"${vendor_data['TOTAL SALES']:,.2f}", 
            f"{diff_sales:+,.2f} vs average"
        )
        col_m3.metric(
            "Sales Average", 
            f"{vendor_data['SALES AVERAGE']:.4f}", 
            f"{diff_avg:+.4f} vs average"
        )
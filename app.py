# APP DEMO

# Note: I ran this on my terminal:
#cd ~/Desktop/Prof\ Projects/Forest\ Fires/
#streamlit run app.py

#  And got this:
#  You can now view your Streamlit app in your browser.

#  Local URL: http://localhost:8504
#  Network URL: http://10.128.238.124:8504

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# 1. App Title and Description
# ---------------------------
st.title("BC Wildfire Data Explorer")
st.markdown("""
This app allows you to explore the **BC Wildfire Dataset** after cleaning and preprocessing.
You can view the dataset, summary statistics, and interactive plots.
""")

# ---------------------------
# 2. Load Dataset
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Fires.csv", parse_dates=["IGN_DATE", "FR_T_DTE"])
    return df

df = load_data()

# ---------------------------
# 3. Sidebar Options
# ---------------------------
st.sidebar.title("Options")
show_data = st.sidebar.checkbox("Show Raw Data")
show_summary = st.sidebar.checkbox("Show Summary Statistics")
show_distribution = st.sidebar.checkbox("Show Fire Size Distribution")
show_trends = st.sidebar.checkbox("Show Yearly Trends")

# ---------------------------
# 4. Display Raw Data (limited)
# ---------------------------
MAX_ROWS = 500  # Max rows to display

if show_data:
    st.subheader(f"Raw Dataset (showing up to {MAX_ROWS} rows)")
    if len(df) > MAX_ROWS:
        st.dataframe(df.sample(MAX_ROWS))  # Random sample
    else:
        st.dataframe(df)

# ---------------------------
# 5. Summary Statistics
# ---------------------------
if show_summary:
    st.subheader("Summary Statistics of Fire Size")
    stats = {
        "Total Fires": len(df),
        "Average Size (ha)": df["SIZE_HA"].mean(),
        "Median Size (ha)": df["SIZE_HA"].median(),
        "Min Size (ha)": df["SIZE_HA"].min(),
        "Max Size (ha)": df["SIZE_HA"].max()
    }
    st.table(pd.DataFrame.from_dict(stats, orient="index", columns=["Value"]))

# ---------------------------
# 6. Distribution Plot (downsample if needed)
# ---------------------------
if show_distribution:
    st.subheader("Fire Size Distribution")
    fig, ax = plt.subplots(figsize=(10,5))
    
    # Downsample to avoid browser overload
    SAMPLE_SIZE = 5000
    plot_df = df.sample(min(len(df), SAMPLE_SIZE))
    
    sns.histplot(plot_df["SIZE_HA"], bins=30, kde=True, color="orange", ax=ax)
    ax.set_xlabel("Fire Size (Hectares)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

# ---------------------------
# 7. Yearly Trends
# ---------------------------
if show_trends:
    st.subheader("Average Fire Size Per Year")
    yearly = df.groupby("FIRE_YEAR")["SIZE_HA"].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=yearly, x="FIRE_YEAR", y="SIZE_HA", marker="o", color="#0072B2", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Fire Size (Hectares)")
    st.pyplot(fig)

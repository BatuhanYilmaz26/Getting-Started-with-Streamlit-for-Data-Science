import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# Plotly, seaborn, matplotlib visualizations
# Streamlit allows us to call Plotly graphs from within Streamlit apps using the 
# st.plotly_chart() function

st.write("""
## SF Trees
##### This app analyses trees in San Francisco using a dataset kindly provided by SF DPW
""")

trees_df = pd.read_csv("trees.csv")
st.write(trees_df.head())

st.write("### Plotly Chart")
fig = px.histogram(trees_df["dbh"])
st.plotly_chart(fig)

# Figure out the age of each tree in days, and plot that 
# histogram using Seaborn and Matplotlib.
trees_df["age"] = (pd.to_datetime("today") - pd.to_datetime(trees_df["date"])).dt.days

st.write("### Seaborn Chart")
fig_sb, ax_sb = plt.subplots()
ax_sb = sns.histplot(trees_df["age"])
plt.xlabel("Age (Days)")
st.pyplot(fig_sb)

st.write("### Matplotlib Chart")
fig_mpl, ax_mpl = plt.subplots()
ax_mpl = plt.hist(trees_df["age"])
plt.xlabel("Age (Days)")
st.pyplot(fig_mpl)
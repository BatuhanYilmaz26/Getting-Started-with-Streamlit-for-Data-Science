import streamlit as st
import pandas as pd
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt

st.write("""
## SF Trees
##### This app analyses trees in San Francisco using a dataset kindly provided by SF DPW
""")
# Load trees dataset, add age column in days
trees_df = pd.read_csv("trees.csv")
trees_df["age"] = (pd.to_datetime("today") - pd.to_datetime(trees_df["date"])).dt.days

#add tree owner filter to sidebar, then filter, get color
owners = st.sidebar.multiselect(label="Tree Owner Filter",
    options=trees_df["caretaker"].unique())
st.write(f"##### The current analysis is of trees owned by {owners}.")

graph_color = st.sidebar.color_picker(label="Graph Colors")

if owners:
    trees_df = trees_df[trees_df["caretaker"].isin(owners)]

# group by dbh for the leftmost graph
df_dbh_grouped = pd.DataFrame(trees_df.groupby(["dbh"]).count()["tree_id"])
df_dbh_grouped.columns = ["tree_count"]

# define columns and add graphs
col1, col2 = st.columns(2)
with col1:
    st.write("Trees by Width")
    fig1, ax1 = plt.subplots()
    ax1 = sns.histplot(trees_df["dbh"], color=graph_color)
    plt.xlabel("Tree Width")
    st.pyplot(fig1)
with col2:
    st.write("Trees by Age")
    fig2, ax2 = plt.subplots()
    ax2 = sns.histplot(trees_df["age"], color=graph_color)
    plt.xlabel("Age (Days)")
    st.pyplot(fig2)

st.write("Trees by Location")
trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df = trees_df.sample(n=1000, replace=True)
st.map(trees_df)
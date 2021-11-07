import streamlit as st
import pandas as pd
import numpy as np

# Intro to visualizations

st.write("""
## SF Trees
##### This app analyses trees in San Francisco using a dataset kindly provided by SF DPW
""")

trees_df = pd.read_csv("trees.csv")
st.write(trees_df.head())

df_dbh_grouped = pd.DataFrame(trees_df.groupby(["dbh"]).count()["tree_id"])
df_dbh_grouped.columns = ["tree_count"]

st.bar_chart(df_dbh_grouped)
st.area_chart(df_dbh_grouped)
st.line_chart(df_dbh_grouped)
df_dbh_grouped["new_col"] = np.random.randn(len(df_dbh_grouped))  * 500
st.line_chart(df_dbh_grouped)


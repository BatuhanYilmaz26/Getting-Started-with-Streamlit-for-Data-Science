import streamlit as st
import pandas as pd

# The default for Streamlit apps is to have a centered page layout.
# The following code sets up our Streamlit app in a wide format instead of our default centered one:
st.set_page_config(layout="wide")

st.write("""
## SF Trees
#### This app analyses trees in San Francisco using a dataset kindly provided by SF DPW
""")
trees_df = pd.read_csv("trees.csv")

df_dbh_grouped = pd.DataFrame(trees_df.groupby(["dbh"]).count())["tree_id"]
df_dbh_grouped.columns = ["tree_count"]

col1, col2, col3 = st.columns(3)

with col1:
    st.line_chart(df_dbh_grouped)
with col2:
    st.bar_chart(df_dbh_grouped)
with col3:
    st.area_chart(df_dbh_grouped)
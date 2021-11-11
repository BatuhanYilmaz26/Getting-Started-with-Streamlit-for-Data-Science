import streamlit as st
import pandas as pd

st.write("""
## SF Trees
#### This app analyses trees in San Francisco using a dataset kindly provided by SF DPW
""")
trees_df = pd.read_csv("trees.csv")

col1, col2 , col3 = st.columns([1, 1, 1])

with col1:
    st.write("First column")

with col2:
    st.write("Second column")

with col3:
    st.write("Third column")

# As we can see, st.columns() defines three columns of equal length, and we use the with notation to print some text in each.
# We can also call the st.write() function (or any other Streamlit function that writes content to our Streamlit app) 
# directly on our predefined columns for the same outcome, as shown in the following code.

col1.write("First column")
col2.write('Second column')
col3.write('Third column')
# As we write more complex Streamlit apps with more content in each column, with statements 
# tend to make for cleaner apps that are easier to understand and debug.

# In Streamlit, the column width is relative to the size of the other defined columns. 
# Because of this, if we scale up the width of each column to 10 instead of 1, our app will not change at all.
# The following code block shows three options for column width that all result in the same column widths:
#option 1
col1, col2, col3 = st.columns([1, 1, 1])
#option 2
col1, col2, col3 = st.columns([10, 10, 10])
#option 3
col1, col2, col3 = st.columns(3)

# As a final example, the following code block allows the user input to determine the width of each column.
st.write("""#### Change the values below to customize the column widths.""")
first_width = st.number_input(label="First Width", min_value=1, value=1)
second_width = st.number_input(label="Second Width", min_value=1, value=1)
third_width = st.number_input(label="Third Width", min_value=1, value=1)

col1, col2, col3 = st.columns([first_width, second_width, third_width])

with col1:
    st.write("First column")

with col2:
    st.write("Second column")

with col3:
    st.write("Third column")
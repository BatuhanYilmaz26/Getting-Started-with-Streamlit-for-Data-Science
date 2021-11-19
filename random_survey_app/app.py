import streamlit as st
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")
st.header("Deciding Survey Sample Size")
st.write("""
Please use the following app to see how representative and expensive 
a set sample is for our survey design.
""")
np.random.seed(1)
# Setting a seed in numpy allows reproducible results with randomly selected data.
# (When developing a user-facing app, I would recommend leaving this out, otherwise 
# clever users will be more suspicious about your random selection methods!)

num_surveys = 100
num_surveys = st.slider(label="Number of Surveys Sent",
    min_value=5, max_value=150, value=50)
max_amount = st.number_input(label="What is the maximum amount you want to spend on the survey?",
    value=num_surveys*50, step=500)
user_time_spent = np.random.normal(50.5, 10, 1000)
my_sample = np.random.choice(user_time_spent, size=100)

# Calculating the cost of the sample
    # For this hypothetical survey, the cost of any individual survey respondent is a 10% chance 
    # at a $500 gift card, so we should show the expected value as 10% times $500, which is $50 on average. 
expected_cost = 50 * num_surveys
max_amount = 5000
# We can simulate this survey running 10,000 times and count how often 
# the cost of the experiment goes over a certain value.
percent_change_over = 100 * sum(np.random.binomial(n=num_surveys, p=0.1, 
    size=10000) > max_amount/500)/10000
st.write(f"##### The expected cost of this sample is {expected_cost}.")
st.write(f"##### The percent chance the cost goes over {max_amount} is {percent_change_over}%.")

col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(data_frame=user_time_spent, title="Total Time Spent")
    fig.update_traces(xbins=dict(start=0, end=100, size=5))
    st.plotly_chart(fig)

with col2:
    fig2 = px.histogram(data_frame=my_sample, title="Sample Time Spent")
    fig.update_traces(xbins=dict(start=0, end=100, size=5))
    st.plotly_chart(fig2)
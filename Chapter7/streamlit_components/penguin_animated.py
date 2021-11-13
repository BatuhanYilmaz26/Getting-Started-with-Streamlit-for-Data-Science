import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# website of the animations -> https://lottiefiles.com
# github page of the streamlit_lottie library -> https://github.com/andfanilo/streamlit-lottie
# define a function that we can use to load lottie files from a link.
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_penguin = load_lottieurl('https://assets5.lottiefiles.com/private_files/lf30_ttgwkuhd.json')
st_lottie(lottie_penguin, height=200)

# Get user input for penguin features
st.title("Palmer's Penguins")
st.markdown('Use this Streamlit app to make your own scatterplot about penguins!')
selected_x_var = st.selectbox('What do want the x variable to be?', 
  ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']) 
selected_y_var = st.selectbox('What about the y?', 
  ['bill_depth_mm', 'bill_length_mm', 'flipper_length_mm', 'body_mass_g'])

penguin_file = st.file_uploader('Select Your Local Penguins CSV (default provided)')

# Get the dataset from the user (optional)
@st.cache()
def load_file(penguin_file):
    if penguin_file is not None:
        df = pd.read_csv(penguin_file)
    else:
        df = pd.read_csv("penguins.csv")
    return df

penguins_df = load_file(penguin_file)

# Plot the penguin data for selected features
sns.set_style('darkgrid')
markers = {"Adelie": "X", "Gentoo": "s", "Chinstrap":'o'}
fig, ax = plt.subplots()
ax = sns.scatterplot(x = penguins_df[selected_x_var], y = penguins_df[selected_y_var],
    hue=penguins_df["species"], markers=markers, style=penguins_df["species"])
plt.xlabel(selected_x_var)
plt.ylabel(selected_y_var)
plt.title("Scatterplot of Palmer's Penguins")
st.pyplot(fig)

# Use pandas profiling for automated EDA.
st.write("## Pandas Profiling of Palmer's Penguins Dataset")
penguin_profile = ProfileReport(penguins_df, explorative=True)
st_profile_report(penguin_profile)
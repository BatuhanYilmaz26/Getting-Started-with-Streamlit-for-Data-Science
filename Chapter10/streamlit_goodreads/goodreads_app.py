from re import S
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_lottie import st_lottie
import requests

st.set_page_config(layout="wide")

# define a function that we can use to load lottie files from a link.
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

file_url = "https://assets9.lottiefiles.com/packages/lf20_Q895iE.json"
lottie_book = load_lottieurl(file_url)
st_lottie(lottie_book, speed=1, height=200, key="initial")

st.write("""
## Analyzing Your Goodreads Reading Habits
### A Web App by Batuhan Yilmaz \n
Hey there! Welcome to Batuhan's Goodreads Analysis App. \n
This app analyzes (and never stores!) the books you've read using the popular service Goodreads,
including looking at the distribution of the age and length of books you've read. \n
Give it a go by uploading your data below!
""")

goodreads_file = st.file_uploader("Please Import Your Goodreads Data")
if goodreads_file is None:
    books_df = pd.read_csv("goodreads_history.csv")
    st.write("Analyzing Batuhan's Goodreads history")
else:
    books_df = pd.read_csv(goodreads_file)
    st.write("Analyzing your Goodreads history")

st.write(books_df.head())

books_finished = books_df[books_df["Exclusive Shelf"] == "read"]
unique_book_count = len(books_finished["Book Id"].unique())
unique_author_count = len(books_finished["Author"].unique())
mode_author = books_finished["Author"].mode()[0]
st.write(f"##### It looks like you have finished {unique_book_count} books with a total of {unique_author_count} unique authors.")
st.write(f"##### Your most read author is {mode_author}!")

st.write("""
Your app results can be found below, we have analyzed everything from your book length
distribution to how you rate books.\n
Take a look around, all the graphs are interactive!
""")
# How many books do I read each year? 
    # Convert our column into datetime format.
    # Extract the year from the Date Read column.
    # Group the books by this column and make a count for books per year.
    # Graph this using Plotly.
books_df["Year Finished"] = pd.to_datetime(books_df["Date Read"]).dt.year
books_per_year = books_df.groupby("Year Finished")["Book Id"].count().reset_index()
books_per_year.columns = ["Year Finished", "Count"]

col1, col2= st.columns(2)
with col1:
    mode_year_finished = int(books_df["Year Finished"].mode()[0])
    fig_year_finished = px.bar(data_frame=books_per_year, x="Year Finished",
        y="Count", title="Books Finished per Year")
    st.plotly_chart(fig_year_finished)
    st.write(f"You finished the most books in {mode_year_finished}.\n\n Awesome job! ")

# How long does it take for me to finish a book that I have started?
    # Convert the "Date Read" and "Date Added" columns into datetime format.
    # Find the difference between the two columns in days.
    # Plot this difference in a histogram.
books_df["days_to_finish"] = (pd.to_datetime(
    books_df["Date Read"]) - pd.to_datetime(books_df["Date Added"])).dt.days

# Filter the dataset to just include books where the number of days is positive 
# AND(&) filtering the data to only finished books.
books_df["days_to_finish"] = (pd.to_datetime(
    books_df["Date Read"]) - pd.to_datetime(books_df["Date Added"])).dt.days
books_finished_filtered = books_df[(books_df["Exclusive Shelf"] == "read") 
    & (books_df["days_to_finish"] >= 0)]

with col2:
    fig_days_finished = px.histogram(data_frame=books_df, x="days_to_finish",
    title="Count of the Number of Days to finish a book")
    st.plotly_chart(fig_days_finished)

    
col3, col4= st.columns(2)
with col3:
    fig_days_finished_filtered = px.histogram(data_frame=books_finished_filtered,
        x="days_to_finish", title="Count of the Number of Days to finish a book(filtered)",
        labels={"days_to_finish": "days"})
    st.plotly_chart(fig_days_finished_filtered)

    mean_days_to_finish = int(books_finished_filtered["days_to_finish"].mean())
    st.write(f"It took you an average of {mean_days_to_finish} days between when the book was added to Goodreads and when you finished the book.")
    st.write("This is not a perfect metric, as you may have added this book to a to-read list!")


# How long are the books that I have read?
    # This information already exists in the dataset.
with col4:    
    fig_num_pages = px.histogram(data_frame=books_df, x="Number of Pages",
        title="Book Length Histogram")
    st.plotly_chart(fig_num_pages)

    avg_pages = int(books_df["Number of Pages"].mean())
    st.write(f"Your books are an average of {avg_pages} pages long, check out the distribution above!")

# How old are the books that I have read?
    # The code block below checks if the original publication year is 
    # later than the publication year.
# st.write("Assumption check")
# st.write(len(books_df[books_df["Original Publication Year"] > books_df["Year Published"]]))
# When we run this, the app should return zero books with the original publication year
# as greater than the year published. 

# Now that we have checked this assumption, we can do the following:
    # 1. Group the books by the original publication year.
    # 2. Plot this on a bar chart.
col5, col6= st.columns(2)
books_publication_year = books_df.groupby("Original Publication Year")["Book Id"].count().reset_index()
books_publication_year.columns = ["Year Published", "Count"]
with col5:
    fig_year_published = px.bar(data_frame=books_publication_year, x="Year Published",
        y="Count", title="Book Age Plot")
    st.plotly_chart(fig_year_published)


# At first glance, this graph does not appear to be incredibly useful, as there are quite a few
# books written so far back in history (for example, Plato's writings in -375 BCE) 
# that the entire graph is hard to read.
# We can set a default zoom state for the graph and also alert users at the bottom 
# that they can zoom in as they'd like.
books_publication_year = books_df.groupby("Original Publication Year")["Book Id"].count().reset_index()
books_publication_year.columns = ["Year Published", "Count"]
st.write("Here you can see the books sorted by Original Publication Year in ascending order.")
st.write(books_df.sort_values(by="Original Publication Year").head())
with col6:
    fig_year_published = px.bar(data_frame=books_publication_year, x="Year Published",
        y="Count", title="Book Age Plot")
    fig_year_published.update_xaxes(range=[1850, 2021])
    st.plotly_chart(fig_year_published)
    st.write("""This chart above has been zoomed into the period of 1850-2021, but is 
    interactive so try zooming in/out on interesting periods! 
    (Double-click the chart to undo it.)""")

# How do I rate books compared to other Goodreads users?
    # 1. Filter the books according to the ones we have rated (and, therefore, read).
    # 2. Create a histogram of the average rating per book for our first graph.
    # 3. Create another histogram for your own ratings.
books_rated = books_df[books_df["My Rating"] != 0]
col7, col8 = st.columns(2)
with col7:
    fig_my_rating = px.histogram(data_frame=books_rated, x="My Rating",
        title="User Rating")
    st.plotly_chart(fig_my_rating)

    avg_my_rating = round(books_rated["My Rating"].mean(), 2)
    st.write(f"You rate books an average of {avg_my_rating} stars on Goodreads.")

with col8:
    fig_avg_rating = px.histogram(data_frame=books_rated, x="Average Rating",
        title="Average Goodreads Rating")
    st.plotly_chart(fig_avg_rating)

# We can also calculate whether, on average, we rate books higher or lower than the Goodreads average.
avg_difference = np.round(np.mean(books_rated["My Rating"] - books_rated["Average Rating"]), 2)
if avg_difference >= 0:
    sign = "higher"
else:
    sign = "lower"
st.write(f"###### You rate books {sign} than the average Goodreads user by {abs(avg_difference)}!")
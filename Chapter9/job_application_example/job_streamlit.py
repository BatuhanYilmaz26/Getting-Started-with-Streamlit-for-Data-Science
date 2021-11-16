import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import requests

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_airplane = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_tCIUzD.json")
st_lottie(lottie_airplane, speed=1, height=200, key="initial")

st.write("""
## Major US Airline Job Application
by Batuhan Yilmaz
#### Question 1: Airport Distance
The first exercise asks us,

    Given the table of airports and locations (in latitude and longitude) below,
    write a function that takes an airport code as input and returns the airports 
    listed from nearest to furthest from the input airport.
There are four steps here:
- Load the data.
- Implement distance algorithm.
- Apply distance formula across all airports other than the input.
- Return sorted list of airports distance
""")

airport_distance_df = pd.read_csv("airport_location.csv")
# st.echo() -> Use in a `with` block to draw some code on the app, then execute it.
with st.echo():
    #load necessary data
    airport_distance_df = pd.read_csv("airport_location.csv")

st.write("""
- From some quick googling, I found that the Haversine Distance is a good approximation for distance.
At least good enough to get the distance between airports!
- Haversine distances can be off by up to 0.5%, because the earth is not actually a sphere.
    - It looks like the latitudes and longitudes are in degrees, so I'll make sure to have a way to account that as well.
- The haversine distance formula is labeled below, followed by an implementation in python.
""")
st.image("haversine.png")

# Print out the Haversine Distance function on the Streamlit app.
with st.echo():
    from math import radians, sin, cos, atan2, sqrt
    def haversine_distance(long1, lat1, long2, lat2, degrees=False):
        # degrees vs radians
        if degrees == True:
            long1 = radians(long1)
            lat1 = radians(lat1)
            long2 = radians(long2)
            lat2 = radians(lat2)
        
        #implementing haversine
        a = sin((lat2-lat1) / 2)**2 + cos(lat1) * cos(lat2) * sin((long2-long1) / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = 6371 * c # radius of earth in kilometers
        return(distance)

# execute haversine function definition
from math import radians, sin, cos, atan2, sqrt

def haversine_distance(long1, lat1, long2, lat2, degrees=False):
    #degrees vs radians
    if degrees == True:
        long1 = radians(long1)
        lat1 = radians(lat1)
        long2 = radians(long2)
        lat2 = radians(lat2)
    
    #implementing haversine
    a = sin((lat2-lat1) / 2)**2 + cos(lat1) * cos(lat2) * sin((long2-long1) / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = 6371 * c #radius of earth in kilometers
    return(distance)

# We have completed our Haversine implementation! 
# Whenever we want to find the distance between two locations, we can call our formula, 
# input the longitude and latitude, and get the distance in kilometers.

st.write("""
Now, we need to test out our function!\n
The distance between the default point is 18,986 kilometers, 
but feel free to try out your own points of interest.
""")

long1 = st.number_input("Longitude 1", value = 2.55)
long2 = st.number_input("Longitude 2", value = 172.00)
lat1 = st.number_input("Latitude 1", value = 49.01)
lat2 = st.number_input("Latitude 2", value=-43.48)

test_distance = haversine_distance(long1=long1, long2=long2,
    lat1=lat1, lat2=lat2, degrees=True)

st.write(f"Your distance is: {round(test_distance, 2)} kilometers.")

st.write("""\n
We have the Haversine Distance implemented, and we also have proven to ourselves
that it works reasonably well.\n
Our next step is to implement this in a function!
""")

# Print out the get_distance_list function on the Streamlit app.
with st.echo():
    def get_distance_list(airport_dataframe, airport_code):
	    df = airport_dataframe.copy() #creates a copy of our dataframe for our function to use
	    row = df[df.loc[:,'Airport Code'] == airport_code] #selects the row from our airport code input
	    lat = row['Lat'] #get latitude
	    long = row['Long'] #get longitude
	    df = df[df['Airport Code'] != airport_code] #filter out our airport, implement haversine distance
	    df['Distance'] = df.apply(lambda x: haversine_distance(lat1=lat, long1=long, 
	    	lat2 = x.Lat, long2 = x.Long, degrees=True), axis=1)
	    return(df.sort_values(by='Distance').reset_index()['Airport Code']) #return values sorted

def get_distance_list(airport_dataframe, airport_code):
    df = airport_dataframe.copy()
    row = df[df.loc[:, "Airport Code"] == airport_code]
    lat = row["Lat"]
    long = row["Long"]
    df = df[df["Airport Code"] != airport_code]
    df["Distance"] = df.apply(lambda x: haversine_distance(lat1=lat, long1=long,
        lat2=x.Lat, long2=x.Long, degrees=True), axis=1)
    return(df.sort_values(by="Distance").reset_index()["Airport Code"])

st.write("""
To use this function, select an airport from the airports provided in the dataframe
and this application will find the distance between each one, and 
return a list of the airports closest to furthest.
""")

selected_airport = st.selectbox(label = "Airport Code", 
    options = airport_distance_df["Airport Code"])
distance_airports = get_distance_list(airport_dataframe = airport_distance_df,
    airport_code = selected_airport)

st.write(f"##### Your closest airports in order are: {list(distance_airports)}")

st.write("""\n
This all seems to work just fine! \n
There are a few ways I would improve this if I was working on 
this for a longer period of time.  
- I would implement the [Vincenty Distance](https://en.wikipedia.org/wiki/Vincenty%27s_formulae) 
instead of the Haversine distance, which is much more accurate but cumbersome to implement.  
- I would vectorize this function and make it more efficient overall.
    - Because this dataset is only 7 rows long, it wasn't particularly important,
     but if this was a crucial function that was run in production we would want to vectorize it for speed. 
""")

st.write("""
#### Question 2: Representation
For this transformation, there are a few things that I would start with. 
- First, I would have to define what a unique trip actually was. 
    - In order to do this, I would  group by the origin, the destination, and the departure date 
    (for the departure date, often customers will change around this departure date, 
    so we should group by the date plus or minus at least 1 buffer day to capture all the correct dates).   
- Additionally, we can see that often users search from an entire city, 
and then shrink that down into a specific airport. 
    - So we should also  consider a group of individual queries from cities and airpots 
    in the same city, as the same search, and do the same for destination.    
- From that point, we should add these important columns to each unique search.
""")

# Now, we can think of some columns that would be useful for when we are making
#a representation of when a user is searching for flights on this major US airline. 
# We can put them into an example dataframe, as follows:
example_df = pd.DataFrame(columns=["user_id", "number_of_queries", "round_trip",
    "distance", "number_of_unique_destinations", "number_of_unique_origins",
    "datetime_first_searched", "average_length_of_stay", "length_of_search"])

example_row = {"user_id": 98593, "number_of_queries": 5, "round_trip": 1,
    "distance": 893, "number_of_unique_destinations": 5,
    "number_of_unique_origins": 1, "datetime_first_searched": "2015-01-09",
    "average_length_of_stay": 5, "length_of_search": 4}

st.write(example_df.append(example_row, ignore_index=True))

st.write("""
- For answering the second part of the question, we should take the euclidian distance 
on two normalized vectors. 
- There are two solid options for comparing two entirely numeric rows, the euclidian distance
(which is just the straight line difference between two values), and the manhattan distance
(think of this as the distance traveled if you had to use city blocks to travel diagonally across manhattan). 
- Because we have normalized data, and the data is not high dimensional or sparse, I would recommend using the euclidian distance to start off. 
    - This distance would tell us how similar two trips were.
""")
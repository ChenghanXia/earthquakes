from datetime import date
import requests
import matplotlib.pyplot as plt
import json
from collections import defaultdict
import numpy as np

def get_data():
    """Retrieve the data we will be working with."""
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )


    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_by_year = defaultdict(list)
    for quake in earthquakes:
        year = get_year(quake)
        magnitude = get_magnitude(quake)
        if magnitude:  # Skip earthquakes without magnitude data
            magnitudes_by_year[year].append(magnitude)
    return magnitudes_by_year


def plot_average_magnitude_per_year(earthquakes):
    counts_by_year = defaultdict(int)
    for quake in earthquakes:
        year = get_year(quake)
        counts_by_year[year] += 1

    years = sorted(counts_by_year.keys())
    counts = [counts_by_year[year] for year in years]

    plt.bar(years, counts, color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.title('Number of Earthquakes Per Year')
    plt.xticks(np.arange(min(years), max(years)+1, step=2), rotation=45)
    plt.tight_layout()
    plt.show()


def plot_number_per_year(earthquakes):
    """Plot the average magnitude of earthquakes per year."""
    magnitudes_by_year = get_magnitudes_per_year(earthquakes)
    
    years = sorted(magnitudes_by_year.keys())
    avg_magnitudes = [np.mean(magnitudes_by_year[year]) for year in years]
    
    plt.plot(years, avg_magnitudes, marker='o', color='orange')
    plt.xlabel('Year')
    plt.ylabel('Average Magnitude')
    plt.title('Average Earthquake Magnitude Per Year')
    plt.xticks(np.arange(min(years), max(years)+1, step=2), rotation=45)
    plt.tight_layout()
    plt.show()



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
# Add Matplotlib inline magic command
#matplotlib inline
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd

# File to Load (Remember to change these)
city_data_to_load = "Resources/city_data.csv"
ride_data_to_load = "Resources/ride_data.csv"

# Read the City and Ride Data
city_data_df = pd.read_csv(city_data_to_load)
ride_data_df = pd.read_csv(ride_data_to_load)
# Combine the data into a single dataset
pyber_data_df = pd.merge(ride_data_df, city_data_df, how="left", on=["city", "city"])

# Display the data table for preview
pyber_data_df.head()
#  1. Get the total rides for each city type
rides_by_type = pyber_data_df.groupby(["type"]).count()["ride_id"]
# 2. Get the total drivers for each city type
drivers_by_type = city_data_df.groupby(["type"]).sum()["driver_count"]
fares_by_type = pyber_data_df.groupby(["type"]).sum()["fare"]
avg_fare_per_ride = fares_by_type / rides_by_type
avg_fare_per_driver = fares_by_type / drivers_by_type
pyber_summary_df = pd.DataFrame({
    "Total Rides": rides_by_type,
    "Total Drivers": drivers_by_type,
    "Total Fares": fares_by_type,
    "Average Fare per Ride": avg_fare_per_ride,
    "Average Fare per Driver": avg_fare_per_driver})
#  7. Cleaning up the DataFrame. Delete the index name
pyber_summary_df.index.name = None
#  8. Format the columns.
pyber_summary_df["Total Rides"] = pyber_summary_df["Total Rides"].map("{:,}".format)
pyber_summary_df["Total Drivers"] = pyber_summary_df["Total Drivers"].map("{:,}".format)
pyber_summary_df["Total Fares"] = pyber_summary_df["Total Fares"].map("${:,.2f}".format)
pyber_summary_df["Average Fare per Ride"] = pyber_summary_df["Average Fare per Ride"].map("${:,.2f}".format)
pyber_summary_df["Average Fare per Driver"] = pyber_summary_df["Average Fare per Driver"].map("${:,.2f}".format)
pyber_summary_df

# 1. Using groupby() to create a new DataFrame showing the sum of the fares
#  for each date where the indices are the city type and date.
fares_by_type_date_df = pyber_data_df.groupby(["type", "date"]).sum()[["fare"]]

# 2. Reset the index on the DataFrame you created in #1. This is needed to use the 'pivot()' function.
fares_by_type_date_df = fares_by_type_date_df.reset_index()

# 3. Create a pivot table with the 'date' as the index, the columns ='type', and values='fare'
# to get the total fares for each type of city by the date.
fares_type_date_pivot = fares_by_type_date_df.pivot(index="date", columns="type", values="fare")
fares_type_date_pivot.head(10)

# 4. Create a new DataFrame from the pivot table DataFrame using loc on the given dates, '2019-01-01':'2019-04-29'.
jan_to_apr_df = fares_type_date_pivot.loc['2019-01-01': '2019-04-29']
jan_to_apr_df.head(10)

# 5. Set the "date" index to datetime datatype. This is necessary to use the resample() method in Step 8.
jan_to_apr_df.index = pd.to_datetime(jan_to_apr_df.index)

# 6. Check that the datatype for the index is datetime using df.info()
jan_to_apr_df.info()

# 7. Create a new DataFrame using the "resample()" function by week 'W' and get the sum of the fares for each week.
jan_to_apr_month_df = jan_to_apr_df.resample("W").sum()

# 8. Using the object-oriented interface method, plot the resample DataFrame using the df.plot() function.
ax = jan_to_apr_month_df.plot(figsize=(15, 6))

# Add y-axis label
ax.set_ylabel("Fare ($USD)")
# Remove x-axis label
x_axis = ax.axes.get_xaxis()
x_label = x_axis.get_label()
x_label.set_visible(False)
# Add title
ax.set_title("Total Fare by City Type")
# Legend formatting
lgnd = plt.legend(loc="center", title="type")

# Import the style from Matplotlib.
from matplotlib import style
# Use the graph style fivethirtyeight.
style.use('fivethirtyeight')

# Save the figure
plt.savefig("analysis/PyBer_fare_summary.png")

plt.show()
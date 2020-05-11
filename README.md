# SQLAlchemyHW

## Step 1 - Climate Analysis and Exploration

* Create engine:
<code>engine = create_engine("sqlite:///Resources/hawaii.sqlite")</code>

* Reflect tables into classes:
<code>Base = automap_base()
Base.prepare(engine, reflect=True)</code>

### Precipitation Analysis
* Query for last 12 months of prcp data & plot the results
<code>data = session.query(Measurement.date, Measurement.prcp)\
.filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
df = pd.DataFrame(data).set_index('date')
df.plot(rot=90)
plt.show()</code>


* Pandas Summary Statistics
<code>df.describe()</code>

### Station Analysis

* Calculate the total number of stations and find the most active station
<code>data2 = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station)\
.order_by(func.count(Measurement.station).desc()).all()
data2</code>

Most Active Station: "USC00519281"

* Query to retrieve the last 12 months of temperature observation data (TOBS).
<code>histdata = session.query(Measurement.tobs).\
filter(Measurement.station == 'USC00519281')\
.filter(Measurement.date >= '2016-08-23').all()</code>
histdata
<br>
<code>pd.DataFrame(histdata).plot.hist(bins =12)</code>


- - -

## Step 2 - Climate App

Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

* Use Flask to create your routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  
  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


- - -

## Bonus: Temperature Analysis

The starter notebook contains a function called `calc_temps` that will accept a start date and end date in the format `%Y-%m-%d`. The function will return the minimum, average, and maximum temperatures for that range of dates.
<code>def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.  </code>
    <code>Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d  
    Returns:
        TMIN, TAVE, and TMAX</code>
   <code> """
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
print(calc_temps('2012-02-28', '2012-03-05'))</code>

Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
for your trip using the previous year's data for those same dates.
<code>def calc_temps(start_date, end_date):</code>
     <code>return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
temp = calc_temps('2012-02-28', '2012-03-03')[0]
print(temp)</code>

Plot the results from your previous query as a bar chart. 
Use "Trip Avg Temp" as your Title
Use the average temperature for the y value
Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)

<code>
x_axis = 1
tick_locations = temp
plt.bar(x_axis, temp[2], color='r', alpha=0.5, align="center", yerr = temp[2]-temp[0])
plt.title("Trip Avg Temp")
plt.ylabel("Temp")
plt.grid(axis = 'both')
plt.tight_layout()
plt.show()
</code>

Create a query that will calculate the daily normals 
(i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)
<code>
def daily_normals(date):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
daily_normals("01-01")</code>

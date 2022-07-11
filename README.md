# fremont-bridge-bike-predictor
This application uses historical Fremont bridge bike crossing data from the city of Seattle and weather data from open weather to generate a linear regression for predicting the number of bikes to cross the Fremont bridge based on forecasted temperature.

## Requirements

* Open Weather API Key 
  * https://openweathermap.org/
  * Must have One Call by Call subscription access
  * Saved as OPEN_WEATHER_API_KEY in .env file
* Fremont Bridge Bicycle Counter API Key
  * https://data.seattle.gov/Transportation/Fremont-Bridge-Bicycle-Counter/65db-xm6k
  * Saved as FREMONT_API_KEY in .env file
* Requests
* Pandas
* Numpy

## Process

### Load historical Fremont bridge bike data
The Fremont bridge bike traffic is pulled using an API pull through requests. The API response is read into a dataframe where it is manipulated to remove the northbound and southbound traffic columns. The data is provided on an hourly basis therefore it is transformed into one value per day by grouping by the dates and summing the total crossings. 

### Load historical Temperature data
The historical temperature data is added to the dataframe for each of the dates. The temperature is taken from the Open Weather API historical data and is taken as of 2pm for each date using the latitude and longitude of the Fremont bridge. The date is converted into epoch time and is sent through an API request to grab the temperature and added to the dataframe. 

### TO BE COMPLETED
* Run the linear regression in Numpy using the compiled dataframe

* Use forecast API to allow user to enter date and retrieve forecasted temp
  * Return predicted number of bicycles crossing bridge based on forecast temp

* Create command prompt user interface to interact with program
  * Option 1: Load historical data & run linear regression
  * Option 2: Enter date to get forecast and return num of bike crossings based on regression
  * Option 3: Enter temperature and return num of bike crossings based on regression
  * Option 4: Exit

## Limitations

The Fremont Bridge API pull is limited to only 1000 rows and includes a row for every hour, therefore there is only around 40 days worth of data in the final dataframe. This limited sample size will not be a great representation for an accurate analysis. Additionally, a simple linear regression is not the best model to use for this question. Many factors besides temperature influence the number of riders, such as precipitation, day of week, and events in the city to name a few. 

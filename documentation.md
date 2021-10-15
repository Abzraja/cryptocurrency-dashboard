# Crypto Decryption

## Background

This project was devised to visually present live data about crypto-currency values and trades, with the aim of helping to inform decisions for investors and potential investors.

To make the project viable with the resource and time available, data was sourced from one location (the Binance API), and is only obtained and presented for five pre-selected coins and in relation to GBP (pound sterling).

Data is obtained API calls to the Binance API, and stored in a local SQLite database. This data is served to the output webpages through a Flask application.

Output is presented in a series of HTML pages, each one showing one visualisation. The user can customise each visualisation, as explained below.

## Installation
The code for obtaining, storing and serving the data and web pages is in Python. Visualisations are presented using JavaScript.

The file <requirements.txt> lists the Python installation requirements for the project, as shown below. Any web browser with JavaScript capability is able to render the HTML and visualisations.

**List requirements**

A valid API_KEY and API_SECRET for the Binance API will be required, contained within a local config.py file.

## Deployment
The repository requires both the following python files to be running live:  
* app.py (web server and database management)
* live_update.py (live data)

The visualisations are accessed from the root on the web server (e.g. http://127.0.0.1/)

## User interactions
All visualisations are presented for the following five coins:
1. Bitcoin
2. Etherium
3. Ada
4. Ripple
5. Solana

### Line chart

This chart shows, for each of the coins, the trade data over a selected time period. The user can select both the time period (365 days, 30 days, 7 days) and whether the chart shows the volume of trades made, or the number of trades. Data is presented for each day within the chosen time period.

The user can additionally turn each data line on or off to further customise the visualisation.

### Historical candlestick chart

This chart shows data for each day in the historical period (one year). Each day shows:
* Open and close values, as a thick bar between the two values
* High and low values, as thin lines extending beyond the open and close values (as appropriate)

The candlestick chart shows how the data changes day by day, with the bar for one day following on from the previous day. A bar coloured red indicates that the close value was lower than the open value (the coin lost value) whereas a bar coloured green indicates the close value was higher than the open value (the coin gained value).

The user can interact with the chart by selecting which coin is displayed, and also zooming in and out of the chart on dates of particular interest.

### Live candlestick chart

This chart has the same functionality as the historical chart, but uses live data. The data is presented for each minute over the previous day, and is updated each minute as new data is available.

The user can  interact with the chart by selecting which coin is displayed, and also zooming in and out of the chart.

## Code details
The code consists of three Python scripts and three JavaScript files. The Python scripts are used for obtaining, storing and serving the data, with the JavaScript files used to retrieve the data and present them in visualisations.

The details of each script is given below. Code excerpts are not presented.

### Python
#### historical_api.py
This file interacts with the Binance API through the Python library python_binance.

Two functions are provided, both with near identical functionality. Each function returns data from the Binance API, the differences being the time period and interval of the data collected:  

Function | Time interval | Time period
-------- | ------------- | -----------
historical_api_call | 1 day | 1 year
shortinterval_api_call | 1 minute | 1 day

For each function the process is identical.

1. Define the dates/times for the API connection
2. Define the crypto coin handles to be collected
3. For each coin, connect to the Binance API, collect the data and store the results in a list of result containers
4. Loop through the result containers, process the data and store in a Pandas dataframe

Each function returns the API data as a processed and formatted Pandas dataframe

#### app.py

This is the primary Python file, containing the Flask application and the interaction with the SQLite database

**Binance data**  
It commences by obtaining the two datasources from binance.py, which are returned as Pandas dataframes. These dataframes are then stored in the SQLite database for later retrieval.

The functions are set to collect fresh data at regular intervals which are stored in the database. The short_interval data updates at 60 second intervals, with the historical data updating every 600 seconds. This ensures that any data retrieval calls from our application uses the latest data. Limiting our application to the local database reduces the number of calls to the external API, allowing a number of users to interact with the charts on a frequent basis, and helps manage the flow of data.

**Flask application**  
The remainder of the script consists of a Flask application, serving both static webpages (with JavaScript visualisations) and the data from the SQLite database as an API.

There are four Flask routes to serve HTML files; these are static files from the 'templates' folder with JavaScript functionality discussed below.

Additional routes are available for each chart, to retrieve the data from the SQLite database and present them for use. In each case, the data is presented as a JSON file.

*linechart*  
This route extracts and returns the following data for all coins, to be presented on a single chart:

* Coin handle
* Date
* Volume of trades on that date
* Number of trades on that date

The JSON return is structured as:  
{id: {dictionary of data}}

*historical/`<coin>`*  
The route extracts and returns the following data for the requested coin. This is used for the candlestick chart

* Coin handle
* Date
* Open value on that date
* Close value on that date
* High value on that date
* Low value on that date
* Volume of trades on that date
* Number of trades on that date

The JSON return is structured as:  
{id: {dictionary of data}}

*shortinterval/`<coin>`*  
This route extracts the same data as the historical data, but from the short_interval table in the database.

*sumtrades*  
An additional route is available but not presently used in visualisations with this application. It returns, for each coin, the sum of the number of trades made within the time covered in the database (one year).

The JSON return is structured as:  
{coin: sum_of_trades} 

#### live_update.py
This file obtains the same data as in historical_data, but uses a websocket to do so on a live basis, returning data whenever the source is updated.

### JavaScript
#### line-chart.js
This script uses the LightweightCharts library to produce a line chart of data, using the D3 library to call and process a JSON API call to the local database.

Additional D3 processes are used to create and react to user interactions:  
* A dropdown for time period (365 days, 30 days, 7 days)
* Buttons for each line source

A separate user interaction exists in the HTML code to choose between volume traded or number of trades in a day.

After initialising the chart space, the script calls the main chart display function to present the initial chart. This uses D3 to obtain the JSON file and processes it into an array based on the user selection between 'volume' and 'trade'.

The data is then processed further to reform the data into a series for each coin. A supplementary function converts the time to a Unix timestamp and sets the visible range to the range selected by the user. Tooltips are prepared for each point on the chart, displaying the date as a string together with the appropriate datapoint.

Each time either of the dropdowns are changed, the chart display function is called to display the required data.

#### hist-cs-chart.js
This script uses the LightweightCharts library to create a candestick chart, using the D3 library to call and process a JSON API call to the local database.

Selection boxes are created for the list of coins and the available time options (365 days, 30 days, 7 days). 

After initialising the chart space, the script calls the main chart display function to present the initial chart. This uses D3 to obtain the JSON file of data for the selected coin. This data is passed to the chart to be visualised. A supplementary function converts the time to a Unix timestamp and sets the visible range to the range selected by the user.

Each time either of the selections are changed, the chart display function is called to display the required data.
# Project #3: Crypto Decryption 
 
 ## Contents

* [Team Members](#team_members)
* [Project Proposal](#project_header)

## <a id="team_members"></a>Team Members

* [Abdurrahman Raja](https://github.com/Abzraja)
* [James Lilley](https://github.com/jimbleslilley)
* [Serdar Bayramov](https://github.com/serdar-bayramov)
* [Tom Oldershaw](https://github.com/TomHOldershaw)


## <a id="project_header"></a>Project Proposal

### Project Overview

The project focuses on cryptocurrencies and providing our users with a tool which allows them to observe insights into the top seven* cryptocurrencies. 
We would like our users to be able to use the visualisations presented to find out more about these selected cryptocurrencies and their recorded past. 

*The top seven would be based on popularity from an API search. 


### Data Sources

Our data will either be pulled from Binance or Coin Gecko's APIs.
We are going to explore the information obtainable from each to decide which is the most appropriate. 

[Binance API](https://binance-docs.github.io/apidocs/spot/en/#general-info)


[CoinGecko API](https://www.coingecko.com/en/api)




### Overview of Visualisations 

We hope to visualise the following three points: 

* Top seven crypto plot - gives user overview of data (data range needs to be specified)
* [Bar Chart Race](https://observablehq.com/@d3/bar-chart-race) to show all seven cryptos over the past two years. (Replay button / filter for data to race) 
* [Candlestick plot](https://www.amcharts.com/demos/stock-chart-candlesticks) last 20 days for a cryptocurrency (shows alphabetically first crypto, dropdown to choose others).


### Task Breakdown

**Flask Application (Python)**

* API call for top seven crypto.
* Return JSON to be read by Java Script.

**Java Script**

* Reads in data created by Flask Application
* Data Visualisation

**HTML**

* Website Layout

## <a id="project_retrospective"></a>Project Retrospective

Quickly into our project we decided on using Binance as our API of choice. We found the functionality and ease of use with Websocket higher with Binance. We could request to the API with two separate queries - one to collate a year's worth of data daily, and a second to collate a day's worth of data minute by minute. These two separate intervals of data were converted into Pandas dataframes and sqlite databases.


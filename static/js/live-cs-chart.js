// coins list to populate selection box
let coins = ["bitcoin","etherium","ripple","ada","solana"]

//populate selection box with coins list
for (i in coins) {
 d3.select("#selDataset").append("option").attr("value", `${coins[i]}_gbp`).text(coins[i]);
};

// Use D3 to select dropdown menu
var dropdownMenu = d3.select("#selDataset"); 

// Assign the value of the dropdown menu option to a variable
var coin = dropdownMenu.property("value");

// List of time ranges for selection box
let time_deltas = [{"Last 30 Minutes":1800}]


// create chart
var chart = LightweightCharts.createChart(document.body, {
    width: 1000,
  height: 500,
    layout: {
        // backgroundColor: '#000000',
        // textColor: 'rgba(255, 255, 255, 0.9)',
    },
    grid: {
        vertLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
        horzLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    },
    rightPriceScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
    timeScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
});

var candleSeries = chart.addCandlestickSeries({
//   upColor: 'rgba(255, 144, 0, 1)',
//   downColor: '#000',
//   borderDownColor: 'rgba(255, 144, 0, 1)',
//   borderUpColor: 'rgba(255, 144, 0, 1)',
//   wickDownColor: 'rgba(255, 144, 0, 1)',
//   wickUpColor: 'rgba(255, 144, 0, 1)',
});


// run function optionChanged and pass it variable coin
optionChanged(coin);

// function that is activated on page load and on selection box change
function optionChanged(coin, time_delta) {
     

    // pull from api
    d3.json(`/liveinterval/${coin}`).then(function(data) {


        // set data for chart
        candleSeries.setData(
            
            // Our data object is a dictionary of dictionaries so this returns the values for each key.
            Object.values(data)

            // this is just an example of the format of data expected
            // { time: '2018-10-19', open: 180.34, high: 180.99, low: 178.57, close: 179.85 },
        
        );

        //31 minutes in seconds
        time_delta = 1860;
        
        // run changeTime function
        changeTime(time_delta);
        
        
    });


};


function changeTime(time_delta) {
    
    // get current date in and convert to unix timestamp in seconds
    var last_date = new Date().getTime() / 1000;
    
    // set the time scale on chart
    chart.timeScale().setVisibleRange({
    from: last_date - time_delta,
    to: last_date,
    });
    }
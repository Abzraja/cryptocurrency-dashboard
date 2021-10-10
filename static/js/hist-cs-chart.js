// coins list to populate selection box
let coins = ["bitcoin_gbp","etherium_gbp","ripple_gbp","ada_gbp","solana_gbp"]

//populate selection box
for (i in coins) {
 d3.select("select").append("option").attr("value", coins[i]).text(coins[i]);
};

// Use D3 to select dropdown menu
var dropdownMenu = d3.select("#selDataset"); 

// Assign the value of the dropdown menu option to a variable
var coin = dropdownMenu.property("value");


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
function optionChanged(coin) {
     
    



    // pull from api
    d3.json(`/historical/${coin}`).then(function(data) {
        
        // adjust data for chart. change "date" key in object to "time".
        for (i in data) {
        data[i]["time"] = data[i]["date"]
        delete data[i]["date"]
        }

    
        
        // set data for chart
        candleSeries.setData(Object.values(data)
            
            // { time: '2018-10-19', open: 180.34, high: 180.99, low: 178.57, close: 179.85 },
        
        
        );

        



    });

};
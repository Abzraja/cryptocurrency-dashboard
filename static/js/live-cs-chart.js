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

var chart = LightweightCharts.createChart(document.body, {
	width: 900,
  	height: 450,
	localization: {
        priceFormatter: price =>
        // add £ sign before price
    
            '£' + Math.round(price*100)/100
        ,
    },
	layout: {
		//backgroundColor: '#000000',
		//textColor: 'rgba(255, 255, 255, 0.9)',
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
	priceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
		timeVisible: true,
		secondsVisible: false,
	},
});

var candleSeries = chart.addCandlestickSeries({
	upColor: '#00ff00',
	downColor: '#ff0000', 
	borderDownColor: 'rgba(255, 144, 0, 1)',
	borderUpColor: 'rgba(255, 144, 0, 1)',
	wickDownColor: 'rgba(255, 144, 0, 1)',
	wickUpColor: 'rgba(255, 144, 0, 1)',
});

// Run chart function
optionChanged(coin);

// Function to update chart data when coin is changed
function optionChanged(coin) {
    fetch(`/api/shortinterval/${coin}`)
	    .then((r) => r.json())
	    .then((response) => {

		    candleSeries.setData(Object.values(response));
	    })

    var cointag = "";

    if (coin === "bitcoin_gbp") {
        cointag = "btcgbp"
    } else if (coin === "etherium_gbp") {
        cointag = "ethgbp"
    } else if (coin === "ripple_gbp") {
        cointag = "xrpgbp"
    } else if (coin === "ada_gbp") {
        cointag = "adagbp"
    } else if (coin === "solana_gbp") {
        cointag = "solgbp"
    };


    var coinsocket = "wss://stream.binance.com:9443/ws/" + cointag + "@kline_1m";

    var binanceSocket = new WebSocket(coinsocket);

    binanceSocket.onmessage = function (event) {	
	    var message = JSON.parse(event.data);

	    var candlestick = message.k;

	    console.log(candlestick)

	    candleSeries.update({
            time: candlestick.t / 1000,
		    open: candlestick.o,
		    high: candlestick.h,
		    low: candlestick.l,
		    close: candlestick.c
	    })
    }

};


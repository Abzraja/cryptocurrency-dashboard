//coins list
var coins = [{"btc":"Bitcoin"}, {"eth":"Ethereum"}, {"xrp":"Ripple"}, {"ada":"Cardano"}, {"sol":"Solana"}]

// List of time ranges for selection box
let time_deltas = [{"Last 365 Days":31622400}, {"Last 90 Days":7862400}, {"Last 30 Days":2678400}, {"Last 7 Days":691200}]

//populate selection box with time ranges list
for (i in time_deltas) {
    d3.select("#selTime").append("option").attr("value", Object.values(time_deltas[i])).text(Object.keys(time_deltas[i]));
   };



//build chart

document.body.style.position = 'relative';

var container = document.createElement('div');
document.body.appendChild(container);

var width = 800;
var height = 400;

var chart = LightweightCharts.createChart(container, {
  rightPriceScale: {
    scaleMargins: {
      top: 0.2,
      bottom: 0.05,
    },
    borderVisible: false,
  },
  timeScale: {
    borderVisible: false,
  },
  layout: {
    backgroundColor: '#ffffff',
    textColor: '#333',
  },
  grid: {
    horzLines: {
      color: '#eee',
    },
    vertLines: {
      color: '#ffffff',
    },
  },
  crosshair: {
    vertLine: {
      labelVisible: false,
    },
  },
});

chart.resize(width, height);

// Button container
var btn_container = document.createElement('div');
btn_container.setAttribute("id", "buttons")
document.body.appendChild(btn_container);

// Select container and create buttons
for (i in coins) {
d3.select("#buttons").append("button").attr("type", "button").attr("id", Object.keys(coins[i])).attr("value", `${Object.keys(coins[i])}`).attr("onclick", "toggleSeries(this.value)").text(Object.values(coins[i]))
}

// Use D3 to select dropdown menu
var button = d3.select("#buttons"); 

// Assign the value of the dropdown menu option to a variable
var coin = button.property("value");

// Set flag variables
var btc_show = true;
var eth_show = true;
var xrp_show = true;
var ada_show = true;
var sol_show = true;

// Series visibility.
function toggleSeries(coin) {
//hidden=true;
if (coin === "btc") {
    if (btc_show === true) {
        btc_series.applyOptions({
        visible: false,
    })
        btc_show = false
    } else {
            btc_series.applyOptions({
            visible: true,
            })
            btc_show = true
        }
} else if (coin === "eth") {
    if (eth_show === true) {
    eth_series.applyOptions({
    visible: false,
    })
    eth_show = false
} else {
        eth_series.applyOptions({
        visible: true,
        })
        eth_show = true

}
} else if (coin === "xrp") {
    if (xrp_show === true) {
    xrp_series.applyOptions({
    visible: false,
    })
    xrp_show = false
} else {
    xrp_series.applyOptions({
        visible: true,
        })
        xrp_show = true
}
} else if (coin === "ada") {
    if (ada_show === true) {
    ada_series.applyOptions({
    visible: false,
    })
    ada_show = false
} else {
    ada_series.applyOptions({
        visible: true,
        })
        ada_show = true
}
} else if (coin === "sol") {
    if (sol_show === true) {
    sol_series.applyOptions({
    visible: false,
    })
    sol_show = false
} else {
    sol_series.applyOptions({
    visible: true,
    })
sol_show = true
}

}}


// BTC line
var btc_series = chart.addLineSeries({
    title: 'Bitcoin',
    color: 'rgba(242, 169, 0, 0.8)',
});

// ETH line
var eth_series = chart.addLineSeries({
    title: 'Ethereum',
    color: 'rgba(113, 107, 148, 0.8)',
});

// XRP line
var xrp_series = chart.addLineSeries({
    title: 'XRP',
    color: 'rgba(0, 96, 151, 0.8)',
});

// ADA line
var ada_series = chart.addLineSeries({
    title: 'Cardano',
    color: 'rgba(51, 51, 51, 0.8)',
});

// SOL line
var sol_series = chart.addLineSeries({
    title: 'Solana',
    color: 'rgba(0, 255, 163, 0.8)',
  });

function changeOption() {


// Use D3 to select dropdown menu
var dropdownMenu = d3.select("#selDataset"); 

// Assign the value of the dropdown menu option to a variable
var dataset = dropdownMenu.property("value");


// Use D3 to select time dropdown menu
var dropdownMenu2 = d3.select("#selTime"); 

// Assign the value of the dropdown menu option to a variable
var time_delta = dropdownMenu2.property("value");


// pull from api
d3.json(`/api/linechart`).then(function(data) {
			
    
        // if dataset value is trade then give "value" the value for "trade"
        if (dataset === "trade") {
            for (i in data) {
                data[i]["value"] = data[i]["trade"];
                delete data[i]["trade"];
            }
        } else if (dataset ==="volume") {
            for (i in data) {
                data[i]["value"] = data[i]["volume"];
                delete data[i]["volume"];
            }
        }

    data_array = Object.values(data)

    btc_data = data_array.filter(coin => coin.crypto == "bitcoin_gbp")
    eth_data = data_array.filter(coin => coin.crypto == "etherium_gbp")
    xrp_data = data_array.filter(coin => coin.crypto == "ripple_gbp")
    ada_data = data_array.filter(coin => coin.crypto == "ada_gbp")
    sol_data = data_array.filter(coin => coin.crypto == "solana_gbp")


// BTC Data
btc_series.setData(
    Object.values(btc_data)
    //how it wants the data
	// { time: "2018-03-28", value: 154 },
);

// ETH Data
eth_series.setData(
    Object.values(eth_data)
);

// XRP Data
xrp_series.setData(
    Object.values(xrp_data)
);


// ADA Data
ada_series.setData(
    Object.values(ada_data)
);


// SOL Data
sol_series.setData(
    Object.values(sol_data)
);


// function businessDayToString(businessDay) {
// 	return businessDay.year + '-' + businessDay.month + '-' + businessDay.day;
// }

// var toolTipWidth = 80;
// var toolTipHeight = 80;
// var toolTipMargin = 15;

// var toolTip = document.createElement('div');
// toolTip.className = 'floating-tooltip-2';
// container.appendChild(toolTip);

// // update tooltip
// chart.subscribeCrosshairMove(function(param) {
// 		if (param.point === undefined || !param.time || param.point.x < 0 || param.point.x > container.clientWidth || param.point.y < 0 || param.point.y > container.clientHeight) {
// 			toolTip.style.display = 'none';
// 		} else {
// 			const dateStr = businessDayToString(param.time);
// 			toolTip.style.display = 'block';
// 			var price = param.seriesPrices.get(series);
// 			toolTip.innerHTML = '<div style="color: #009688">Test Inc.</div><div style="font-size: 24px; margin: 4px 0px; color: #21384d">' + Math.round(100 * price) / 100 + '</div><div style="color: #21384d">' + dateStr + '</div>';
// 			var coordinate = series.priceToCoordinate(price);
// 			var shiftedCoordinate = param.point.x - 50;
// 			if (coordinate === null) {
// 				return;
// 			}
// 			shiftedCoordinate = Math.max(0, Math.min(container.clientWidth - toolTipWidth, shiftedCoordinate));
// 			var coordinateY = coordinate - toolTipHeight - toolTipMargin > 0 ? coordinate - toolTipHeight - toolTipMargin : Math.max(0, Math.min(container.clientHeight - toolTipHeight - toolTipMargin, coordinate + toolTipMargin));
// 			toolTip.style.left = shiftedCoordinate + 'px';
// 			toolTip.style.top = coordinateY + 'px';
// 		}
// });


// fun function changeTime
changeTime(time_delta);

// Close D3 Json function defintion
})


// Close changeOption function definition
}
changeOption();

function changeTime(time_delta) {
    
    // get current date in and convert to unix timestamp in seconds
    var last_date = new Date().getTime() / 1000;
    
    // set the time scale on chart
    chart.timeScale().setVisibleRange({
    from: last_date - time_delta,
    to: last_date,
    });
    }
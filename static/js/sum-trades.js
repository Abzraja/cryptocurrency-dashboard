// pull from api
d3.json(`/api/sumtrades`).then(function(data) {

coin_data = Object.values(data)

// sort data to use for plot
coins_list = []
values_list = []
colors_list = []
names_list = []
for (i in coin_data) {
  coins_list.push(coin_data[i]["coin"])
  values_list.push(coin_data[i]["sum"])
  colors_list.push(coin_data[i]["color"])
  names_list.push(coin_data[i]["name"])
}

// set traces
trace_list = []
for (i in coin_data) {
trace_list.push({
  x: [coins_list[i]],
  y: [values_list[i]],
  name: names_list[i],
  type: "bar",
  marker: {
    color: colors_list[i],
  }
})
}

// set chart data
var data = trace_list;

// set layout
var layout = {
  title:'Total Number of Trades in Last 365 Days',
  xaxis: {
    title: "Coin"
  },
  yaxis: {
    title: "Number of Trades"
  },
  showlegend:true
};

// plot chart
Plotly.newPlot('myDiv', data, layout);

})
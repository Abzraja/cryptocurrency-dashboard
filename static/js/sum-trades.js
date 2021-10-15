// pull from api
d3.json(`/api/sumtrades`).then(function(data) {

coin_data = Object.values(data)
console.log(coin_data)


coins_list = []
values_list = []
for (i in coin_data) {
  coins_list.push(coin_data[i]["coin"])
  values_list.push(coin_data[i]["sum"])
}
console.log(coins_list)
console.log(values_list)
var data = [
  {
    x: coins_list,
    y: values_list,
    type: 'bar',
    marker: {
      color: [ 'rgba(51, 51, 51, 0.8)', 'rgba(242, 169, 0, 0.8)', 'rgba(113, 107, 148, 0.8)', 'rgba(0, 96, 151, 0.8)', 'rgba(0, 255, 163, 0.8)']
    }
  }
];

Plotly.newPlot('myDiv', data);

})
// set the dimensions and margins of the graph
const margin = {top: 10, right: 30, bottom: 90, left: 40},
    width = 460 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// pull from api
d3.json(`/api/sumtrades`).then(function(data) {

coin_data = Object.values(data)
console.log(coin_data)

// X axis
const x = d3.scaleBand()
  .range([ 0, width ])
  .domain(coin_data.map(d => d.coin))
  .padding(0.2);
svg.append("g")
  .attr("transform", `translate(0,${height})`)
  .call(d3.axisBottom(x))
  .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");

// Add Y axis
const y = d3.scaleLinear()
  .domain([0, d3.max(coin_data, d => d.sum)])
  .range([ height, 0]);
svg.append("g")
  .call(d3.axisLeft(y));

// Bars
svg.selectAll("mybar")
  .data(coin_data)
  .join("rect")
    .attr("x", d => x(d.coin))
    .attr("width", x.bandwidth())
    .attr("fill", "#69b3a2")
    // no bar at the beginning thus:
    .attr("height", d => height - y(0)) // always equal to 0
    .attr("y", d => y(0))

// Animation
svg.selectAll("rect")
  .transition()
  .duration(800)
  .attr("y", d => y(d.sum))
  .attr("height", d => height - y(d.sum))
  .delay((d,i) => {console.log(i); return i*100})

})
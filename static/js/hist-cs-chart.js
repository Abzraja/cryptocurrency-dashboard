function optionChanged() {

    d3.json("/historical/bitcoin_gbp").then(function(data) {
        
        for (i in data) {
        data[i]["time"] = data[i]["date"]
        delete data[i]["date"]
        }
       


        var chart = LightweightCharts.createChart(document.body, {
            width: 600,
          height: 300,
            layout: {
                backgroundColor: '#000000',
                textColor: 'rgba(255, 255, 255, 0.9)',
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
          upColor: 'rgba(255, 144, 0, 1)',
          downColor: '#000',
          borderDownColor: 'rgba(255, 144, 0, 1)',
          borderUpColor: 'rgba(255, 144, 0, 1)',
          wickDownColor: 'rgba(255, 144, 0, 1)',
          wickUpColor: 'rgba(255, 144, 0, 1)',
        });
        
        candleSeries.setData(Object.values(data)
            
            // { time: '2018-10-19', open: 180.34, high: 180.99, low: 178.57, close: 179.85 },
        
        
        );

        



    });

}








document.addEventListener("DOMContentLoaded", function() {
    optionChanged()
  });
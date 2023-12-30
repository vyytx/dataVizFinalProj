/**
 * 
 * @param {Array<{ z: number, location: string }>} chart_data 
 * @param {string} element 
 */
const choropleth = (chart_data, element) => {
    const data = [{
      type: 'choroplethmapbox', 
      name: 'Taiwan', 
      geojson: 'static/counties.json', 
      locations: unpack(chart_data, 'location'),
      z: unpack(chart_data, 'z')
    }]
    const layout = {
      mapbox: {
        style: 'white-bg', 
        center: {lon: 120.9738819, lat: 23.97565}, 
        zoom: 5.7
      },
      showlegend: false,
      margin: {t: 30, b: 10, l: 10, r:10},
    };
    const config = {
      responsive: true
    }
    Plotly.newPlot(element, data, layout, config)
      .then((chart) => {
        chart.on('plotly_click', (data) => {
          const countyName = data.points[0].location
          window.location.assign(`/county/${countyName}`)
        })
      })
    
}

const temperature_forecast_scatter = (chart_data, element) => {
  const data = [
    {
      type: 'scatter', 
      mode: 'lines+markers',
      name: '最低溫度',
      x: chart_data['x'],
      y: chart_data['MinT'],
      hovertemplate: '%{y}°C'
    },
    {
      type: 'scatter', 
      mode: 'lines+markers',
      name: '最高溫度',
      x: chart_data['x'],
      y: chart_data['MaxT'],
      hovertemplate: '%{y}°C'
    },
  ]

  const layout = {
    title: '未來 36 小時最高和最低溫度',
    xaxis: {
      tickmode: 'array',
      tickvals: chart_data['ticks']
    },
    margin: {t:100},
  };
  const config = {
    responsive: true
  }
  Plotly.newPlot(element, data, layout, config)
  
}
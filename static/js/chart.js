/**
 * 
 * @param {Array<{ z: number, location: string }>} chart_data 
 * @param {string} element 
 */
const choropleth = (chart_data, element) => {
    const data = [{
      type: "choroplethmapbox", 
      name: "Taiwan", 
      geojson: "static/counties.json", 
      locations: unpack(chart_data, 'location'),
      z: unpack(chart_data, 'z')
    }]
    const layout = {
      mapbox: {
        style: "white-bg", 
        center: {lon: 120.9738819, lat: 23.97565}, 
        zoom: 5.7
      }, 
      width: 600, 
      height: 400, 
      margin: {t: 0, b: 0}
    };
    Plotly.newPlot(element, data, layout)
}
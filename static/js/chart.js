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

// 創建兩種不同排序的直方圖
const createHistogram = (chart_data, element) => {
  // 將資料轉換為直方圖需要的格式
  const sortedData = chart_data.slice().sort((a, b) => a.z - b.z); // 按照氣溫排序

  const locations = chart_data.map(item => item.location);
  const temperatures = chart_data.map(item => item.z);

  const sortedLocations = sortedData.map(item => item.location);
  const sortedTemperatures = sortedData.map(item => item.z);

  // 創建直方圖的 trace，並使用色彩映射
  const trace1 = {
    x: locations, // 將縣市放在 x 軸
    y: temperatures, // 將氣溫放在 y 軸
    type: 'bar',
    orientation: 'v', // 垂直方向顯示直方圖
    marker: {
      color: temperatures, // 根據溫度資料設定顏色
      colorscale: 'Reds', // 設定紅色系漸層
    },
    name: '未排序',
    visible: true,
  };

  const trace2 = {
    x: sortedLocations, // 將縣市放在 x 軸
    y: sortedTemperatures, // 將氣溫放在 y 軸
    type: 'bar',
    orientation: 'v', // 垂直方向顯示直方圖
    marker: {
      color: sortedTemperatures, // 根據溫度資料設定顏色
      colorscale: 'Reds', // 設定紅色系漸層
    },
    name: '排序',
    visible: false,
  };

  const data = [trace1, trace2];

  // 創建直方圖的 layout
  const layout = {
    title: '各縣市比較',
    xaxis: {
      title: '縣市', // 修改 x 軸標題
      tickangle: -45,
    },
    yaxis: {
      title: '平均數值', // 修改 y 軸標題
    },
    margin: {
      l: 100,
      r: 20,
      t: 50,
      b: 50,
    },
    updatemenus: [
      {
        y: 1.2,
        x: 0.3,
        yanchor: 'top',
        buttons: [
          {
            method: 'restyle',
            args: ['visible', [true, false]],
            label: '未排序',
          },
          {
            method: 'restyle',
            args: ['visible', [false, true]],
            label: '排序',
          },
        ],
      },
    ],
  };

  // 設定配置
  const config = {
    responsive: true,
  };

  // 繪製直方圖
  Plotly.newPlot(element, data, layout, config);
};




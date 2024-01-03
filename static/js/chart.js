/**
 * 
 * @param {Array<{ z: number, location: string }>} chart_data 
 * @param {string} element 
 */


const choropleth = (chart_data, element, geojson_path) => {
  const data = [{
    type: 'choroplethmapbox',
    name: 'Taiwan',
    geojson: geojson_path,
    locations: unpack(chart_data, 'location'),
    z: unpack(chart_data, 'z'),
  }]
  const layout = {
    width: 550,
    mapbox: {
      style: 'white-bg',
      center: { lon: 120.9738819, lat: 23.97565 },
      zoom: 5.7
    },
    showlegend: false,
    margin: { t: 30, b: 10, l: 10, r: 10 },
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

const temperature_scatter = (forcast_data, history_data, element) => {
  const data = [
    {
      type: 'scatter',
      mode: 'lines+markers',
      name: '最低溫度',
      x: forcast_data['x'],
      y: forcast_data['MinT'],
      text: forcast_data['range'],
      hovertemplate: '%{text}' + '%{y}°C',
    },
    {
      type: 'scatter',
      mode: 'lines+markers',
      name: '最高溫度',
      x: forcast_data['x'],
      y: forcast_data['MaxT'],
      text: forcast_data['range'],
      hovertemplate: '%{y}°C<br>%{text}',
    }
  ]
  if (history_data) {
    data.push({
      type: 'scatter',
      mode: 'lines+markers',
      x: unpack(history_data, 'date'),
      y: unpack(history_data, 'temperature'),
      visible: false
    })
  }

  const updatemenus = [
    {
      y: 1.3,
      x: 0,
      yanchor: 'top',
      type: 'buttons',
      direction: 'right',
      buttons: [
        {
          method: 'update',
          args: [
            {'visible': [true, true, false]},
            {'title': '未來7天最高和最低溫度'}
          ],
          label: '預測'
        },
        {
          method: 'update',
          args: [
            {'visible': [false, false, true]},
            {'title': '過去30天平均溫度'}
          ],
          label: '歷史'
        }
      ],
    },
  ]

  const layout = {
    title: '未來7天最高和最低溫度',
    margin: { t: 100 },
    updatemenus: history_data ? updatemenus : []
  };
  const config = {
    responsive: true
  }
  Plotly.newPlot(element, data, layout, config)

}

// 創建兩種不同排序的直方圖
const createHistogram = (chart_data, element, yaxix_title) => {
  // 將資料轉換為直方圖需要的格式
  const sorted_chart_data = _.cloneDeep(chart_data);
  sorted_chart_data.sort((a, b) => b.z - a.z)// 按照氣溫排序

  // 創建直方圖的 trace，並使用色彩映射
  const trace1 = {
    x: unpack(chart_data, 'location'), // 將縣市放在 x 軸
    y: unpack(chart_data, 'z'), // 將氣溫放在 y 軸
    type: 'bar',
    orientation: 'v', // 垂直方向顯示直方圖
    marker: {
      color: unpack(chart_data, 'z'), // 根據溫度資料設定顏色
      colorscale: 'Reds', // 設定紅色系漸層
    },
    name: '未排序',
    visible: true,
  };

  const trace2 = {
    x: unpack(sorted_chart_data, 'location'), // 將縣市放在 x 軸
    y: unpack(sorted_chart_data, 'z'), // 將氣溫放在 y 軸
    type: 'bar',
    orientation: 'v', // 垂直方向顯示直方圖
    marker: {
      color: unpack(sorted_chart_data, 'z'), // 根據溫度資料設定顏色
      colorscale: 'Reds', // 設定紅色系漸層
    },
    name: '排序',
    visible: false,
  };

  const data = [trace1, trace2];

  // 創建直方圖的 layout
  const layout = {
    width: 600,
    xaxis: {
      title: '縣市', // 修改 x 軸標題
      tickangle: -45,
    },
    yaxis: {
      title: yaxix_title, // 修改 y 軸標題
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
        x: 0.1,
        yanchor: 'top',
        type: 'buttons',
        direction: 'right',
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




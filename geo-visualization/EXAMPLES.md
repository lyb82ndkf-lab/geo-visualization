# 地理数据可视化示例

## 示例1：IP地址地理分布热力图

### 场景描述
可视化网站访问用户的IP地址地理位置分布，识别高访问量区域。

### 数据准备
```python
# 模拟IP地址数据
import pandas as pd
import numpy as np

# 生成模拟数据：1000个随机IP地址位置
np.random.seed(42)
ip_data = pd.DataFrame({
    'latitude': np.random.normal(39.9, 2, 1000),  # 以北京为中心
    'longitude': np.random.normal(116.4, 2, 1000),
    'count': np.random.randint(1, 100, 1000)  # 访问次数
})
```

### 可视化代码
```python
import folium
from folium.plugins import HeatMap

# 创建地图
m = folium.Map(location=[39.9042, 116.4074], zoom_start=6)

# 准备热力图数据
heat_data = ip_data[['latitude', 'longitude', 'count']].values.tolist()

# 添加热力图层
HeatMap(
    heat_data,
    name='IP访问热力图',
    min_opacity=0.3,
    max_val=100,
    radius=20,
    blur=15,
    gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
).add_to(m)

# 添加图层控制
folium.LayerControl().add_to(m)

# 保存地图
m.save('ip_heatmap.html')
```

## 示例2：中国省份人口密度可视化

### 场景描述
按省份显示中国人口密度分布，颜色深浅表示人口密度高低。

### 数据准备
```python
# 省份人口数据（示例数据）
province_data = pd.DataFrame({
    'province': ['北京', '上海', '广东', '山东', '河南', '四川', '江苏', '河北', '湖南', '湖北'],
    'population': [2171, 2487, 12601, 10047, 9605, 8367, 8475, 7591, 6644, 5775],
    'area': [16410, 6340, 179800, 155800, 167000, 485000, 107200, 187700, 211800, 185900]
})

# 计算人口密度（人/平方公里）
province_data['density'] = province_data['population'] / province_data['area'] * 10000
```

### 可视化代码
```python
import folium
import json

# 加载中国省份GeoJSON数据
# 需要下载中国省份边界数据
with open('china_provinces.geojson', 'r', encoding='utf-8') as f:
    china_geo = json.load(f)

# 创建地图
m = folium.Map(location=[35.8617, 104.1954], zoom_start=4)

# 创建省份分级图
folium.Choropleth(
    geo_data=china_geo,
    data=province_data,
    columns=['province', 'density'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='人口密度 (人/平方公里)',
    nan_fill_color='white'
).add_to(m)

# 添加悬停信息
folium.GeoJson(
    china_geo,
    style_function=lambda x: {'fillColor': '#ffffff', 'color': '#000000', 'fillOpacity': 0.1, 'weight': 0.1},
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['省份:'])
).add_to(m)

m.save('province_population.html')
```

## 示例3：城市天气散点可视化

### 场景描述
在地图上显示各城市的天气信息，使用不同颜色和大小表示温度和天气状况。

### 数据准备
```python
# 城市天气数据（示例数据）
weather_data = pd.DataFrame({
    'city': ['北京', '上海', '广州', '深圳', '成都', '杭州', '武汉', '西安'],
    'latitude': [39.9042, 31.2304, 23.1291, 22.5431, 30.5728, 30.2741, 30.5928, 34.3416],
    'longitude': [116.4074, 121.4737, 113.2644, 114.0579, 104.0668, 120.1551, 114.3055, 108.9398],
    'temperature': [25, 28, 32, 33, 26, 27, 29, 24],
    'weather': ['晴', '多云', '雷阵雨', '雷阵雨', '多云', '晴', '晴', '多云'],
    'humidity': [45, 65, 80, 82, 70, 60, 55, 50]
})
```

### 可视化代码
```python
import folium

# 创建地图
m = folium.Map(location=[35.8617, 104.1954], zoom_start=5)

# 定义天气颜色映射
weather_colors = {
    '晴': 'red',
    '多云': 'orange',
    '雷阵雨': 'blue',
    '小雨': 'lightblue',
    '大雨': 'darkblue'
}

# 添加城市天气标记
for idx, row in weather_data.iterrows():
    # 根据温度设置大小
    radius = row['temperature'] / 5
    
    # 根据天气设置颜色
    color = weather_colors.get(row['weather'], 'gray')
    
    # 创建弹出信息
    popup_html = f"""
    <div style="width:200px">
        <h4>{row['city']}</h4>
        <p>温度: {row['temperature']}°C</p>
        <p>天气: {row['weather']}</p>
        <p>湿度: {row['humidity']}%</p>
    </div>
    """
    
    # 添加圆形标记
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{row['city']}: {row['temperature']}°C"
    ).add_to(m)

# 添加图例
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 150px; height: 120px; 
            border:2px solid grey; z-index:9999; font-size:12px;
            background-color:white;
            ">&nbsp; <b>天气图例</b> <br>
            &nbsp; <i class="fa fa-circle" style="color:red"></i> 晴<br>
            &nbsp; <i class="fa fa-circle" style="color:orange"></i> 多云<br>
            &nbsp; <i class="fa fa-circle" style="color:blue"></i> 雷阵雨
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

m.save('city_weather.html')
```

## 示例4：商业选址分析

### 场景描述
分析潜在商业选址，结合人口密度、竞争对手位置和交通便利性。

### 数据准备
```python
# 潜在选址点
potential_locations = pd.DataFrame({
    'name': ['A商场', 'B商场', 'C商场'],
    'latitude': [39.9142, 39.9242, 39.9342],
    'longitude': [116.4174, 116.4274, 116.4374],
    'score': [85, 92, 78]  # 综合评分
})

# 竞争对手位置
competitors = pd.DataFrame({
    'name': ['竞争店1', '竞争店2', '竞争店3'],
    'latitude': [39.9100, 39.9200, 39.9300],
    'longitude': [116.4100, 116.4200, 116.4300]
})
```

### 可视化代码
```python
import folium

# 创建地图
m = folium.Map(location=[39.9242, 116.4274], zoom_start=14)

# 添加潜在选址点（绿色）
for idx, row in potential_locations.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['name']}<br>评分: {row['score']}",
        icon=folium.Icon(color='green', icon='star')
    ).add_to(m)

# 添加竞争对手位置（红色）
for idx, row in competitors.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name'],
        icon=folium.Icon(color='red', icon='warning-sign')
    ).add_to(m)

# 添加覆盖范围圈（500米半径）
for idx, row in potential_locations.iterrows():
    folium.Circle(
        location=[row['latitude'], row['longitude']],
        radius=500,
        color='green',
        fill=True,
        fill_opacity=0.1,
        popup=f"{row['name']} 覆盖范围"
    ).add_to(m)

m.save('business_location.html')
```

## 示例5：时间序列动画

### 场景描述
展示数据随时间变化的过程，如疫情传播、人口迁移等。

### 可视化代码
```python
import folium
from folium.plugins import TimestampedGeoJson
import json

# 准备时间序列数据
features = []
for i in range(10):
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [116.4 + i * 0.01, 39.9 + i * 0.01]
        },
        'properties': {
            'time': f'2023-01-{i+1:02d}',
            'popup': f'时间点 {i+1}',
            'icon': 'circle',
            'iconstyle': {
                'fillColor': 'red',
                'fillOpacity': 0.6,
                'stroke': 'false',
                'radius': 5 + i
            }
        }
    }
    features.append(feature)

# 创建时间序列GeoJSON
timestamped_geojson = {
    'type': 'FeatureCollection',
    'features': features
}

# 创建地图
m = folium.Map(location=[39.9, 116.4], zoom_start=12)

# 添加时间序列图层
TimestampedGeoJson(
    timestamped_geojson,
    period='P1D',
    add_last_point=True,
    auto_play=False,
    loop=True,
    max_speed=10,
    loop_button=True,
    date_options='YYYY-MM-DD',
    time_slider_drag_update=True
).add_to(m)

m.save('time_animation.html')
```

## 运行示例

1. 安装依赖：`pip install folium pandas numpy geopy`
2. 下载中国省份GeoJSON数据
3. 运行对应的Python脚本
4. 在浏览器中打开生成的HTML文件

## 注意事项

1. 确保坐标系统正确（WGS84标准）
2. 大数据量时考虑性能优化
3. 注意API调用限制和数据隐私
4. 定期更新地理数据以保持准确性
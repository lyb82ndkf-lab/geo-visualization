# 地理数据可视化参考文档

## 数据源

### 1. 地理坐标数据
- **GPS数据**：从移动设备或GPS记录器获取
- **IP地理定位**：使用IP地址查询地理位置
- **地址解析**：将地址转换为经纬度坐标

### 2. 行政区划数据
- **中国省份边界**：GeoJSON格式的省级行政区划
- **城市边界**：市级行政区划数据
- **区县边界**：区县级行政区划数据

### 3. 统计数据
- **人口数据**：国家统计局发布的人口统计数据
- **经济数据**：GDP、收入等经济指标
- **天气数据**：气象站观测数据

## API参考

### Folium库核心API

#### 创建地图
```python
folium.Map(
    location=[纬度, 经度],  # 地图中心点
    zoom_start=12,          # 初始缩放级别
    tiles='OpenStreetMap',  # 地图样式
    control_scale=True      # 显示比例尺
)
```

#### 热力图图层
```python
from folium.plugins import HeatMap

HeatMap(
    data=坐标数据,           # [[纬度, 经度, 权重], ...]
    name='热力图',           # 图层名称
    min_opacity=0.5,         # 最小透明度
    max_zoom=18,             # 最大缩放级别
    radius=25,               # 点半径
    blur=15,                 # 模糊程度
    gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}  # 颜色渐变
)
```

#### 散点图层
```python
folium.CircleMarker(
    location=[纬度, 经度],
    radius=5,                # 半径
    color='red',             # 边框颜色
    fill=True,               # 是否填充
    fill_color='blue',       # 填充颜色
    fill_opacity=0.7,        # 填充透明度
    popup='信息',            # 点击弹出信息
    tooltip='提示'           # 悬停提示
)
```

#### 省份可视化
```python
folium.Choropleth(
    geo_data=省份GeoJSON,    # 行政区划数据
    data=统计数据,           # 统计数据
    columns=['省份', '值'],   # 数据列
    key_on='feature.properties.name',  # 匹配键
    fill_color='YlOrRd',     # 填充颜色
    fill_opacity=0.7,        # 填充透明度
    line_opacity=0.2,        # 边界透明度
    legend_name='图例名称'   # 图例标题
)
```

### 数据处理工具

#### 地理编码
```python
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geo_app")
location = geolocator.geocode("北京市天安门广场")
print((location.latitude, location.longitude))
```

#### 坐标转换
```python
# WGS84 (GPS) 转 GCJ02 (高德、腾讯)
def wgs84_to_gcj02(lng, lat):
    # 转换算法实现
    pass

# GCJ02 转 BD09 (百度)
def gcj02_to_bd09(lng, lat):
    # 謀定算法实现
    pass
```

## 常用地图样式

### OpenStreetMap
- 默认样式，免费使用
- 适合一般用途

### 高德地图
```python
tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}'
```

### 天地图
```python
tiles='http://t0.tianditu.gov.cn/vec_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=您的密钥'
```

## 性能优化

### 大数据量处理
1. **数据采样**：对大量数据点进行随机采样
2. **聚合显示**：使用MarkerCluster进行点聚合
3. **分块加载**：按区域或时间分块加载数据

### 渲染优化
1. **WebGL加速**：使用Leaflet.gl插件
2. ** Canvas渲染**：对于大量点使用Canvas而非SVG
3. **图层缓存**：缓存已渲染的图层

## 错误处理

### 常见问题
1. **坐标偏移**：检查坐标系是否正确（WGS84/GCJ02/BD09）
2. **数据格式**：确保GeoJSON格式正确
3. **内存溢出**：大数据量时使用流式处理

### 调试技巧
1. **逐步构建**：先创建基础地图，再逐步添加图层
2. **数据验证**：在添加到地图前验证数据格式
3. **浏览器控制台**：查看JavaScript错误信息

## 扩展资源

### 相关库
- **Folium**：Python地图可视化库
- **Leaflet**：JavaScript地图库
- **Mapbox GL**：高性能地图渲染
- **Deck.gl**：大规模数据可视化

### 数据资源
- **DataV.GeoAtlas**：中国行政区划GeoJSON
- **阿里云数据可视化**：地理数据集
- **国家统计局**：官方统计数据
# 地理数据可视化技能

一个用于地理数据可视化的综合工具包，支持热力图、省份可视化、散点图和地图生成。

## 功能特性

- **热力图可视化**：基于地理位置的数据密度展示
- **省份可视化**：按行政区划显示统计数据
- **散点可视化**：离散数据点的地理位置展示
- **地图生成**：创建交互式HTML地图
- **数据获取**：支持IP定位、天气数据获取
- **数据处理**：坐标转换、数据清洗、聚合分析

## 快速开始

### 安装依赖
```bash
pip install folium pandas numpy geopy requests
```

### 基础使用

#### 1. 创建热力图
```python
from scripts.visualizer import GeoVisualizer
import pandas as pd
import numpy as np

# 创建示例数据
data = pd.DataFrame({
    'latitude': np.random.normal(39.9, 0.5, 100),
    'longitude': np.random.normal(116.4, 0.5, 100),
    'value': np.random.randint(1, 100, 100)
})

# 创建热力图
visualizer = GeoVisualizer(center=(39.9, 116.4), zoom_start=10)
visualizer.create_heatmap_from_df(
    data,
    weight_col='value',
    output_file='heatmap.html'
)
```

#### 2. 获取天气数据
```python
from scripts.data_fetcher import GeoDataFetcher

fetcher = GeoDataFetcher()
weather = fetcher.get_weather_by_city("北京")
print(f"北京天气: {weather['temperature']}°C, {weather['weather']}")
```

#### 3. 处理地理数据
```python
from scripts.data_processor import GeoDataProcessor

processor = GeoDataProcessor()
clean_data = processor.clean_geo_data(raw_data)
china_data = processor.filter_china_bounds(clean_data)
```

## 工作流程

1. **数据准备**
   - 收集地理坐标数据（经纬度）
   - 清洗和验证数据格式
   - 可选：添加权重列用于热力图强度

2. **选择可视化类型**
   - 热力图：显示数据密度分布
   - 散点图：显示离散数据点位置
   - 省份可视化：按行政区划显示统计数据
   - 聚合图：显示数据点聚合效果

3. **配置地图参数**
   - 设置中心点坐标
   - 选择地图样式（默认、地形、卫星）
   - 配置缩放级别和交互选项

4. **添加数据图层**
   - 使用对应的可视化插件
   - 配置颜色、大小、透明度等样式
   - 添加图例和标注

5. **导出和分享**
   - 保存为HTML文件（交互式）
   - 导出为图片（静态）
   - 嵌入到Web应用中

## 目录结构

```
skills/geo-visualization/
├── SKILL.md           # 技能说明文档
├── REFERENCE.md       # 详细API参考文档
├── EXAMPLES.md        # 使用示例
├── README.md          # 中文README
├── README_EN.md       # 英文README
└── scripts/           # 工具脚本
    ├── data_fetcher.py    # 数据获取脚本
    ├── data_processor.py  # 数据处理脚本
    └── visualizer.py      # 可视化脚本
```

## 使用场景

### 1. IP地址地理分布
可视化网站访问用户的IP地址地理位置分布，识别高访问量区域。

### 2. 城市天气展示
在地图上显示各城市的天气信息，使用不同颜色和大小表示温度和天气状况。

### 3. 人口密度分析
按省份显示中国人口密度分布，颜色深浅表示人口密度高低。

### 4. 商业选址分析
分析潜在商业选址，结合人口密度、竞争对手位置和交通便利性。

### 5. 时间序列动画
展示数据随时间变化的过程，如疫情传播、人口迁移等。

## API参考

### 核心类

#### GeoDataFetcher
- `get_location_by_ip(ip)`: 通过IP地址获取地理位置
- `get_weather_by_city(city)`: 获取城市天气信息
- `geocode_address(address)`: 将地址转换为经纬度坐标
- `batch_geocode(addresses)`: 批量地理编码
- `get_china_provinces_geojson()`: 获取中国省份GeoJSON数据
- `generate_sample_data(data_type, count)`: 生成示例数据

#### GeoDataProcessor
- `validate_coordinates(latitude, longitude)`: 验证坐标是否有效
- `clean_geo_data(df)`: 清洗地理数据
- `filter_by_bounds(df, bounds)`: 按边界过滤数据
- `filter_china_bounds(df)`: 过滤中国范围内的数据
- `calculate_distance(lat1, lon1, lat2, lon2)`: 计算两点之间的距离
- `add_distance_column(df, center_lat, center_lon)`: 添加距离列
- `aggregate_by_grid(df, grid_size)`: 按网格聚合数据
- `create_heatmap_data(df)`: 创建热力图数据格式
- `convert_coordinate_system(df)`: 转换坐标系统
- `export_to_geojson(df)`: 导出数据为GeoJSON格式

#### GeoVisualizer
- `create_base_map(tiles)`: 创建基础地图
- `add_heatmap(data)`: 添加热力图层
- `add_markers(df)`: 添加标记点
- `add_circle_markers(df)`: 添加圆形标记
- `add_choropleth(geo_data, data)`: 添加分级统计图
- `add_layer_control()`: 添加图层控制
- `add_legend(legend_html)`: 添加自定义图例
- `save_map(output_file)`: 保存地图为HTML文件
- `create_heatmap_from_df(df)`: 从DataFrame创建热力图
- `create_marker_map_from_df(df)`: 从DataFrame创建标记地图
- `create_choropleth_map(geo_data, data)`: 创建分级统计地图
- `create_weather_map(weather_data)`: 创建天气地图

## 数据源

### 地理坐标数据
- GPS数据：从移动设备或GPS记录器获取
- IP地理定位：使用IP地址查询地理位置
- 地址解析：将地址转换为经纬度坐标

### 行政区划数据
- 中国省份边界：GeoJSON格式的省级行政区划
- 城市边界：市级行政区划数据
- 区县边界：区县级行政区划数据

### 统计数据
- 人口数据：国家统计局发布的人口统计数据
- 经济数据：GDP、收入等经济指标
- 天气数据：气象站观测数据

## 性能优化

### 大数据量处理
1. **数据采样**：对大量数据点进行随机采样
2. **聚合显示**：使用MarkerCluster进行点聚合
3. **分块加载**：按区域或时间分块加载数据

### 渲染优化
1. **WebGL加速**：使用Leaflet.gl插件
2. **Canvas渲染**：对于大量点使用Canvas而非SVG
3. **图层缓存**：缓存已渲染的图层

## 常见问题

### 1. 坐标偏移
检查坐标系是否正确（WGS84/GCJ02/BD09），中国境内地图需要使用GCJ02坐标系。

### 2. 数据格式错误
确保GeoJSON格式正确，坐标顺序为[经度, 纬度]。

### 3. 内存溢出
大数据量时使用流式处理或数据采样。

### 4. 地图加载缓慢
减少数据点数量，使用聚合显示，或启用WebGL加速。

## 扩展资源

### 相关库
- **Folium**: Python地图可视化库
- **Leaflet**: JavaScript地图库
- **Mapbox GL**: 高性能地图渲染
- **Deck.gl**: 大规模数据可视化

### 数据资源
- **DataV.GeoAtlas**: 中国行政区划GeoJSON
- **阿里云数据可视化**: 地理数据集
- **国家统计局**: 官方统计数据

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个工具。

---
name: geo-visualization
description: 地理数据可视化工具，支持热力图、省份可视化、散点图和地图生成。当需要可视化地理位置数据、创建地图或展示地理分布时使用。
---

# 地理数据可视化技能

## 快速开始

### 安装依赖
```bash
pip install folium pandas numpy geopy
```

### 基础地图生成
```python
import folium

# 创建基础地图
m = folium.Map(location=[39.9042, 116.4074], zoom_start=12)
m.save('basic_map.html')
```

### 热力图示例
```python
import folium
from folium.plugins import HeatMap
import numpy as np

# 生成示例数据
data = np.random.randn(100, 2) * 0.1 + [39.9, 116.4]

# 创建热力图
m = folium.Map(location=[39.9042, 116.4074], zoom_start=12)
HeatMap(data).add_to(m)
m.save('heatmap.html')
```

## 工作流程

### 1. 数据准备
- 收集地理坐标数据（经纬度）
- 清洗和验证数据格式
- 可选：添加权重列用于热力图强度

### 2. 选择可视化类型
- **热力图**：显示数据密度分布
- **散点图**：显示离散数据点位置
- **省份可视化**：按行政区划显示统计数据
- **聚合图**：显示数据点聚合效果

### 3. 配置地图参数
- 设置中心点坐标
- 选择地图样式（默认、地形、卫星）
- 配置缩放级别和交互选项

### 4. 添加数据图层
- 使用对应的可视化插件
- 配置颜色、大小、透明度等样式
- 添加图例和标注

### 5. 导出和分享
- 保存为HTML文件（交互式）
- 导出为图片（静态）
- 嵌入到Web应用中

## 高级功能

### 自定义样式
- 配置颜色渐变
- 设置动态半径
- 添加点击事件和弹出窗口

### 多图层叠加
- 同时显示多种可视化
- 图层控制开关
- 时间序列动画

### 性能优化
- 大数据量采样策略
- 聚合算法选择
- WebGL加速渲染

详细API文档和高级配置请参考 [REFERENCE.md](REFERENCE.md)

## 使用场景

1. **IP地址地理分布**：可视化用户访问来源
2. **城市天气展示**：在地图上显示天气信息
3. **人口密度分析**：按省份显示人口分布
4. **商业选址分析**：基于地理数据的决策支持

更多示例请参考 [EXAMPLES.md](EXAMPLES.md)
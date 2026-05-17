#!/usr/bin/env python3
"""
地理数据可视化工具脚本
用于创建各种类型的地图可视化
"""

import folium
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import json
import os

class GeoVisualizer:
    """地理数据可视化类"""
    
    def __init__(self, center: Tuple[float, float] = (35.8617, 104.1954), zoom_start: int = 5):
        """
        初始化可视化器
        
        Args:
            center: 地图中心点坐标 (纬度, 经度)
            zoom_start: 初始缩放级别
        """
        self.center = center
        self.zoom_start = zoom_start
        self.map = None
        
    def create_base_map(self, 
                       tiles: str = 'OpenStreetMap',
                       control_scale: bool = True,
                       **kwargs) -> folium.Map:
        """
        创建基础地图
        
        Args:
            tiles: 地图样式
            control_scale: 是否显示比例尺
            **kwargs: 其他地图参数
            
        Returns:
            Folium地图对象
        """
        self.map = folium.Map(
            location=self.center,
            zoom_start=self.zoom_start,
            tiles=tiles,
            control_scale=control_scale,
            **kwargs
        )
        return self.map
    
    def add_heatmap(self, 
                   data: List[List[float]],
                   name: str = '热力图',
                   min_opacity: float = 0.5,
                   max_zoom: int = 18,
                   radius: int = 25,
                   blur: int = 15,
                   gradient: Optional[Dict] = None) -> None:
        """
        添加热力图层
        
        Args:
            data: 热力图数据 [[纬度, 经度, 权重], ...]
            name: 图层名称
            min_opacity: 最小透明度
            max_zoom: 最大缩放级别
            radius: 点半径
            blur: 模糊程度
            gradient: 颜色渐变配置
        """
        from folium.plugins import HeatMap
        
        if self.map is None:
            self.create_base_map()
        
        if gradient is None:
            gradient = {0.4: 'blue', 0.65: 'lime', 1: 'red'}
        
        HeatMap(
            data,
            name=name,
            min_opacity=min_opacity,
            max_zoom=max_zoom,
            radius=radius,
            blur=blur,
            gradient=gradient
        ).add_to(self.map)
    
    def add_markers(self,
                   df: pd.DataFrame,
                   lat_col: str = 'latitude',
                   lon_col: str = 'longitude',
                   popup_col: Optional[str] = None,
                   tooltip_col: Optional[str] = None,
                   icon_color: str = 'blue',
                   icon: str = 'info-sign',
                   cluster: bool = False) -> None:
        """
        添加标记点
        
        Args:
            df: 包含坐标的DataFrame
            lat_col: 纬度列名
            lon_col: 经度列名
            popup_col: 弹出信息列名
            tooltip_col: 悬停提示列名
            icon_color: 图标颜色
            icon: 图标类型
            cluster: 是否使用聚合显示
        """
        if self.map is None:
            self.create_base_map()
        
        if cluster:
            from folium.plugins import MarkerCluster
            marker_cluster = MarkerCluster(name="标记点").add_to(self.map)
            target = marker_cluster
        else:
            target = self.map
        
        for idx, row in df.iterrows():
            popup = str(row[popup_col]) if popup_col and popup_col in row else None
            tooltip = str(row[tooltip_col]) if tooltip_col and tooltip_col in row else None
            
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=popup,
                tooltip=tooltip,
                icon=folium.Icon(color=icon_color, icon=icon)
            ).add_to(target)
    
    def add_circle_markers(self,
                          df: pd.DataFrame,
                          lat_col: str = 'latitude',
                          lon_col: str = 'longitude',
                          radius_col: Optional[str] = None,
                          color_col: Optional[str] = None,
                          popup_col: Optional[str] = None,
                          tooltip_col: Optional[str] = None,
                          default_radius: int = 5,
                          default_color: str = 'blue',
                          fill_opacity: float = 0.7) -> None:
        """
        添加圆形标记
        
        Args:
            df: 包含坐标的DataFrame
            lat_col: 纬度列名
            lon_col: 经度列名
            radius_col: 半径列名
            color_col: 颜色列名
            popup_col: 弹出信息列名
            tooltip_col: 悬停提示列名
            default_radius: 默认半径
            default_color: 默认颜色
            fill_opacity: 填充透明度
        """
        if self.map is None:
            self.create_base_map()
        
        for idx, row in df.iterrows():
            radius = row[radius_col] if radius_col and radius_col in row else default_radius
            color = row[color_col] if color_col and color_col in row else default_color
            popup = str(row[popup_col]) if popup_col and popup_col in row else None
            tooltip = str(row[tooltip_col]) if tooltip_col and tooltip_col in row else None
            
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=fill_opacity,
                popup=popup,
                tooltip=tooltip
            ).add_to(self.map)
    
    def add_choropleth(self,
                      geo_data: Dict,
                      data: pd.DataFrame,
                      columns: List[str],
                      key_on: str = 'feature.properties.name',
                      fill_color: str = 'YlOrRd',
                      fill_opacity: float = 0.7,
                      line_opacity: float = 0.2,
                      legend_name: str = '图例',
                      nan_fill_color: str = 'white') -> None:
        """
        添加分级统计图
        
        Args:
            geo_data: GeoJSON数据
            data: 统计数据
            columns: 数据列 [key列, value列]
            key_on: GeoJSON匹配键
            fill_color: 填充颜色
            fill_opacity: 填充透明度
            line_opacity: 边界透明度
            legend_name: 图例名称
            nan_fill_color: 无数据填充颜色
        """
        if self.map is None:
            self.create_base_map()
        
        folium.Choropleth(
            geo_data=geo_data,
            data=data,
            columns=columns,
            key_on=key_on,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            line_opacity=line_opacity,
            legend_name=legend_name,
            nan_fill_color=nan_fill_color
        ).add_to(self.map)
    
    def add_layer_control(self) -> None:
        """添加图层控制"""
        if self.map:
            folium.LayerControl().add_to(self.map)
    
    def add_legend(self, 
                  legend_html: str,
                  position: str = 'bottomright') -> None:
        """
        添加自定义图例
        
        Args:
            legend_html: 图例HTML代码
            position: 位置 ('bottomright', 'bottomleft', 'topright', 'topleft')
        """
        if self.map:
            self.map.get_root().html.add_child(folium.Element(legend_html))
    
    def save_map(self, output_file: str = 'map.html') -> str:
        """
        保存地图为HTML文件
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if self.map:
            self.map.save(output_file)
            print(f"地图已保存到 {output_file}")
            return output_file
        else:
            print("错误：地图未创建")
            return None
    
    def create_heatmap_from_df(self,
                              df: pd.DataFrame,
                              lat_col: str = 'latitude',
                              lon_col: str = 'longitude',
                              weight_col: Optional[str] = None,
                              output_file: str = 'heatmap.html',
                              **kwargs) -> str:
        """
        从DataFrame创建热力图
        
        Args:
            df: 包含坐标的DataFrame
            lat_col: 纬度列名
            lon_col: 经度列名
            weight_col: 权重列名
            output_file: 输出文件路径
            **kwargs: 其他热力图参数
            
        Returns:
            输出文件路径
        """
        # 准备数据
        if weight_col:
            heat_data = df[[lat_col, lon_col, weight_col]].values.tolist()
        else:
            heat_data = df[[lat_col, lon_col]].assign(weight=1).values.tolist()
        
        # 创建地图
        self.create_base_map()
        
        # 添加热力图
        self.add_heatmap(heat_data, **kwargs)
        
        # 保存地图
        return self.save_map(output_file)
    
    def create_marker_map_from_df(self,
                                 df: pd.DataFrame,
                                 lat_col: str = 'latitude',
                                 lon_col: str = 'longitude',
                                 popup_col: Optional[str] = None,
                                 tooltip_col: Optional[str] = None,
                                 output_file: str = 'markers.html',
                                 cluster: bool = False,
                                 **kwargs) -> str:
        """
        从DataFrame创建标记地图
        
        Args:
            df: 包含坐标的DataFrame
            lat_col: 纬度列名
            lon_col: 经度列名
            popup_col: 弹出信息列名
            tooltip_col: 悬停提示列名
            output_file: 输出文件路径
            cluster: 是否使用聚合显示
            **kwargs: 其他标记参数
            
        Returns:
            输出文件路径
        """
        # 创建地图
        self.create_base_map()
        
        # 添加标记
        self.add_markers(
            df, lat_col, lon_col,
            popup_col, tooltip_col,
            cluster=cluster, **kwargs
        )
        
        # 保存地图
        return self.save_map(output_file)
    
    def create_choropleth_map(self,
                             geo_data: Dict,
                             data: pd.DataFrame,
                             columns: List[str],
                             key_on: str = 'feature.properties.name',
                             output_file: str = 'choropleth.html',
                             **kwargs) -> str:
        """
        创建分级统计地图
        
        Args:
            geo_data: GeoJSON数据
            data: 统计数据
            columns: 数据列 [key列, value列]
            key_on: GeoJSON匹配键
            output_file: 输出文件路径
            **kwargs: 其他分级统计参数
            
        Returns:
            输出文件路径
        """
        # 创建地图
        self.create_base_map()
        
        # 添加分级统计图
        self.add_choropleth(geo_data, data, columns, key_on, **kwargs)
        
        # 保存地图
        return self.save_map(output_file)
    
    def create_weather_map(self,
                          weather_data: pd.DataFrame,
                          lat_col: str = 'latitude',
                          lon_col: str = 'longitude',
                          city_col: str = 'city',
                          temp_col: str = 'temperature',
                          weather_col: str = 'weather',
                          output_file: str = 'weather_map.html') -> str:
        """
        创建天气地图
        
        Args:
            weather_data: 天气数据
            lat_col: 纬度列名
            lon_col: 经度列名
            city_col: 城市列名
            temp_col: 温度列名
            weather_col: 天气列名
            output_file: 输出文件路径
            
        Returns:
            输出文件路径
        """
        # 创建地图
        self.create_base_map(zoom_start=5)
        
        # 天气颜色映射
        weather_colors = {
            '晴': 'red',
            '多云': 'orange',
            '阴': 'gray',
            '小雨': 'lightblue',
            '中雨': 'blue',
            '大雨': 'darkblue',
            '雷阵雨': 'purple',
            '雪': 'white'
        }
        
        # 添加天气标记
        for idx, row in weather_data.iterrows():
            # 根据温度设置大小
            radius = max(5, row[temp_col] / 5)
            
            # 根据天气设置颜色
            color = weather_colors.get(row[weather_col], 'gray')
            
            # 创建弹出信息
            popup_html = f"""
            <div style="width:200px">
                <h4>{row[city_col]}</h4>
                <p>温度: {row[temp_col]}°C</p>
                <p>天气: {row[weather_col]}</p>
            </div>
            """
            
            # 添加圆形标记
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{row[city_col]}: {row[temp_col]}°C"
            ).add_to(self.map)
        
        # 添加图例
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 150px; height: 120px; 
                    border:2px solid grey; z-index:9999; font-size:12px;
                    background-color:white;
                    ">&nbsp; <b>天气图例</b> <br>
                    &nbsp; <i class="fa fa-circle" style="color:red"></i> 晴<br>
                    &nbsp; <i class="fa fa-circle" style="color:orange"></i> 多云<br>
                    &nbsp; <i class="fa fa-circle" style="color:blue"></i> 雨
        </div>
        '''
        self.add_legend(legend_html)
        
        # 保存地图
        return self.save_map(output_file)

def main():
    """主函数，演示可视化功能"""
    print("=== 地理数据可视化工具演示 ===")
    
    # 创建示例数据
    np.random.seed(42)
    
    # 1. 热力图示例
    print("\n1. 创建热力图:")
    heatmap_data = pd.DataFrame({
        'latitude': np.random.normal(39.9, 0.5, 100),
        'longitude': np.random.normal(116.4, 0.5, 100),
        'value': np.random.randint(1, 100, 100)
    })
    
    visualizer = GeoVisualizer(center=(39.9, 116.4), zoom_start=10)
    visualizer.create_heatmap_from_df(
        heatmap_data,
        weight_col='value',
        output_file='demo_heatmap.html'
    )
    
    # 2. 标记图示例
    print("\n2. 创建标记图:")
    marker_data = pd.DataFrame({
        'latitude': [39.9042, 31.2304, 23.1291, 22.5431],
        'longitude': [116.4074, 121.4737, 113.2644, 114.0579],
        'city': ['北京', '上海', '广州', '深圳'],
        'population': [2171, 2487, 12601, 12591]
    })
    
    visualizer2 = GeoVisualizer(center=(35, 110), zoom_start=5)
    visualizer2.create_marker_map_from_df(
        marker_data,
        popup_col='city',
        tooltip_col='city',
        output_file='demo_markers.html',
        cluster=True
    )
    
    print("\n演示完成！请查看生成的HTML文件。")

if __name__ == "__main__":
    main()
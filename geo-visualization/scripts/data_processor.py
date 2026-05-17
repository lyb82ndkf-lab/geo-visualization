#!/usr/bin/env python3
"""
地理数据处理工具脚本
用于清洗、转换和验证地理数据
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import json
import math

class GeoDataProcessor:
    """地理数据处理类"""
    
    def __init__(self):
        """初始化数据处理器"""
        pass
    
    def validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """
        验证坐标是否有效
        
        Args:
            latitude: 纬度
            longitude: 经度
            
        Returns:
            坐标是否有效
        """
        return (-90 <= latitude <= 90) and (-180 <= longitude <= 180)
    
    def clean_geo_data(self, df: pd.DataFrame, 
                       lat_col: str = 'latitude', 
                       lon_col: str = 'longitude') -> pd.DataFrame:
        """
        清洗地理数据
        
        Args:
            df: 包含地理坐标的DataFrame
            lat_col: 纬度列名
            lon_col: 经度列名
            
        Returns:
            清洗后的DataFrame
        """
        # 删除缺失值
        df_clean = df.dropna(subset=[lat_col, lon_col]).copy()
        
        # 验证坐标范围
        valid_mask = df_clean.apply(
            lambda row: self.validate_coordinates(row[lat_col], row[lon_col]), 
            axis=1
        )
        df_clean = df_clean[valid_mask]
        
        # 删除重复值
        df_clean = df_clean.drop_duplicates(subset=[lat_col, lon_col])
        
        print(f"数据清洗完成: 原始数据 {len(df)} 条, 清洗后 {len(df_clean)} 条")
        return df_clean
    
    def filter_by_bounds(self, df: pd.DataFrame,
                         bounds: Dict[str, float],
                         lat_col: str = 'latitude',
                         lon_col: str = 'longitude') -> pd.DataFrame:
        """
        按边界过滤数据
        
        Args:
            df: 包含地理坐标的DataFrame
            bounds: 边界字典 {'min_lat': ..., 'max_lat': ..., 'min_lon': ..., 'max_lon': ...}
            lat_col: 纬度列名
            lon_col: 经度列名
            
        Returns:
            过滤后的DataFrame
        """
        mask = (
            (df[lat_col] >= bounds['min_lat']) &
            (df[lat_col] <= bounds['max_lat']) &
            (df[lon_col] >= bounds['min_lon']) &
            (df[lon_col] <= bounds['max_lon'])
        )
        return df[mask].copy()
    
    def filter_china_bounds(self, df: pd.DataFrame,
                           lat_col: str = 'latitude',
                           lon_col: str = 'longitude') -> pd.DataFrame:
        """
        过滤中国范围内的数据
        
        Args:
            df: 包含地理坐标的DataFrame
            lat_col: 纬度列名
            lon_col: 经度列名
            
        Returns:
            中国范围内的数据
        """
        china_bounds = {
            'min_lat': 18,
            'max_lat': 53,
            'min_lon': 73,
            'max_lon': 135
        }
        return self.filter_by_bounds(df, china_bounds, lat_col, lon_col)
    
    def calculate_distance(self, lat1: float, lon1: float, 
                          lat2: float, lon2: float) -> float:
        """
        计算两点之间的距离（公里）
        使用Haversine公式
        
        Args:
            lat1, lon1: 第一个点的坐标
            lat2, lon2: 第二个点的坐标
            
        Returns:
            距离（公里）
        """
        R = 6371  # 地球半径（公里）
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def add_distance_column(self, df: pd.DataFrame,
                           center_lat: float,
                           center_lon: float,
                           lat_col: str = 'latitude',
                           lon_col: str = 'longitude',
                           new_col: str = 'distance_km') -> pd.DataFrame:
        """
        添加距离列到DataFrame
        
        Args:
            df: 包含地理坐标的DataFrame
            center_lat, center_lon: 中心点坐标
            lat_col: 纬度列名
            lon_col: 经度列名
            new_col: 新列名
            
        Returns:
            添加距离列后的DataFrame
        """
        df_result = df.copy()
        df_result[new_col] = df_result.apply(
            lambda row: self.calculate_distance(
                center_lat, center_lon,
                row[lat_col], row[lon_col]
            ),
            axis=1
        )
        return df_result
    
    def aggregate_by_grid(self, df: pd.DataFrame,
                         grid_size: float = 0.01,
                         lat_col: str = 'latitude',
                         lon_col: str = 'longitude',
                         value_col: Optional[str] = None) -> pd.DataFrame:
        """
        按网格聚合数据
        
        Args:
            df: 包含地理坐标的DataFrame
            grid_size: 网格大小（度）
            lat_col: 纬度列名
            lon_col: 经度列名
            value_col: 值列名（可选）
            
        Returns:
            聚合后的DataFrame
        """
        df_agg = df.copy()
        
        # 计算网格坐标
        df_agg['grid_lat'] = (df_agg[lat_col] / grid_size).astype(int) * grid_size
        df_agg['grid_lon'] = (df_agg[lon_col] / grid_size).astype(int) * grid_size
        
        # 按网格分组聚合
        if value_col:
            agg_func = {value_col: 'mean', lat_col: 'count'}
            agg_df = df_agg.groupby(['grid_lat', 'grid_lon']).agg(agg_func).reset_index()
            agg_df.rename(columns={lat_col: 'count', value_col: 'avg_value'}, inplace=True)
        else:
            agg_df = df_agg.groupby(['grid_lat', 'grid_lon']).size().reset_index(name='count')
        
        # 计算网格中心点
        agg_df['center_lat'] = agg_df['grid_lat'] + grid_size / 2
        agg_df['center_lon'] = agg_df['grid_lon'] + grid_size / 2
        
        return agg_df
    
    def create_heatmap_data(self, df: pd.DataFrame,
                           lat_col: str = 'latitude',
                           lon_col: str = 'longitude',
                           weight_col: Optional[str] = None,
                           normalize: bool = True) -> List[List[float]]:
        """
        创建热力图数据格式
        
        Args:
            df: 包含地理坐标的DataFrame
            lat_col: 纬度列名
            lon_col: 经度列名
            weight_col: 权重列名（可选）
            normalize: 是否归一化权重
            
        Returns:
            热力图数据列表 [[lat, lon, weight], ...]
        """
        if weight_col:
            weights = df[weight_col].values
            if normalize:
                max_weight = weights.max()
                if max_weight > 0:
                    weights = weights / max_weight
            return df[[lat_col, lon_col]].assign(weight=weights).values.tolist()
        else:
            return df[[lat_col, lon_col]].assign(weight=1).values.tolist()
    
    def convert_coordinate_system(self, df: pd.DataFrame,
                                 from_system: str = 'wgs84',
                                 to_system: str = 'gcj02',
                                 lat_col: str = 'latitude',
                                 lon_col: str = 'longitude') -> pd.DataFrame:
        """
        转换坐标系统
        
        Args:
            df: 包含地理坐标的DataFrame
            from_system: 源坐标系统 ('wgs84', 'gcj02', 'bd09')
            to_system: 目标坐标系统
            lat_col: 纬度列名
            lon_col: 经度列名
            
        Returns:
            转换坐标后的DataFrame
        """
        df_result = df.copy()
        
        # 坐标转换常量
        PI = math.pi
        A = 6378245.0  # 长半轴
        EE = 0.00669342162296594  # 偏心率平方
        
        def _transform_lat(x, y):
            ret = (-100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x)))
            ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
            ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
            ret += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
            return ret
        
        def _transform_lon(x, y):
            ret = (300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x)))
            ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
            ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
            ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
            return ret
        
        def wgs84_to_gcj02(lng, lat):
            dlat = _transform_lat(lng - 105.0, lat - 35.0)
            dlng = _transform_lon(lng - 105.0, lat - 35.0)
            radlat = lat / 180.0 * PI
            magic = math.sin(radlat)
            magic = 1 - EE * magic * magic
            sqrtmagic = math.sqrt(magic)
            dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
            dlng = (dlng * 180.0) / (A / sqrtmagic * math.cos(radlat) * PI)
            return lat + dlat, lng + dlng
        
        def gcj02_to_wgs84(lng, lat):
            # 反向转换（近似）
            wgs_lat, wgs_lng = wgs84_to_gcj02(lng, lat)
            return 2 * lat - wgs_lat, 2 * lng - wgs_lng
        
        # 根据坐标系统选择转换函数
        if from_system == 'wgs84' and to_system == 'gcj02':
            convert_func = wgs84_to_gcj02
        elif from_system == 'gcj02' and to_system == 'wgs84':
            convert_func = gcj02_to_wgs84
        else:
            print(f"不支持从 {from_system} 到 {to_system} 的转换")
            return df_result
        
        # 应用转换
        converted_coords = df_result.apply(
            lambda row: convert_func(row[lon_col], row[lat_col]),
            axis=1
        )
        
        df_result[lat_col] = converted_coords.apply(lambda x: x[0])
        df_result[lon_col] = converted_coords.apply(lambda x: x[1])
        
        return df_result
    
    def export_to_geojson(self, df: pd.DataFrame,
                         lat_col: str = 'latitude',
                         lon_col: str = 'longitude',
                         properties: Optional[List[str]] = None,
                         output_file: str = 'data.geojson') -> None:
        """
        导出数据为GeoJSON格式
        
        Args:
            df: 包含地理坐标的DataFrame
            lat_col: 纬度列名
            lon_col: 经度列名
            properties: 要包含的属性列列表
            output_file: 输出文件路径
        """
        features = []
        
        for _, row in df.iterrows():
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [row[lon_col], row[lat_col]]
                },
                'properties': {}
            }
            
            # 添加属性
            if properties:
                for prop in properties:
                    if prop in row:
                        feature['properties'][prop] = row[prop]
            
            features.append(feature)
        
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)
        
        print(f"数据已导出到 {output_file}")

def main():
    """主函数，演示数据处理功能"""
    processor = GeoDataProcessor()
    
    print("=== 地理数据处理工具演示 ===")
    
    # 创建示例数据
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'latitude': np.random.normal(39.9, 0.5, 100),
        'longitude': np.random.normal(116.4, 0.5, 100),
        'value': np.random.randint(1, 100, 100)
    })
    
    print(f"\n原始数据: {len(sample_data)} 条")
    print(sample_data.head())
    
    # 1. 清洗数据
    print("\n1. 清洗数据:")
    clean_data = processor.clean_geo_data(sample_data)
    
    # 2. 过滤中国范围
    print("\n2. 过滤中国范围:")
    china_data = processor.filter_china_bounds(clean_data)
    print(f"中国范围内数据: {len(china_data)} 条")
    
    # 3. 添加距离列
    print("\n3. 添加距离列:")
    data_with_distance = processor.add_distance_column(
        china_data, 39.9, 116.4  # 以北京为中心
    )
    print(data_with_distance[['latitude', 'longitude', 'distance_km']].head())
    
    # 4. 按网格聚合
    print("\n4. 按网格聚合:")
    grid_data = processor.aggregate_by_grid(china_data, grid_size=0.1)
    print(f"网格数量: {len(grid_data)}")
    print(grid_data.head())
    
    # 5. 创建热力图数据
    print("\n5. 创建热力图数据:")
    heatmap_data = processor.create_heatmap_data(china_data, weight_col='value')
    print(f"热力图数据点: {len(heatmap_data)}")
    
    # 6. 导出为GeoJSON
    print("\n6. 导出为GeoJSON:")
    processor.export_to_geojson(
        china_data,
        properties=['value'],
        output_file='sample_data.geojson'
    )

if __name__ == "__main__":
    main()
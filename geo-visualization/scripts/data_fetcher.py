#!/usr/bin/env python3
"""
地理数据获取工具脚本
用于获取地理位置信息、天气数据等
"""

import json
import requests
import pandas as pd
from typing import List, Dict, Tuple, Optional
import time

class GeoDataFetcher:
    """地理数据获取类"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化数据获取器
        
        Args:
            api_key: 高德地图API密钥（可选）
        """
        self.api_key = api_key
        self.session = requests.Session()
        
    def get_location_by_ip(self, ip: str) -> Optional[Dict]:
        """
        通过IP地址获取地理位置
        
        Args:
            ip: IP地址
            
        Returns:
            包含经纬度和地址的字典
        """
        try:
            # 使用免费IP地理定位API
            url = f"http://ip-api.com/json/{ip}?lang=zh-CN"
            response = self.session.get(url, timeout=5)
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    'ip': ip,
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'country': data.get('country'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                    'isp': data.get('isp')
                }
            return None
        except Exception as e:
            print(f"获取IP地理位置失败: {e}")
            return None
    
    def get_weather_by_city(self, city: str) -> Optional[Dict]:
        """
        获取城市天气信息
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息字典
        """
        try:
            # 使用wttr.in免费天气API
            url = f"https://wttr.in/{city}?format=j1"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            current = data.get('current_condition', [{}])[0]
            return {
                'city': city,
                'temperature': current.get('temp_C'),
                'weather': current.get('lang_zh', [{}])[0].get('value', '未知'),
                'humidity': current.get('humidity'),
                'wind_speed': current.get('windspeedKmph'),
                'wind_direction': current.get('winddir16Point'),
                'pressure': current.get('pressure'),
                'visibility': current.get('visibility')
            }
        except Exception as e:
            print(f"获取天气信息失败: {e}")
            return None
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        将地址转换为经纬度坐标
        
        Args:
            address: 地址字符串
            
        Returns:
            (纬度, 经度) 元组
        """
        try:
            # 使用Nominatim地理编码服务
            from geopy.geocoders import Nominatim
            
            geolocator = Nominatim(user_agent="geo_visualization_tool")
            location = geolocator.geocode(address, timeout=10)
            
            if location:
                return (location.latitude, location.longitude)
            return None
        except Exception as e:
            print(f"地理编码失败: {e}")
            return None
    
    def batch_geocode(self, addresses: List[str], delay: float = 1.0) -> List[Dict]:
        """
        批量地理编码
        
        Args:
            addresses: 地址列表
            delay: 请求间隔（秒）
            
        Returns:
            包含地址和坐标的字典列表
        """
        results = []
        for i, address in enumerate(addresses):
            coords = self.geocode_address(address)
            if coords:
                results.append({
                    'address': address,
                    'latitude': coords[0],
                    'longitude': coords[1]
                })
            else:
                results.append({
                    'address': address,
                    'latitude': None,
                    'longitude': None
                })
            
            # 避免请求过于频繁
            if i < len(addresses) - 1:
                time.sleep(delay)
        
        return results
    
    def get_china_provinces_geojson(self) -> Optional[Dict]:
        """
        获取中国省份GeoJSON数据
        
        Returns:
            GeoJSON字典
        """
        try:
            # 从DataV.GeoAtlas获取中国省份数据
            url = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
            response = self.session.get(url, timeout=10)
            return response.json()
        except Exception as e:
            print(f"获取省份GeoJSON失败: {e}")
            return None
    
    def generate_sample_data(self, data_type: str = "random", count: int = 100) -> pd.DataFrame:
        """
        生成示例数据
        
        Args:
            data_type: 数据类型 ("random", "beijing", "china_cities")
            count: 数据点数量
            
        Returns:
            包含经纬度数据的DataFrame
        """
        import numpy as np
        
        if data_type == "random":
            # 随机生成中国范围内的坐标
            np.random.seed(42)
            data = {
                'latitude': np.random.uniform(18, 53, count),  # 中国纬度范围
                'longitude': np.random.uniform(73, 135, count),  # 中国经度范围
                'value': np.random.randint(1, 100, count)
            }
            return pd.DataFrame(data)
        
        elif data_type == "beijing":
            # 以北京为中心的坐标
            np.random.seed(42)
            data = {
                'latitude': np.random.normal(39.9, 0.1, count),
                'longitude': np.random.normal(116.4, 0.1, count),
                'value': np.random.randint(1, 100, count)
            }
            return pd.DataFrame(data)
        
        elif data_type == "china_cities":
            # 中国主要城市坐标
            cities = [
                ('北京', 39.9042, 116.4074),
                ('上海', 31.2304, 121.4737),
                ('广州', 23.1291, 113.2644),
                ('深圳', 22.5431, 114.0579),
                ('成都', 30.5728, 104.0668),
                ('杭州', 30.2741, 120.1551),
                ('武汉', 30.5928, 114.3055),
                ('西安', 34.3416, 108.9398),
                ('重庆', 29.5630, 106.5516),
                ('天津', 39.3434, 117.3616)
            ]
            
            data = []
            for city, lat, lon in cities:
                data.append({
                    'city': city,
                    'latitude': lat,
                    'longitude': lon,
                    'value': np.random.randint(10, 100)
                })
            
            return pd.DataFrame(data)
        
        else:
            raise ValueError(f"未知的数据类型: {data_type}")

def main():
    """主函数，演示数据获取功能"""
    fetcher = GeoDataFetcher()
    
    print("=== 地理数据获取工具演示 ===")
    
    # 1. 获取IP地理位置
    print("\n1. 获取IP地理位置:")
    ip_info = fetcher.get_location_by_ip("8.8.8.8")
    if ip_info:
        print(f"IP: {ip_info['ip']}")
        print(f"位置: {ip_info['country']} {ip_info['region']} {ip_info['city']}")
        print(f"坐标: {ip_info['latitude']}, {ip_info['longitude']}")
    
    # 2. 获取天气信息
    print("\n2. 获取天气信息:")
    weather_info = fetcher.get_weather_by_city("北京")
    if weather_info:
        print(f"城市: {weather_info['city']}")
        print(f"温度: {weather_info['temperature']}°C")
        print(f"天气: {weather_info['weather']}")
        print(f"湿度: {weather_info['humidity']}%")
    
    # 3. 生成示例数据
    print("\n3. 生成示例数据:")
    sample_data = fetcher.generate_sample_data("china_cities")
    print(sample_data.head())
    
    # 4. 保存数据到文件
    sample_data.to_csv("sample_geo_data.csv", index=False, encoding='utf-8-sig')
    print("\n示例数据已保存到 sample_geo_data.csv")

if __name__ == "__main__":
    main()
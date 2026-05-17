# Geo-Visualization Skill

A comprehensive toolkit for geographic data visualization, supporting heatmaps, province visualization, scatter plots, and map generation.

## Features

- **Heatmap Visualization**: Display data density based on geographic locations
- **Province Visualization**: Show statistical data by administrative divisions
- **Scatter Visualization**: Display discrete data points on geographic locations
- **Map Generation**: Create interactive HTML maps
- **Data Fetching**: Support IP geolocation and weather data retrieval
- **Data Processing**: Coordinate transformation, data cleaning, and aggregation analysis

## Quick Start

### Install Dependencies
```bash
pip install folium pandas numpy geopy requests
```

### Basic Usage

#### 1. Create Heatmap
```python
from scripts.visualizer import GeoVisualizer
import pandas as pd
import numpy as np

# Create sample data
data = pd.DataFrame({
    'latitude': np.random.normal(39.9, 0.5, 100),
    'longitude': np.random.normal(116.4, 0.5, 100),
    'value': np.random.randint(1, 100, 100)
})

# Create heatmap
visualizer = GeoVisualizer(center=(39.9, 116.4), zoom_start=10)
visualizer.create_heatmap_from_df(
    data,
    weight_col='value',
    output_file='heatmap.html'
)
```

#### 2. Fetch Weather Data
```python
from scripts.data_fetcher import GeoDataFetcher

fetcher = GeoDataFetcher()
weather = fetcher.get_weather_by_city("Beijing")
print(f"Beijing Weather: {weather['temperature']}°C, {weather['weather']}")
```

#### 3. Process Geographic Data
```python
from scripts.data_processor import GeoDataProcessor

processor = GeoDataProcessor()
clean_data = processor.clean_geo_data(raw_data)
china_data = processor.filter_china_bounds(clean_data)
```

## Workflow

1. **Data Preparation**
   - Collect geographic coordinate data (latitude/longitude)
   - Clean and validate data format
   - Optional: Add weight column for heatmap intensity

2. **Choose Visualization Type**
   - Heatmap: Display data density distribution
   - Scatter plot: Show discrete data point locations
   - Province visualization: Display statistical data by administrative divisions
   - Aggregation: Show data point aggregation effects

3. **Configure Map Parameters**
   - Set center coordinates
   - Choose map style (default, terrain, satellite)
   - Configure zoom level and interaction options

4. **Add Data Layers**
   - Use corresponding visualization plugins
   - Configure colors, sizes, transparency, etc.
   - Add legends and annotations

5. **Export and Share**
   - Save as HTML file (interactive)
   - Export as image (static)
   - Embed into web applications

## Directory Structure

```
skills/geo-visualization/
├── SKILL.md           # Skill documentation
├── REFERENCE.md       # Detailed API reference
├── EXAMPLES.md        # Usage examples
├── README.md          # Chinese README
├── README_EN.md       # English README
└── scripts/           # Utility scripts
    ├── data_fetcher.py    # Data fetching script
    ├── data_processor.py  # Data processing script
    └── visualizer.py      # Visualization script
```

## Use Cases

### 1. IP Address Geographic Distribution
Visualize the geographic distribution of website visitors' IP addresses to identify high-traffic areas.

### 2. City Weather Display
Display weather information for various cities on a map, using different colors and sizes to represent temperature and weather conditions.

### 3. Population Density Analysis
Display China's population density by province, with color depth indicating population density levels.

### 4. Business Location Analysis
Analyze potential business locations by combining population density, competitor locations, and transportation accessibility.

### 5. Time Series Animation
Show processes that change over time, such as epidemic spread, population migration, etc.

## API Reference

### Core Classes

#### GeoDataFetcher
- `get_location_by_ip(ip)`: Get geographic location by IP address
- `get_weather_by_city(city)`: Get city weather information
- `geocode_address(address)`: Convert address to latitude/longitude coordinates
- `batch_geocode(addresses)`: Batch geocoding
- `get_china_provinces_geojson()`: Get China province GeoJSON data
- `generate_sample_data(data_type, count)`: Generate sample data

#### GeoDataProcessor
- `validate_coordinates(latitude, longitude)`: Validate if coordinates are valid
- `clean_geo_data(df)`: Clean geographic data
- `filter_by_bounds(df, bounds)`: Filter data by bounds
- `filter_china_bounds(df)`: Filter data within China bounds
- `calculate_distance(lat1, lon1, lat2, lon2)`: Calculate distance between two points
- `add_distance_column(df, center_lat, center_lon)`: Add distance column
- `aggregate_by_grid(df, grid_size)`: Aggregate data by grid
- `create_heatmap_data(df)`: Create heatmap data format
- `convert_coordinate_system(df)`: Convert coordinate system
- `export_to_geojson(df)`: Export data to GeoJSON format

#### GeoVisualizer
- `create_base_map(tiles)`: Create base map
- `add_heatmap(data)`: Add heatmap layer
- `add_markers(df)`: Add markers
- `add_circle_markers(df)`: Add circle markers
- `add_choropleth(geo_data, data)`: Add choropleth layer
- `add_layer_control()`: Add layer control
- `add_legend(legend_html)`: Add custom legend
- `save_map(output_file)`: Save map as HTML file
- `create_heatmap_from_df(df)`: Create heatmap from DataFrame
- `create_marker_map_from_df(df)`: Create marker map from DataFrame
- `create_choropleth_map(geo_data, data)`: Create choropleth map
- `create_weather_map(weather_data)`: Create weather map

## Data Sources

### Geographic Coordinate Data
- GPS data: From mobile devices or GPS loggers
- IP geolocation: Query geographic location by IP address
- Address geocoding: Convert addresses to latitude/longitude coordinates

### Administrative Division Data
- China province boundaries: GeoJSON format provincial administrative divisions
- City boundaries: Municipal administrative division data
- District/county boundaries: District/county level administrative division data

### Statistical Data
- Population data: Population statistics published by National Bureau of Statistics
- Economic data: GDP, income, and other economic indicators
- Weather data: Meteorological station observation data

## Performance Optimization

### Large Data Volume Processing
1. **Data Sampling**: Random sampling of large datasets
2. **Aggregated Display**: Use MarkerCluster for point aggregation
3. **Chunked Loading**: Load data by region or time chunks

### Rendering Optimization
1. **WebGL Acceleration**: Use Leaflet.gl plugin
2. **Canvas Rendering**: Use Canvas instead of SVG for large numbers of points
3. **Layer Caching**: Cache rendered layers

## Common Issues

### 1. Coordinate Offset
Check if the coordinate system is correct (WGS84/GCJ02/BD09). Maps in China need to use GCJ02 coordinate system.

### 2. Data Format Error
Ensure GeoJSON format is correct, coordinate order is [longitude, latitude].

### 3. Memory Overflow
Use streaming processing or data sampling for large datasets.

### 4. Slow Map Loading
Reduce number of data points, use aggregated display, or enable WebGL acceleration.

## Extended Resources

### Related Libraries
- **Folium**: Python map visualization library
- **Leaflet**: JavaScript map library
- **Mapbox GL**: High-performance map rendering
- **Deck.gl**: Large-scale data visualization

### Data Resources
- **DataV.GeoAtlas**: China administrative division GeoJSON
- **Alibaba Cloud Data Visualization**: Geographic datasets
- **National Bureau of Statistics**: Official statistical data

## License

MIT License

## Contributions

Welcome to submit Issues and Pull Requests to improve this tool.
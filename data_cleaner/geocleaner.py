import geopandas as gpd
from shapely.geometry import Point, Polygon

def check_geo_integrity(dataframe, lat_col, lon_col, boundary):
    """
    Check if geographic coordinates fall within a specified boundary.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame containing the geographic data.
    - lat_col (str): Column name for latitude.
    - lon_col (str): Column name for longitude.
    - boundary (Polygon): A Shapely Polygon defining the boundary.

    Returns:
    - pd.DataFrame: DataFrame with a new column 'geo_valid' indicating if the point is within the boundary.
    """
    # create gdb from normal df
    gdf = gpd.GeoDataFrame(dataframe, geometry=[Point(xy) for xy in zip(dataframe[lon_col], dataframe[lat_col])])

    # check if points are within boundary
    gdf['geo_valid'] = gdf['geometry'].apply(lambda point: point.within(boundary))
    gdf['orignal_Longitude'] = gdf['geometry'].x
    gdf['original_Latitude'] = gdf['geometry'].y
    gdf.drop(columns=['geometry'], inplace=True)

    return gdf

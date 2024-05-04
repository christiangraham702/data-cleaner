import pandas as pd


def remove_duplicates(dataframe):
    return dataframe.drop_duplicates()

def fill_missing(dataframe, strategies=None, custom_values=None, verbose=True):
    """
    Fill missing values in a DataFrame using various strategies.

    Parameters:
    - dataframe (pd.DataFrame): DataFrame with missing values.
    - strategies (dict): A dictionary specifying fill strategies ('mean', 'median', 'mode', 'ffill', 'bfill') for specific columns.
    - custom_values (dict): A dictionary specifying exact fill values for specific columns.
    - verbose (bool): If True, print information about the fill operations performed.

    Returns:
    - pd.DataFrame: DataFrame with missing values filled.
    """
    if strategies:
        for column, method in strategies.items():
            if method == 'mean' and dataframe[column].dtype in ['float64', 'int64']:
                dataframe[column] = dataframe[column].fillna(dataframe[column].mean())
            elif method == 'median' and dataframe[column].dtype in ['float64', 'int64']:
                dataframe[column] = dataframe[column].fillna(dataframe[column].median())
            elif method == 'mode':
                mode_value = dataframe[column].mode().iloc[0]
                dataframe[column] = dataframe[column].fillna(mode_value)
            elif method == 'ffill':
                dataframe[column] = dataframe[column].ffill()
            elif method == 'bfill':
                dataframe[column] = dataframe[column].bfill()
            if verbose:
                print(f"Filled missing values in {column} using {method}")

    if custom_values:
        for column, value in custom_values.items():
            dataframe[column] = dataframe[column].fillna(value)
            if verbose:
                print(f"Filled missing values in {column} with custom value {value}")

    return dataframe


def normalize_data(dataframe, text_norm='lower', scale_nums=False, date_cols=None):
    """
    Normalize data in a DataFrame.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame to normalize.
    - text_norm (str): Normalization for text data ('lower', 'upper', 'title').
    - scale_nums (bool): Whether to scale numerical columns using Min-Max scaling.
    - date_cols (dict): Dictionary specifying columns and formats to parse dates.

    Returns:
    - pd.DataFrame: The normalized DataFrame.
    """
    # Normalize text data
    if text_norm in ['lower', 'upper', 'title']:
        for column in dataframe.select_dtypes(include=[object]):
            if text_norm == 'lower':
                dataframe[column] = dataframe[column].str.lower()
            elif text_norm == 'upper':
                dataframe[column] = dataframe[column].str.upper()
            elif text_norm == 'title':
                dataframe[column] = dataframe[column].str.title()

    # Scale numerical data
    if scale_nums:
        for column in dataframe.select_dtypes(include=[int, float]):
            min_val = dataframe[column].min()
            max_val = dataframe[column].max()
            dataframe[column] = (dataframe[column] - min_val) / (max_val - min_val)

    # Standardize date columns
    if date_cols:
        for column, fmt in date_cols.items():
            dataframe[column] = pd.to_datetime(dataframe[column], format=fmt, errors='coerce')

    return dataframe



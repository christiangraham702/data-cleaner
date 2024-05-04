import argparse
import pandas as pd
import json
from data_cleaner.cleaner import remove_duplicates, fill_missing, normalize_data
from data_cleaner.geocleaner import check_geo_integrity
from shapely.geometry import Polygon

def main():
    parser = argparse.ArgumentParser(description="Data Cleaning CLI Tool")
    parser.add_argument("input_file", type=str, help="Path to the input data file to be cleaned")
    parser.add_argument("--remove-duplicates", action="store_true", help="Remove duplicate rows")
    parser.add_argument("--fill-strategies", type=str, help="JSON string specifying missing value fill strategies for columns")
    parser.add_argument("--normalize", action="store_true", help="Normalize data formats")
    parser.add_argument("--text-norm", type=str, choices=['lower', 'upper', 'title'], help="Normalize text data (lower, upper, title)")
    parser.add_argument("--scale-nums", action='store_true', help="Scale numerical data using min-max normalization")
    parser.add_argument("--date-cols", type=str, help="JSON string specifying date columns and their formats")
    parser.add_argument("--check-geo", action='store_true', help="Check geospatial integrity")
    parser.add_argument("--lat-col", type=str, help="Latitude column name")
    parser.add_argument("--lon-col", type=str, help="Longitude column name")
    parser.add_argument("--boundary", type=str, help="Boundary polygon as a string of coordinates")
    parser.add_argument("--output", type=str, help="Specify output file path")
    args = parser.parse_args()

    # Read the input file
    try:
        if args.input_file.endswith('.csv'):
            cleaned_df = pd.read_csv(args.input_file)
        elif args.input_file.endswith('.xlsx'):
            cleaned_df = pd.read_excel(args.input_file)
        else:
            print("Unsupported file format. Please use .csv or .xlsx files.")
            return
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return

    # Data cleaning operations
    if args.remove_duplicates:
        try:
            cleaned_df = remove_duplicates(cleaned_df)
            print('\nDuplicates removed ✅')
        except Exception as e:
            print('Error removing duplicates: ', str(e))

    if args.fill_strategies:
        try:
            strategies = json.loads(args.fill_strategies)
            cleaned_df = fill_missing(cleaned_df, strategies=strategies)
            print('Missing values filled ✅')
        except Exception as e:
            print('Error filling missing values: ', str(e))

    if args.normalize:
        try:
            cleaned_df = normalize_data(cleaned_df, text_norm=args.text_norm, scale_nums=args.scale_nums)
            print('Data normalized ✅')
        except Exception as e:
            print('Error normalizing data: ', str(e))

    if args.check_geo:
        try:
            boundary = Polygon([(float(lon), float(lat)) for lon, lat in json.loads(args.boundary)])
            cleaned_df = check_geo_integrity(cleaned_df, args.lat_col, args.lon_col, boundary)
            print('Geospatial integrity checked ✅')
        except Exception as e:
            print('Error in geospatial integrity check: ', str(e))

    # Save the cleaned DataFrame
    try:
        output_file = args.output if args.output else 'cleaned_data.csv'
        cleaned_df.to_csv(output_file, index=False)
        print(f'\nData cleaning complete. Cleaned data saved to {output_file}')
    except Exception as e:
        print('Error saving the cleaned data: ', str(e))

if __name__ == "__main__":
    main()

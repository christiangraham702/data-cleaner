## Data Cleaning CLI Tool

This is a CLI tool designed to automate data cleaning and preprocessing datasets. It currently can remove duplicates, fill missing values, normalize data, and chek the integrity of geospatial data. I find it the easiest to use when I only do one opeation at time, as some more complex operations have many parameters.

### Installation

- Make sure you have python3 installed. 
- Clone this repository
  - `git clone https://github.com/christiangraham702/data-cleaner`
- **Optional:** Create a virtual environment to run the tool
  - `python3 -m venv venv`
  - `source venv/bin/activate`
- and then install dependencies with:
  - `pip install -r requirements.txt` 

The tool can be invoked from the command line by specifying different flags for each cleaning operation you wish to perform. Below is the description of how to use each functionality:
<br><br>

### 1. Removing Duplicates

To remove duplicate rows from your dataset, use the --remove-duplicates flag. This function checks for and removes any rows that are complete duplicates of another.

`python3 main.py <input_file> --remove-duplicates --output <output_file>`


### 2. Filling Missing Values

Missing values in the dataset can be filled using a specified strategy per column. Strategies include 'mean', 'median', 'mode', 'ffill' (forward fill), and 'bfill' (backward fill). Use the --fill-strategies flag followed by a JSON string that describes the strategy for each column.

`python main.py <input_file> --fill-strategies '{"column1": "mean", "column2": "mode"}' --output <output_file>`<br>

**Ensure the json string is formatted correctly**



### 3. Normalizing Data

Data normalization includes converting text to a uniform case (lower, upper, title) and scaling numerical columns using min-max normalization. Use the --normalize flag along with --text-norm for text normalization and --scale-nums for numerical scaling.

`python main.py <input_file> --normalize --text-norm title --scale-nums --output <output_file>`<br>

**`--scale-nums` normalizes all numbers in a table**



### 4. Checking Geospatial Integrity

To check the geospatial integrity of data, specify the columns containing latitude and longitude data and define a boundary within which the points should lie. The boundary should be provided as a JSON string of coordinates forming a polygon.

`python main.py <input_file> --check-geo --lat-col "Latitude" --lon-col "Longitude" --boundary '[[-180, -90], [-180, 90], [180, 90], [180, -90]]' --output <output_file>`

**Ensure json string is formatted correctly `'[[lat, long], ..., [lat,long]]'`**




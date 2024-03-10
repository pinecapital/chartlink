import pandas as pd

def read_instruments_to_dataframe(file_path):
    # Read the JSON file into a pandas DataFrame
    df = pd.read_json(file_path)
    
    # Optionally, perform any necessary data cleaning or transformations here
    # For example, you might want to convert string dates to datetime objects:
    # df['date_column'] = pd.to_datetime(df['date_column'])
    
    return df

def main():
    instruments_file_path = 'instruments.json'  # Adjust the file path if necessary
    instruments_df = read_instruments_to_dataframe(instruments_file_path)
    
    # Now you can use instruments_df to perform various analyses or data manipulations
    print(instruments_df.head())  # Display the first few rows of the DataFrame

if __name__ == "__main__":
    main()

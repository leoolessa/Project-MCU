import pandas as pd 
import csv
import os


def csv_read(file):
    """_summary_

    Args:
        file (str): Name of the CSV file (without extension) to be read.

    Returns:
        DataFrame: DataFrame containing data read from the specified CSV file.
    """
    df = pd.read_csv(f'data/datasets/{file}.csv')
    return df


def save_as_csv(input_string, filename):
    lines = input_string.strip().split('\n')
    data_lines = lines[1:]
    data = []
    for line in data_lines:
        values = line.split('\t')
        data.append(values)
    header = ["Units", "Comic-book Title", "Issue", "Price",'On sale', "Publisher", "Est. units"]
    if not filename.endswith('.csv'):
        filename += '.csv'
    data_folder = 'data/datasets'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    filepath = os.path.join(data_folder, filename)
    with open(filepath, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        csv_writer.writerows(data)
        
        
input_string = '''
Units	Comic-book Title	Issue	Price	On sale	Publisher	Est. units
'''        
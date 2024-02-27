import pandas as pd 
import numpy as np
from math import log10, floor

def generate_last_digits(index):
    """
    Summary: 
        Generates the last digits of an index.
    Args:
        index (int): The index from which to generate the last digits.
    Returns:
        int: The generated last digits.

    """
    num_digits = len(str(index))
    return index % (1 ** (num_digits - 5))


def format_number(value):
    """
    Summary: 
        Formats a numerical value into a string with appropriate units (M, K) based on magnitude.
    Args:
        value (float): The numerical value to be formatted.
    Returns:
        str: The formatted value as a string.
    """
    if value >= 1e6:
        return f"{value / 1e6:.2f}M"
    elif value >= 1e3:
        return f"{value / 1e3:.2f}K"
    else:
        return f"{value:.2f}"


def comics_creator(data, date):
    """_summary_

    Args:
        data (DataFrame): A DataFrame containing comic book data.
        date (str): The publish date for the comics.

    Returns:
        DataFrame: Processed DataFrame with added columns and formatted values.
    """
    data['Publish Date'] = date
    second_column = data.pop('Publish Date')
    data.insert(1, 'Publish Date', second_column)
    data['Price'] = data['Price'].replace('[\$,]', '', regex=True).astype(float)
    data['Est. units'] = data['Est. units'].replace(',', '', regex=True).astype(float)
    data['Total'] = data['Price'] * data['Est. units']
    data['Comic_ID'] = data.index
    
    data_list = []
    df = pd.DataFrame(columns=['Comic_ID', 'Publish Date', 'Comic-book Title', 'Price', 'Publisher', 'Est. units', 'Total', 'Unformatted Total'])
    
    for index, result in data.iterrows():
        local = {}
        local['Comic_ID'] = result['Comic_ID']
        local['Publish Date'] = result['Publish Date']
        local['Comic-book Title'] = result['Comic-book Title']
        local['Price'] = result['Price']
        local['Publisher'] = result['Publisher']
        local['Est. units'] = result['Est. units']
        local['Unformatted Total'] = result['Total']
        data_list.append(local)
    df = pd.DataFrame(data_list)
        
    df['Total'] = df['Unformatted Total'].apply(format_number)
        
    df['Publish Date'] = df['Publish Date'].astype(int)
    last_two_digits = str(date[-2:])
    identifier = {'legend': 315, 'date': last_two_digits, 'index': df.index}
    last_digits = generate_last_digits(df.index)
    df['Comic_ID'] = str(identifier['legend']) + str(identifier['date']) + last_digits.astype(str) + identifier['index'].astype(str)
    
    file_name = f'comic_{date}'
    df.to_csv(f'data/comics_by_year/{file_name}.csv', index=False)
    
    return df


def box_characters_creator(df, check_list, date):
    """_summary_

    Args:
        df (DataFrame): The DataFrame containing comic book data.
        check_list (list): A list of character names to filter the DataFrame.
        date (str): The date associated with the characters.

    Returns:
        DataFrame: Processed DataFrame with character information, including IDs and totals.
    """
    matches = df[df['Comic-book Title'].str.contains('|'.join(check_list))]
    result_dict = {}
    for valor_b in check_list:
        matching_rows = matches[matches['Comic-book Title'].str.contains(valor_b)]
        if not matching_rows.empty:
            result_dict[valor_b] = {'Name': valor_b, 'Total': matching_rows['Unformatted Total'].sum()} 
    result_df = pd.DataFrame.from_dict(result_dict, orient='index').reset_index()
    result_df.columns = ['Character_Name', 'Character_ID', 'Unformatted Total']
    
    identifier = []
    check_letter = {'box': 21524}
    identifier.append(check_letter.get('box',0))
    result_df['Date'] = date
    result_df['Date'] = result_df['Date'].astype(int)
    last_two_digits = result_df['Date'] % 100
    identifier.append(last_two_digits.unique()[0])
    identifier.append(result_df.index)
    result_df['Character_ID'] = result_df.index
    result_df['Character_ID'] = identifier[0] * 10000 + identifier[1] * 100 + identifier[2]
    
    result_df['Total'] = result_df['Unformatted Total'].apply(format_number)
    
    result_df = result_df[['Character_ID', 'Date', 'Character_Name', 'Total', 'Unformatted Total']]
    file_name = f'box_office_characters_{date}'
    result_df.to_csv(f'data/characters_by_year/{file_name}.csv', index=False)
    
    return result_df


def film_creator(df):
    """_summary_

    Args:
        df (DataFrame): DataFrame containing film-related data.

    Returns:
        DataFrame: Processed DataFrame with added columns, formatted values, and unique Film_IDs.
    """
    identifier = []
    check_letter = {'m': 13}
    identifier.append(check_letter.get('m',0))
    
    df['Opening weekend(North America)'] = df['Opening weekend(North America)'].replace('[\$,]', '', regex=True).astype(float)
    df['North America'] = df['North America'].replace('[\$,]', '', regex=True).astype(float)
    df['Other territories'] = df['Other territories'].replace('[\$,]', '', regex=True).astype(float)
    df['Worldwide'] = df['Worldwide'].replace('[\$,]', '', regex=True).astype(float)
    
    df['For Opening weekend(North America)'] = df['Opening weekend(North America)'].apply(format_number)
    df['For North America'] = df['North America'].apply(format_number)
    df['For Other territories'] = df['Other territories'].apply(format_number)
    df['For Worldwide'] = df['Worldwide'].apply(format_number)
    
    df['Release year'] = df['Release date(United States)'].str.extract(r'(\d{4})')
    df['Release year'] = df['Release year'].astype(int)
    df.drop('Release date(United States)', axis=1, inplace=True)
    second_column = df.pop('Release year')
    df.insert(2, 'Release year', second_column)
    last_two_digits = df['Release year'] % 100
    
    identifier.append(last_two_digits.unique()[0])
    identifier.append(df.index)
    
    df['Film_ID'] = df.index
    df['Film_ID'] = identifier[0] * 10000 + identifier[1] * 100 + identifier[2]
    
    cols = list(df.columns)
    cols = ['Film_ID'] + cols[:-1]
    df = df[cols]
    
    df.to_csv(f'data/box_office_film.csv', index=False)
    df.to_excel(f'data/excel/box_office_film.xlsx', index=False)
    return df


def join_df(dfs, name):
    """_summary_

    Args:
        dfs (list): List of DataFrames to be concatenated.
        name (str): Name used for saving the resulting CSV and Excel files.

    Returns:
        None
    """
    df = pd.concat(dfs, ignore_index=True)
    file_name = f'{name}'
    df.to_csv(f'data/{file_name}.csv', index=False)
    df.to_excel(f'data/excel/{file_name}.xlsx', index=False)


check_list = [
    'Absorbing Man', 'A.I.M.', 'Anole', 'Apocalypse', 'Archangel', 'Avalanche', 'Bastion', 'Beast',
    'Beyonder', 'Black Panther', 'Black Widow', 'Blob', 'Cable', 'Cannonball', 'Captain America',
    'Cassandra Nova', 'Chamber', 'Colossus', 'Crossbones', 'Cypher', 'Daredevil', 'Dark Phoenix',
    'Deadpool', 'Doctor Strange', 'Domino', 'Dust', 'Emma Frost', 'Exodus', 'Falcon', 'Fantomex',
    'Feral', 'Forge', 'Gambit', 'Gideon', 'Grandmaster', 'Grim Reaper', 'Havok', 'Hela', 'Hellion',
    'Hope Summers', 'Hulk', 'Iceman', 'Iron Man', 'Iron Patriot', 'Jean Grey', 'Jean Grey', 'Jubilee',
    'Juggernaut', 'Juggernaut', 'Kang', 'Karma', 'Korvac', 'Klaw', 'Lady Deathstrike', 'Living Laser',
    'Loki', 'Longshot', 'Luke Cage', 'M.O.D.O.K.', 'Magneto', 'Marrow', 'Mastermind', 'Master Mold',
    'Marauders', 'Marvel Boy', 'Multiple Man', 'Mystique', 'Nightcrawler', 'Omega Red', 'Onslaught',
    'Pixie', 'Polaris', 'Prodigy', 'Professor X', 'Psylocke', 'Red Skull', 'Rhino', 'Rockslide',
    'Rogue', 'Scarlet Witch', 'Sebastian Shaw', 'Selene', 'Shadowcat', 'Shadow King', 'Shatterstar',
    'Silver Samurai', 'Sinister Six', 'Skrulls', 'Sage', 'Spider-Man', 'Storm', 'Strong Guy', 'Sunspot',
    'Surge', 'Taskmaster', 'Thanos', 'The Hand', 'The Hood', 'Thor', 'U-Foes', 'Ultron', 'Vision',
    'Warpath', 'Wasp', 'William Stryker', 'Wolverine', 'Wolverine', 'X-23','X-Men', 'Avengers',
    'Ghost Rider', 'Venom', 'Dark Phoenix', 'Inhumans', 'Guardians of the Galaxy', 'Logan', 'Fantastic Four',
    'Punisher'
]


















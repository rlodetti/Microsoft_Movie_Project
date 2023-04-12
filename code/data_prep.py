import pandas as pd
import string

def prep_the_numbers(df):
    """
    This function cleans and prepares the_numbers dataframe.
    """
    # Convert currencies to integers.
    for i in ['production_budget', 'worldwide_gross']:
        df[i] = df[i].str.replace('$', '')
        df[i] = df[i].str.replace(',', '')
        df[i] = df[i].str.replace(' ', '')
        df[i] = df[i].astype(int)

    # Extracting the year from 'release_date' column.
    df['year'] = pd.to_datetime(df['release_date']).dt.year

    # Norming and filtering column names
    df.rename(columns={
        'movie': 'title',
        'production_budget': 'budget'
    },
              inplace=True)
    for i in ['title']:
        df[i] = df[i].str.translate(str.maketrans('', '', string.punctuation))
        df[i] = df[i].str.replace(' ', '')
        df[i] = df[i].str.lower()
    df = df[['title', 'year', 'budget', 'worldwide_gross']]
    return df


def prep_imdb(df):
    """
    This function cleans and prepares the imdb dataframe.
    """
    # Cleaning/Norming the title names
    for i in ['title']:
        df[i] = df[i].str.translate(str.maketrans('', '', string.punctuation))
        df[i] = df[i].str.replace(' ', '')
        df[i] = df[i].str.lower()
    # Expanding the comma separated genres column into one genre per row.
    df['genres'] = df['genres'].map(lambda x: x.split(','), na_action='ignore')
    df = df.explode('genres')
    return df


def merge(df1, df2):
    """
    This function merges the_numbers and imdb dataframes.
    """
    df = pd.merge(df1, df2, how='inner', on=['title', 'year'])
    return df


def add_features(df):
    """
    This function takes the movies dataframe, calculates a ROI column, 
    finds the top and bottom producers by ROI, and labels them via a 
    producer_rank colum.
    """
    # Calculate and add an ROI column
    profit_df = df['worldwide_gross'] - df['budget']
    df['ROI'] = (profit_df / df['budget']) * 100

    # Find top and bottom 5 producers by ROI, with a minimum of 7 movie credits.
    producers_df = df.drop_duplicates(['movie_id', 'producer'])
    producer_count_df = producers_df['producer'].value_counts()
    producer_count_filtered_df = producer_count_df[producer_count_df > 6]
    producer_count_filtered_list = list(producer_count_filtered_df.index)
    producers_filtered_df = producers_df[producers_df['producer'].isin(
        producer_count_filtered_list)]
    producers_roi_df = producers_filtered_df.groupby(
        'producer').median()['ROI'].sort_values(ascending=False)
    high_roi_producers_list = list(producers_roi_df.head(5).index)
    low_roi_producers_list = list(producers_roi_df.tail(5).index)

    # Add a producer_rank column labeling producer groups
    df.loc[df['producer'].isin(high_roi_producers_list),
           'producer_rank'] = 'High ROI Producers'
    df.loc[df['producer'].isin(low_roi_producers_list),
           'producer_rank'] = 'Low ROI Producers'
    return df
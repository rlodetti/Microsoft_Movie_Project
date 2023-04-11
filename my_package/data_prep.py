import pandas as pd
import string

def prep_the_numbers(df):
    # Convert currencies to integers.
    for i in ['production_budget', 'worldwide_gross']:
        df[i] = df[i].str.replace('$', '')
        df[i] = df[i].str.replace(',', '')
        df[i] = df[i].str.replace(' ', '')
        df[i] = df[i].astype(int)

    # Extracting the year from 'release_date' column.
    df['year'] = pd.to_datetime(df['release_date']).dt.year

    # Norming and filtering column names
    df.rename(columns={'movie': 'title',
                       'production_budget': 'budget'}, inplace=True)
    for i in ['title']:
        df[i] = df[i].str.translate(str.maketrans('', '', string.punctuation))
        df[i] = df[i].str.replace(' ', '')
        df[i] = df[i].str.lower()
    df = df[['title', 'year', 'budget', 'worldwide_gross']]
    return df

def prep_imdb(df):
    for i in ['title']:
        df[i] = df[i].str.translate(str.maketrans('', '', string.punctuation))
        df[i] = df[i].str.replace(' ', '')
        df[i] = df[i].str.lower()
    df['genres'] = df['genres'].map(lambda x: x.split(','), na_action='ignore')
    df = df.explode('genres')
    return df

def merge(df1,df2):
    df = pd.merge(df1,df2,how='inner',on=['title','year'])
    return df

def add_features(df):
    profit = df['worldwide_gross'] - df['budget']
    df['ROI'] = (profit/df['budget']) * 100
    
    producers = df.drop_duplicates(['movie_id','producer']) 
    prod_count = producers['producer'].value_counts()
    prod_filtered = prod_count[prod_count>6]
    prod_list = list(prod_filtered.index)
    producers = producers[producers['producer'].isin(prod_list)]
    prod_roi = producers.groupby('producer').median()['ROI'].sort_values(ascending=False)
    top_prod = list(prod_roi.head(5).index)
    bot_prod = list(prod_roi.tail(5).index)
    df.loc[df['producer'].isin(top_prod), 'producer_rank'] = 'High ROI Producers'
    df.loc[df['producer'].isin(bot_prod), 'producer_rank'] = 'Low ROI Producers'
    return df
    
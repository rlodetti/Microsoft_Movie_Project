#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def eda_viz(df):
    """
    This function takes the movies dataframe and creates a pairplot to look 
    for correlations between Production Budgets, Worldwide Gross, and ROI.
    """
    df_no_outliers = df[df['ROI'] < 6000]  # Excluding some outliers to make the graphs more readable.
    df_no_dupes = df_no_outliers.drop_duplicates('movie_id')
    df_clean = df_no_dupes[['budget', 'worldwide_gross', 'ROI']]
    sns.reset_defaults()
    sns.pairplot(data=df_clean)
    plt.show()

def roi_viz(df):
    """
    This function takes the movies dataframe and creates a countplot to show
    the distribution of the ROI of all movies in the dataset. 
    """
    df_no_dupes = df.drop_duplicates('movie_id')
    ROI = df_no_dupes['ROI']

    # Creating a new column to group and label ROI values
    df_no_dupes.loc[ROI < 0, 'ROI_rank'] = '< 0'
    df_no_dupes.loc[(ROI >= 0) & (ROI < 200), 'ROI_rank'] = '0 - 200'
    df_no_dupes.loc[(ROI >= 200) & (ROI < 400), 'ROI_rank'] = '200 - 400'
    df_no_dupes.loc[(ROI >= 400) & (ROI < 600), 'ROI_rank'] = '400 - 600'
    df_no_dupes.loc[(ROI >= 600) & (ROI < 800), 'ROI_rank'] = '600 - 800'
    df_no_dupes.loc[(ROI >= 800) & (ROI < 1000), 'ROI_rank'] = '800 - 1,000'
    df_no_dupes.loc[ROI >= 1000, 'ROI_rank'] = '> 1,000'

    sns.set_context('talk')
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(7,5))
    sns.countplot(data=df_no_dupes,
                  y='ROI_rank',
                  order=[
                      '< 0', '0 - 200', '200 - 400', '400 - 600', '600 - 800',
                      '800 - 1,000', '> 1,000'
                  ])
    ax.set(title='Distribution of ROI', xlabel='Number of Movies')
    ax.set_ylabel('ROI', rotation=0, labelpad=25)
    fig.tight_layout(pad=0.5)
    plt.show()
    

def producer_budget(df):
    """
    This function takes the movies dataframe and creates a box plot comparing
    movie budgets between high and low ROI producers.
    """
    # Filtering data for High and Low ROI producers, then removing any movie duplicates.
    df_clean = df.dropna(axis=0,
                         subset=['producer_rank']).drop_duplicates('movie_id')
    sns.set_context('talk')
    sns.set_style('whitegrid')
    colors = {'High ROI Producers': '#377eb8', 'Low ROI Producers': '#ff7f00'}
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.boxplot(data=df_clean,
                x='producer_rank',
                y='budget',
                showfliers=False,
                order=['High ROI Producers', 'Low ROI Producers'],
                width=0.4,
                palette=colors)
    ax.set(title='High ROI Producers Keep Budgets Low',
           ylabel='Budget (in millions)',
           xlabel=None,
           xticklabels=['High ROI\nMovies', 'Low ROI\nMovies'],
           position=[.19, 0.13, 0.75, 0.75])
    ax.yaxis.set_major_formatter(lambda x, pos: f'${int(x/1000000)}')
    plt.show()


def producer_runtime(df):
    """
    This function takes the movies dataframe and creates a box plot comparing
    movie lengths between high and low ROI producers.
    """
    # Filtering data for High and Low ROI producers, then removing any movie duplicates.
    df_clean = df.dropna(axis=0,
                         subset=['producer_rank']).drop_duplicates('movie_id')
    sns.set_context('talk')
    sns.set_style('whitegrid')
    colors = {'High ROI Producers': '#377eb8', 'Low ROI Producers': '#ff7f00'}
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.boxplot(data=df_clean,
                x='producer_rank',
                y='runtime',
                showfliers=False,
                order=['High ROI Producers', 'Low ROI Producers'],
                width=0.4,
                palette=colors)
    ax.set(title='High ROI Producers Keep Movies Short',
           ylabel='Movie Length (in minutes)',
           xlabel=None,
           xticklabels=['High ROI\nMovies', 'Low ROI\nMovies'],
           position=[.19, 0.13, 0.75, 0.75])
    plt.show()


def producer_genre(df):
    """
    This function takes the movies dataframe makes a barchart comparing the 
    frequency rate of each genre in movies from high ROI producers, 
    low ROI producers, and all of the movies in the dataset.
    """
    # Find the most common genres and rates in each group.
    high_df = df[df['producer_rank'] == 'High ROI Producers']
    high_unique_df = high_df.drop_duplicates(['movie_id', 'genres'])
    high_rates_df = high_unique_df['genres'].value_counts(
        normalize=True).reset_index().rename(columns={
            'index': 'genre',
            'genres': 'rate',
        })
    sns.set_context('talk')
    sns.set_style('whitegrid')
    colors = {'Horror': '#377eb8', 'Thriller': '#377eb8', 'Mystery': '#377eb8'}
    fig, ax = plt.subplots(figsize=(8, 4))
    g = sns.barplot(data=high_rates_df,
                    x='rate',
                    y='genre',
                    edgecolor='black',
                    palette=colors,
                    order=['Horror', 'Thriller', 'Mystery'])
    g.xaxis.set_major_formatter(lambda x, pos: "{:.0%}".format(x))
    g.set(title='Most Frequently Occuring Genres\nby High ROI Movies',
          ylabel=None,
          xlabel=None,
          position=[.19, 0.13, 0.75, 0.7])  
    plt.show()
    

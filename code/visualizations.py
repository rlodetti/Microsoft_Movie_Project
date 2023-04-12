#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    colors = {
        'High ROI Producers': '#377eb8',
        'Average': '#999999',
        'Low ROI Producers': '#ff7f00'
    }
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
           xticklabels=['High ROI\nProducers', 'Low ROI\nProducers'])
    ax.yaxis.set_major_formatter(lambda x, pos: f'${int(x/1000000)}')

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
    colors = {
        'High ROI Producers': '#377eb8',
        'Average': '#999999',
        'Low ROI Producers': '#ff7f00'
    }
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
           xticklabels=['High ROI\nProducers', 'Low ROI\nProducers'],
           position=[0.2,0.15,0.7,0.7])

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
        normalize=True).reset_index()

    low_df = df[df['producer_rank'] == 'Low ROI Producers']
    low_unique_df = low_df.drop_duplicates(['movie_id', 'genres'])
    low_rates_df = low_unique_df['genres'].value_counts(
        normalize=True).reset_index()

    # Merge data along genres.
    merged_rates_df = pd.merge(high_rates_df,
                               low_rates_df,
                               how='outer',
                               on='index').fillna(0)
    merged_named_df = merged_rates_df.rename(
        columns={
            'index': 'genre',
            'genres_x': 'High ROI Producers',
            'genres_y': 'Low ROI Producers'
        })

    # Finding the largest differnces between high and low producers.
    merged_named_df['abs_diff'] = abs(merged_named_df['High ROI Producers'] -
                                      merged_named_df['Low ROI Producers'])
    merged_sorted_df = merged_named_df.sort_values(
        'abs_diff', ascending=False).drop('abs_diff', axis=1)

    # Converting dataframe to long format, slicing to include relevant data for graphing.
    merged_long_df = merged_sorted_df.melt('genre')

    sns.set_context('talk')
    sns.set_style('whitegrid')
    colors = {'High ROI Producers': '#377eb8', 'Low ROI Producers': '#ff7f00'}
    fig, ax = plt.subplots(figsize=(8, 6))
    g = sns.barplot(
        data=merged_long_df,
        x='genre',
        y='value',
        hue='variable',
        edgecolor='black',
        palette=colors,
        order=['Horror', 'Thriller', 'Mystery', 'Drama', 'Comedy', 'Crime'])
    ax.tick_params(axis='y', labelright=True)
    plt.legend(bbox_to_anchor=(.75, -.1))
    g.yaxis.set_major_formatter(lambda x, pos: "{:.0%}".format(x))
    g.set(title='Largest Differences in Genre Frequency Rate',
          ylabel=None,
          xlabel=None,
          position=[0.1,0.23,0.8,0.7])    
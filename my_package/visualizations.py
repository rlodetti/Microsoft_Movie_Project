#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def producer_budget(df):
    prod_ranked = df.drop_duplicates(['movie_id', 'producer']).dropna(
        axis=0, subset=['producer_rank'])
    sns.set_context('talk')
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.boxplot(data=prod_ranked, x='producer_rank', y='budget', showfliers=False, order=[
                'High ROI Producers', 'Low ROI Producers'], width=0.4)
    ax.set_title('Distribution of Production Budgets\nby Producers')
    ax.set(ylabel='Budget (in millions of dollars)',
           xlabel=None)
    ax.yaxis.set_major_formatter(lambda x, pos: f'${int(x/1000000)}')
    ax.set_xticklabels(['High ROI\nProducers', 'Low ROI\nProducers'])

def producer_runtime(df):
    prod_ranked = df.drop_duplicates(['movie_id', 'producer']).dropna(
        axis=0, subset=['producer_rank'])
    sns.set_context('talk')
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.boxplot(data=prod_ranked, x='producer_rank', y='runtime', showfliers=False, order=[
                'High ROI Producers', 'Low ROI Producers'], width=0.4)
    ax.set_title('Distribution Movie Length\nby Producers')
    ax.set(ylabel='Movie Length (in minutes)',
           xlabel=None)
    #ax.yaxis.set_major_formatter(lambda x, pos: f'${int(x/1000000)}')
    ax.set_xticklabels(['High ROI\nProducers', 'Low ROI\nProducers'])

def producer_genre_old(df):
    genres = df.dropna(axis=0, subset=['producer_rank']).drop_duplicates(
        ['movie_id', 'genres'])
    top_gen = genres[genres['producer_rank'] == 'High ROI Producers']
    bot_gen = genres[genres['producer_rank'] == 'Low ROI Producers']
    df1 = top_gen['genres'].value_counts(normalize=True)[:5]
    df2 = bot_gen['genres'].value_counts(normalize=True)[:5]
    hlabels = list(df1.map(lambda x: "{:.0%}".format(x)))
    llabels = list(df2.map(lambda x: "{:.0%}".format(x)))

    colors = {'Horror': '#377eb8', 'Thriller': '#377eb8', 'Mystery': '#377eb8', 'Drama': '#999999',
              'Sci-Fi': '#377eb8', 'Action': '#ff7f00', 'Comedy': '#ff7f00', 'Crime': '#ff7f00', 'Adventure': '#ff7f00'}

    fig, ax = plt.subplots(1, 2, figsize=(20, 4), sharex=True)
    high = sns.barplot(y=df1.index, x=df1.values,
                       ax=ax[0], edgecolor='black', palette=colors)
    low = sns.barplot(y=df2.index, x=df2.values,
                      ax=ax[1], edgecolor='black', palette=colors)
    high.set_title('High ROI Producers')
    low.set_title('Low ROI Producers')
    fig.suptitle('Most Common Genres\nby Producer Type', y=1.1)
    patches = high.patches
    for i in range(len(patches)):
        x = patches[i].get_x()+patches[i].get_width()-.002
        y = patches[i].get_y()+0.55
        high.text(x, y, hlabels[i], c='white', weight='bold', ha='right')

    patches1 = low.patches
    for i in range(len(patches1)):
        x = patches1[i].get_x()+patches1[i].get_width()-0.002
        y = patches1[i].get_y()+0.55
        low.text(x, y, llabels[i], c='white', weight='bold', ha='right')

    high.xaxis.set_major_formatter(lambda x, pos: "{:.0%}".format(x))
    
    
    
    
    
    
    
    
def producer_genre(df):
    genres = df.dropna(axis=0, subset=['producer_rank']).drop_duplicates(
        ['movie_id', 'genres'])
    top_gen = genres[genres['producer_rank'] == 'High ROI Producers']
    bot_gen = genres[genres['producer_rank'] == 'Low ROI Producers']
    s1 = top_gen['genres'].value_counts(normalize=True)[:5]
    s2 = bot_gen['genres'].value_counts(normalize=True)[:5]
    s3 = genres['genres'].value_counts(normalize=True)
    s4 = pd.Series([s3[i] for i in list(s1.index)],index=list(s1.index))
    s5 = pd.Series([s3[i] for i in list(s2.index)],index=list(s2.index))
    df1 = pd.concat([s1,s4],axis=1).reset_index().rename(columns={'index':'genre','genres':'High ROI Producers',0:'Average'}).melt('genre')
    df2 = pd.concat([s2,s5],axis=1).reset_index().rename(columns={'index':'genre','genres':'Low ROI Producers',0:'Average'}).melt('genre')

    s1_list = list(s1.map(lambda x: "{:.0%}".format(x)))
    s2_list = list(s2.map(lambda x: "{:.0%}".format(x)))
    colors = {'High ROI Producers': '#377eb8', 'Average': '#999999', 'Low ROI Producers': '#ff7f00'}
    sns.set_context('talk')
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(1, 2, figsize=(19, 6), sharex=True)

    high = sns.barplot(data = df1, y='genre', x='value', hue='variable',ax=ax[0], edgecolor='black', palette=colors)
    low = sns.barplot(data = df2, y='genre', x='value', hue='variable',ax=ax[1], edgecolor='black', palette=colors)

    patches = high.patches
    for i in range(5):
        x = patches[i].get_x()+patches[i].get_width()-.002
        y = patches[i].get_y()+(patches[i].get_height()/1.35)
        high.text(x, y, s1_list[i], c='white', weight='bold', ha='right')

    patches1 = low.patches
    for i in range(5):
        x = patches1[i].get_x()+patches1[i].get_width()-0.002
        y = patches1[i].get_y()+(patches[i].get_height()/1.35)
        low.text(x, y, s2_list[i], c='white', weight='bold', ha='right')

    fig.suptitle('Most Common Genres by Producer Type')
    high.xaxis.set_major_formatter(lambda x, pos: "{:.0%}".format(x))
    high.set(ylabel=None,xlabel=None)
    low.set(ylabel=None,xlabel=None)

    ax[0].legend([],[], frameon=False)
    ax[1].legend([],[], frameon=False)
    handles, labels = ax[0].get_legend_handles_labels()
    handles.append(ax[1].get_legend_handles_labels()[0][0])
    labels.append(ax[1].get_legend_handles_labels()[1][0])
    fig.legend(handles, labels,loc=(0.78,0.1))


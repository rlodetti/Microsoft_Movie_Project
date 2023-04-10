#!/usr/bin/env python
# coding: utf-8

# In[7]:


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

def producer_genre(df):
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


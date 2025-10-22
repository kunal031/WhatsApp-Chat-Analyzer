from numpy.fft import helper
from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
import re
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns


def fetch_stats(selected_user,df):
# Restructured Code
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())


    num_media_messages = df[df['message'] == '<image omitted>\n'].shape[0]

    # fetch number of linked shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)
# this is old code and replaced by codes above this named "Restructured Code"
    #
    # # noinspection PyUnresolvedReferences
    # if selected_user == 'Overall':
    #     # 1. fetch number of messages
    #     num_messages = df.shape[0]
    #
    #     # 2. no. of words
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())
    #
    #     return num_messages,len(words)
    # else:
    #     new_df = df[df['user'] == selected_user]
    #     num_messages = new_df.shape[0]
    #     words = []
    #     for message in new_df['message']:
    #         words.extend(message.split())
    #
    #     return num_messages,len(words)

    # fetch number of media messages

def most_busy_users(df):
    x = df['user'].value_counts()
    df = round(df['user'].value_counts() / df.shape[0] * 100).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})
    return x,df

def create_word_cloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df["user"] == selected_user]


    temp = df[df['user'] != 'group_notificaton']
    temp = temp[temp['message'] != '‎image omitted\n‎']

    pattern1 = r'IMG_\d{4}\.HEIC ‎document omitted\n‎'
    temp = temp[~temp['message'].astype(str).str.contains(pattern1, regex=True, na=False)]

    pattern2 = r'IMG_\d{4}\.MOV ‎document omitted\n‎'
    temp = temp[~temp['message'].astype(str).str.contains(pattern2, regex=True, na=False)]

    wc = WordCloud(width=500, height=500, background_color='white',min_font_size=10)
    text = temp['message'].str.cat(sep=' ')
    df_wc = wc.generate(text)
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notificaton']
    temp = temp[temp['message'] != '‎image omitted\n‎']

    pattern1 = r'IMG_\d{4}\.HEIC ‎document omitted\n‎'
    temp = temp[~temp['message'].astype(str).str.contains(pattern1, regex=True, na=False)]

    pattern2 = r'IMG_\d{4}\.MOV ‎document omitted\n‎'
    temp = temp[~temp['message'].astype(str).str.contains(pattern2, regex=True, na=False)]

    words = []

    for message in temp['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap

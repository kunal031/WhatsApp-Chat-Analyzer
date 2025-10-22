import re
import pandas as pd
def preprocessor(data):
    pattern = r'\[\d{2}/\d{2}/\d{2},\s*\d{1,2}:\d{2}:\d{2}\s*(?:AM|PM)?\]\s*'
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)
    messages.pop()
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df.drop(columns=['user_message'], inplace=True)

    df['user'] = users
    df['message'] = messages

    df['message_date'] = pd.to_datetime(df['message_date'], format='[%d/%m/%y, %H:%M:%S] ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []

    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

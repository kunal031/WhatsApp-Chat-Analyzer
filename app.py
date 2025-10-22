import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocessor(data)

    st.dataframe(df)


    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt ",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,words,media_shared, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(media_shared)
        with col4:
            st.header("Link Shared")
            st.title(num_links)

        # Monthly TimeLine
        st.title('Monthly TimeLine')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots(figsize=(3,2))
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Daily TimeLine
        st.title('Daily TimeLine')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig,ax = plt.subplots(figsize=(3,2))
            ax.bar(busy_day.index, busy_day.values, color='blue')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2 :
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig,ax = plt.subplots(figsize=(3,2))
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



        # finding the busiest user in the group
        if selected_user == "Overall":
            st.title("Most Busy User")
            x, new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color="green")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

    # WordCloud
    st.title("Word Cloud")
    df_wc = helper.create_word_cloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # most common words
    most_common_df = helper.most_common_words(selected_user,df)

    fig,ax = plt.subplots()

    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title("Most Common Words")
    st.pyplot(fig)
    # st.dataframe(most_common_df)


    # Emoji Analysis
    emoji_df = helper.emoji_helper(selected_user,df)
    st.dataframe(emoji_df)


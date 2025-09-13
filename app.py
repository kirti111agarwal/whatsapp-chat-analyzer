import streamlit as st 
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)


    user_list=df['user'].unique().tolist()
    if('group_notification' in user_list):
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4=st.columns(4)
        with col1:
            st.header("Total Msg")
            st.title(num_messages) 
        with col2:
            st.header("Total Words")
            st.title(words) 
        with col3  :
            st.header("Media Shared")
            st.title(num_media_messages) 
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #timeline of msgs sent monthly 
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        #timeline of msgs sent dialy 
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline_func(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #activity map (weekly)
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header('Most busy days of the Week')
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most busy days of the month")
            busy_week=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_week.index,busy_week.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        #finding which is the time in 24hr where users are more active according to days of the week
        st.title("Weekly Activity Time (24 hour) Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
        
        #finding the busiest user in the group 
        if selected_user=="Overall":
            st.title("Most busy users")
            x,new_df=helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        st.title('WordCloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        #emoji_analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.dataframe(emoji_df)







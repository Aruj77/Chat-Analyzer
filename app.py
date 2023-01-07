import matplotlib.pyplot as plt
import streamlit as st
import preprocessor,helper
import seaborn as sns


st.sidebar.title('WABRA')
st.sidebar.header('Chat Analyzer')
uploaded_file=st.sidebar.file_uploader('Choose a File')
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)
    
    #fetching unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox('Show Analysis of:', user_list)
    if st.sidebar.button('Show Analysis'):
        
        num_messages,words,num_media,links=helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media)
        with col4:
            st.header('Links Shared')
            st.title(links)
            
        #finding the most active users in the group (only for group)
        if selected_user=='Overall':
            st.title('Most Busy Users')
            x,df_per=helper.most_busy_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(df_per)
        
        #WorldCloud
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        #Most Common Words
        st.title('Most Common Words')
        col1,col2=st.columns(2)
        most_common_df=helper.most_common_words(selected_user,df)
        with col1 :
            fig,ax=plt.subplots()
            plt.xticks(rotation='vertical')
            ax.barh(most_common_df[0],most_common_df[1])
            st.pyplot(fig)
            
            # sns.barplot(most_common_df[0],most_common_df[1])
            
        with col2:        
            st.dataframe(most_common_df)
            
        #Emoji Analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
        
        #Timeline Analysis (monthly)
        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #Timeline Analysis (daily)
        st.title('Daily Timeline')
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        
        
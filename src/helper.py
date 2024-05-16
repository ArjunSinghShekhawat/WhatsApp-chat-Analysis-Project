from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import emoji
from src.logger import logging
from src.exception import CustomException
import sys,os

extractor = URLExtract()

#-----------------------------------------------Fetch Stats---------------------------------------------------------

def fetch_stats(selected_user,df):
   
   """This function is used to fetch all stats from the dataframe"""

   logging.info("I am inside fetch stats method :")

   try:

    if selected_user !="Overall":
        df  =df[df['Users']==selected_user]
    
    total_message = df.shape[0]
    total_words = []

    for message in df['Messages']:
        total_words.extend(message.split(' '))
    
    total_media_messages = df[df['Messages']=='<Media omitted>'].shape[0]

    links = []

    for message in df['Messages']:
        links.extend(extractor.find_urls(message))
    
    logging.info("Successfully Find All Stats total_messages {} total_words {} total_media_messages {} links {} ".format(total_message,len(total_words),total_media_messages,len(links)))
    
    return total_message,len(total_words),total_media_messages,len(links)
   
   except Exception as e:
       raise CustomException(e,sys)
   

#-----------------------------------------------Most Busy Person---------------------------------------------------------

def most_busy_person(df):

    """This function is used to fetch the all most busy users on whatsapp char"""

    logging.info("I am inside most busy person method :")

    try:
        data = df['Users'].value_counts().head()

    except Exception as e:
        raise CustomException(e,sys)

    logging.info("Successfully fetch the all busy person on whatsapp chat {}".format(data))

    return data


#-----------------------------------------------Create Word Cloud---------------------------------------------------------

    
def create_word_cloud(selected_user,df):

    """This function is used to find word cloud """

    logging.info("I im inside Create Word Cloud Method :")
    try:
        if selected_user !="Overall":
            df  =df[df['Users']==selected_user]
    
        # Read stop words into a set
        with open(r"E:\Chat Analysis Project\notebooks\stop_hinglish.txt", 'r') as f:
            stop_words = set(f.read().split())
    
        # Filter out group notifications and media omitted messages
        temp = df[(df['Users'] != 'group notification') & (df['Messages'] != '<Media omitted>')]

        def remove_stopwords(message):
            words = []

            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)
            return " ".join(words)
    
        temp['Messages'] = temp['Messages'].apply(remove_stopwords)

        wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
        df_wc = wc.generate(temp['Messages'].str.cat(sep=" "))

        logging.info("Successfully find the word cloud :")

        return df_wc
    
    except Exception as e:
        raise CustomException(e,sys)


#-----------------------------------------------Most Common Word---------------------------------------------------------

def most_common_word(selected_user,df):

    """This function is used to find the most common words"""

    logging.info("I im inside most common word Method :")

    try:
        if selected_user !="Overall":
            df  =df[df['Users']==selected_user]

        # Read stop words into a set
        with open(r"E:\Chat Analysis Project\notebooks\stop_hinglish.txt", 'r') as f:
            stop_words = set(f.read().split())
        
        # Filter out group notifications and media omitted messages
        temp = df[(df['Users'] != 'group notification') & (df['Messages'] != '<Media omitted>')]

        # Create a translation table to remove punctuation
        translator = str.maketrans('', '', string.punctuation)

        
        words = []

        
        for message in temp['Messages']:
            message = emoji.replace_emoji(message)
            
            # Remove punctuation and split into words
            for word in message.translate(translator).lower().split():

                # Append non-stop words to the list
                if word not in stop_words:
                    words.append(word)

        # Use Counter to get the most common words
        word_counts = Counter(words).most_common(20)

        # Create a DataFrame from the word counts
        return_df = pd.DataFrame(word_counts, columns=['Word', 'Count'])

        logging.info("Successfully find most common words used in whatsapp chat")

        return return_df
    
    except Exception as e:
        raise CustomException(e,sys)


#-----------------------------------------------Most Common Emoji---------------------------------------------------------


def most_common_emoji(selected_user,df):

    """This function is used to find the most common emoji """

    logging.info("I im inside most common emoji Method :")

    try:
        if selected_user !="Overall":
            df  =df[df['Users']==selected_user]
            
        # List to store emojis
        emojis = []

        # Check the version of the emoji library to use the correct attribute
        if hasattr(emoji, 'EMOJI_DATA'):
            emoji_dict = emoji.EMOJI_DATA

        elif hasattr(emoji, 'UNICODE_EMOJI'):
            emoji_dict = emoji.UNICODE_EMOJI

        else:
            raise AttributeError("The emoji library doesn't have the expected attributes")

        # Extract emojis from each message
        for message in df['Messages']:
            emojis.extend([c for c in message if c in emoji_dict])

        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['Emoji','Count'])

        logging.info("Successfully find all most common emoji used in whatsapp chat")

        return emoji_df
    
    except Exception as e:
        raise CustomException(e,sys)


#-----------------------------------------------Monthly Timeline---------------------------------------------------------

def monthly_timeline(selected_user,df):

    """This function is used to find monthly timeline in whatsapp chat """

    logging.info("I im inside monthly timeline Method :")

    try:
        if selected_user !="Overall":
            df  =df[df['Users']==selected_user]
    
        timeline = df.groupby(['Year','Month_Number','Month']).count()['Messages'].reset_index()

        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['Month'][i]+ " - " +str(timeline['Year'][i]))
    
        timeline['time'] = time

        logging.info("Successfully find monthly timeline on whatsapp chat")

        return timeline
    
    except Exception as e:
        raise CustomException(e,sys)

#-----------------------------------------------Daily Timeline---------------------------------------------------------

def daily_timeline(selected_user,df):

    """This function is used to find the daily timeline on whatsapp chat """

    logging.info("I im inside daily timeline  Method :")

    try:
        if selected_user !="Overall":
            df  =df[df['Users']==selected_user]
    
        timeline = df.groupby(['Date']).count()['Messages'].reset_index()

        logging.info("Successfully find daily timeline on whatsapp chat")

        return timeline
    
    except Exception as e:
        raise CustomException(e,sys)


#-----------------------------------------------weekly activity map---------------------------------------------------------

def week_activity_map(selected_user,df):

    """This function is used to find the weekly activity on whatsapp chat """

    logging.info("I im inside weekly activity map Method :")

    try:
        if selected_user !="Overall":
            df  =df[df['Users']==selected_user]

        logging.info("Successfully find weekly activity on whatsapp chat")
    
        return df['Day_Name'].value_counts()

    except Exception as e:
        raise CustomException(e,sys)

#-----------------------------------------------month activity map---------------------------------------------------------
def month_activity_map(selected_user,df):

    """This function is used to find the monthly activity on whatsapp chat """

    logging.info("I im inside monthly activity map Method :")

    try:
        if selected_user !="Overall":
            df  =df[df['Users']==selected_user]
        
        logging.info("Successfully find monthly activity on whatsapp chat")
    
        return df['Month'].value_counts()
    
    except Exception as e:
        raise CustomException(e,sys)
    

#-----------------------------------------------activity heatmap---------------------------------------------------------
def activity_heatmap(selected_user,df):

    """This function is used to find the  activity heatmap on whatsapp chat """

    logging.info("I im inside  activity heatmap Method :")

    try:
        if selected_user != 'Overall':
            df = df[df['Users'] == selected_user]

        user_heatmap = df.pivot_table(index='Day_Name', columns='Period', values='Messages', aggfunc='count').fillna(0)

        logging.info("Successfully find  activity heatmap on whatsapp chat")

        return user_heatmap
    
    except Exception as e:
        raise CustomException(e,sys)

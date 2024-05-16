import re
import pandas as pd
from src.exception import CustomException
from src.logger import logging
import sys,os

def preprocessor(data):
    """This function is used to preprocess the dataset and clean all data"""

    logging.info("I am inside preprocessor method")

    try:
        pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s"

        messages = re.split(pattern,data)
        dates = re.findall(pattern,data)

        df = pd.DataFrame({"Message":messages[1:],"Dates":dates})

        df['Dates'] = df['Dates'].apply(lambda x:x.replace("AM",""))
        df['Dates'] = df['Dates'].apply(lambda x:x.replace("PM",""))
        df['Dates'] = df['Dates'].apply(lambda x:x.replace("\u202f",""))
        df['Dates'] = pd.to_datetime(df['Dates'],format=('%m/%d/%y, %H:%M - '))

        df['Year'] = df['Dates'].dt.year
        df['Month'] = df['Dates'].dt.month_name()
        df['Day'] = df['Dates'].dt.day
        df['Hour'] = df['Dates'].dt.hour
        df['Minute'] = df['Dates'].dt.minute
        df["Month_Number"] = df['Dates'].dt.month
        df['Date'] = df['Dates'].dt.date
        df['Day_Name'] = df['Dates'].dt.day_name()

        users = []
        _messages = []

        for message in df['Message']:
            entry = re.split('([\w\W]+?):\s',message)
        
            if entry[1:]:
                users.append(entry[1])
                _messages.append(entry[2])
            else:
                users.append("group notification")
                _messages.append(entry[0])
    
        df['Users'] = users
        df['Messages'] = _messages

        df.drop("Message",axis=1,inplace=True)
    

        df['Messages'] = df['Messages'].apply(lambda x:x.replace("\n",""))

        period = []
        for hour in df[['Day_Name', 'Hour']]['Hour']:
            if hour == 23:
                period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
                period.append(str('00') + "-" + str(hour + 1))
            else:
                period.append(str(hour) + "-" + str(hour + 1))

        df['Period'] = period

        return df
    
    except Exception as e:
        raise CustomException(e,sys)


import streamlit as st
import src.preprocessor.preprocessor as preprocessor,src.helper as helper
import seaborn as sns
import matplotlib.pyplot as plt



main_style = """
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f6;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1200px;
            margin: auto;
            padding: 20px;
        }
        .sidebar {
            background-color: #2c3e50;
            color: #fff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .content {
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
        }
        .title {
            color: #2980b9;
            margin-top: 0;
            margin-bottom: 20px;
        }
    </style>
"""

# Inject CSS
st.markdown(main_style, unsafe_allow_html=True)


# Display the header using st.markdown
st.markdown("<h1 class='title'>WhatsApp Chat Analyzer</h1>", unsafe_allow_html=True)


uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt'])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocessor(data)


    User_list = df['Users'].unique().tolist()
    User_list.remove('group notification')
    User_list.sort()
    User_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("All Users In this chat",User_list)

    # Define CSS styles
    main_style = """
    <style>
        .row {
            display: flex;
            flex-wrap: wrap;
            margin: 0 -10px;
        }
        .column {
            flex: 25%;
            padding: 0 10px;
        }
        .stat-box {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .stat-box h2 {
            color: #2980b9;
            margin-top: 0;
            margin-bottom: 10px;
        }
        .stat-box p {
            font-size: 24px;
            color: black;
            margin: 0;
            font-size: 24px;
            font-weight: bold;
            font-family: 'Segoe UI Emoji', sans-serif; /* Specify the desired font family */
}
    </style>
    """

# Inject CSS
    st.markdown(main_style, unsafe_allow_html=True)


    if st.sidebar.button("Show Analysis"):
        st.markdown("<h1 class='title'>Top Statistics</h1>", unsafe_allow_html=True)
        
        # Fetch Stats
        total_messages, total_words, total_media_messages, total_links = helper.fetch_stats(selected_user, df)
        
       

        # Display Stats in a 4-column layout
        st.markdown("""
          <div class="row">
            <div class="column">
                <div class="stat-box">
                    <h2>Total Messages</h2>
                    <p>{}</p>
                </div>
            </div>
            <div class="column">
                <div class="stat-box">
                    <h2>Total Words</h2>
                    <p>{}</p>
                </div>
            </div>
            <div class="column">
                <div class="stat-box">
                    <h2>Media Shared</h2>
                    <p>{}</p>
                </div>
            </div>
            <div class="column">
                <div class="stat-box">
                    <h2>Links</h2>
                    <p>{}</p>
                </div>
            </div>
        </div>
    """.format(total_messages, total_words, total_media_messages, total_links), unsafe_allow_html=True)
        
        

        
        #Monthly Timeline
        st.markdown("<h2 class='title'>Monthly Timeline</h2>", unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        timeline = helper.monthly_timeline(selected_user,df)


        with col1:
            fig,ax = plt.subplots()
            ax.plot(timeline['time'],timeline['Messages'],color='red')
            ax.set_xticklabels(timeline['time'], rotation='vertical')
            st.pyplot(fig)

        with col2:
            fig,ax = plt.subplots()
            ax.bar(timeline['time'],timeline['Messages'],color='orange')
            ax.set_xticklabels(timeline['time'], rotation='vertical')
            st.pyplot(fig)
        
        #daily Timeline
        st.markdown("<h2 class='title'>Daily Timeline</h2>", unsafe_allow_html=True)
        
        col1,col2 = st.columns(2)
        timeline = helper.daily_timeline(selected_user,df)


        with col1:
            fig,ax = plt.subplots()
            ax.plot(timeline['Date'],timeline['Messages'],color='green')
            ax.set_xticklabels(timeline['Date'], rotation='vertical')
            st.pyplot(fig)

        with col2:
            fig,ax = plt.subplots()
            ax.bar(timeline['Date'],timeline['Messages'],color='purple')
            ax.set_xticklabels(timeline['Date'], rotation='vertical')
            st.pyplot(fig)

        #Weekly Activated
        busy_day = helper.week_activity_map(selected_user,df)
        st.markdown("<h2 class='title'>Activity Map</h2>", unsafe_allow_html=True)

        col1,col2 = st.columns(2)

        with col1:
            fig,ax = plt.subplots()
            st.markdown("<h3 class='title'>Most Busy Day</h3>", unsafe_allow_html=True)
            ax.bar(busy_day.index,busy_day.values,color='skyblue')
            ax.set_xticklabels(busy_day.index, rotation='45')
            st.pyplot(fig)

        with col2:
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            st.markdown("<h3 class='title'>Most Busy Month</h3>", unsafe_allow_html=True)
            ax.bar(busy_month.index,busy_month.values,color="green")
            ax.set_xticklabels(busy_month.index, rotation='45')
            st.pyplot(fig)

        #Find out the busy person in whatsapp
        if selected_user == 'Overall':
            st.markdown("<h2 class='title'>Most Busy Users In Whatsapp Chat</h2>", unsafe_allow_html=True)
            data_ = helper.most_busy_person(df)

    
            figsize = (12, 8)

            fig1, ax1 = plt.subplots(figsize=figsize)
            fig2, ax2 = plt.subplots(figsize=figsize)
    
            col1, col2 = st.columns(2)

            with col1:
                ax1.bar(data_.index, data_.values,color='pink')
                ax1.set_xticklabels(data_.index, rotation='vertical')
                st.pyplot(fig1)
            
            with col2:
                ax2.pie(data_.values, labels=data_.index, autopct="%1.1f%%", shadow=True)
                st.pyplot(fig2)
        
        st.markdown("<h2 class='title'>Word Cloud</h2>", unsafe_allow_html=True)
        df_wc = helper.create_word_cloud(selected_user,df)

        fig,ax = plt.subplots()
        ax.imshow(df_wc)

        st.pyplot(fig)

        ##Most Common Words
        most_common_df = helper.most_common_word(selected_user,df)
        fig,ax = plt.subplots()
        
        st.markdown("<h2 class='title'>Most Common Words</h2>", unsafe_allow_html=True)

        ax.bar(most_common_df['Word'],most_common_df['Count'],color="#9999FF")

        ax.set_xticklabels(most_common_df['Word'], rotation='vertical')
        st.pyplot(fig)

        #Most Used Emoji 
        emoji_df = helper.most_common_emoji(selected_user,df)

        st.markdown("<h2 class='title'>Emoji Analysis</h2>", unsafe_allow_html=True)

        fig, ax = plt.subplots()

        # Define a color map
        cmap = plt.get_cmap('viridis')

        # Normalize count values to range [0, 1] for colormap
        normalize = plt.Normalize(vmin=0, vmax=max(emoji_df['Count']))
        colors = [cmap(normalize(value)) for value in emoji_df['Count']]

        # Plot the bar chart with dynamically assigned colors
        bars = ax.bar(range(len(emoji_df)), emoji_df['Count'], color=colors)


        # Annotate the bars with emojis
        for i, (label, count) in enumerate(zip(emoji_df['Emoji'], emoji_df['Count'])):
            ax.text(i, count + 0.5, label, ha='center', fontname='Segoe UI Emoji', fontsize=14, color='black')

        # Hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        st.pyplot(fig)
    
        st.markdown("<h2 class='title'>Weekly Activity Map</h2>", unsafe_allow_html=True)
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



                
            






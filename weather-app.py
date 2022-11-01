import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
plt.style.use('seaborn')

st.snow()
st.image(Image.open('title.jpg'))
st.title('Overview of precipitation in Australia and its influencing factors')

df = pd.read_csv('weatherAUS.csv')
# see if there are null data
df.isnull().sum()

#delete null infomation
df.dropna(inplace=True)

# process the data
def delete_outlier(dfs, i):
    zscore = i + '_z'
    dfs.zscore = (dfs[i] - dfs[i].mean())/dfs[i].std() 
    dfs = dfs[(dfs.zscore > -3) & (dfs.zscore < 3)]
    return(dfs)

numerical_features = []
for col in df.columns:
    if df[col].dtype != "object":
        numerical_features.append(col)
for i in numerical_features:
    delete_outlier(df, i)

# random sample 5000 rows
df = df.sample(50000, ignore_index=True)  

st.markdown('### See average rainfall of each city in Australia less than the value')

rainfall_filter = st.slider('Average rainfall', 0.00000, 6.00000, 2.00001)
df_rain = df[df.AverageRainfall <= rainfall_filter]
st.map(df_rain)

# add two column to datetime format
df['Date'] = pd.to_datetime(df["Date"])
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month

# Overview of Precipitation in Australia
# rainfall in each year, month

df_year = df[['year', 'Rainfall','RainToday']].sort_values(by='year',ignore_index=True)
df_month = df[['month', 'Rainfall','RainToday']].sort_values(by='month',ignore_index=True)

st.markdown('### Overview of Precipitation in Australia')
fig, ax = plt.subplots(1,2,figsize = (10,5))
df_year.groupby('year').mean()['Rainfall'].plot(ax=ax[0])
df_month.groupby('month').mean()['Rainfall'].plot.bar(ax=ax[1]) 
ax[0].set_xlabel('rainfall for different years')
ax[1].set_xlabel('rainfall for different months')
st.pyplot(fig)

# create a input form
form = st.sidebar.form("country_form")
country_filter = form.text_input('Enter the city where you want to search for precipitation information (enter ALL to reset)', 'ALL')
form.form_submit_button("Apply")
df_info = df[['Location','Rainfall', 'RainToday','RainTomorrow']]
if country_filter!='ALL' :
    df_info = df_info[df_info.Location == country_filter]
    df = df[df.Location == country_filter]
st.sidebar.dataframe(df_info, 500, 200)

# The factors that affect the precipitation in Australia

st.markdown("### Select an option to see how this factor relates to whether rain will fall tomorrow in the city you enter")

if st.button('Show conclusion'):
    txt = st.text_area('','There are high chance to rain tomorrow when:  \n• It rained today \n• The presure is low\n• The humidity is high \n• Wind speed is high\n• Max temp and min temp are close to each other')

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    ['min and max Temp', 'Evaporation', 'Sunshine','WindSpeed','Pressure','Cloud', 'Humidity', 'Wind Direction']
)

with tab1:
    st.header('Min and Max Temp in '+country_filter)
    st.image(Image.open('tab1-tem.jpg'))
    st.write('###### The minimum and the maximum temperature in degrees celsius')
    st.write('As can be seen from the two boxplots, if it rains tomorrow, the highest temperature will mostly concentrate in the range of 17 degrees Celsius to 27 degrees Celsius, and the lowest temperature will concentrate in the range of 9 degrees Celsius to 20 degrees Celsius. \nThe scatter plot shows that the probability of rain tomorrow is higher when the temperature difference between the highest temperature and the lowest temperature is smaller.')


    fig, ax = plt.subplots(1, 2, figsize=(15,5))
    df[df.RainTomorrow=='Yes'].MaxTemp.plot.box(ax=ax[0])
    ax[0].set_xlabel('Rain Tomorrow')
    ax[0].set_ylabel('Temperature') 
    df[df.RainTomorrow=='Yes'].MinTemp.plot.box(ax=ax[1])
    ax[1].set_xlabel('Rain Tomorrow')
    st.pyplot(fig)

    fig1, ax = plt.subplots()
    ax.scatter(df[df.RainTomorrow=='Yes']['MinTemp'],df[df.RainTomorrow=='Yes']['MaxTemp'],c='olivedrab',label='Tomorrow Rain = Yes') 
    ax.scatter(df[df.RainTomorrow=='No']['MinTemp'],df[df.RainTomorrow=='No']['MaxTemp'],c='dodgerblue',alpha=0.3,label='Tomorrow Rain = No') 
    fig1.set_figheight(6)
    fig1.set_figwidth(10)
    plt.legend()
    st.pyplot(fig1)

with tab2:
    st.header('Evaporation in '+country_filter)
    st.image(Image.open('tab3-Evaporation.jpg'))
    st.write('###### The so-called Class A pan evaporation (mm) in the 24 hours to 9am')
    st.write('Boxplot shows that if it rains tomorrow, evaporation will be less than 10mm today. \n· But it is worth noting that even though we have removed the outliers from the data, the rest of the data are still quite different. ')

    fig, ax = plt.subplots()
    df[df.RainTomorrow=='Yes'].Evaporation.plot.box(ax=ax)
    ax.set_xlabel('Rain Tomorrow')
    ax.set_ylabel('Today\'s Evaporation')
    st.pyplot(fig)

with tab3:
    st.header('Sunshine in '+country_filter)
    st.image(Image.open('tab4-sunshine.jpg'))
    st.write('###### The number of hours of bright sunshine in the day.')
    st.write('The boxplot shows that if it rains tomorrow, the sunshine will be within 1h-7h today.')

    fig, ax = plt.subplots()
    df[df.RainTomorrow=='Yes'].Sunshine.plot.box(ax=ax)
    ax.set_xlabel('Rain Tomorrow')
    ax.set_ylabel('Today\'s Sunshine') 
    st.pyplot(fig)

with tab4:
    st.header('WindSpeed in '+country_filter)
    st.image(Image.open('tab5-wind.jpg'))
    st.write('###### The speed (km/h) of the strongest wind gust in the 24 hours to midnight')
    st.write('Boxplots show that if it rains tomorrow, the maximum wind speed today will be within 35km/h-55km/h.')

    fig, ax = plt.subplots()
    df[df.RainTomorrow=='Yes'].WindGustSpeed.plot.box(ax=ax)
    ax.set_xlabel('Rain Tomorrow')
    ax.set_ylabel('Today\'s WindGustSpeed')  
    st.pyplot(fig)

with tab5:
    st.header('Pressure in '+country_filter)
    st.image(Image.open('tab6-pressure.jpg'))
    st.write('###### Atmospheric pressure (hpa) reduced to mean sea level at 9am and 3pm')
    st.write('Comparing the pressure value of the next day rain and without rain, we can conclude that \nif the pressure value is low today, there is a higher probability of rain tomorrow.')

    fig, ax = plt.subplots(2, 2, figsize=(45,25))
    df[df.RainTomorrow=='Yes'].Pressure9am.plot.box(ax=ax[0, 0])
    ax[0, 0].set_ylabel('Rain Tomorrow')
    df[df.RainTomorrow=='Yes'].Pressure3pm.plot.box(ax=ax[0,1])
    df[df.RainTomorrow=='No'].Pressure9am.plot.box(ax=ax[1, 0])
    ax[1, 0].set_ylabel('Not Rain Tomorrow')
    df[df.RainTomorrow=='No'].Pressure3pm.plot.box(ax=ax[1, 1])
    st.pyplot(fig)

    fig1, ax = plt.subplots()
    ax.scatter(df[df.RainTomorrow=='Yes']['Pressure9am'],df[df.RainTomorrow=='Yes']['Pressure3pm'],c='plum',alpha=1,label='Tomorrow Rain = Yes') 
    ax.scatter(df[df.RainTomorrow=='No']['Pressure9am'],df[df.RainTomorrow=='No']['Pressure3pm'],c='slategrey',alpha=1,label='Tomorrow Rain = No') 
    fig1.set_figheight(6)
    fig1.set_figwidth(10)
    plt.legend()
    st.pyplot(fig1)

with tab6:
    st.header('Cloud in '+country_filter)
    st.image(Image.open('tab7-cloud.jpg'))
    st.write('###### Fraction of sky obscured by cloud at 9am and 3pm. This is measured in "oktas", which are a unit of eigths.')
    st.write('The box plot shows the amount of cloud cover today if it rains the next day.\n->By comparison, we can conclude that cloud cover has no significant effect on whether it will rain tomorrow ')

    fig, ax = plt.subplots(2, 2)
    df[df.RainTomorrow=='Yes'].Cloud9am.plot.box(ax=ax[0, 0])
    ax[0, 0].set_ylabel('Rain Tomorrow')
    df[df.RainTomorrow=='Yes'].Cloud3pm.plot.box(ax=ax[0, 1])
    df[df.RainTomorrow=='No'].Cloud9am.plot.box(ax=ax[1, 0])
    ax[0, 0].set_ylabel('Not Rain Tomorrow')
    df[df.RainTomorrow=='No'].Cloud3pm.plot.box(ax=ax[1, 1])
    st.pyplot(fig)

with tab7:
    st.header('Humdity in '+country_filter)
    st.image(Image.open('tab8-humdity.jpg'))
    st.write('###### Humidity (percent) at 9am and 3pm')
    st.write('By comparing the boxplot of not rain tomorrow and the boxplot of rain tomorrow, it can be concluded that if it rains tomorrow, the humidity will be higher today. ')

    fig, ax = plt.subplots(2, 2)
    df[df.RainTomorrow=='Yes'].Humidity9am.plot.box(ax=ax[0, 0])
    ax[0, 0].set_ylabel('Rain Tomorrow')
    df[df.RainTomorrow=='Yes'].Humidity3pm.plot.box(ax=ax[0, 1])
    df[df.RainTomorrow=='No'].Humidity9am.plot.box(ax=ax[1, 0])
    ax[1, 0].set_ylabel('Rain Tomorrow')
    df[df.RainTomorrow=='No'].Humidity3pm.plot.box(ax=ax[1, 1])
    st.pyplot(fig)
    fig1, ax = plt.subplots()
    ax.scatter(df[df.RainTomorrow=='Yes']['Humidity9am'],df[df.RainTomorrow=='Yes']['Humidity3pm'],c='plum',alpha=1,label='Tomorrow Rain = Yes') 
    ax.scatter(df[df.RainTomorrow=='No']['Humidity9am'],df[df.RainTomorrow=='No']['Humidity3pm'],c='slategrey',alpha=1,label='Tomorrow Rain = No') 
    fig1.set_figheight(6)
    fig1.set_figwidth(10)
    plt.legend()
    st.pyplot(fig1)

with tab8:
    winddirect = df[(df.RainTomorrow=='Yes')&(df.WindGustDir)].groupby('WindGustDir')['RainTomorrow'].count()/len(df[df.RainTomorrow=='Yes'])
    windgustspeed_frame = pd.DataFrame(winddirect)
    wind_direct_9am = (df[(df.RainTomorrow=='Yes')&(df.WindDir9am)].groupby('WindDir9am')['RainTomorrow'].count())/len(df[df.RainTomorrow=='Yes'])*100
    winddir9am_frame = pd.DataFrame(wind_direct_9am)
    wind_direct_3pm = df[(df.RainTomorrow=='Yes')&(df.WindDir3pm)].groupby('WindDir3pm')['RainTomorrow'].count()
    winddir3pm_frame = pd.DataFrame(wind_direct_3pm)

    st.markdown('#### If tomorrow will rain, today\'s wind guest direction are as follows')
    st.dataframe(windgustspeed_frame, 400, 200)
    st.markdown('#### If tomorrow will rain, today\'s wind direction at 9am are as follows')
    st.dataframe(winddir9am_frame, 400, 200)
    st.markdown('#### If tomorrow will rain, today\'s wind direction at 3pm are as follows')
    st.dataframe(winddir9am_frame, 400, 200)
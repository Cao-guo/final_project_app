# Streaming Media Platform Data App (EDA)
 **Team 3 - MISY225 Final Project**
 > By: Jiang Meng & Cheng Haoguo<br>
 > Create date: 2022-11-05

You can see some details when clicking the following link:<br>
[Our streamlit app](https://cao-guo-final-project-app-weather-app-zofvpp.streamlitapp.com/)<br>
[GitHubPages](https://github.com/Cao-guo/final_project_app)<br>
[Slides](https://github.com/Cao-guo/final_project_app/blob/main/Team-3.pdf)<br>
[Deployed python file is](https://github.com/Cao-guo/final_project_app/blob/main/weather-app.py)<br>


## Project Introduction
 This dataset contains about 10 years of daily weather observations from many locations across Australia. RainTomorrow is the target variable to predict. It means -- did it rain the next day, Yes or No? This column is Yes if the rain for that day was 1mm or more. <br>
 We select and analyze the data and give the conclusion of our project. You can get more information in the following part!

## Dataset Description
 The csv file is here: (https://github.com/Cao-guo/final_project_app/blob/main/weatherAUS.csv)
 + Location：The common name of the location of the weather station.
 + Lat and lon: The latitude and longitude of the location.
 + MinTemp: The minimum temperature in degrees celsius.
 + MaxTemp: The maximum temperature in degrees Celsius.
 + Rainfall: The amount of rainfall recorded for the day in mm.
 + Evaporation: The so-called Class A pan evaporation (mm) in the 24 hours to 9am.
 + Sunshine: The number of hours of bright sunshine in the day.
 + WindGustDir: The direction of the strongest wind gust in the 24 hours to midnight.
 + WindGustSpeed: The speed (km/h) of the strongest wind gust in the 24 hours to midnight.
 + WindDir9am: Direction of the wind at 9am.
 + WindDir3pm: Direction of the wind at 3pm.
 + WindSpeed9am: Wind speed (km/hr) averaged over 10 minutes prior to 9am.
 + WindSpeed3pm: Wind speed (km/hr) averaged over 10 minutes prior to 3pm.
 + Humidity9am: Humidity (percent) at 9am.
 + Humidity3pm: Humidity (percent) at 3pm.
 + Pressure9am: Atmospheric pressure (hpa) reduced to mean sea level at 9am.
 + Pressure3pm: Atmospheric pressure (hpa) reduced to mean sea level at 3pm.
 + Cloud9am: Fraction of sky obscure
 + Cloud3pm: Fraction of sky obscured by cloud (in "oktas": eighths) at 3pm.
 + Temp9am: Temperature (degrees C) at 9am.
 + Temp3pm: Temperature (degrees C) at 3pm.
 + RainToday: Boolean: 1 if precipitation (mm) in the 24 hours to 9am exceeds 1mm, otherwise 0.
 + RainTomorro: The amount of next day rain in mm. Used to create response variable RainTomorrow. A kind of measure of the "risk".

## Data process
 - Use df.dropna() to delete the null numbers.
 - Delete outliers to get a better boxplot for the factors.
 - Randomly select 50,000 data.

## Main functions of the streamlit page
 1. **Map** of regional rainfall in Australia, with a slider which filtered for average rainfall.<br>
 2. **Histograms** of rainfall by year and by month<br>
 3. The **tab** blocks show the 9 variables that affect rainfall and the relationship between the variable and the forecast for tomorrow's rainfall in different tabs.<br>
 4. **Sidebar** which users can enter the names of different areas to see statistics on rainfall at different times of the year and whether it will rain today or tomorrow.<br>

## Explanation of Data App
 1. In the map, you can go over the average rainfall of each city in Australia less than the value we select in the slider.
   - In **conclusion**, we can see that the southeast coast of Australia have a higher rainfall average.
 2. We show how the precipitation in Australia for years and for months in these two histograms. 
   - In **conclusion**, we can say that the average rainfall of 2007 is higher than the others, and it rains more in Novermber to February.
 3. Next, we set eight tab blocks to show the factors relate to whether rain will fall tomorrow. 
  We select the data which match tomorrow rain is TURE, then we use the data to make boxplot to get the overview of this factor. In the min and max Temp, Pressure, Humdity, we also set dot plot, which shows the difference of data between tomorrow rain is TRUE and FALSE.
   - We set the **conclusion** in a text box, which shows that it has a high chance to rain tomorrow when:<br>
   • It rained today<br>
   • The presure is low<br>
   • The humidity is high<br>
   • Wind speed is high<br>
   • Max and min temp are close to each other<br>
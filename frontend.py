import streamlit as st
from weather import city_weather
import pandas as pd
import plotly.express as px
from datetime import date

st.title("Weather Forecast")

city  = st.text_input("Enter the city name can also enter multiple cities for comaprision: ")


data,data1 = None,None

if st.button("Get Weather"):
    with st.spinner("Gathering weather info..."):
        data, data1 = city_weather(city)
    if data and 'location' in data:
        # Display from current (data)
        # Display forecast (data1)
        # If future date selected, use data2
        st.subheader(f"The Weather in {data['location']['name']}")
        st.write(f"Temperature: {data['current']['temp_c']} °C")
        st.write(f"Feels Like: {data['current']['feelslike_c']} °C")
        if data1 and 'forecast' in data1:
            st.markdown("### Forecast")
            st.write(f"Date: {data1['forecast']['forecastday'][0]['date']}")
            st.write(f"Sunrise: {data1['forecast']['forecastday'][0]['astro']['sunrise']}")
            st.write(f"Humidity (Hour 0): {data1['forecast']['forecastday'][0]['hour'][0]['humidity']}%")
            st.write(f"Chance of Rain (Hour 0): {data1['forecast']['forecastday'][0]['hour'][0]['chance_of_rain']}%")

            forecast_hours = data1['forecast']['forecastday'][0]['hour']

            hours = [hour['time'].split(' ')[1] for hour in forecast_hours]
            temperature = [hour['temp_c'] for hour in forecast_hours]

            df = pd.DataFrame({'Time':hours,
                                'Temeperature' : temperature}
                                )
            st.markdown("Temperature Forecast in next 24 hours")
            st.line_chart(df.set_index('Time'))
        else:
            st.warning("Forecast data is missing or invalid.")

        
    else:
        st.error("Failed to get current weather data.")

    


#st.set_page_config("Multiple Cities Weather Comparision")
st.title("Multiple cities comparision")
multi_city = st.text_input("Enter multiple city names for comparision")
if st.button("Compare Cities"):
    cities = [c.strip() for c in multi_city.split(",") if c.strip()]
    if len(cities) < 2 or len(cities) > 3:
        st.error(" Please enter 2 or 3 valid city names.")
    else:
        comparision_data = []
        forecast_chart_data = []
        cols = st.columns(len(cities))
        for i,city in enumerate(cities):
            data,data1, = city_weather(city)
            with cols[i]:
                if data:
                    st.subheader(f"The Weather in {data['location']['name']}")
                    st.metric("Temp", f"{data['current']['temp_c']}°C", f"Feels like {data['current']['feelslike_c']}°C")
                    st.metric("Humidity", f"{data['current']['humidity']}%")
                    st.caption(data['current']['condition']['text'])
                if data1 and 'forecast' in data1:
                    for hour in data1['forecast']['forecastday'][0]['hour']:
                        time = hour['time'].split(' ')[1][:2]
                        forecast_chart_data.append(
                            {
                                'City' : city.title(),
                                'Time' : time,
                                'Temperature' : hour['temp_c']
                            }
                        )
        if forecast_chart_data:
            df = pd.DataFrame(forecast_chart_data)
            st.markdown("Temperature comparison for multiple cities for next 24 hours")
            fig = px.line(df,x = "Time",y = "Temperature", color = "City", markers = True)
            st.plotly_chart(fig,use_container_width=True)
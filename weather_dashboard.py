import streamlit as st
import hashlib
import requests
import cohere
cohere_client = cohere.Client('uG2UTtCStEOSwS8YYphxmMatu3sbEoNb5BnXfWvu') 
# Hardcoded username and password
USERNAME = "admin"
PASSWORD = "password123"

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Display the image (replace with your actual path)
st.image('C:\\Users\\Hp\\Desktop\\streamlit 2\\Image2.jpg', width=250)

# Function for authentication
def authenticate():
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login", key="login button"):
        if username == USERNAME and hash_password(password) == hash_password(PASSWORD):
            # Store user authentication status in session state
            st.session_state["authenticated"] = True
            st.session_state["page"] = "weather"  # Set the page to "weather" after successful login
            st.success("Login successful!")
            st.rerun()  # Corrected to st.rerun() after successful login
        else:
            st.session_state["authenticated"] = False
            st.error("Invalid username or password. Please try again.")

# Weather function to fetch current and 5-day forecast data
def get_weather(city):
    api_key = "25b5203749e95de7070452b2b9b844bc"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"  # URL for 5-day forecast
    
    # Get current weather
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] == "404":
            st.error("City not found!")
        else:
            main_data = data["main"]
            wind_data = data["wind"]
            weather_data = data["weather"][0]
            
            temperature = main_data["temp"]
            humidity = main_data["humidity"]
            wind_speed = wind_data["speed"]
            description = weather_data["description"]
            icon = weather_data["icon"]
            
            st.write(f"### Current Weather in {city}")
            st.metric("Temperature", f"{temperature} °C")
            st.metric("Humidity", f"{humidity} %")
            st.metric("Wind Speed", f"{wind_speed} m/s")
            st.write(f"**Description**: {description.capitalize()}")
            
            icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
            st.image(icon_url, width=100)
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")

    # Get 5-day weather forecast
    try:
        forecast_complete_url = f"{forecast_url}q={city}&appid={api_key}&units=metric"
        forecast_response = requests.get(forecast_complete_url)
        forecast_data = forecast_response.json()
        
        if forecast_data["cod"] != "200":
            st.error("Could not fetch forecast data.")
        else:
            st.write(f"### 5-Day Weather Forecast for {city}")
            for day_data in forecast_data["list"][::8]:  # Get the data for 12:00 PM for each day
                date = day_data["dt_txt"]
                temperature = day_data["main"]["temp"]
                humidity = day_data["main"]["humidity"]
                description = day_data["weather"][0]["description"]
                wind_speed = day_data["wind"]["speed"]
                icon = day_data["weather"][0]["icon"]
                
                # Display each day's weather
                st.write(f"#### {date}")
                st.metric("Temperature", f"{temperature} °C")
                st.metric("Humidity", f"{humidity} %")
                st.metric("Wind Speed", f"{wind_speed} m/s")
                st.write(f"**Description**: {description.capitalize()}")
                
                icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
                st.image(icon_url, width=50)

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast data: {e}")

# Track and display recent searches in the sidebar
def display_recent_searches(city):
    # Initialize the recent searches in session state if not already initialized
    if "recent_searches" not in st.session_state:
        st.session_state["recent_searches"] = []

    # Add current search to the list of recent searches if it's not already in the list
    if city and city not in st.session_state["recent_searches"]:
        st.session_state["recent_searches"].append(city)

    # Show recent searches in the sidebar
    st.sidebar.title("Recent Searches")
    for i, recent_city in enumerate(reversed(st.session_state["recent_searches"])):
        if st.sidebar.button(recent_city, key=f"recent_city_{i}"):
            get_weather(recent_city)




# Main function to control page navigation
def main():
    # Initialize session state for user authentication and page state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "login"  # Default page is the login page

    if st.session_state["authenticated"]:
        if st.session_state["page"] == "weather":
            # Show weather page if authenticated
            st.title("Weather Forecasting ")
            st.write("Welcome to the Weather Forecasting App!")

            city = st.text_input("Enter City Name", key="main_city_input")
            if city:
                get_weather(city)
                display_recent_searches(city)


            # Logout button to log out and return to the login page
            if st.button("Logout", key="logout_button"):
                st.session_state["authenticated"] = False
                st.success("You have logged out successfully.")
                st.rerun()  # Refresh the app after logout

    else:
        # Show login page if not authenticated
        st.title("Credentials")
        st.write("Please log in to access the weather app.")
        authenticate()

# Run the main function to handle the app's flow
if __name__ == "__main__":
    main()

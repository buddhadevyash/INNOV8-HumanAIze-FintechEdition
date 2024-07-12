import streamlit as st

# Set page config at the very top
st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")

from ai_assistant_page import ai_assistant_page
from fitness_score_page import fitness_score_page
from choose_base_plans_page import choose_base_plans_page
from make_your_own_plan_page import make_your_own_plan_page
from home import home_page
from Bussiness_Dashboard.Home import Home  # Import the Home function from Business_Dashboard/Home.py

def main():
    st.title("Revolutionizing Insurance with SmartSure")

    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Select a page",
        ("Home", "AI Assistant", "Fitness Score", "Choose from Base Plans", "Make Your Own Plan", "Business Dashboard")
    )

    if page == "Home":
        home_page()  # Display content from home_page function in home.py
    elif page == "AI Assistant":
        ai_assistant_page()
    elif page == "Fitness Score":
        fitness_score_page()
    elif page == "Choose from Base Plans":
        choose_base_plans_page()
    elif page == "Make Your Own Plan":
        make_your_own_plan_page()
    elif page == "Business Dashboard":
        Home()  # Call the Home function from Business_Dashboard/Home.py

if __name__ == "__main__":
    main()

# home.py

import streamlit as st

def home_page():
    custom_css = """
        <style>
            body {
                font-family: 'Georgia', sans-serif;
                background-color: #3d0e4f; /* Purple background */
                color: #ffffff; /* White text */
                line-height: 1.6;
                padding-top: 20px;
            }
            .sidebar .sidebar-content {
                background-color: #3d0e4f; /* Purple background for sidebar */
                color: #ffffff; /* White text in sidebar */
            }
            .dashboard-title {
                font-size: 36px;
                font-weight: bold;
                color: #ffcc00; /* Yellow accent color */
                margin-bottom: 20px;
            }
            .dashboard-text {
                font-size: 20px;
                color: #dddddd; /* Light grey text */
                margin-bottom: 10px;
            }
            .action-list {
                font-size: 22px;
                color: #ffcc00; /* Yellow accent color */
                margin-bottom: 20px;
                list-style-type: disc; /* Bullet points for actions */
                padding-left: 20px;
            }
            .footer {
                margin-top: 40px;
                font-size: 14px;
                color: #dddddd; /* Light grey text for footer */
                text-align: center;
            }
        </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)


    st.write("Welcome to the Insurance Dashboard developed by Team Innov8.")
    st.write("You can perform the following actions here:")
    st.write("- Interact with PolicyPal AI.")
    st.write("- Check your Fitness Score and Claim Discounts.")
    st.write("- Choose from Base Insurance Plans.")
    st.write("- Make Your Own Custom Insurance Plan.")
    st.write("Select a page from the sidebar to get started!")

    st.markdown("---")
    st.write("Made with ☕ and 💻 by Akshansh, Harsh, Vatsal & Yash.")

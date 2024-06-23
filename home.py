# home.py

import streamlit as st

def home_page():
    custom_css = """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #0a192f; /* Dark blue background */
                color: #64ffda; /* Light teal text */
                line-height: 1.6;
                padding-top: 20px;
            }
            .sidebar .sidebar-content {
                background-color: #172a45; /* Slightly lighter blue for sidebar */
                color: #64ffda; /* Light teal text in sidebar */
            }
            .dashboard-title {
                font-size: 36px;
                font-weight: bold;
                color: #ffa500; /* Orange accent color */
                margin-bottom: 20px;
            }
            .team-name {
                font-size: 24px;
                font-weight: bold;
                color: #ff6b6b; /* Coral color for team name */
                margin-bottom: 20px;
            }
            .dashboard-text {
                font-size: 20px;
                color: #8892b0; /* Light blue-grey text */
                margin-bottom: 10px;
            }
            .action-list {
                font-size: 22px;
                color: #64ffda; /* Light teal for action items */
                margin-bottom: 20px;
                list-style-type: none;
                padding-left: 0;
            }
            .action-list li:before {
                content: '➤ ';
                color: #ffa500; /* Orange bullet points */
            }
            .footer {
                margin-top: 40px;
                font-size: 14px;
                color: #8892b0; /* Light blue-grey text for footer */
                text-align: center;
            }
        </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)

    st.markdown("<h1 class='dashboard-title'>Welcome to the Insurance Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='team-name'>Developed by Team Innov8</p>", unsafe_allow_html=True)
    
    st.markdown("<p class='dashboard-text'>You can perform the following actions here:</p>", unsafe_allow_html=True)
    st.markdown("""
    <ul class='action-list'>
        <li>Interact with PolicyPal AI</li>
        <li>Check your Fitness Score and Claim Discounts</li>
        <li>Choose from Base Insurance Plans</li>
        <li>Make Your Own Custom Insurance Plan</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown("<p class='dashboard-text'>Select a page from the sidebar to get started!</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p class='footer'>Made with ☕ and 💻 by Akshansh, Harsh, Vatsal & Yash</p>", unsafe_allow_html=True)
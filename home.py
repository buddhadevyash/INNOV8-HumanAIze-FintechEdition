import streamlit as st

def home_page():
    custom_css = """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #0a192f;
                color: #64ffda;
                line-height: 1.6;
                padding-top: 20px;
            }
            .sidebar .sidebar-content {
                background-color: #172a45;
                color: #64ffda;
            }
            .dashboard-title {
                font-size: 36px;
                font-weight: bold;
                color: #ffa500;
                margin-bottom: 10px;  /* Reduced from 20px to 10px */
            }
            .team-name {
                font-size: 24px;
                font-weight: bold;
                color: #ff6b6b;
                margin-bottom: 20px;
            }
            .dashboard-text {
                font-size: 20px;
                color: #8892b0;
                margin-bottom: 10px;
            }
            .action-list {
                font-size: 22px;
                color: #a4d8d8;
                margin-bottom: 20px;
                list-style-type: none;
                padding-left: 0;
            }
            .action-list li:before {
                content: '➤ ';
                color: #ffa500;
            }
            .footer {
                margin-top: 40px;
                font-size: 14px;
                color: #8892b0;
                text-align: center;
            }
            .motto {
                font-size: 20px;
                color: #ffa500;
                text-align: left;
                margin: 20px 0;
            }
            .center-content {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                margin: 10px 0;  /* Reduced from 20px to 10px */
            }
            .center-content h3 {
                margin-bottom: 5px;  /* Reduced from 10px to 5px */
                color: #64ffda;
            }
            .center-content img {
                max-width: 100%;
                height: auto;
            }
        </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown("<h1 class='dashboard-title'>Welcome to Smartsure!</h1>", unsafe_allow_html=True)
   
    
    image_url = "https://i.ibb.co/3s7JppM/Insurance-logo.png"
    st.markdown(f"""
    <div class='center-content'>
        <img src='{image_url}' width='175'>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<p class='dashboard-text'>Select a page from the sidebar to get started!</p>", unsafe_allow_html=True)
    st.markdown("<p class='motto'>Our AI-driven platform provides personalized insurance plans, exclusive discounts, and expert financial advice, all based on your comprehensive fitness scores tracked monthly. Now get rewarded for maintaining a healthy lifestyle with SmartSure.</p>", unsafe_allow_html=True)
    st.markdown("<p class='dashboard-text'>You can perform the following actions here:</p>", unsafe_allow_html=True)
    st.markdown("""
    <ul class='action-list'>
        <li>Interact with PolicyPal AI</li>
        <li>Check your Fitness Score and Claim Discounts</li>
        <li>Choose from Base Insurance Plans</li>
        <li>Make Your Own Custom Insurance Plan</li>
        <li>Visit the dynamic Business Dashboard</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p class='footer'>Made with ☕ and 💻 by Harsh, Vatsal, Yash & Akshansh</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    home_page()

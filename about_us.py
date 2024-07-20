import json
import streamlit as st

def about_us_page():
    st.title("About Us")
    
    # Team data with placeholders for image URLs
    data = {
        "member1": {
            "name": "Harsh Chitaliya",
            "sr": "Team Innov8 Member 1",
            "phone": "+91 9321694382",
            "mail": "harshchitaliya010@gmail.com",
            "linkedIn": "https://www.linkedin.com/in/harshchitaliya/",
            "github": "github.com/harshchi19",
            "urlToimage": "harsh.jpg"
        },
        "member2": {
            "name": "Yash Buddhadev",
            "sr": "Team Innov8 Member 2",
            "phone": "+91 8369306269",
            "mail": "yashbuddhadev21@gmail.com",
            "linkedIn": "https://www.linkedin.com/in/yash-buddhadev-889955289/",
            "github": "https://github.com/buddhadevyash",
            "urlToimage": "yash.jpg"
        },
        "member3": {
            "name": "Vatsal Kotha",
            "sr": "Team Innov8 Member 3",
            "phone": "+91 9137401776",
            "mail": "vatsalkotha@gmail.com",
            "linkedIn": "https://www.linkedin.com/in/vatsal-kotha/",
            "github": "https://github.com/VatsalKotha",
            "urlToimage": "vatsal.jpg"
        },
        "akshansh": {
            "name": "Akshansh Dwivedi",
            "sr": "Team Innov8 Member 4",
            "phone": "+91 8097949196",
            "mail": "akshansh2624@gmail.com",
            "linkedIn": "https://www.linkedin.com/in/akshansh2624",
            "github": "https://github.com/akshansh2624",
            "urlToimage": "akshansh.jpg"
        }
    }

    # Custom CSS for circular images and styled buttons
    st.markdown("""
    <style>
    .circular-image {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        object-fit: cover;
    }
    .social-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8px 12px;
        margin: 2px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        text-decoration: none;
        color: white;
        width: 110px;
        height: 36px;
        background-color: #555555;
    }
    .social-button:hover {
        background-color: #444444;
    }
    </style>
    """, unsafe_allow_html=True)

    for i, key in enumerate(data):
        unique_key = f"{i}_{key}"
        col1, col2 = st.columns(2)
        with col1:
            st.image(data[key]["urlToimage"], width=200, output_format="PNG", use_column_width=False)

        with col2:
            st.text(data[key]["sr"])
            st.header(data[key]["name"])
            st.text("📞 " + data[key]["phone"])
            
            linkedin_url = data[key]['linkedIn']
            github_url = data[key]['github']
            email = data[key]["mail"]
            
            # LinkedIn, GitHub, and Email buttons without icons
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start;">
                <a href="{linkedin_url}" target="_blank" class="social-button">
                    LinkedIn
                </a>
                <a href="{github_url}" target="_blank" class="social-button">
                    GitHub
                </a>
                <a href="mailto:{email}" class="social-button">
                    Email
                </a>
            </div>
            """, unsafe_allow_html=True)

    # Hide Streamlit style
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Call the function
about_us_page()

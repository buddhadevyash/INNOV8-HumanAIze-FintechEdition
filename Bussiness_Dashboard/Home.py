import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go

# Set Streamlit options
st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to detect theme and apply styles dynamically
def apply_theme():
    is_dark_theme = st.session_state["theme"] == "dark"
    text_color = "#ffffff" if is_dark_theme else "#000000"
    bg_color = "#333333" if is_dark_theme else "#ffffff"
    grid_color = "#555555" if is_dark_theme else "#dddddd"
    plot_bg_color = "rgba(0,0,0,0)" if is_dark_theme else "rgba(255,255,255,1)"
    return text_color, bg_color, grid_color, plot_bg_color

# Set initial theme
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

# Toggle theme button
if st.button("Toggle Theme"):
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

text_color, bg_color, grid_color, plot_bg_color = apply_theme()

# Centered header using HTML and CSS
st.markdown(
    f"""
    <style>
    .centered-header {{
        text-align: center;
        color: {text_color};
    }}
    </style>
    <h1 class="centered-header">SmartSure Business Analytics Dashboard 💰</h1>
    """,
    unsafe_allow_html=True
)
st.subheader("ANALYTICAL PROCESSING, KPI, TRENDS & PREDICTIONS")

# Load Style CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Excel file | comment this line when you fetch data from MySQL
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Side bar logo
st.sidebar.image("data/logo1.png", caption="")

# Switcher
region = st.sidebar.multiselect(
    "SELECT REGION",
    options=df["Region"].unique(),
    default=df["Region"].unique(),
)
location = st.sidebar.multiselect(
    "SELECT LOCATION",
    options=df["Location"].unique(),
    default=df["Location"].unique(),
)
construction = st.sidebar.multiselect(
    "SELECT CONSTRUCTION",
    options=df["Construction"].unique(),
    default=df["Construction"].unique(),
)

df_selection = df.query(
    "Region==@region & Location==@location & Construction ==@construction"
)

# This function performs basic descriptive analytics like Mean, Mode, Sum, etc.
def Home():
    with st.expander("VIEW EXCEL DATASET"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=["Policy", "Expiry", "Location", "State", "Region", "Investment", "Construction", "BusinessType", "Earthquake", "Flood", "Rating"])
        st.dataframe(df_selection[showData], use_container_width=True)
    
    # Compute top analytics
    total_investment = float(pd.Series(df_selection['Investment']).sum())
    investment_mode = float(pd.Series(df_selection['Investment']).mode())
    investment_mean = float(pd.Series(df_selection['Investment']).mean())
    investment_median = float(pd.Series(df_selection['Investment']).median()) 
    rating = float(pd.Series(df_selection['Rating']).sum())

    total1, total2, total3, total4, total5 = st.columns(5, gap='small')
    with total1:
        st.info('Sum Investment', icon="💰")
        st.metric(label="Sum TZS", value=f"{total_investment:,.0f}")

    with total2:
        st.info('Most Investment', icon="💰")
        st.metric(label="Mode TZS", value=f"{investment_mode:,.0f}")

    with total3:
        st.info('Average', icon="💰")
        st.metric(label="Average TZS", value=f"{investment_mean:,.0f}")

    with total4:
        st.info('Central Earnings', icon="💰")
        st.metric(label="Median TZS", value=f"{investment_median:,.0f}")

    with total5:
        st.info('Ratings', icon="💰")
        st.metric(label="Rating", value=numerize(rating), help=f""" Total Rating: {rating} """)
    style_metric_cards(background_color=bg_color, border_left_color=text_color, border_color=text_color, box_shadow="#F71938")

    # Variable distribution Histogram
    with st.expander("DISTRIBUTIONS BY FREQUENCY"):
        df.hist(figsize=(16, 8), color=text_color, zorder=2, rwidth=0.9, legend=['Investment'])
        st.pyplot()

# Graphs
def graphs():
    investment_by_business_type = (
        df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
    )
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="<b> INVESTMENT BY BUSINESS TYPE </b>",
        color_discrete_sequence=["#00FF00"] * len(investment_by_business_type),
        template="plotly_dark" if st.session_state["theme"] == "dark" else "plotly_white",
    )
    fig_investment.update_layout(
        plot_bgcolor=plot_bg_color,
        font=dict(color=text_color),
        yaxis=dict(showgrid=True, gridcolor=grid_color),  # Show y-axis grid and set its color  
        paper_bgcolor=plot_bg_color,  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor=grid_color),  # Show x-axis grid and set its color
    )

    investment_state = df_selection.groupby(by=["State"]).count()[["Investment"]]
    fig_state = px.line(
        investment_state,
        x=investment_state.index,
        y="Investment",
        orientation="v",
        title="<b> INVESTMENT BY STATE </b>",
        color_discrete_sequence=["#00FF00"] * len(investment_state),
        template="plotly_dark" if st.session_state["theme"] == "dark" else "plotly_white",
    )
    fig_state.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor=plot_bg_color,
        yaxis=(dict(showgrid=False))
    )

    left, right, center = st.columns(3)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)
    
    with center:
        fig = px.pie(df_selection, values='Rating', names='State', title='RATINGS BY REGIONS')
        fig.update_layout(legend_title="Regions", legend_y=0.9)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True)

# Function to show current earnings against expected target
def Progressbar():
    st.markdown(f"""<style>.stProgress > div > div > div > div {{ background-image: linear-gradient(to right, #00FF00 , #FFFF00)}}</style>""", unsafe_allow_html=True)
    target = 3000000000
    current = df_selection["Investment"].sum()
    percent = round((current / target * 100))
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Target done !")
    else:
        st.write(f"you have {percent}% of {format(target, 'd')} TZS")
        for percent_complete in range(percent):
            time.sleep(0.1)
            mybar.progress(percent_complete + 1, text=" Target Percentage")

# Menu bar
def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        Home()
        graphs()
    if selected == "Progress":
        Progressbar()
        graphs()

sideBar()

st.subheader('PICK FEATURES TO EXPLORE DISTRIBUTIONS TRENDS BY QUARTILES')
feature_y = st.selectbox('Select feature for y Quantitative Data', df_selection.select_dtypes("number").columns)
fig2 = go.Figure(
    data=[go.Box(x=df['BusinessType'], y=df[feature_y])],
    layout=go.Layout(
        title=go.layout.Title(text="BUSINESS TYPE BY QUARTILES OF INVESTMENT"),
        plot_bgcolor=plot_bg_color,  # Set plot background color to transparent
        paper_bgcolor=plot_bg_color,  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor=grid_color),  # Show x-axis grid and set its color
        yaxis=dict(showgrid=True, gridcolor=grid_color),  # Show y-axis grid and set its color
        font=dict(color=text_color),  # Set text color
    )
)
# Display the Plotly figure using Streamlit
st.plotly_chart(fig2, use_container_width=True)

# Theme
hide_st_style = f""" 
<style>
#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}
body {{background-color: {bg_color};}}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

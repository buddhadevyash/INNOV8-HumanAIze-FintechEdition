import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

def create_pdf_certificate(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.image('certificate.jpg', x=0, y=0, w=210, h=297)  # Assuming A4 size

    frame_width = 210
    text_width = 180
    x_position = (frame_width - text_width) / 2
    y_position = 60

    for key, value in data.items():
        pdf.set_xy(x_position, y_position)
        pdf.cell(0, 10, txt=f"{key}: {value}", ln=True, align='L')
        y_position += 10

    return pdf.output(dest='S').encode('latin-1')

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv('fitness_claim_dataset.csv')

data = load_data()

# Streamlit app
st.title("Health Certificate Generator")

# Select name from the dataset
selected_name = st.selectbox("Select a name", data['Name'].tolist())

if st.button("Generate Certificate"):
    # Get the row for the selected name
    selected_data = data[data['Name'] == selected_name].iloc[0].to_dict()
    
    # Create PDF
    pdf_bytes = create_pdf_certificate(selected_data)
    
    # Create download button
    b64_pdf = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="health_certificate.pdf">Download Health Certificate</a>'
    st.markdown(href, unsafe_allow_html=True)

# Optional: Display the selected data
if st.checkbox("Show selected data"):
    st.write(data[data['Name'] == selected_name])

# Optional: Display the entire dataset
if st.checkbox("Show entire dataset"):
    st.dataframe(data)

# Instructions for use
st.subheader("How to use:")
st.write("1. Select a name from the dropdown menu.")
st.write("2. Click 'Generate Certificate' to create the PDF.")
st.write("3. Click the 'Download Health Certificate' link to download the PDF.")
st.write("Note: Make sure you have a 'certificate.jpg' file and 'fitness_claim_dataset.csv' file in the same directory as this script.")
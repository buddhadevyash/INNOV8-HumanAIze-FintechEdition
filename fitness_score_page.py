import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import plotly.express as px
<<<<<<< HEAD
import base64
from fpdf import FPDF
=======

# Function to display the Home page
def home_page():
    st.title('Home Page')
    st.write("This is the home page content.")

# Function to display the AI Assistant page
def ai_assistant_page():
    st.title('AI Assistant Page')
    st.write("This is the AI assistant page content.")
>>>>>>> 3be87cfa897a55e64a18f5708c552b69febce075

# Function to load data and model, and preprocess data
@st.cache(allow_output_mutation=True)
def load_data_and_model():
    df = pd.read_csv('fitness_claim_dataset.csv')
    df = df.dropna()

    categorical_columns = df.select_dtypes(include=['object']).columns.difference(['Name'])
    label_encoders = {}
    for column in categorical_columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    scaler = StandardScaler()
    numerical_columns = df.select_dtypes(include=[np.number]).columns.difference(['Age'])
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    df['Fitness Score'] = (
        0.1 * df['Blood Pressure (Systolic)'] +
        0.1 * df['Blood Pressure (Diastolic)'] +
        0.15 * df['Heart Beats'] +
        0.15 * df['BMI'] +
        0.1 * df['Cholesterol'] +
        0.2 * df['Steps Taken'] +
        0.1 * df['Active Minutes'] +
        0.1 * df['Sleep Duration'] +
        0.05 * df['Sleep Quality'] +
        0.15 * df['VO2 Max'] +
        0.1 * df['Calories Burned'] +
        0.15 * df['SpO2 Levels'] +
        -0.2 * df['Stress Levels']
    )

    df['Fitness Score'] = (df['Fitness Score'] - df['Fitness Score'].min()) / (df['Fitness Score'].max() - df['Fitness Score'].min()) * 100

    X = df.drop(['Name', 'Fitness Score'], axis=1)
    y = df['Fitness Score']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_regressor.fit(X_train, y_train)

    return df, rf_regressor

def create_pdf_certificate(data, fitness_score):
    pdf = FPDF()
    pdf.add_page()
    
    # Add a fancy font
    pdf.add_font('FancyFont', '', 'font.ttf', uni=True)
    pdf.set_font("FancyFont", size=12)
    
    pdf.image('certificate.jpg', x=0, y=0, w=210, h=297)  # Assuming A4 size

    frame_width = 210
    text_width = 180
    x_position = (frame_width - text_width) / 2
    y_position = 60

    pdf.set_text_color(255, 255, 0)  # Set text color to yellow

    for key, value in data.items():
        pdf.set_xy(x_position, y_position)
        pdf.cell(0, 10, txt=f"{key}: {value}", ln=True, align='L')
        y_position += 10

    # Add Fitness Score
    pdf.set_xy(x_position, y_position)
    # pdf.cell(0, 10, txt=f"Fitness Score: {fitness_score:.2f}", ln=True, align='L')

    return pdf.output(dest='S').encode('latin-1')

<<<<<<< HEAD
=======
    # Create DataFrame for visualization
    viz_df = df.copy()
    viz_df['Predicted Discount'] = viz_df['Fitness Score'].apply(predict_discount)

    # Create 3D scatter plot
    fig = px.scatter_3d(viz_df, x='Fitness Score', y='Predicted Discount', z='Age',
                        color='Predicted Discount', size='Fitness Score',
                        hover_data=['Name', 'Age'], title='3D Scatter Plot of Fitness Score, Predicted Discount, and Age')

    fig.update_layout(scene = dict(
                        xaxis_title='Fitness Score',
                        yaxis_title='Predicted Discount',
                        zaxis_title='Age'),
                        width=800,
                        height=800)

    # Display the plot in Streamlit
    st.plotly_chart(fig)

# Function to get fitness score and predicted discount
>>>>>>> 3be87cfa897a55e64a18f5708c552b69febce075
def get_fitness_score_and_discount(df, rf_regressor, name, age):
    row = df[(df['Name'] == name) & (df['Age'] == age)]
    if not row.empty:
        features = row.drop(['Name', 'Fitness Score'], axis=1)
        fitness_score = rf_regressor.predict(features)[0]
        discount = predict_discount(fitness_score)
        selected_data = row.iloc[0].to_dict()
        return fitness_score, discount, selected_data
    else:
        return None, None, None

def predict_discount(fitness_score):
    if fitness_score >= 90:
        return 30  # 30% discount
    elif fitness_score >= 80:
        return 25  # 25% discount
    elif fitness_score >= 70:
        return 20  # 20% discount
    elif fitness_score >= 60:
        return 15  # 15% discount
    elif fitness_score >= 50:
        return 10  # 10% discount
    elif fitness_score >= 40:
        return 5  # 5% discount
    else:
        return 0  # No discount

def display_model_metrics(df, rf_regressor):
    X = df.drop(['Name', 'Fitness Score'], axis=1)
    y = df['Fitness Score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    y_pred_train = rf_regressor.predict(X_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))

    y_pred_test = rf_regressor.predict(X_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

    target_variance = np.var(y_test)
    explained_variance_percentage = (1 - (test_rmse ** 2 / target_variance)) * 100

    r_squared = r2_score(y_test, y_pred_test)
    mae = mean_absolute_error(y_test, y_pred_test)
    mse = mean_squared_error(y_test, y_pred_test)

    st.write("## Model Performance Metrics")
    st.write(f"Train RMSE: {train_rmse:.2f}")
    st.write(f"Test RMSE: {test_rmse:.2f}")
    st.write(f"Explained Variance Percentage: {explained_variance_percentage:.2f}%")
    st.write(f"R-squared: {r_squared:.2f}")
    st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
    st.write(f"Mean Squared Error (MSE): {mse:.2f}")
    st.write(f"Root Mean Squared Error (RMSE): {test_rmse:.2f}")

def fitness_score_page():
    st.title('Fitness Claim Discount Predictor and Certificate Generator')

    # Load data and model
    df, rf_regressor = load_data_and_model()

    # User input
    name = st.text_input("Enter name:")
    age = st.number_input("Enter age:", min_value=0)

    if st.button('Get Fitness Score, Discount, and Generate Certificate'):
        if name and age:
            fitness_score, discount, selected_data = get_fitness_score_and_discount(df, rf_regressor, name, age)
            if fitness_score is not None:
                st.write(f"Fitness Score for {name} (age {age}): {fitness_score:.2f}")
                st.write(f"Discount for {name} (age {age}): {discount}%")

                # Generate certificate
                pdf_bytes = create_pdf_certificate(selected_data, fitness_score)
                
                # Create download button
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="health_certificate.pdf">Download Health Certificate</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.write(f"No data found for {name} (age {age}). Please check your input.")
        else:
            st.write("Please enter both name and age.")

    # Display model performance metrics
    display_model_metrics(df, rf_regressor)

    # Create DataFrame for visualization
    viz_df = df.copy()
    viz_df['Predicted Discount'] = viz_df['Fitness Score'].apply(predict_discount)

    # Create 3D scatter plot
    fig = px.scatter_3d(viz_df, x='Fitness Score', y='Predicted Discount', z='Age',
                        color='Predicted Discount', size='Fitness Score',
                        hover_data=['Name', 'Age'], title='3D Scatter Plot of Fitness Score, Predicted Discount, and Age')

    fig.update_layout(scene = dict(
                        xaxis_title='Fitness Score',
                        yaxis_title='Predicted Discount',
                        zaxis_title='Age'),
                        width=800,
                        height=800)

    # Display the plot in Streamlit
    st.plotly_chart(fig)

# Main function to control page navigation
def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ('Home', 'AI Assistant', 'Fitness Score'))

    if page == "Home":
        st.title('Home Page')
        st.write("Welcome to the Fitness Claim Discount Predictor app.")
    elif page == "AI Assistant":
        st.title('AI Assistant Page')
        st.write("This is the AI assistant page content.")
    elif page == "Fitness Score":
        fitness_score_page()

if __name__ == "__main__":
    main()

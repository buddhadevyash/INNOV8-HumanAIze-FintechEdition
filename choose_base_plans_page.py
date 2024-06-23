import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import streamlit as st
import matplotlib.pyplot as plt

def choose_base_plans_page():
    st.title('Choose from Base Plans')
    st.write("This is the page where users can choose from base insurance plans.")

    # Load data
    df = pd.read_csv("base_plans.csv")

    # Data Preprocessing
    df.dropna(inplace=True)
    df.drop(['perc_premium_paid_by_cash_credit','Count_3-6_months_late','Count_6-12_months_late',
             'Count_more_than_12_months_late','application_underwriting_score','target'], axis='columns', inplace=True)
    df.drop(['sourcing_channel','residence_area_type'], axis='columns', inplace=True)

    df['age_in_years'] = df['age_in_days'] // 365

    np.random.seed(42)
    occupations = ['Engineer', 'Doctor', 'Teacher', 'Clerk', 'Manager', 'Laborer', 'Mechanic', 'Driver']
    df['occupation'] = np.random.choice(occupations, size=len(df))
    df['job_type'] = df['occupation'].apply(lambda x: 'White-collar' if x in ['Engineer', 'Doctor', 'Teacher', 'Manager'] else 'Blue-collar')
    df['policy'] = None

    df.loc[df['age_in_years'] < 18, 'policy'] = 'LIC'
    df.loc[(df['age_in_years'] >= 18) & (df['Income'] > 50000), 'policy'] = 'StarLite'
    df.loc[(df['age_in_years'] >= 18) & (df['Income'] <= 50000), 'policy'] = 'Maxbupa'

    # Model Training
    features = ['age_in_years', 'Income']
    X = df[features]
    y = df['policy']

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)

    # Prediction function
    def predict_policy(age, income=None, occupation=None):
        age_in_years = age // 365
        if age_in_years < 18:
            return 'LIC'
        job_type = 'White-collar' if occupation in ['Engineer', 'Doctor', 'Teacher', 'Manager'] else 'Blue-collar'
        user_data = pd.DataFrame({'age_in_years': [age_in_years], 'Income': [income]})
        policy_index = knn.predict(user_data)[0]
        policy = le.inverse_transform([policy_index])[0]
        return policy

    # Input fields
    user_age = st.number_input("Enter your age in years:", min_value=0, max_value=100, step=1)
    
    user_age_in_days = user_age * 365

    if user_age_in_days < 6570:
        st.write('The best insurance policy for you is: LIC')
    else:
        user_income = st.number_input("Enter your income:", min_value=0, step=1)
        user_occupation = st.selectbox("Select your occupation:", occupations)
        best_policy = predict_policy(user_age_in_days, user_income, user_occupation)
        st.write(f'The best insurance policy for you is: {best_policy}')

    # Plot: No of premiums paid vs premium
    st.subheader('No of premiums paid vs premium')
    fig, ax = plt.subplots()
    df.plot(kind='scatter', x='no_of_premiums_paid', y='premium', s=32, alpha=.8, ax=ax)
    ax.spines[['top', 'right']].set_visible(False)
    st.pyplot(fig)

    # Plot: Occupation vs Job Type
    st.subheader('Occupation vs Job Type')
    fig, ax = plt.subplots(figsize=(8, 8))
    df_2dhist = pd.DataFrame({
        x_label: grp['job_type'].value_counts()
        for x_label, grp in df.groupby('occupation')
    })
    sns.heatmap(df_2dhist, cmap='viridis', ax=ax)
    ax.set_xlabel('Occupation')
    ax.set_ylabel('Job Type')
    st.pyplot(fig)

    # Plot: Income Distribution by Occupation and Job Type
    st.subheader('Income Distribution by Occupation and Job Type')
    fig, ax = plt.subplots(figsize=(12, 8))
    df.boxplot(column='Income', by=['occupation', 'job_type'], ax=ax)
    plt.xticks(rotation=45)
    ax.set_xlabel('Occupation, Job Type')
    ax.set_ylabel('Income')
    ax.set_title('Income Distribution by Occupation and Job Type')
    st.pyplot(fig)

    # Plot: Occupation Count
    st.subheader('Occupation Count')
    fig, ax = plt.subplots()
    df.groupby('occupation').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'), ax=ax)
    ax.spines[['top', 'right']].set_visible(False)
    st.pyplot(fig)

if __name__ == "__main__":
    choose_base_plans_page()

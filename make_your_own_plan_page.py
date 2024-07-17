import streamlit as st

def calculate_base_premium(age, gender, profession, insurance_type, coverage_amount=0):
    base_rate = 0

    health_base_rates = {
        'young': 3000,  # Monthly: 250
        'adult': 5000,  # Monthly: 416
        'middle_age': 7000,  # Monthly: 583
        'senior': 10000  # Monthly: 833
    }

    life_base_rates = {
        'young': 6000,  # Monthly: 500
        'adult': 8400,  # Monthly: 700
        'middle_age': 12000,  # Monthly: 1000
        'senior': 18000  # Monthly: 1500
    }

    # Age categories
    if age < 25:
        age_category = 'young'
    elif age < 35:
        age_category = 'adult'
    elif age < 45:
        age_category = 'middle_age'
    else:
        age_category = 'senior'

    if insurance_type == 'Health Insurance':
        base_rate = health_base_rates[age_category]
    elif insurance_type == 'Life Insurance':
        base_rate = life_base_rates[age_category] * (coverage_amount / 10000000)

    if gender.lower() == 'female':
        base_rate *= 0.95

    high_risk_professions = ['manual labor', 'construction worker', 'police officer', 'firefighter']
    medium_risk_professions = ['teacher', 'it professional', 'office worker', 'salesperson']

    profession_lower = profession.lower()
    if profession_lower in [p.lower() for p in high_risk_professions]:
        base_rate *= 1.3
    elif profession_lower in [p.lower() for p in medium_risk_professions]:
        base_rate *= 1.1
    else:
        base_rate *= 1.2

    base_rate /= 12
    return base_rate

def calculate_discount(fitness_score):
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


def generate_personalized_plan(age, gender, profession, fitness_score, insurance_type, coverage_amount=0):

    base_premium = calculate_base_premium(age, gender, profession, insurance_type, coverage_amount)

    discount_rate = calculate_discount(fitness_score)
    discount_amount = base_premium * (discount_rate / 100)
    discounted_premium = base_premium - discount_amount

    max_discount_rate = 30
    max_discount_amount = base_premium * (max_discount_rate / 100)
    max_discounted_premium = base_premium - max_discount_amount

    return base_premium, discount_rate, discount_amount, discounted_premium, max_discounted_premium


# List of professions
professions = [
    'Accountant', 'Actor', 'Architect', 'Artist', 'Business Analyst', 'Chef', 'Construction Worker',
    'Designer', 'Doctor', 'Engineer', 'Farmer', 'Firefighter', 'IT Professional', 'Journalist',
    'Lawyer', 'Manual Labor', 'Nurse', 'Office Worker', 'Police Officer', 'Salesperson',
    'Scientist', 'Teacher', 'Technician', 'Writer', 'Other'
]

# List of coverage amounts for Life Insurance
coverage_amounts = ['50L', '1Cr', '1.5Cr', '2Cr', '2.5Cr', '3Cr', '3.5Cr', '4Cr', '4.5Cr', '5Cr']

def make_your_own_plan_page():
    st.title("Personalized Health and Life Insurance Plan Generator")

    st.header("Enter your details:")

    # User inputs
    age = st.number_input("Enter your age:", min_value=0, max_value=100, step=1)
    gender = st.selectbox("Select your gender:", options=["Male", "Female", "Other"])
    profession = st.selectbox("Select your profession:", options=professions)
    fitness_score = st.slider("Enter your fitness score (0-100):", min_value=0, max_value=100)
    insurance_type = st.selectbox("Select the type of insurance plan:", options=["Health Insurance", "Life Insurance"])

    coverage_amount = 0
    if insurance_type == "Life Insurance":
        selected_coverage = st.selectbox("Select your coverage amount:", options=coverage_amounts)
        if 'L' in selected_coverage:
            coverage_amount = int(selected_coverage[:-1]) * 100000
        else:
            coverage_amount = float(selected_coverage[:-2]) * 10000000

    if st.button("Generate Plan"):
        base_premium, discount_rate, discount_amount, discounted_premium, max_discounted_premium = generate_personalized_plan(
            age, gender, profession, fitness_score, insurance_type, coverage_amount)

        st.subheader("Personalized Insurance Plan Details")
        st.markdown(f"""
        **Insurance Type:** {insurance_type}

        **Base Premium (Monthly):** INR {base_premium:.2f}

        **Discount based on current fitness score:** {discount_rate}%

        **Discount Amount:** INR {discount_amount:.2f}

        **Discounted Premium (Monthly):** INR {discounted_premium:.2f}

        **Potential Maximum Discounted Premium (Monthly):** INR {max_discounted_premium:.2f}

        ---

        ### Additional Information:

        - **Age:** {age}
        - **Gender:** {gender}
        - **Profession:** {profession}
        - **Current Fitness Score:** {fitness_score}
        - **Coverage Amount:** {selected_coverage if insurance_type == 'Life Insurance' else 'N/A'}

        **Note:** Your premium will be recalculated every month based on your updated fitness score. 
        Stay active to maximize your discounts!
        """)

        st.write("### Potential Maximum Discount:")
        st.write(
            f"With a fitness score of 90 or above, you could achieve a discount of up to 30% on your premium, bringing your monthly cost down to INR {max_discounted_premium:.2f}.")

        st.write("### Health Tips:")
        st.write("""
        - Regular exercise is crucial for maintaining good health.
        - A balanced diet can greatly improve your overall fitness.
        - Make sure to get enough sleep and manage stress effectively.
        - Regular health check-ups can help detect issues early.
        """)

        st.write("### FAQ:")
        st.write("""
        **Q: How is my fitness score calculated?**
        A: Your fitness score is calculated based on the data from your fitness tracker, including metrics such as steps taken, calories burned, heart rate, and other activity levels.

        **Q: Can my premium increase if my fitness score decreases?**
        A: Yes, since your premium is dynamically calculated each month based on your fitness score, a lower fitness score may result in a higher premium.

        **Q: How can I maximize my discount?**
        A: To maximize your discount, maintain a high fitness score by staying active and healthy throughout the month.
        """)

if __name__ == "__main__":
    main()

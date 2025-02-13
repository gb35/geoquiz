import streamlit as st
import requests
import random

# st.set_page_config(page_title="🌍 Country Quiz PWA", layout="wide")
st.set_page_config(page_title="🌍 Country Quiz PWA")

@st.cache_data
def fetch_countries():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url).json()
    country_data = {}
    for country in response:
        # name = country["name"]["common"]
        name = country["translations"]["fra"]["common"]
        flag_url = country["flags"]["png"]
        country_data[name] = flag_url  
    return country_data

country_flags = fetch_countries()
countries = list(country_flags.keys())

def get_quiz_data():
    correct_country = random.choice(countries)
    correct_flag = country_flags[correct_country]
    wrong_countries = random.sample([c for c in countries if c != correct_country], 3)
    choices = [correct_country] + wrong_countries
    random.shuffle(choices)
    return correct_country, correct_flag, choices

st.title("🌍 Country Quiz")

tab1, tab2 = st.tabs(["🌎 Country → Flag", "🚩 Flag → Country"])

# ---- Quiz 1: Country → Flag ----
with tab1:
    st.subheader("Which flag belongs to this country?")
    
    # Initialize quiz in session state if not already set
    if "quiz1" not in st.session_state:
        correct_country, correct_flag, choices = get_quiz_data()
        st.session_state.quiz1 = {
            "correct_country": correct_country,
            "correct_flag": correct_flag,
            "choices": choices
        }
    else:
        correct_country = st.session_state.quiz1["correct_country"]
        correct_flag = st.session_state.quiz1["correct_flag"]
        choices = st.session_state.quiz1["choices"]

    st.write(f"**Country:** {correct_country}")

    # Assign numbers 1-4 to choices
    choice_numbers = {i+1: choice for i, choice in enumerate(choices)}

    cols = st.columns(4)
    
    if "selected_number" not in st.session_state:
        st.session_state.selected_number = None  # Track user's choice

    for i, (num, choice) in enumerate(choice_numbers.items()):
        with cols[i]:
            st.image(country_flags[choice], width=50%)
            if st.button(str(num), key=f"q1_{num}"):  # Button displays number instead of name
                st.session_state.selected_number = num  # Store the selected number

    if st.session_state.selected_number is not None:
        selected_country = choice_numbers[st.session_state.selected_number]  # Convert number back to country
        
        if selected_country == correct_country:
            with st.expander("✅ Correct! 🎉"):
                st.success(f"Good job! {correct_country} is the correct answer.")
        else:
            with st.expander("❌ Wrong Answer!"):
                st.error(f"Oops! The correct answer is **{correct_country}**.")
                st.image(correct_flag, width=100)

    # Number-to-country mapping (hidden via CSS)
    st.markdown(
        """
        <style>
        .hidden-options { visibility: hidden; height: 0; }
        </style>
        <div class="hidden-options">
        """,
        unsafe_allow_html=True
    )
#    for num, choice in choice_numbers.items():
#        st.write(f"{num} → {choice}")  # This will be hidden
#    st.markdown("</div>", unsafe_allow_html=True)

    # Button to generate a new quiz round
    if st.button("🔄 New Question"):
        correct_country, correct_flag, choices = get_quiz_data()
        st.session_state.quiz1 = {
            "correct_country": correct_country,
            "correct_flag": correct_flag,
            "choices": choices
        }
        st.session_state.selected_number = None  # Reset selection
        st.rerun()  # Force refresh

# ---- Quiz 2: Flag → Country ----
with tab2:
    st.subheader("Which country does this flag belong to?")
    cols = st.columns(4)
    # Initialize quiz in session state if not already set
    if "quiz2" not in st.session_state:
        correct_country, correct_flag, choices = get_quiz_data()
        st.session_state.quiz2 = {
            "correct_country": correct_country,
            "correct_flag": correct_flag,
            "choices": choices
        }
    else:
        correct_country = st.session_state.quiz2["correct_country"]
        correct_flag = st.session_state.quiz2["correct_flag"]
        choices = st.session_state.quiz2["choices"]

    st.image(correct_flag, width=100)

    if "selected_q2" not in st.session_state:
        st.session_state.selected_q2 = None  # Track user's choice

    for choice in choices:
        if st.button(choice, key=f"q2_{choice}"):
            st.session_state.selected_q2 = choice  # Store selected answer

    if st.session_state.selected_q2 is not None:
        selected_country = st.session_state.selected_q2  # Get user's choice

        if selected_country == correct_country:
            with st.expander("✅ Correct! 🎉"):
                st.success(f"Good job! {correct_country} is the correct answer.")
        else:
            with st.expander("❌ Wrong Answer!"):
                st.error(f"Oops! The correct answer is **{correct_country}**.")
                st.image(correct_flag, width=100)

    # Button to generate a new quiz round
    if st.button("🔄 New Question", key="new_q2"):
        correct_country, correct_flag, choices = get_quiz_data()
        st.session_state.quiz2 = {
            "correct_country": correct_country,
            "correct_flag": correct_flag,
            "choices": choices
        }
        st.session_state.selected_q2 = None  # Reset selection
        st.rerun()  # Force refresh



# ---- Wikipedia Country List ----
#with tab3:
#    st.subheader("Learn More About Countries")
#    lang = st.selectbox("Choose Language", ["en", "fr", "es", "it", "de", "nl"])
#    
#    country = st.selectbox("Select a country", countries)
#    wiki_url = f"https://{lang}.wikipedia.org/wiki/{country.replace(' ', '_')}"
#    st.components.v1.iframe(wiki_url, height=600)

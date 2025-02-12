import streamlit as st
import requests
import random

st.set_page_config(page_title="🌍 Country Quiz PWA", layout="wide")

@st.cache_data
def fetch_countries():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url).json()
    country_data = {}
    for country in response:
        name = country["name"]["common"]
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

tab1, tab2, tab3 = st.tabs(["🌎 Country → Flag", "🚩 Flag → Country", "📖 Wikipedia"])

# ---- Quiz 1: Country → Flag ----
with tab1:
    st.subheader("Which flag belongs to this country?")
    correct_country, correct_flag, choices = get_quiz_data()
    st.write(f"**Country:** {correct_country}")

    cols = st.columns(4)
    for i, choice in enumerate(choices):
        with cols[i]:
            st.image(country_flags[choice], width=100)
            if st.button(choice, key=f"q1_{choice}"):
                if choice == correct_country:
                    with st.expander("✅ Correct! 🎉"):
                        st.success(f"Good job! {correct_country} is the correct answer.")
                else:
                    with st.expander("❌ Wrong Answer!"):
                        st.error(f"Oops! The correct answer is **{correct_country}**.")
                        st.image(correct_flag, width=150)

# ---- Quiz 2: Flag → Country ----
with tab2:
    st.subheader("Which country does this flag belong to?")
    correct_country, correct_flag, choices = get_quiz_data()
    st.image(correct_flag, width=150)

    for choice in choices:
        if st.button(choice, key=f"q2_{choice}"):
            if choice == correct_country:
                with st.expander("✅ Correct! 🎉"):
                    st.success(f"Good job! {correct_country} is the correct answer.")
            else:
                with st.expander("❌ Wrong Answer!"):
                    st.error(f"Oops! The correct answer is **{correct_country}**.")
                    st.image(correct_flag, width=150)

# ---- Wikipedia Country List ----
with tab3:
    st.subheader("Learn More About Countries")
    lang = st.selectbox("Choose Language", ["en", "fr", "es", "it", "de", "nl"])
    
    country = st.selectbox("Select a country", countries)
    wiki_url = f"https://{lang}.wikipedia.org/wiki/{country.replace(' ', '_')}"
    st.components.v1.iframe(wiki_url, height=600)

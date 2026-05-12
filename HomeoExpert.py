import streamlit as st
import google.generativeai as genai

# Secrets থেকে API Key নেওয়া (সহজ উপায়)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "AIzaSyAV32pSAQ0TW7WCS73uBXZQTN1mNRtR3Xg" # ব্যাকআপ হিসেবে আপনার কি

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro')

st.title("🩺 Shanta Homeo Expert")

# সেশন স্টেট সেটআপ
if 'step' not in st.session_state:
    st.session_state.step = 1

# ধাপ ১: রোগীর নাম
if st.session_state.step == 1:
    name = st.text_input("রোগীর নাম লিখুন")
    if st.button("পরবর্তী ধাপ") and name:
        st.session_state.p_name = name
        st.session_state.step = 2
        st.rerun()

# ধাপ ২: লক্ষণ ও বিশ্লেষণ
elif st.session_state.step == 2:
    st.subheader(f"রোগী: {st.session_state.p_name}")
    problem = st.text_area("লক্ষণগুলো বিস্তারিত লিখুন")
    
    if st.button("বিশ্লেষণ করুন"):
        try:
            response = model.generate_content(f"Homeopathic analysis for: {problem}")
            st.write(response.text)
        except Exception as e:
            st.error(f"এপিআই এরর। কি-টি ঠিক আছে তো? {e}")

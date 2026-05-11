import streamlit as st
import random
import google.generativeai as genai

# ১. কনফিগারেশন এবং এপিআই সেটআপ (আপনার API Key এখানে দিন)
# নিরাপদ থাকার জন্য Streamlit Secrets ব্যবহার করা ভালো
API_KEY = "AIzaSyCiHlaNSDV88cTVEVNWDebtf92f74mNQbo" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Shanta Homeo Expert", layout="wide")

# ২. সেশন স্টেট ম্যানেজমেন্ট (তথ্য ধরে রাখার জন্য)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'patient_count' not in st.session_state:
    st.session_state.patient_count = 1

if 'patient_id' not in st.session_state:
    st.session_state.patient_id = f"SHM-{st.session_state.patient_count:02d}"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ৩. সাইডবার ডিজাইন
with st.sidebar:
    st.title("মেনু নির্বাচন করুন")
    st.radio("অপশন", ["নতুন রোগী", "পুরানো রোগী", "রোগীর লিস্ট"], key="menu_choice")
    st.write("---")
    st.info("Shanta Homeo & Modern Health Care v2.5")

st.title("⚕️ Shanta Homeo & Modern Health Care")
# ৪. মেনু অনুযায়ী ইন্টারফেস পরিবর্তন (লাইন ৩৯ এর পরে বসান)
if st.session_state.menu_choice == "পুরানো রোগী":
    st.header("🔍 পুরানো রোগীর তথ্য খুঁজুন")
    patient_search = st.text_input("রোগীর আইডি বা নাম দিয়ে সার্চ করুন")
    if st.button("সার্চ"):
        st.write("তথ্য খোঁজা হচ্ছে...")
    st.stop() # এটি দিলে নিচের নতুন রোগীর অংশটি আর দেখাবে না

elif st.session_state.menu_choice == "রোগীর লিস্ট":
    st.header("📋 নিবন্ধিত রোগীর তালিকা")
    # এখানে আপনার ডাটাবেস বা এক্সেল ফাইল থাকলে তা দেখাবে
    st.info("বর্তমানে কোনো তালিকা সংরক্ষিত নেই।")
    st.stop()

# ধাপ ১: রেজিস্ট্রেশন ও রিপোর্ট আপলোড
if st.session_state.step == 1:
    st.header("👤 নতুন রোগী নিবন্ধন")
    st.info(f"রোগীর ইউনিক আইডি: **{st.session_state.patient_id}**")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("রোগীর নাম")
    with col2:
        age = st.number_input("রোগীর বয়স", min_value=0, max_value=120)
    
    uploaded_file = st.file_uploader("মেডিকেল রিপোর্ট আপলোড করুন (ঐচ্ছিক)", type=['pdf', 'jpg', 'png', 'jpeg'])
    
    if st.button("পরবর্তী ধাপে যান ➡️"):
        if name:
            st.session_state.patient_name = name
            st.session_state.patient_age = age
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("দয়া করে নাম লিখুন।")

# ধাপ ২: প্রধান সমস্যা সংগ্রহ ও AI বিশ্লেষণ
elif st.session_state.step == 2:
    st.header(f"📋 প্রধান সমস্যা - {st.session_state.patient_name}")
    chief_complaint = st.text_area("রোগীর প্রধান সমস্যাগুলো বিস্তারিত লিখুন:")
    
    if st.button("লক্ষণ বিশ্লেষণ শুরু করুন ✨"):
        if chief_complaint:
            st.session_state.chief_complaint = chief_complaint
            # AI-এর জন্য প্রম্পট তৈরি
            prompt = f"একজন হোমিওপ্যাথিক ডাক্তার হিসেবে, রোগীর এই সমস্যাগুলো বিশ্লেষণ করো: '{chief_complaint}'। এই সমস্যার ভিত্তিতে রোগীকে জিজ্ঞেস করার জন্য ৩টি গুরুত্বপূর্ণ প্রশ্ন তৈরি করো এবং উত্তর দেওয়ার জন্য সম্ভাব্য অপশন দাও।"
            
            try:
                response = model.generate_content(prompt)
                st.session_state.ai_questions = response.text
                st.session_state.step = 3
                st.rerun()
            except Exception as e:
                st.error(f"API এরর: {e}")

# ধাপ ৩: AI ভিত্তিক প্রশ্নোত্তর ও চ্যাট বক্স
elif st.session_state.step == 3:
    st.header("🔍 বিস্তারিত লক্ষণ সংগ্রহ (AI Assistant)")
    st.write(st.session_state.ai_questions)
    
    st.write("---")
    st.subheader("💬 অতিরিক্ত তথ্য বা চ্যাট")
    user_input = st.text_input("এখানে রোগীর উত্তর বা বাড়তি লক্ষণগুলো লিখুন:")
    
    if st.button("প্রেসক্রিপশন জেনারেট করুন"):
        final_prompt = f"রোগীর নাম: {st.session_state.patient_name}, বয়স: {st.session_state.patient_age}, প্রধান সমস্যা: {st.session_state.chief_complaint}, অতিরিক্ত লক্ষণ: {user_input}। এই তথ্যের ভিত্তিতে একটি সম্ভাব্য হোমিওপ্যাথিক ঔষধের পরামর্শ এবং নির্দেশিকা দাও।"
        
        response = model.generate_content(final_prompt)
        st.subheader("💊 সম্ভাব্য পরামর্শ:")
        st.write(response.text)
        
        if st.button("নতুন রোগী শুরু করুন"):
            st.session_state.patient_count += 1
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


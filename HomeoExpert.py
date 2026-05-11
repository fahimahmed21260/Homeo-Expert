import streamlit as st
import google.generativeai as genai

# ১. এপিআই কনফিগারেশন
API_KEY = "AIzaSyAV32pSAQ0TW7WCS73uBXZQTN1mNRtR3Xg"
# আপনার এপিআই কি এখানে দিন
genai.configure(api_key=API_KEY)

# সঠিক মডেল ব্যবহার করুন
model = genai.GenerativeModel('gemini-1.5-flash')

# ২. সেশন স্টেট ম্যানেজমেন্ট
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = "SHM-01"

# ৩. সাইডবার ডিজাইন
with st.sidebar:
    st.title("🏥 Shanta Homeo Expert")
    menu = st.radio("মেনু নির্বাচন করুন", ["নতুন রোগী", "পুরানো রোগী", "রোগীর লিস্ট"], key="menu_choice")
    st.write("---")
    st.info("Shanta Homeo & Modern Health Care v2.5")

st.title("🩺 Shanta Homeo & Modern Health Care")

# ৪. মেনু লজিক (ইন্ডেন্টেশন ঠিক করা হয়েছে)
if st.session_state.menu_choice == "পুরানো রোগী":
    st.header("🔍 পুরানো রোগীর তথ্য")
    st.text_input("সার্চ করুন")

elif st.session_state.menu_choice == "রোগীর লিস্ট":
    st.header("📋 নিবন্ধিত তালিকা")
    st.info("তালিকা খালি।")

else:
    # নতুন রোগী - ধাপ ১
    if st.session_state.step == 1:
        st.header("👤 নতুন রোগী নিবন্ধন")
        name = st.text_input("রোগীর নাম")
        if st.button("পরবর্তী ধাপে যান"):
            if name:
                st.session_state.patient_name = name
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("দয়া করে নাম লিখুন")

    # নতুন রোগী - ধাপ ২
    elif st.session_state.step == 2:
        st.header(f"📝 সমস্যা সংগ্রহ - {st.session_state.patient_name}")
        complaint = st.text_area("রোগীর সমস্যা বিস্তারিত লিখুন")
        if st.button("বিশ্লেষণ শুরু করুন ✨"):
            if complaint:
                try:
                    # এপিআই কল
                    response = model.generate_content(f"বিশ্লেষণ করুন: {complaint}")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"API Error: {str(e)}")
            else:
                st.warning("সমস্যা লিখুন")

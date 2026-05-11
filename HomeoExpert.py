import streamlit as st
import google.generativeai as genai

# ১. সঠিক এপিআই কনফিগারেশন
API_KEY = "AIzaSyAV32pSAQ0TW7WCS73uBXzQTNlmNRtr3Xg" 
genai.configure(api_key=API_KEY)

# মডেল ডিক্লেয়ারেশন (সরাসরি ফ্ল্যাশ মডেল কল)
model = genai.GenerativeModel('gemini-1.5-flash')

# ২. সেশন স্টেট ম্যানেজমেন্ট
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
    st.title("🏥 Shanta Homeo Expert")
    menu = st.radio("মেনু নির্বাচন করুন", ["নতুন রোগী", "পুরানো রোগী", "রোগীর লিস্ট"], key="menu_choice")
    st.write("---")
    st.info("Shanta Homeo & Modern Health Care v2.5")

st.title("🩺 Shanta Homeo & Modern Health Care")

# ৪. মেনু অনুযায়ী লজিক বিভাজন
if st.session_state.menu_choice == "পুরানো রোগী":
    st.header("🔍 পুরানো রোগীর তথ্য খুঁজুন")
    patient_search = st.text_input("রোগীর আইডি বা নাম দিয়ে সার্চ করুন")
if st.button("সার্চ"):
        st.write("তথ্য খোঁজা হচ্ছে...")

elif st.session_state.menu_choice == "রোগীর লিস্ট":
    st.header("📋 নিবন্ধিত রোগীর তালিকা")
    st.info("বর্তমানে কোনো তালিকা সংরক্ষিত নেই।")

else:
    # ধাপ ১: রেজিস্ট্রেশন
if st.session_state.step == 1:
        st.header("👤 নতুন রোগী নিবন্ধন")
        st.info(f"রোগীর ইউনিক আইডি: **{st.session_state.patient_id}**")
        
        name = st.text_input("রোগীর নাম")
        age = st.number_input("রোগীর বয়স", min_value=0, max_value=120)
        uploaded_file = st.file_uploader("মেডিকেল রিপোর্ট আপলোড করুন", type=['pdf', 'jpg', 'png'])
        
if st.button("পরবর্তী ধাপে যান ➡️"):
if name:
    st.session_state.patient_name = name
    st.session_state.step = 2
    st.rerun()
else:
    st.error("দয়া করে নাম লিখুন।")

    # ধাপ ২: সমস্যা সংগ্রহ ও এআই বিশ্লেষণ
elif st.session_state.step == 2:
        st.header(f"📝 প্রধান সমস্যা - {st.session_state.patient_name}")
        chief_complaint = st.text_area("রোগীর প্রধান সমস্যাগুলো বিস্তারিত লিখুন:")
        
if st.button("লক্ষণ বিশ্লেষণ শুরু করুন ✨"):
if chief_complaint:
                try:
                    prompt = f"একজন হোমিওপ্যাথিক ডাক্তার হিসেবে, রোগীর এই সমস্যাগুলো বিশ্লেষণ করুন: {chief_complaint}"
                    response = model.generate_content(prompt)
                    st.session_state.ai_analysis = response.text
                    st.session_state.step = 3
                    st.rerun()
                except Exception as e:
                    st.error(f"API এরর: {str(e)}")
else:
    st.warning("দয়া করে সমস্যাগুলো লিখুন।")

    # ধাপ ৩: ফলাফল প্রদর্শন
elif st.session_state.step == 3:
    st.header("🔬 এআই বিশ্লেষণ ফলাফল")
    st.write(st.session_state.ai_analysis)
if st.button("নতুন রোগী শুরু করুন"):
    st.session_state.step = 1
    st.rerun()

import streamlit as st
import google.generativeai as genai
import pandas as pd
import datetime
import os
import uuid

# ১. API Key সেটআপ (আপনার কী এখানে বসান)
genai.configure(api_key="AIzaSyCiHlaNSDV88cTVEVNWDebtf92f74mNQbo")

# ২. পেজ কনফিগারেশন এবং স্টাইল
st.set_page_config(page_title="Homeo Expert", layout="wide")

# হোমিওপ্যাথি থিম বা ব্যাকগ্রাউন্ড স্টাইল
st.markdown('''
    <style>
    .stApp {
        background-color: #f1f8e9; /* Light Herbal Green */
    }
    .main-card {
        background-color: white;
        padding: 2rem;
        border-radius: 1rem;
        border-left: 5px solid #2e7d32;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    h1 { color: #1b5e20; }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
    }
    </style>
    ''', unsafe_allow_html=True)

# ৩. ডাটাবেজ ফাইল লোড করা (CSV ব্যবহার করে)
DB_FILE = "patient_records.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["ID", "Name", "Age", "Date", "History"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# ৪. ইন্টারফেস লজিক
st.title("🩺 Shanta Homeo & Modern Health Care")
st.write("---")

# সাইডবারে অপশন মেনু
menu = st.sidebar.radio("মেনু নির্বাচন করুন", ["নতুন রোগী", "ফলো-আপ রোগী", "রোগীর লিস্ট"])

df = load_data()

if menu == "নতুন রোগী":
    st.header("👤 নতুন রোগী নিবন্ধন")
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        name = st.text_input("রোগীর নাম")
        age = st.number_input("রোগীর বয়স", min_value=0, max_value=120)
        
        if st.button("নিবন্ধন করুন"):
            if name:
                new_id = f"SH-{str(uuid.uuid4())[:6].upper()}"
                new_patient = {
                    "ID": new_id,
                    "Name": name,
                    "Age": age,
                    "Date": str(datetime.date.today()),
                    "History": ""
                }
                df = pd.concat([df, pd.DataFrame([new_patient])], ignore_index=True)
                save_data(df)
                st.success(f"নিবন্ধন সফল! রোগীর আইডি: **{new_id}**")
                st.info("আইডিটি লিখে রাখুন অথবা লিস্টে চেক করুন।")
            else:
                st.error("দয়া করে নাম লিখুন।")
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "ফলো-আপ রোগী":
    st.header("🔄 ফলো-আপ রোগী অনুসন্ধান")
    search_query = st.text_input("রোগীর নাম অথবা আইডি দিয়ে সার্চ করুন")
    
    if search_query:
        # সার্চ লজিক
        results = df[(df['Name'].str.contains(search_query, case=False, na=False)) | (df['ID'].str.contains(search_query, case=False, na=False))]
        
        if not results.empty:
            for index, row in results.iterrows():
                with st.expander(f"{row['Name']} (ID: {row['ID']})"):
                    st.write(f"বয়স: {row['Age']}")
                    st.write(f"রেজিস্ট্রেশন তারিখ: {row['Date']}")
                    
                    # পুরাতন হিস্ট্রি দেখানো
                    history_text = row['History'] if not pd.isna(row['History']) and row['History'] else "কোনো হিস্ট্রি নেই।"
                    st.text_area("পুরাতন হিস্ট্রি", value=history_text, height=150, disabled=True)
                    
                    # নতুন লক্ষণ ইনপুট
                    user_msg = st.text_area(f"নতুন লক্ষণ লিখুন ({row['Name']})", key=f"input_{row['ID']}")
                    if st.button(f"এআই বিশ্লেষণ শুরু করুন", key=f"btn_{row['ID']}"):
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = f"Patient: {row['Name']}, Age: {row['Age']}. Symptoms: {user_msg}. Provide homeopathic remedies and reasoning."
                        response = model.generate_content(prompt)
                        st.markdown("### এআই পরামর্শ:")
                        st.write(response.text)
                        
                        # আপডেট হিস্ট্রি
                        current_history = str(row['History']) if not pd.isna(row['History']) else ""
                        df.at[index, 'History'] = current_history + f"\n[{datetime.date.today()}]: " + user_msg
                        save_data(df)
                        st.success("হিস্ট্রি আপডেট করা হয়েছে।")
        else:
            st.warning("এই নামে বা আইডি তে কোনো রোগী পাওয়া যায়নি।")

elif menu == "রোগীর লিস্ট":
    st.header("📋 নিবন্ধিত রোগীর তালিকা")
    if not df.empty:
        st.dataframe(df[["ID", "Name", "Age", "Date"]], use_container_width=True)
        # ডাটা ডাউনলোড করার অপশন
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Excel/CSV হিসেবে ডাউনলোড করুন", data=csv, file_name="patient_list.csv", mime="text/csv")
    else:
        st.info("এখনো কোনো রোগী নিবন্ধিত হয়নি।")
        # ফাইল আপলোড অপশন (অপশনাল)
uploaded_file = st.file_uploader("রোগীর কোনো পূর্ববর্তী রিপোর্ট থাকলে আপলোড করুন (ঐচ্ছিক)", type=['pdf', 'jpg', 'png'])

# রোগীর প্রধান সমস্যা জানার জন্য
chief_complaint = st.text_area("আপনার প্রধান সমস্যাগুলো বিস্তারিত লিখুন:")

if st.button("পরবর্তী ধাপে যান"):
    if chief_complaint:
        # এখানে Gemini API-কে কল করে লক্ষণভিত্তিক প্রশ্ন তৈরি করতে হবে
        # উদাহরণস্বরূপ একটি প্রশ্ন এবং অপশন:
        st.subheader("লক্ষণ সংক্রান্ত কিছু প্রশ্ন:")
        q1 = st.radio("আপনার ব্যথার ধরণ কেমন?", ["তীব্র", "ধীরে ধীরে বাড়ে", "মাঝে মাঝে হয়"])
        
        # চ্যাট করে উত্তর দেওয়ার জন্য অপশন
        additional_info = st.text_input("অন্য কোনো কিছু জানাতে চাইলে এখানে লিখুন:")
        # সেশন স্টেটে কাউন্টার রাখার জন্য
if 'patient_count' not in st.session_state:
    st.session_state.patient_count = 1

# আইডি তৈরির ফরম্যাট
unique_id = f"SHM-{st.session_state.patient_count:02d}"

st.sidebar.write("---")
st.sidebar.info("Shanta Homeo & Modern Health Care v2.0")

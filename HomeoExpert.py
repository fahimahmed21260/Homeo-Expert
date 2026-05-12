import streamlit as st
from openai import OpenAI

# ১. এপিআই কি সেটআপ
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🩺 Shanta Homeo AI Assistant")
st.write("রোগীর লক্ষণগুলো নিচে লিখুন:")

# ২. ইনপুট সেকশন
user_input = st.text_area("লক্ষণ (Symptoms):", placeholder="যেমন: রাতে বেশি কাশি, পানি পিপাসা কম...")

# ৩. এআই প্রম্পট ইঞ্জিনিয়ারিং
if st.button("বিশ্লেষণ করুন"):
    if user_input:
        try:
            # এখানে সিস্টেম মেসেজে আপনি বটকে 'হোমিওপ্যাথিক বিশেষজ্ঞ' হিসেবে সেট করছেন
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # অথবা gpt-4
                messages=[
                    {"role": "system", "content": "তুমি একজন অভিজ্ঞ হোমিওপ্যাথিক ডাক্তার। রোগীর লক্ষণ অনুযায়ী সঠিক রেমেডি এবং পরামর্শ দাও।"},
                    {"role": "user", "content": user_input}
                ]
            )
            
            # ফলাফল প্রদর্শন
            st.success("এআই বিশ্লেষণ:")
            st.write(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("দয়া করে কিছু লক্ষণ লিখুন।")

import streamlit as st
import streamlit.components as stc

import pandas as pd
import neattext.functions as nfx

import base64
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

def make_downloadable(data,task_type):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download Results File ** ")
    new_filename = "extracted_{}_result_{}.csv".format(task_type,timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)

def make_downloadable_df(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download CSV File ** ")
    new_filename = "extracted_data_result_{}.csv".format(timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)

def main():
    menu = ["Home", "Single Extractor", "Bulk Extractor", "DataStorage", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Search & Extractor")
    elif choice == "Single Extractor":
        st.subheader("Extract A Single Term")
        text = st.text_area("Paste Text Here")
        task_option = st.sidebar.selectbox("Task", ["Emails", "URLS", "Phonenumbers"])
        if st.button("Extract"):      
            if task_option == "URLS":
                results = nfx.extract_urls(text)
            elif task_option == "Phonenumbers":
                results = nfx.extract_phone_numbers(text)
            else:
                results = nfx.extract_emails(text)
            st.write(results)
            with st.expander("Result As DataFrame"):
                result_df = pd.DataFrame({'Results': results})
                st.dataframe(result_df)
                make_downloadable(result_df, task_option)

    elif choice == "Bulk Extractor":
        st.subheader("Bulk Extractor")
        text = st.text_area("Paste Text Here")
        task_list = ["Emails", "URLS", "Phonenumbers"]
        task_option = st.sidebar.multiselect('Task', task_list, default="Emails")
        task_mapper = {
            "Emails": nfx.extract_emails(text),
            "URLS" : nfx.extract_urls(text),
            "Phonenumbers" : nfx.extract_phone_numbers(text)
        }
        all_results = []
        for task in task_option:
            result = task_mapper[task]
            all_results.append(result)
        st.write(all_results)

        with st.expander("Results As DataFrame"):
            result_df = pd.DataFrame(all_results).T
            result_df.columns = task_option
            st.dataframe(result_df)
    else:
        st.subheader("About")



if __name__ == '__main__':
    main()
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

def run_analysis(search_word):
    past_df = pd.read_excel('past.xlsx')
    present_df = pd.read_excel('present.xlsx')
    filter_condition_past = (past_df['author 1'] == search_word) | past_df.filter(like='category ').apply(lambda col: col == search_word).any(axis=1)

    filtered_past_df = past_df[filter_condition_past]
    addresses_to_search = filtered_past_df['Address'].tolist()
    present_filter_condition = present_df['Address'].isin(addresses_to_search)
    filtered_present_df = present_df[present_filter_condition]

    result_df = pd.merge(filtered_past_df[['Address', 'Clicks', 'Impressions']],
                         filtered_present_df[['Address', 'Clicks', 'Impressions']],
                         on='Address', suffixes=('_Past', '_Present'))

    result_df['Clicks_Difference'] = result_df['Clicks_Present'] - result_df['Clicks_Past']
    result_df['Impressions_Difference'] = result_df['Impressions_Present'] - result_df['Impressions_Past']

    return result_df


st.header(":chart_with_upwards_trend: Analyzing Category and Author Clicks and Impression")
# Input the word you want to search for using Streamlit
search_word = st.text_input("Enter a category or author name:", "category or author name")  # Set default input as "category name"

if st.button("Run"):
    result_df = run_analysis(search_word)

    # Display the result DataFrame using Streamlit
    st.subheader("DataFrame")
    st.dataframe(result_df)

    # Clicks Section
    st.subheader("Clicks Analysis")
    fig_clicks, ax_clicks = plt.subplots(figsize=(10, 6))
    ax_clicks.plot(result_df['Address'], result_df['Clicks_Past'], label='Past Clicks')
    ax_clicks.plot(result_df['Address'], result_df['Clicks_Present'], label='Present Clicks')
    ax_clicks.set_yscale('log')  # Set y-axis to logarithmic scale
    ax_clicks.set_xlabel('Address')
    ax_clicks.set_ylabel('Clicks')
    ax_clicks.legend()
    st.pyplot(fig_clicks)

    # Impressions Section
    st.subheader("Impressions Analysis")
    fig_impressions, ax_impressions = plt.subplots(figsize=(10, 6))
    ax_impressions.plot(result_df['Address'], result_df['Impressions_Past'], label='Past Impressions')
    ax_impressions.plot(result_df['Address'], result_df['Impressions_Present'], label='Present Impressions')
    ax_impressions.set_yscale('log')  # Set y-axis to logarithmic scale
    ax_impressions.set_xlabel('Address')
    ax_impressions.set_ylabel('Impressions')
    ax_impressions.legend()
    st.pyplot(fig_impressions)

    st.subheader("Download DataFrame as Excel")
    excel_buffer = BytesIO()
    result_df.to_excel(excel_buffer, index=False, encoding='utf-8-sig')
    excel_buffer.seek(0)
    st.download_button(label="Download Excel", data=excel_buffer, file_name=f'{search_word}.xlsx', key='download_excel')

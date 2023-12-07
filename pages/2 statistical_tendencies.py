import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import function as func
import re


st.title("Statistical Tendencies")

x_option = st.selectbox("Select Features", ["Salary vs years of programming",
                                            "Company Size vs Average Compensation",
                                            "ML Spent vs Current Role"])
filter_option = st.multiselect("Select Filters", ["Country", "Gender"])
gender = ''
combined_df = pd.DataFrame()
# add filter_dict
filter_dict = {'Country': '', 'Gender': ''}
years = st.slider('Select a range of years', 2020, 2022, (2020, 2022))
if 'Country' in filter_option:
    country = st.text_input("Type in the country you want to inspect", key="name")
    filter_dict['Country'] = country
if 'Gender' in filter_option:
    gender = st.selectbox("Select the gender of the participants", ['Woman', 'Man'])
    filter_dict['Gender'] = gender

if x_option == "Salary vs years of programming":
    salaries = func.total_compensation(filter_dict)
    salaries = func.selected_years(salaries, years)
    if salaries.empty:
        st.write('Input is not valid')
    else:
        func.compensation_visualization(salaries)
    years_of_programming = func.total_programming_years(filter_dict)
    years_of_programming = func.selected_years(years_of_programming, years)
    if years_of_programming.empty:
        st.write('Input is not valid')
    else:
        func.programming_years_visualization(years_of_programming)
        final_df = func.compensation_vs_programming_years_visualization(filter_dict, years)
        # st.write(final_df)

if x_option == "ML Spent vs Current Role":
    final_df = func.ml_spent_vs_current_role_visualization(filter_dict, years)
    # st.write(final_df)

if x_option == 'Company Size vs Average Compensation':

    dataf = func.compensation_vs_company_size_visualization(filter_dict, years)
    # st.write(dataf)


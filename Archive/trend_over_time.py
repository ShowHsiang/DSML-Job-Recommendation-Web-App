import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import function as func
import re


def app():
    st.title("Trend Over Time")

    x_option = st.selectbox("Select Features",
                            ["languages used on a regular basis",
                             "Course Platform chosen",
                             "years of programming",
                             "Company size"])
    filter_option = st.multiselect("Select Filters", ["Country", "Gender"])
    gender = ''
    combined_df = pd.DataFrame()
    # add filter_dict
    filter_dict = {'Country': '', 'Gender': ''}

    if 'Country' in filter_option:
        country = st.text_input("Type in the country you want to inspect", key="name")
        filter_dict['Country'] = country
    if 'Gender' in filter_option:
        gender = st.selectbox("Select the gender of the participants", ['Woman', 'Man'])
        filter_dict['Gender'] = gender

    if x_option == "languages used on a regular basis":

        for year in range(2020, 2023):
            data = func.load_data(year)

            if year in [2020, 2021]:
                languages = data[
                    ['Q2', 'Q3', 'Q7_Part_1', 'Q7_Part_2', 'Q7_Part_3', 'Q7_Part_4', 'Q7_Part_5', 'Q7_Part_6',
                     'Q7_Part_7', 'Q7_Part_8', 'Q7_Part_10', 'Q7_Part_11']]
                languages.columns = ['Gender', 'Country', 'Python', 'R', 'SQL', 'C', 'C++', 'Java', 'Javascript',
                                     'Julia', 'Bash', 'MATLAB']
                languages['year'] = year
                languages = func.filter_operation(languages, filter_option, gender)
                combined_df = pd.concat([combined_df, languages], ignore_index=True)

            elif year == 2022:
                languages = data[['Q3', 'Q4', 'Q12_1', 'Q12_2', 'Q12_3', 'Q12_4', 'Q12_6',
                                  'Q12_7', 'Q12_8', 'Q12_12', 'Q12_9', 'Q12_11']]
                languages.columns = ['Gender', 'Country', 'Python', 'R', 'SQL', 'C', 'C++', 'Java', 'Javascript',
                                     'Julia', 'Bash', 'MATLAB']
                languages['year'] = year
                languages = func.filter_operation(languages, filter_option, gender)
                combined_df = pd.concat([combined_df, languages], ignore_index=True)

        func.visualization(combined_df, 'Programming Language')

    if x_option == 'Course Platform chosen':

        for year in range(2020, 2023):
            data = func.load_data(year)
            columns = ['Gender', 'Country', 'Coursera', 'edX', 'Kaggle Learn Courses',
                       'DataCamp', 'Fast.ai', 'Udacity', 'Udemy', 'LinkedIn Learning',
                       'Cloud programs', 'University Courses']
            if year == 2020:
                platform = data[['Q2', 'Q3', 'Q37_Part_1', 'Q37_Part_2', 'Q37_Part_3', 'Q37_Part_4', 'Q37_Part_5',
                                 'Q37_Part_6', 'Q37_Part_7', 'Q37_Part_8', 'Q37_Part_9', 'Q37_Part_10']]
                platform.columns = columns
                platform['year'] = year
                platform = func.filter_operation(platform, filter_option, gender)
                combined_df = pd.concat([combined_df, platform], ignore_index=True)

            elif year == 2021:
                platform = data[['Q2', 'Q3', 'Q40_Part_1', 'Q40_Part_2', 'Q40_Part_3', 'Q40_Part_4', 'Q40_Part_5',
                                 'Q40_Part_6', 'Q40_Part_7', 'Q40_Part_8', 'Q40_Part_9', 'Q40_Part_10']]
                platform.columns = columns
                platform['year'] = year
                platform = func.filter_operation(platform, filter_option, gender)
                combined_df = pd.concat([combined_df, platform], ignore_index=True)

            elif year == 2022:
                platform = data[
                    ['Q3', 'Q4', 'Q6_1', 'Q6_2', 'Q6_3', 'Q6_4', 'Q6_5', 'Q6_6', 'Q6_7', 'Q6_8', 'Q6_8', 'Q6_10']]
                platform.columns = columns
                platform['year'] = year
                platform = func.filter_operation(platform, filter_option, gender)
                combined_df = pd.concat([combined_df, platform], ignore_index=True)

        func.visualization(combined_df, 'Course Platform')

    if x_option == 'Company size':

        for year in range(2020, 2023):
            data = func.load_data(year)
            columns = ['Gender', 'Country', 'companysize']
            if year == 2020:
                cy = data[['Q2', 'Q3', 'Q20']]
                cy.columns = columns
                cy['year'] = year
                cy = func.filter_operation(cy, filter_option, gender)
                combined_df = pd.concat([combined_df, cy], ignore_index=True)

            elif year == 2021:
                cy = data[['Q2', 'Q3', 'Q21']]
                cy.columns = columns
                cy['year'] = year
                cy = func.filter_operation(cy, filter_option, gender)
                combined_df = pd.concat([combined_df, cy], ignore_index=True)

            elif year == 2022:
                cy = data[
                    ['Q3', 'Q4', 'Q25']]
                cy.columns = columns
                cy['year'] = year
                cy = func.filter_operation(cy, filter_option, gender)
                combined_df = pd.concat([combined_df, cy], ignore_index=True)
        combined_df.dropna(subset=['companysize'], inplace=True)
        combined_df['companysize'] = pd.Categorical(combined_df['companysize'],
                                                    categories=combined_df['companysize'].unique())
        combined_df.sort_values(by=['companysize'], inplace=True)
        year_2020 = combined_df[combined_df['year'] == 2020]['companysize'].value_counts()
        year_2021 = combined_df[combined_df['year'] == 2021]['companysize'].value_counts()
        year_2022 = combined_df[combined_df['year'] == 2022]['companysize'].value_counts()

        fig, axes = plt.subplots(1, 3, figsize=(16, 8))

        sns.set(style="whitegrid")
        custom_colors = {
            '0-49 employees': 'lightblue',
            '10,000 or more employees': 'lightgreen',
            '1000-9,999 employees': 'lightcoral',
            '50-249 employees': 'lightsalmon',
            '250-999 employees': 'lightseagreen',
        }

        axes[0].pie(year_2020, labels=year_2020.index, autopct='%1.1f%%', startangle=90,
                    colors=[custom_colors[label] for label in year_2020.index])
        axes[0].set_title('year = 2020', fontweight='bold')

        axes[1].pie(year_2021, labels=year_2021.index, autopct='%1.1f%%', startangle=90,
                    colors=[custom_colors[label] for label in year_2021.index])
        axes[1].set_title('year = 2021', fontweight='bold')

        axes[2].pie(year_2022, labels=year_2022.index, autopct='%1.1f%%', startangle=90,
                    colors=[custom_colors[label] for label in year_2022.index])
        axes[2].set_title('year = 2022', fontweight='bold')

        plt.tight_layout()

        st.pyplot(fig)

    if x_option == "years of programming":
        years_of_programming = func.total_programming_years(filter_dict)
        # years_of_programming.style.background_gradient(axis=0, cmap='Blues')
        if years_of_programming.empty:
            st.write('Input is not valid')
        else:
            func.bar_plot(years_of_programming)

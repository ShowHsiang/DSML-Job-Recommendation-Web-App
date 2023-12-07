import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


@st.cache_data
def load_data(year):
    data = pd.read_csv(f'kaggle_survey_{year}_responses.csv')
    data.drop(0, inplace=True)
    return data


def filter_operation(data, option, gender):
    data['Country'] = data['Country'].replace('United States of America', 'US')
    if 'Country' in option:
        data = data[data['Country'] == st.session_state.name]
    if 'Gender' in option:
        data = data[data['Gender'] == gender]
    data.drop('Country', axis=1, inplace=True)
    data.drop('Gender', axis=1, inplace=True)
    return data


def visualization(data, text):
    fig, ax = plt.subplots(figsize=(16, 7))
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    bar_data = data.groupby('year').count().T
    styled_bar_data = bar_data.style.background_gradient(axis=0, cmap='Blues')
    st.write(styled_bar_data)
    bar_data_percent = bar_data.apply(lambda row: row / row.sum(), axis=0)
    try:
        bar_data_percent.plot(kind='bar', ax=ax)
        plt.title('Percentage of ' + text + ' Used Among Respondents Over the Years')
        plt.xlabel('Year')
        plt.ylabel('Percentage')
        plt.xticks(rotation=0)
        st.pyplot(fig)
    except IndexError and TypeError:
        st.write('No such country exist')


def extract_and_calculate_middle(s):
    numbers = re.findall(r'\d+', s)
    if len(numbers) == 2:

        start = int(numbers[0])
        end = int(numbers[1])
        middle = (start + end) // 2
        return middle
    elif len(numbers) == 1:

        return int(numbers[0])
    else:

        return None


# define read file function
@st.cache_data
def read_file(year):
    gender_dict = {2020: 'Q2', 2021: 'Q2', 2022: 'Q3'}
    country_dict = {2020: 'Q3', 2021: 'Q3', 2022: 'Q4'}
    data = pd.read_csv(f'kaggle_survey_{year}_responses.csv')
    data.drop(0, inplace=True)
    data.rename(columns={gender_dict[year]: 'Gender', country_dict[year]: 'Country'}, inplace=True)
    return data


# define a filter function
def filters(data, filter_dict):
    if filter_dict['Country'] != '':
        data = data[data['Country'] == filter_dict['Country']]
    if filter_dict['Gender'] != '':
        data = data[data['Gender'] == filter_dict['Gender']]
    return data


# Function to convert the range to the average value
def convert_range_to_average(compensation_range):
    if "-" in compensation_range:
        start, end = map(int, compensation_range.replace(",", "").replace("$", "").replace(">", "").split("-"))
        return round((start + end + 1) / 2)
    else:
        return 0


# define a function to select yearly compensation from dataframe
def yearly_compensation(year, filter_dict):
    question_dict = {2020: 'Q24',
                     2021: 'Q25',
                     2022: 'Q29'}
    data = read_file(year)
    data = filters(data, filter_dict)
    compensation = data[question_dict[year]].value_counts().reset_index().rename(
        columns={'index': 'Yearly Compensation', question_dict[year]: year})
    compensation.fillna(0, inplace=True)
    return compensation


# define a function to select total compensation from dataframe
def total_compensation(filter_dict):
    compensation_2020 = yearly_compensation(2020, filter_dict)
    compensation_2021 = yearly_compensation(2021, filter_dict)
    compensation_2022 = yearly_compensation(2022, filter_dict)
    compensation = compensation_2020.merge(compensation_2021, how='outer', on='Yearly Compensation')
    compensation = compensation.merge(compensation_2022, how='outer', on='Yearly Compensation')
    compensation.dropna(inplace=True)
    compensation['Average Compensation'] = compensation.apply(
        lambda row: convert_range_to_average(row['Yearly Compensation']), axis=1)

    compensation.sort_values(by='Average Compensation', inplace=True)
    return compensation


def yearly_programming_years(year, filter_dict):
    question_dict = {2020: 'Q6',
                     2021: 'Q6',
                     2022: 'Q11'}
    data = read_file(year)
    data = filters(data, filter_dict)
    programming_years = data[question_dict[year]].value_counts().reset_index().rename(
        columns={'index': 'Programming Years', question_dict[year]: year})
    if year == 2020:
        programming_years.replace('1-2 years', '1-3 years', inplace=True)
    programming_years.replace('NaN', 'never', inplace=True)
    programming_years.replace('I have never written code', 'never', inplace=True)
    return programming_years


# define a function to select total programming years
def total_programming_years(filter_dict):
    programming_years_2020 = yearly_programming_years(2020, filter_dict)
    programming_years_2021 = yearly_programming_years(2021, filter_dict)
    programming_years_2022 = yearly_programming_years(2022, filter_dict)
    programming_years = programming_years_2020.merge(programming_years_2021, how='outer', left_on='Programming Years',
                                                     right_on='Programming Years')
    programming_years = programming_years.merge(programming_years_2022, how='outer', left_on='Programming Years',
                                                right_on='Programming Years')
    programming_years.fillna(0, inplace=True)
    # Map the strings to a custom order
    order_mapping = {
        'never': 0,
        '< 1 years': 1,
        '1-2 years': 2,
        '3-5 years': 3,
        '5-10 years': 4,
        '10-20 years': 5,
        '20+ years': 6,
    }

    # Assuming df is your DataFrame and 'Programming Years' is the column you want to sort
    programming_years['sort_order'] = programming_years['Programming Years'].map(order_mapping)
    programming_years.sort_values(by='sort_order', inplace=True)
    programming_years.drop('sort_order', axis=1, inplace=True)  # Drop the sort_order column after sorting

    return programming_years


# define selected years of features
def selected_years(features, years):
    features['Total'] = 0
    for year in range(years[0], years[1] + 1):
        features['Total'] += features[year]

    for year in range(2020, 2023):
        features.drop(year, axis=1, inplace=True)
    return features


# define visualization
# define barplot function
def bar_plot(years_of_programming):
    styled_data = years_of_programming.style.background_gradient(axis=0, cmap='Blues')
    st.write(styled_data)

    # use seaborn to create a barplot
    years_of_programming = years_of_programming.melt(id_vars='Programming Years', var_name='Year', value_name='Count')
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    sns.barplot(x='Programming Years', y='Count', hue='Year', data=years_of_programming, palette='viridis')

    plt.legend(title='Year')
    plt.title('Programming Years')

    st.pyplot(plt)


# define visualization for compensation
def compensation_visualization(compensation):
    compensation['Total'] = (compensation['Total'] / compensation['Total'].sum()) * 100
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.set_palette("husl")

    ax = sns.barplot(x='Average Compensation', y='Total', data=compensation, palette='viridis')
    plt.ylabel('Percentage of Participants (%)')
    plt.xticks(rotation=45)
    plt.title('Percentage of Participants for each Compensation Category')

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=11, color='black', xytext=(0, 10),
                    textcoords='offset points')

    st.pyplot(plt)


# define visualization for years of programming
def programming_years_visualization(programming_years):
    # Map the strings to a custom order
    order_mapping = {
        'never': 0,
        '< 1 years': 1,
        '1-3 years': 2,
        '3-5 years': 3,
        '5-10 years': 4,
        '10-20 years': 5,
        '20+ years': 6,
    }
    programming_years['sort_order'] = programming_years['Programming Years'].map(order_mapping)
    programming_years.sort_values(by='sort_order', inplace=True)
    programming_years.drop('sort_order', axis=1, inplace=True)
    # percentile
    programming_years['Total'] = (programming_years['Total'] / programming_years['Total'].sum()) * 100
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    ax = sns.barplot(x='Programming Years', y='Total', data=programming_years, palette='viridis')
    plt.ylabel('Percentage of Participants (%)')
    plt.xticks(rotation=45)
    plt.title('Percentage of Participants for each Programming Years')
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=11, color='black', xytext=(0, 10),
                    textcoords='offset points')
    st.pyplot(plt)


# define compensation vs programming years visualization
def compensation_vs_programming_years_visualization(filter_dict, years):
    # empty df
    final_df = pd.DataFrame(columns=['Programming Years', 'Average Compensation'])

    for year in range(years[0], years[1] + 1):
        # load and filtered
        data = read_file(year)
        data = filters(data, filter_dict)

        # define column
        programming_years_column = 'Q6' if year != 2022 else 'Q11'
        compensation_column = 'Q24' if year == 2020 else 'Q25' if year == 2021 else 'Q29'

        # extract the data
        temp_df = data[[programming_years_column, compensation_column]].copy()
        temp_df.columns = ['Programming Years', 'Average Compensation']
        if year == 2020:
            temp_df.replace('1-2 years', '1-3 years', inplace=True)
        # merge
        final_df = pd.concat([final_df, temp_df], ignore_index=True)

    # get midpoint
    final_df['Average Compensation'] = final_df['Average Compensation'].apply(
        lambda x: x if isinstance(x, (int, float)) else convert_range_to_average(x))

    # drop nan
    final_df.dropna(subset=['Programming Years', 'Average Compensation'], inplace=True)
    final_df.replace('NaN', 'never', inplace=True)
    final_df.replace('I have never written code', 'never', inplace=True)
    # Map the strings to a custom order
    order_mapping = {
        'never': 0,
        '< 1 years': 1,
        '1-3 years': 2,
        '3-5 years': 3,
        '5-10 years': 4,
        '10-20 years': 5,
        '20+ years': 6,
    }
    final_df['sort_order'] = final_df['Programming Years'].map(order_mapping)
    final_df.sort_values(by='sort_order', inplace=True)
    final_df.drop('sort_order', axis=1, inplace=True)

    # plotting
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Programming Years', y='Average Compensation', data=final_df, palette='viridis')
    plt.title('Programming Years vs Average Compensation')
    plt.xlabel('Programming Years')
    plt.ylim(0, 300000)
    plt.ylabel('Average Compensation')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    return final_df


# define compensation vs company size visualization
def compensation_vs_company_size_visualization(filter_dict, years):
    final_df = pd.DataFrame(columns=['Company Size', 'Average Compensation'])

    for year in range(years[0], years[1] + 1):
        data = read_file(year)
        data = filters(data, filter_dict)

        company_size_column = 'Q20' if year == 2020 else 'Q21' if year == 2021 else 'Q25'
        compensation_column = 'Q24' if year == 2020 else 'Q25' if year == 2021 else 'Q29'

        temp_df = data[[company_size_column, compensation_column]].copy()
        temp_df.columns = ['Company Size', 'Average Compensation']

        # convert function
        temp_df['Company Size'] = temp_df['Company Size'].astype(str)
        temp_df['Average Compensation'] = temp_df['Average Compensation'].apply(
            lambda x: x if isinstance(x, (int, float)) else convert_range_to_average(x)
        )
        temp_df = temp_df[temp_df['Average Compensation'] > 2500]
        # merge DataFrame
        final_df = pd.concat([final_df, temp_df], ignore_index=True)

    # cleaning
    final_df.dropna(subset=['Company Size', 'Average Compensation'], inplace=True)

    # Map the strings to a custom order
    order_mapping = {
        '0-49 employees': 0,
        '50-249 employees': 1,
        '250-999 employees': 2,
        '1000-9,999 employees': 3,
        '10,000 or more employees': 4,
    }
    heatmap_data = final_df.pivot_table(index='Average Compensation', columns='Company Size',
                                        aggfunc=len, fill_value=0)
    heatmap_data.sort_index(inplace=True)
    heatmap_data.columns = pd.Categorical(heatmap_data.columns, categories=order_mapping.keys(), ordered=True)
    heatmap_data = heatmap_data.sort_index(axis=1)

    # plotting
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='viridis_r', annot=True, fmt='d')
    plt.title('Heatmap of Company Size vs Average Compensation')
    plt.xlabel('Company Size')
    plt.ylabel('Average Compensation')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    return final_df


# define ML spent vs ML usage
def ml_spent_vs_current_role_visualization(filter_dict, years):
    def convert_ml_spent_to_average(ml_spent):
        if ml_spent == '$0 ($USD)':
            return 0
        elif ml_spent == '$1-$99':
            return (1 + 99) / 2
        elif ml_spent == '$100-$999':
            return (100 + 999) / 2
        elif ml_spent == '$1000-$9,999':
            return (1000 + 9999) / 2
        elif ml_spent == '$10,000-$99,999':
            return (10000 + 99999) / 2
        elif ml_spent == '$100,000 or more ($USD)':
            return 100000
        else:
            return None

    final_df = pd.DataFrame(columns=['Current Role', 'ML Spent'])
    for year in range(years[0], years[1] + 1):
        data = read_file(year)
        data = filters(data, filter_dict)

        current_role_column = 'Q5' if year != 2022 else 'Q23'
        ml_spent_column = 'Q25' if year == 2020 else 'Q26' if year == 2021 else 'Q30'

        temp_df = data[[current_role_column, ml_spent_column]].copy()
        temp_df.columns = ['Current Role', 'ML Spent']

        # convert function
        temp_df['ML Spent'] = temp_df['ML Spent'].apply(convert_ml_spent_to_average)

        # merge DataFrame
        final_df = pd.concat([final_df, temp_df], ignore_index=True)
        final_df.replace('I do not use machine learning methods', 'never', inplace=True)
        final_df = final_df[final_df['ML Spent'] > 0]
    # cleaning
    role_selection = {'Data Engineer',
                      'Data Scientist',
                      'Research Scientist',
                      'Software Engineer',
                      'Statistician'}
    final_df = final_df[final_df['Current Role'].isin(role_selection)]
    final_df.dropna(subset=['Current Role', 'ML Spent'], inplace=True)
    final_df.sort_values(by='ML Spent', inplace=True, ascending=False)
    # plotting heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(final_df.pivot_table(index='ML Spent', columns='Current Role', aggfunc=len, fill_value=0, sort=False),
                cmap='viridis_r', annot=True, fmt='d')
    plt.title('Heatmap of ML Spent vs Current Role')
    plt.ylabel('ML Spent')
    plt.xlabel('Current Role')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    return final_df

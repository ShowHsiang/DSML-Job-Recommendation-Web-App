import streamlit as st
import pandas as pd
import pickle

# Load the trained model from the file
with open('gbm_model.pkl', 'rb') as model_file:
    gbm_model = pickle.load(model_file)

# design
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)

# Title of the app
st.title('Job Role Recommendation App')
st.write("Fill out the information below to get job role recommendations tailored to your skills and experience.")

dict_age = [32, 37, 52, 27, 23, 19, 42, 57, 47, 70, 64]
dict_years_of_programming = [7, 1, 20, 15, 4, 2]
dict_years_of_ml = [3, 2, 1, 7, 4, 20, 15]
dict_company_size = [624, 5499, 149, 24, 10000]
dict_yearly_compensation = [137500, 75000, 500, 175000, 65000, 12500, 17500,
                            4500, 500000, 27500, 85000, 45000, 8750, 112500,
                            275000, 55000, 35000, 2500, 6250, 22500, 225000,
                            400000, 1500, 95000, 3500, 750000, 1000000]

categorical_features = ['Education', 'Language', 'IDE', 'Course_platform', 'ML_algorithm', 'Related_activities']
numerical_features = ['Age', 'Years_of_programming', 'Years_of_machine_learning', 'Company_size', 'Yearly_compensation']
reverse_label_mapping = {0: 'Data Scientist',
                         1: 'Data Analyst',
                         2: 'Machine Learning Engineer',
                         3: 'Research Scientist',
                         4: 'Software Engineer'}
job_info = {
    'Data Scientist': 'Data Scientists interpret and manage data to help companies make better business decisions. '
                      'They design data modeling processes, create algorithms and predictive models, and perform '
                      'custom analysis. Key skills include knowledge of Python, R, SQL, machine learning, '
                      'and data visualization tools.',
    'Data Analyst': 'Data Analysts collect, process, and perform statistical analyses on large datasets. They '
                    'discover how data can be used to answer questions and solve problems. They often report findings '
                    'using data visualization and may require proficiency in tools such as Excel, Tableau, or SQL.',
    'Machine Learning Engineer': 'Machine Learning Engineers create data funnels and deliver software solutions. They '
                                 'are responsible for building and deploying machine learning projects. They '
                                 'typically require a strong background in computer science and statistics, '
                                 'and familiarity with machine learning frameworks like TensorFlow or PyTorch.',
    'Research Scientist': 'Research Scientists are experts who use a variety of techniques to conduct and analyze '
                          'research. They publish findings in reports and papers. They work in diverse fields such as '
                          'biology, physics, and social science, requiring expertise in the scientific method and '
                          'data analysis.',
    'Software Engineer': 'Software Engineers apply engineering principles to build software and systems to solve '
                         'problems. They use programming languages to write, test, and deploy code. Software '
                         'Engineers must have a strong understanding of computer science principles, '
                         'software development methodologies, and experience with coding languages like Java, C++, '
                         'or Python.',
    'Statistician': 'Statisticians apply mathematical and statistical techniques to help solve real-world problems in '
                    'business, engineering, healthcare, or other fields. They are skilled in statistical testing and '
                    'modeling, and often use tools like R or SAS. They are experts in making inferences from data and '
                    'providing actionable insights.'
}

input_features = {feature: 0 for feature in ['Age', 'Years_of_programming', 'Years_of_machine_learning',
                                             'Company_size', 'Yearly_compensation', 'Bachelor’s degree',
                                             'Doctoral degree', 'Master’s degree',
                                             'No formal education past high school', 'Professional degree',
                                             'Professional doctorate',
                                             'Some college/university study without earning a bachelor’s degree',
                                             'Bash', 'C', 'C#', 'C++', 'Go', 'Java', 'Javascript', 'Julia', 'MATLAB',
                                             'None', 'PHP', 'Python', 'R', 'SQL', 'Swift', 'IntelliJ', 'Jupyter',
                                             'Notepad++', 'PyCharm', 'RStudio', 'Spyder', 'Sublime Text',
                                             'Vim / Emacs', 'Visual Studio', 'Visual Studio Code',
                                             'Cloud-certification programs', 'Coursera', 'DataCamp', 'Fast.ai',
                                             'Kaggle Learn Courses', 'LinkedIn Learning', 'Udacity', 'Udemy',
                                             'University Courses', 'edX', 'Autoencoder Networks',
                                             'Bayesian Approaches', 'Convolutional Neural Networks',
                                             'Decision Trees or Random Forests', 'Dense Neural Networks',
                                             'Evolutionary Approaches', 'Generative Adversarial Networks',
                                             'Gradient Boosting Machines', 'Graph Neural Networks',
                                             'Linear or Logistic Regression', 'Recurrent Neural Networks',
                                             'Transformer Networks',
                                             'Analyze and understand data to influence product or business decisions',
                                             'Build and/or run a machine learning service that operationally improves '
                                             'my product or workflows',
                                             'Build and/or run the data infrastructure that my business uses for '
                                             'storing',
                                             'Build prototypes to explore applying machine learning to new areas',
                                             'Do research that advances the state of the art of machine learning',
                                             'Experimentation and iteration to improve existing ML models',
                                             'None of these activities are an important part of my role at work']}


# Function to find the nearest value
def find_nearest(value, options):
    return min(options, key=lambda x: abs(x - value))


# function to Normalize numerical features
def scale_input(input_value, min_value, max_value):
    return (input_value - min_value) / (max_value - min_value)


def find_min_max_values(dict_values, user_input):
    # Find the corresponding list of values
    value_list = dict_values.get(user_input, None)

    if value_list:
        # Find the min and max values in the list
        min_value = min(value_list)
        max_value = max(value_list)
        return min_value, max_value
    else:
        return None, None


education = st.selectbox('Highest Education Level', [
    'No formal education past high school',
    'Some college/university study without earning a bachelor’s degree',
    'Bachelor’s degree', 'Master’s degree', 'Doctoral degree',
    'Professional degree', 'Professional doctorate'
])
# Layout design
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input('Age', min_value=18, max_value=100, step=1, format='%d')
    course_platform = st.multiselect('What course platform do you use?',
                                     ['Udemy', 'Coursera', 'edX', 'Udacity', 'Khan Academy', 'Udacity', 'Other'])
with col2:
    ml_algorithm = st.multiselect('What machine learning algorithm do you use?',
                                  ['Autoencoder Networks', 'Bayesian Approaches', 'Convolutional Neural Networks',
                                   'Decision Trees or Random Forests', 'Dense Neural Networks',
                                   'Evolutionary Approaches',
                                   'Generative Adversarial Networks', 'Gradient Boosting Machines',
                                   'Graph Neural Networks',
                                   'Linear or Logistic Regression', 'Recurrent Neural Networks',
                                   'Transformer Networks'])
    ide = st.multiselect('What IDE do you use?',
                         ['IntelliJ', 'Jupyter', 'Notepad++', 'PyCharm', 'RStudio', 'Spyder', 'Sublime Text',
                          'Vim / Emacs',
                          'Visual Studio', 'Visual Studio Code'])
with col3:
    language = st.multiselect('What programming language do you use?',
                              ['Bash', 'C', 'C#', 'C++', 'Go', 'Java', 'Javascript', 'Julia', 'MATLAB', 'PHP', 'Python',
                               'R',
                               'SQL', 'Swift'])

    related_activities = st.multiselect('What related activities do you participate in?',
                                        ['Analyze and understand data to influence product or business decisions',
                                             'Build and/or run a machine learning service that operationally improves '
                                             'my product or workflows',
                                             'Build and/or run the data infrastructure that my business uses for '
                                             'storing',
                                             'Build prototypes to explore applying machine learning to new areas',
                                             'Do research that advances the state of the art of machine learning',
                                             'Experimentation and iteration to improve existing ML models',
                                             'None of these activities are an important part of my role at work'])

# two columns
col1, col2 = st.columns(2)
with col1:
    years_of_programming = st.slider('For how many years have you been writing code and/or programming?', 0, 50, 1)
    yearly_compensation = st.slider('What is your expected yearly compensation?(USD)', 0, 1000000, step=1000)

with col2:
    years_of_ml = st.slider('For how many years have you used machine learning methods?', 0, 25, 1)
    company_size = st.slider('What is the size of the company where you are looking to work for?', 0, 10000, step=100)

# user profile translate
input_features['Age'] = find_nearest(age, dict_age)
input_features['Years_of_programming'] = find_nearest(years_of_programming, dict_years_of_programming)
input_features['Years_of_machine_learning'] = find_nearest(years_of_ml, dict_years_of_ml)
input_features['Company_size'] = find_nearest(company_size, dict_company_size)
input_features['Yearly_compensation'] = find_nearest(yearly_compensation, dict_yearly_compensation)

# updata input features
# categorical features
input_features[education] = 1
for lang in language:
    if lang in input_features:
        input_features[lang] = 1
for i in ide:
    if i in input_features:
        input_features[i] = 1
for ml in ml_algorithm:
    if ml in input_features:
        input_features[ml] = 1
for related in related_activities:
    if related in input_features:
        input_features[related] = 1
# numerical features
for feature, dict_vals in zip(
        ['Age', 'Years_of_programming', 'Years_of_machine_learning', 'Company_size', 'Yearly_compensation'],
        [dict_age, dict_years_of_programming, dict_years_of_ml, dict_company_size, dict_yearly_compensation]):
    min_val, max_val = min(dict_vals), max(dict_vals)
    input_features[feature] = input_features[feature] = (input_features[feature] - min_val) / (max_val - min_val)
# Convert input_features to DataFrame
input_df = pd.DataFrame([input_features])
# Predict using the model
predicted_job_role = gbm_model.predict(input_df)[0]

# Map the predicted label back to the original job role
predicted_job_role_name = reverse_label_mapping[predicted_job_role]

# Submit button
if st.button('Recommend'):
    # Logic to process input data, make predictions, and output recommendations
    st.markdown(f'#### Recommended Job Role: **{predicted_job_role_name}**', unsafe_allow_html=True)
    # Display job information
    job_description = job_info.get(predicted_job_role_name, "No description available for this role.")
    st.write(job_description)

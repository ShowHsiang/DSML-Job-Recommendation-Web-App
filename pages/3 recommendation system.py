import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import function as func
import re

# set title
st.title("Recommendation System Review")

# part 1
with st.expander("1. Preprocessed Dataset Overview"):
    st.markdown("""
        ### Data Preprocessing Steps
        The following steps were taken to preprocess the dataset:

        - **Survey Questions Combining**: Combine the columns in every dataset that belong to the same question.
        - **Data Combination**: Combined datasets from three consecutive years into a single dataset.
        - **Categorical Encoding**: Encoded categorical features, expand the multiple choices in each column, and represent using binary.
        - **Missing Value Handling**: Drop rows with missing values and make the dataset ready for traning.
        - **Feature Normalization**: Applied normalization to numerical features for uniformity.
        - **Feature Selection**: Employed SelectKBest for feature selection to identify features with the highest relevance to the target variable.
        - **Target Variable selection**: Remove and merge some jobs with insufficient data samples or very similar functions. Increased system accuracy from **47%** to **almost 60%**. 
        
        These preprocessing steps are crucial to ensure that the model has high-quality and relevant data for training, which can significantly impact the model's performance.
        """)
    st.image("./Picture/dataprocesspipeline.png", caption="Data Process Pipeline", use_column_width=True)

# part 2
with st.expander("2. Baseline Model - Random Decision"):
    st.markdown("""
        ### Baseline Model Evaluation
        A baseline model serves as a starting point for comparison with more complex models. In this case, a random decision model was used, which predicts outcomes based on the distribution of classes in the training set.

        This random approach is not expected to be good but provides a floor metric to understand the minimum expected performance and to ensure that subsequent models are indeed learning patterns rather than making random guesses.

        Below are the precision, recall, and f1-score of the random decision model evaluated on the test set:
        """)
    st.image("./Picture/Random Decision Report.png", caption="Baseline Model Report", use_column_width=True)
    st.markdown("""### Overall Accuracy: 0.23""")
# part 3
with st.expander("3. Model Comparisons"):
    st.markdown("""
              ### RandomForest/XGBoost/GBM Comparison
              In our analysis, we compared three distinct models: Random Decision, XGBoost, and Gradient Boosting (GBM).
              Each model brings its own set of strengths and assumptions to the table. The Random Decision serves as our baseline, providing a benchmark for the minimum performance we expect.
              XGBoost and GBM are more sophisticated algorithms designed for performance and accuracy."
              The results of all the models are outlined below: """)
    st.image('./Picture/Comparsion of Different Models.png', use_column_width=True)

# part 4
with st.expander("4. Final Model Selection - GBM"):
    st.markdown("""
        ### Final GBM Model Evaluation
         After thorough evaluation, the GBM (Gradient Boosting Machine) was selected as the final model.
         This decision was underpinned by the model's robustness, efficiency, and superior performance metrics.
         The performance of the GBM model would be represented as in the diagram below""")
    st.image('./Picture/GBM Report.png', use_column_width=True)
    st.markdown("""### Overall Accuracy: 0.59""")
    st.image('./Picture/Confusion Matrix.png', use_column_width=True)


# IT5006
## Project: Job Role Recommendation App

This is the members' table of our team:

| 1         | 2              | 3           |
| --------- | -------------- | ----------- | 
| HUANG HEJIA | XIANG XIAONENG | LIN XUESHUN |

# Installation

### Clone this Repository

Enter the target directory you want to use, and use this command to clone and enter the folder:

```bash
git clone https://github.com/Vicchan2324/IT5006.git
cd IT5006
```

### Create virtual Environment

```bash
conda create -n env5006 python=3.11 -y
conda activate env5006
pip install --upgrade pip
pip install -r requirements.txt
```

### Run the Main.py

```bash
streamlit run Main.py
```

### Dataset:
Kaggle's Annual Machine Learning and Data Science Survey from the past three years (2020-2022)

### Project Tasks
#### [(streamlit app link)](https://it5006-kxx3jsq4iscaa9vyoqohvk.streamlit.app/)

### Files structure   
#### You are recommended to run through notebooks from 0 to 3.
#### 0Preprocess.ipynb is to preprocess the three datasets and merge them by the same questions    
#### 1Data_Cleaning.ipynb is further data cleaning and extract useful features from dirty data.
#### 2Model_Training&Evaluation.ipynb is model training and evaluation. We did feature selection and evaluated three models.
#### 3GBM_Model_training.ipynb is the final model training and model exportation. We selected GBM and exported pretrained model for our streamlit app to use.

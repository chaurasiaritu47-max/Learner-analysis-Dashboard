import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
#for reading the .csv file on local computer use the below code and change the path to your file location
#df = pd.read_csv("D:\\python\\Edupro_final_data.csv")
#for reading the .csv file from github use the below code and change the url to your file location
df = pd.read_csv("Edupro_final_data.csv")
st.title("Learner Demographics and Course Enrollment Behavior Analysis on EduPro")


st.markdown("""
<style>

.stApp {
    background-color: #f0f8ff;  /* AliceBlue for page background */
}

[data-testid="stSidebar"] {
    background-color: #e6f2ff;  /* Light Blue for sidebar*/
}

h1 {
    color: #4B0082;  /* Indigo for project title name*/
    text-align: center;
}

h2 {
    color: #6a0dad;  /* Dark Purple  fot kpi title*/
}

[data-testid="stMetricValue"] {
    color: #00008B !important;   /* dark blue KPI values */
}

[data-testid="stMetricLabel"] {
    color: #4B0082 !important;   /* indigo kpi labels */
}

label {                           /*sidebar label color*/
    color: #4B0082 !important;
    font-weight: bold;
}

h3 {
    color: #800080;   /* Purple for chart title */
    text-align: center;
}

.stPlotlyChart, .stPyplot {         /* chart background */
    background-color: #ffffff;
    padding: 10px;
    border-radius: 10px;
    border: 2px solid #d8bfd8;
}



</style>
""", unsafe_allow_html=True)


# KPIs
filtered_df = df.copy()
gender_filter = st.sidebar.selectbox("Select Gender", ["All"] + list(df['Gender'].unique()))
age_filter = st.sidebar.selectbox("Select Age Group", ["All"] + list(df['AgeGroup'].unique()))
category_filter = st.sidebar.selectbox("Select Course Category", ["All"] + list(df['CourseCategory'].unique()))
level_filter = st.sidebar.selectbox("Select Course Level", ["All"] + list(df['CourseLevel'].unique()))
# Apply filter
if age_filter != "All":
    filtered_df = filtered_df[filtered_df['AgeGroup'] == age_filter]

if gender_filter != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == gender_filter]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df['CourseCategory'] == category_filter]

if level_filter != "All":
    filtered_df = filtered_df[filtered_df['CourseLevel'] == level_filter]


total_enrollments = len(filtered_df)
most_popular_category = filtered_df['CourseCategory'].value_counts().idxmax()
most_common_level = filtered_df['CourseLevel'].value_counts().idxmax()
top_age_group = filtered_df['AgeGroup'].value_counts().idxmax()
gender_ratio = filtered_df['Gender'].value_counts(normalize=True) * 100


st.subheader("Key Performance Indicators (KPIs)")

col1, col2, col3, col4, col5, col6= st.columns(6)

col1.metric("Total Enrollments", total_enrollments)
col2.metric("Course Category", most_popular_category)
col3.metric("Course Level", most_common_level)
col4.metric("Age Group", top_age_group)
col5.metric("Male %", round(gender_ratio.get('Male', 0), 1)) 
col6.metric("Female %", round(gender_ratio.get('Female',0),1))

st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Age Distribution")
    fig, ax = plt.subplots(figsize=(4,4))    # 4 inches wide, 4 inches tall
    filtered_df['AgeGroup'].value_counts().sort_index().plot(kind='bar', ax=ax)
    ax.set_xlabel("Age Group", color='indigo')
    ax.set_ylabel("Enrollments", color='indigo')
    ax.tick_params(axis='x', colors='darkblue', labelsize=11)
    ax.tick_params(axis='y', colors='darkblue', labelsize=11)
    fig.patch.set_facecolor('#f0f8ff')  
    ax.set_facecolor('#f9f9ff') 
    st.pyplot(fig)


with col2:
    short_names = {
    "Data Science": "DS",
    "Web Development": "Web",
    "Project Management":"Project Mgmt",
    "Artificial Intelligence": "AI",
    "Machine Learning": "ML",
    "Cybersecurity": "Cyber",
    "Digital Marketing": "Digital Mktg",
     }

    # Replace long names with short names
    filtered_df['ShortCategory'] = filtered_df['CourseCategory'].replace(short_names)


    st.subheader("Course Popularity")
    fig, ax = plt.subplots(figsize=(4,4))    # 4 inches wide, 7 inches tall
    filtered_df['ShortCategory'].value_counts().plot(kind='bar', ax=ax)
    ax.set_xlabel("Course Category", color='indigo')
    ax.set_ylabel("Enrollments", color='indigo')
    ax.tick_params(axis='x', colors='darkblue', labelsize=11)
    ax.tick_params(axis='y', colors='darkblue', labelsize=11)
    fig.patch.set_facecolor('#f0f8ff')   
    ax.set_facecolor('#f9f9ff')
    st.pyplot(fig)

st.markdown("<br><br>", unsafe_allow_html=True)
# Second Row (2 Charts Side by Side)
col3, col4 = st.columns(2)

with col3:
    st.subheader("Gender vs Course Level")
    pivot = pd.crosstab(filtered_df['Gender'], filtered_df['CourseLevel'])
    fig, ax = plt.subplots(figsize=(7,5))    
    ax.set_xlabel("Gender", color='indigo', fontsize=14)
    ax.set_ylabel("Course Level", color='indigo', fontsize=14)
    ax.tick_params(axis='x', colors='darkblue',labelsize=11)
    ax.tick_params(axis='y', colors='darkblue', labelsize=11)
    sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues", ax=ax)
    fig.patch.set_facecolor('#f0f8ff')   
    ax.set_facecolor('#f9f9ff') 
    st.pyplot(fig)

with col4:
    st.subheader("Age vs Category Heatmap")
    pivot2 = pd.crosstab(filtered_df['AgeGroup'], filtered_df['ShortCategory'])
    fig, ax = plt.subplots(figsize=(7,5))
    ax.set_xlabel("Course Category", color='indigo',  fontsize=14)
    ax.set_ylabel("Age Group", color='indigo', fontsize=14)
    ax.tick_params(axis='x', colors='darkblue', labelsize=11)
    ax.tick_params(axis='y', colors='darkblue', labelsize=11)
    sns.heatmap(pivot2, annot=True, fmt="d", cmap="Oranges", ax=ax)
    fig.patch.set_facecolor('#f0f8ff')  
    ax.set_facecolor('#f9f9ff') 
    st.pyplot(fig)



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file = "D:\\python\\EduPro_Online_Platform.xlsx"

users = pd.read_excel(file, sheet_name="Users")
teachers = pd.read_excel(file, sheet_name="Teachers")
courses = pd.read_excel(file, sheet_name="Courses")
transactions = pd.read_excel(file, sheet_name="Transactions")



merged_df = transactions.merge(users, on="UserID", how="left")
merged_df = merged_df.merge(teachers, on="TeacherID", how="left")
final_df = merged_df.merge(courses, on="CourseID", how="left")

print(final_df.head())
duplicates = final_df.duplicated().sum()
print("Total Duplicate row:",duplicates)
# Create Age Groups
bins = [0, 17, 22, 27, 32, 100]
labels = ['<18', '18-22', '23-27', '28-32', '33+']

final_df['AgeGroup'] = pd.cut(final_df['Age'], bins=bins, labels=labels)

print(final_df.columns)
final_df.drop(columns=['Age'], inplace=True)
print(final_df.columns)


# age distribution
age_dist = final_df['AgeGroup'].value_counts()
print(age_dist)

# gender distribution
gender_dist = final_df['Gender'].value_counts()
print(gender_dist)

# Participation by Age Group
age_participation = final_df.groupby('AgeGroup')['UserID'].count()
print(age_participation)

# participation by gender
gender_participation = final_df.groupby('Gender')['UserID'].count()
print(gender_participation)


# Enrollment by Course Category

category_count = final_df['CourseCategory'].value_counts()
print(category_count)

# Enrollment by Course Type
coursetype_count = final_df['CourseType'].value_counts()
print(coursetype_count)

# Enrollement by course level
course_level_count = final_df['CourseLevel'].value_counts()
print(course_level_count)

# Most Popular Category
print("Most Popular Category:\n", final_df['CourseCategory'].mode())
# least popular category
print("Least Popular Category:\n",final_df['CourseCategory'].value_counts().tail(1))

# age group and course category heatmap
age_category = pd.crosstab(final_df['AgeGroup'], final_df['CourseCategory'])
print(age_category)

plt.figure(figsize=(8,5))
sns.heatmap(age_category, annot=True, fmt="d")
plt.title("Age Group vs Course Category Heatmap")
plt.xlabel("Course Category")
plt.ylabel("Age Group")
plt.show()


# gender and course level heatmap
gender_level = pd.crosstab(final_df['Gender'], final_df['CourseLevel'])
print(gender_level)

import matplotlib.pyplot as plt

gender_level.plot(kind='bar')
plt.title("Gender vs Course Level")
plt.xlabel("Gender")
plt.ylabel("Enrollments")
plt.xticks(rotation=0)
plt.show()


# Identify learner segments and their preferences
age_pref = final_df.groupby('AgeGroup')['CourseCategory'].agg(lambda x: x.value_counts().index[0] if len(x.value_counts()) > 0 else "No Data")
print(age_pref)

gender_pref = final_df.groupby('Gender')['CourseCategory'] .agg(lambda x: x.value_counts().index[0] if len(x.value_counts()) > 0 else "No Data")
print(gender_pref)

level_pref = final_df.groupby('AgeGroup')['CourseLevel'].agg(lambda x: x.value_counts().index[0] if len(x.value_counts()) > 0 else "No Data")
print(level_pref)


# Average Courses Taken Per Learner
avg_courses = final_df.groupby('UserID')['CourseID'].count().mean()
print("Average courses per learner:", avg_courses)

# Enrollment Concentration (Active Users)
courses_per_user = final_df.groupby('UserID')['CourseID'].count()
print(courses_per_user.sort_values(ascending=False).head(10))

# Beginner vs Advanced Behavior patterns
level_behavior = final_df['CourseLevel'].value_counts()
print(level_behavior)

user_level = final_df.groupby(['UserID','CourseLevel']).size()
print(user_level.head(10))

avg_level = final_df.groupby('CourseLevel')['UserID'].count()
print(avg_level) 

final_df.to_csv("D:\\python\\Edupro_final_data.csv", index=False)
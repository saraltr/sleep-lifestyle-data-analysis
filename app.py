import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title="Workplace Health Dashboard", layout="centered")
st.title("Workplace Health Lifestyle Data Analysis")

# caches the result to avoid reloading on every rerun
@st.cache_data
def load_data():
    df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")

    # fill missing values in and remove extra whitespace
    df["Sleep Disorder"] = df["Sleep Disorder"].fillna("No Disorder").str.strip()

    # grouping similar roles
    df["Occupation"] = df["Occupation"].replace({
        "Sales Representative": "Sales",
        "Salesperson": "Sales",
        "Software Engineer": "Engineer"
    })

    # combine normal and normal weight BMI categories
    df["BMI Category"] = df["BMI Category"].replace({"Normal": "Normal Weight"})

    return df

data_load_state = st.text("Loading data...")
df = load_data()
data_load_state.text("Loading data...done! (using st.cache_data)")

# filter
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(df)

# occupation Filter
valid_jobs = df["Occupation"].value_counts()[lambda x: x >= 5].index

selected_jobs = st.multiselect(
    "Select Occupations to display:", 
    valid_jobs, 
    default=valid_jobs, 
    help="Please select at least one job to view data."
)

# defaulting to all jobs if user clears all
if not selected_jobs:
    st.info("At least one occupation must be selected.")
    selected_jobs = valid_jobs

# filter the dataset to include only the selected occupations
filtered_df = df[df["Occupation"].isin(selected_jobs)]

# get the unique occupation labels for the x-axis
labels = filtered_df["Occupation"].unique().tolist()
x = np.arange(len(labels))
width = 0.25 # width of each bar

# 1. Sleep disorder distribution by occupation bar chart
st.subheader("Question 1: Which occupations report the highest percentage of sleep disorders?")

st.markdown("""
This section analyzes which professions report the **highest prevalence of sleep disorders**.

The chart below displays the **percentage distribution** of each sleep disorder (or lack thereof) across occupations.  
This helps highlight whether certain jobs are more strongly associated with sleep-related health issues.
""")

# count the number of occurrences for each occupation/ sleep disorder pair
disorder_counts = filtered_df.groupby(["Occupation", "Sleep Disorder"]).size().unstack(fill_value=0)

# convert counts to percentages
disorder_pct = disorder_counts.div(disorder_counts.sum(axis=1), axis=0) * 100

# extract percentages for main disorder types
insomnia = disorder_pct.get("Insomnia", pd.Series([0]*len(labels), index=labels)).reindex(labels).fillna(0).tolist()

sleep_apnea = disorder_pct.get("Sleep Apnea", pd.Series([0]*len(labels), index=labels)).reindex(labels).fillna(0).tolist()

no_disorder = disorder_pct.get("No Disorder", pd.Series([0]*len(labels), index=labels)).reindex(labels).fillna(0).tolist()

# create the bar chart
fig, ax = plt.subplots(figsize=(10, 6))

# plot each category of sleep disorder
ax.bar(x - width, insomnia, width, label="Insomnia")
ax.bar(x, sleep_apnea, width, label="Sleep Apnea")
ax.bar(x + width, no_disorder, width, label="No Disorder")

# chart title, labels & legend
ax.set_title("Sleep Disorders by Occupation (%)")
ax.set_ylabel("Percentage")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45)
ax.set_ylim(0, 100)
ax.legend()

# add percentage labels above each bar
for i in range(len(labels)):
    ax.text(x[i] - width, insomnia[i] + 0.5, f"{insomnia[i]:.1f}%", ha="center", va="bottom", fontsize=8)
    ax.text(x[i], sleep_apnea[i] + 0.5, f"{sleep_apnea[i]:.1f}%", ha="center", va="bottom", fontsize=8)
    ax.text(x[i] + width, no_disorder[i] + 0.5, f"{no_disorder[i]:.1f}%", ha="center", va="bottom", fontsize=8)

# display the chart
st.pyplot(fig)

st.markdown("#### Conclusion")

st.markdown("""
→ **Sales workers** are the **most affected by sleep disorders**:  
- **85.3%** report **insomnia**  
- **8.8%** report **sleep apnea**  
- Only **5.9%** report **no disorder**
            

→ **Nurses** have the **highest rate of sleep apnea** by far (**83.6%**), significantly exceeding all other professions (ranging from 0% to ~10%).

→ **Teachers** also show **high insomnia prevalence** (**67.5%**), and only **22.5%** report **no disorder**.

→ In contrast, **Doctors, Engineers, Accountants, and Lawyers** show the **lowest disorder rates**, with **over 80%** in each group reporting **no sleep disorder**.
""")


st.markdown("---")
# 2. Sleep duration by stress level bar chart with stress, sleep quality, physical activity)
st.subheader("Question 2: Do occupations with higher stress levels also report lower sleep quality or fewer sleep hours?")

st.markdown("""
This analysis examines whether occupations with **higher average stress levels** also tend to report **lower sleep quality** or **shorter sleep duration**.

The chart below compares **stress levels**, **sleep duration**, and **sleep quality** across professions.  
While the focus is on stress and sleep, **physical activity** is included as a secondary factor to observe whether it may also play a role in sleep health or if **stress remains the stronger predictor**.
""")

# calculate means by Occupation
stress_levels = filtered_df.groupby("Occupation")["Stress Level"].mean().reindex(labels)
sleep_duration = filtered_df.groupby("Occupation")["Sleep Duration"].mean().reindex(labels)
sleep_quality = filtered_df.groupby("Occupation")["Quality of Sleep"].mean().reindex(labels)
physical_activity = filtered_df.groupby("Occupation")["Physical Activity Level"].mean().reindex(labels)

# let the user filter metrics
metric_options = ["Stress Level", "Sleep Duration", "Quality of Sleep"]
selected_metrics = st.multiselect(
    "Select metrics to display:",
    metric_options,
    default=metric_options,
    help="Choose which metrics to show as bars. Line chart always shows Physical Activity."
)

# create the figure
fig, ax1 = plt.subplots(figsize=(10, 6))

# offsets for bar positioning
offsets = {
    "Stress Level": -width,
    "Sleep Duration": 0,
    "Quality of Sleep": width
}

# plot only selected bars
if "Stress Level" in selected_metrics:
    ax1.bar(x + offsets["Stress Level"], stress_levels, width, label="Stress Level")
if "Sleep Duration" in selected_metrics:
    ax1.bar(x + offsets["Sleep Duration"], sleep_duration, width, label="Sleep Duration")
if "Quality of Sleep" in selected_metrics:
    ax1.bar(x + offsets["Quality of Sleep"], sleep_quality, width, label="Quality of Sleep")

# bar axis settings
ax1.set_ylabel("Scale (0–10)")
ax1.set_ylim(0, 10)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45)
ax1.set_title("Stress, Sleep, and Physical Activity by Occupation")

# line chart on twin axis
ax2 = ax1.twinx()
ax2.plot(x, physical_activity, label="Physical Activity", color="tab:red", marker="o", linewidth=2)
ax2.set_ylim(0, 100)
ax2.set_ylabel("Physical Activity Level (0–100)")

# combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

# display chart
st.pyplot(fig)

st.markdown("#### Conclusion")

st.markdown("""

There’s a clear correlation between **higher stress** and **poorer sleep health**.

→ **Sales workers** report the **highest stress level** (**7.1**), **lowest sleep duration** (**6.4 hours**), and **worst sleep quality** (**5.9**).

→ **Doctors** also show **high stress** (**6.7**) and **poor sleep quality** (**6.6**), although their sleep duration is slightly better (**7 hours**).            

→ **Engineers**, on the other hand, report the **lowest stress** (**4.0**), **highest sleep duration** (**7.9 hours**), and **best sleep quality** (**8.3**).
            
**Physical Activity Comparison**  
- **Most Active:** Nurses (78.6), Lawyers (70.4)  
- **Least Active:** Engineers (51.6), Sales Workers (44.1)
            
→ Interestingly, **physical activity levels** appear to vary independently as **nurses (78.6)** and **lawyers (70.4)** report the highest activity, while **engineers (51.6)** and **sales workers (44.1)** are less active. Despite lower activity, engineers report excellent sleep, which may mean **stress has a stronger influence on sleep health** than physical activity alone.
""")



st.markdown("---")
# 3. BMI Category distribution by occupation bar chart with secondary axis for average age
st.subheader("Question 3: Are there noticeable differences in BMI category distribution across occupations?")

st.markdown("""
This analysis investigates how rates of **overweight** and **obesity** vary across different occupations.  
Since both **age** and **gender** are known to influence body mass index, we include them as important factors to contextualize the BMI differences observed.

- **Age** affects metabolism and fat distribution, often increasing BMI as people get older ([Jura M, Kozak LP., 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5005878/)).  
- **Gender** influences body composition and fat patterns, with different prevalence of overweight/obesity between genders ([Koceva A, Herman R, Janez A, Rakusa M, Jensterle M., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11242171/)).

By examining BMI together with average age and gender distribution, we can better understand the patterns by occupation in weight variations and identify whether age or gender alone can explain these differences.
""")


# filter for BMI categories
bmi_options = ["Overweight", "Obese"]
selected_bmi = st.multiselect(
    "Select metrics to display:",
    bmi_options,
    default=bmi_options,
    help="Choose which BMI categories to combine for each occupation."
)

# Compute BMI counts and percentages
bmi_counts = filtered_df.groupby(["Occupation", "BMI Category"]).size().unstack(fill_value=0).reindex(labels).fillna(0)
bmi_pct = bmi_counts.div(bmi_counts.sum(axis=1), axis=0) * 100

# Add together selected categories (default: Overweight + Obese)
bmi_combined = pd.Series([0]*len(labels), index=labels)
for category in selected_bmi:
    if category in bmi_pct.columns:
        bmi_combined += bmi_pct[category]

# Compute average age
age_by_occupation = filtered_df.groupby("Occupation")["Age"].mean().reindex(labels)

# Create plot
fig, ax1 = plt.subplots(figsize=(10, 6))
bars = ax1.bar(x, bmi_combined, color='steelblue')
ax1.set_ylabel("% " + " + ".join(selected_bmi) if selected_bmi else "BMI %")
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45)
y_max = bmi_combined.max() if selected_bmi else 1
ax1.set_ylim(0, y_max + 10)
ax1.set_title("BMI Rate vs Age by Occupation")

# Gender label annotations
gender_counts = filtered_df.groupby(["Occupation", "Gender"]).size().unstack(fill_value=0).reindex(labels).fillna(0)
gender_pct = gender_counts.div(gender_counts.sum(axis=1), axis=0) * 100

for i, occupation in enumerate(labels):
    male_pct = gender_pct.loc[occupation, "Male"] if "Male" in gender_pct.columns else 0
    female_pct = gender_pct.loc[occupation, "Female"] if "Female" in gender_pct.columns else 0
    label = f"{male_pct:.0f}% M" if male_pct > female_pct else f"{female_pct:.0f}% F"
    ax1.text(i, bmi_combined.iloc[i] + 2, label, ha='center', va='bottom', fontsize=9)

# Secondary axis: average age
ax2 = ax1.twinx()
ax2.plot(x, age_by_occupation, color="tab:red", marker='o', linewidth=2, label="Average Age")
ax2.set_ylabel("Average Age")
ax2.set_ylim(age_by_occupation.min() * 0.95, age_by_occupation.max() * 1.05)

# Combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

# Show chart
st.pyplot(fig)

st.markdown("#### Conclusion")

st.markdown("""
→ **Sales workers, nurses, and teachers** exhibit the **highest rates of overweight and obesity** (ranging between **85% and 100%** of participants).

→ **Doctors, engineers, and lawyers** tend to maintain **predominantly healthy BMI levels**.

→ **Age and physical activity alone do not fully explain BMI differences**:  
- Nurses have the **highest physical activity levels** but still poor BMI outcomes.  
- Engineers are on average **older** and moderately active (**51.6**), yet maintain healthy weights.

→ This suggests **other factors** such as **sleep quality, stress, or working conditions** may significantly influence BMI.

→ Regarding **gender distribution**:  
- Occupations with higher overweight/obesity rates are often **female-dominated** (e.g., nurses, teachers).  
- However, sales (a **male-dominated field**) also reports very poor BMI results, indicating gender alone does **not fully explain** the differences.

""")


st.markdown("---")
# 4. Correlation: BMI vs Sleep Quality and Sleep Duration
st.subheader("Extended Conclusion: Revisiting BMI with Sleep as a Key Factor")

st.markdown("""**Additional question:** *What if sleep quality and sleep duration were stronger predictors of BMI than gender or age?*

While the initial analysis of question n°3 showed clear differences in BMI across occupations,  
factors like **age**, **gender**, and **physical activity** offered only **partial explanations**.
            
This section explores the relationship between BMI rates and sleep metrics (quality and duration) across occupations.            
""")


# Combine BMI categories
bmi_percent = filtered_df.groupby(["Occupation", "BMI Category"]).size().unstack(fill_value=0)
bmi_percent = bmi_percent.div(bmi_percent.sum(axis=1), axis=0) * 100

# Combine Overweight + Obese for above-normal BMI %
bmi_overweight_obese = (
    bmi_percent.get("Overweight", pd.Series(0, index=bmi_percent.index)) +
    bmi_percent.get("Obese", pd.Series(0, index=bmi_percent.index))
).reindex(labels).fillna(0)

# Get average sleep quality and duration
sleep_quality = filtered_df.groupby("Occupation")["Quality of Sleep"].mean().reindex(labels)
sleep_duration = filtered_df.groupby("Occupation")["Sleep Duration"].mean().reindex(labels)

# plot
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# BMI vs Sleep Quality
ax[0].scatter(sleep_quality, bmi_overweight_obese)
for i, occ in enumerate(labels):
    ax[0].annotate(occ, (sleep_quality[i], bmi_overweight_obese[i]), fontsize=8)
ax[0].set_xlabel("Average Sleep Quality")
ax[0].set_ylabel("% Overweight + Obese")
ax[0].set_title("BMI vs Sleep Quality")

# BMI vs Sleep Duration
ax[1].scatter(sleep_duration, bmi_overweight_obese)
for i, occ in enumerate(labels):
    ax[1].annotate(occ, (sleep_duration[i], bmi_overweight_obese[i]), fontsize=8)
ax[1].set_xlabel("Average Sleep Duration (hrs)")
ax[1].set_ylabel("% Overweight + Obese")
ax[1].set_title("BMI vs Sleep Duration")

plt.tight_layout()
st.pyplot(fig)

st.markdown("#### Conclusion")

st.markdown("""
By comparing the percentage of overweight and obese individuals in each occupation with their average sleep quality and duration, we can observe the following patterns:

→ **Sales Workers** suffer from the **worst sleep quality** (5.9) and **shortest sleep duration** (6.4 hours),  
resulting in the **highest overweight/obesity rates** (~100%).

→ **Teachers and Nurses** experience **poor sleep health** (quality between 6.3–6.4 and about 6.6 hours sleep),  
with **very high BMI issues** (~85%–90%).

→ **Engineers and Lawyers** enjoy the **best sleep health** (quality between 7.8–8.3 and 7.6–7.9 hours sleep),  
and have the **healthiest BMI profiles**.

→ **Doctors are an exception**: despite **poorer sleep quality than engineers** (6.6 quality, 7.0 hours),  
they maintain better BMI results, likely due to **protective factors** such as:  
- Medical knowledge  
- Healthier lifestyle habits  
- Better dietary choices

→ ** What it demonstrates:** 
Sleep metrics (quality and hours) appear to better align with BMI patterns than other factors.
Occupations with poor sleep tend to have worse BMI outcomes. Additionally, the results also suggest that possible protective factors can also play a strong role in BMI results.
""")

st.markdown("---")

st.subheader("Study Conclusion")

st.markdown("""
This study examined the relationships between occupation, sleep disorders, BMI categories, and sleep quality/duration to understand health disparities **across professions**.

##### Key insights:

- Certain occupations, such as **sales workers, nurses, and teachers**, show significantly higher rates of sleep disorders (especially insomnia and sleep apnea) and elevated BMI levels, which highlights a concerning overlap between poor sleep health and weight issues.

- In contrast, **doctors, engineers, accountants, and lawyers** tend to have lower prevalence of sleep disorders and healthier BMI levels. This may reflect not only greater health awareness, but also more stable work environments, structured routines, and access to resources that support healthier lifestyles. 

- For example, while doctors report poorer sleep than expected, they still maintain relatively healthy BMI levels, likely due to the nature of their profession, which involves medical training and knowledge, and a culture that emphasizes preventive care and healthy habits.

- Similarly, engineers and lawyers, despite mostly sedentary work, show better sleep and BMI profiles, suggesting that job structure plays a key role in shaping a healthy lifestyle.
            
While factors like age, gender, and physical activity do play a role, they do not fully account for the differences observed across occupations. This suggests that other elements, such as sleep or stress may have a stronger and more direct influence on health outcomes.

Therefore, **sleep quality and duration emerge as strong predictors of BMI status across occupations**, as those with poorer sleep consistently show higher rates of overweight and obesity. These findings demonstrate the importance of considering workplace conditions when addressing public health issues related to weight and well-being.

**Protective factors** such as medical knowledge and healthier habits appear to buffer some groups (e.g., doctors) against poor BMI outcomes despite less ideal sleep metrics.

##### Implications:
            
Understanding how work influences and is interconnected to sleep and BMI results can help shape more effective workplace health initiatives. Occupation factors can affect sleep habits, stress levels and long-term weight outcomes. These results emphasize the need for employers to address work-related factors and that targeting occupation-specific challenges could lead to more successful measures. 
            
Future research should explore how specific occupational characteristics interact with sleep and lifestyle behaviors to influence overall health outcomes, as well as how improvements in sleep quality and general health can enhance workplace productivity and performance.

""")
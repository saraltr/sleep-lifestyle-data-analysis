# Workplace Health Lifestyle Data Analysis
[Live Demo – Streamlit App](https://workplace-data-analysis.streamlit.app/)

This project explores the relationships between occupations, sleep disorders, body mass index (BMI), and sleep quality using the [**Sleep Health and Lifestyle Dataset**](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset).

The analysis specifically targets groups based on their occupation or work type to identify how different professions influence healthy lifestyles in order to highlight health disparities between professions.

[Software Demo Video](http://youtube.link.goes.here)

# Data Analysis Results

{List the questions and the answers you found by doing this analysis.}
## Research Questions

### 1. Which occupations report the highest percentage of sleep disorders?
Sales workers, nurses, and teachers demonstrate significantly higher rates of insomnia, sleep apnea, and other sleep disorders compared to other professions.

### 2. Do occupations with higher stress levels also report lower sleep quality or fewer sleep hours?
There’s a clear correlation between higher stress and poor sleep health, as occupations associated with higher stress or irregular schedules generally report poorer sleep quality and shorter sleep duration.

### 3. Are there noticeable differences in BMI category distribution across occupations?
Higher BMI levels and overweight/obesity rates are more common in occupations with higher prevalence of sleep disorders, which demonstrate a link between sleep health and weight status.

#### 3a. Extended question: Is sleep quality and sleep duration stronger predictors of BMI than age or physical activity?  
Yes. Sleep metrics consistently show a stronger association with BMI across occupations, indicating that poor sleep may be a key driver of weight-related health outcomes.


# Development Environment

The analysis was performed using Python 3.10.11 with the following main libraries:
- Pandas 2.1.3 for data manipulation and analysis
- Matplotlib 3.8.1 for creating chart visualizations
- Numpy 1.26.2 for numerical operations
- Streamlit 1.46.1 to deploy the study as an interactive web application

To Run the project:
- python -m streamlit run app.py
or
- streamlit app.py

# Useful Websites

* [Pandas Data Subsetting Tutorial](https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html)
* [Pandas GroupBy Operations](https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html)
* [Aggregation Methods in Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#aggregation)
* [Matplotlib Pyplot Tutorials](https://matplotlib.org/stable/tutorials/pyplot.html)
* [Matplotlib Secondary Axis Example](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html)
* [Data Visualization with Matplotlib](https://realpython.com/python-matplotlib-guide/)
* [Numpy Beginner's Guide](https://numpy.org/doc/stable/user/absolute_beginners.html)
* [Streamlit Installation & CLI Usage](https://docs.streamlit.io/get-started/installation/command-line)
* [Streamlit Core Concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts)


# Future Work

* Study other lifestyle factors not available in this dataset such as diet, mental health to build a more comprehensive model of health influences.
* Incorporate additional work variables such as shift work and workload to better understand their effects on sleep and BMI.
* Explore the impact of workplace health programs.
* Study the impact of healthy lifestyles on work productivity.
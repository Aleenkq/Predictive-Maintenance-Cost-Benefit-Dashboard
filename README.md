
<img width="828" height="414" alt="image" src="https://github.com/user-attachments/assets/57cbdfb9-300c-4ad8-bcbe-774d81bee8e8" />

## Financial Impact Analysis of Predictive Maintenance Using an Interactive Cost-Benefit Simulation Dashboard

An interactive predictive maintenance project that combines machine learning classification with financial simulation to compare reactive and model-based maintenance strategies in smart manufacturing environments.

## Project Overview

The project uses the **AI4I 2020 Predictive Maintenance Dataset** to identify machine failure conditions based on operating variables such as temperature, rotational speed, torque, and tool wear.

Four classification models are evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

The model predictions are then translated into simulated maintenance decisions and used in a cost-benefit analysis to estimate the financial impact of predictive maintenance compared with reactive maintenance.

## Main Workflow

**Industrial Data → Data Preparation & EDA → Failure Classification → Maintenance Decision Simulation → Cost-Benefit Analysis → Interactive Dashboard**

The financial simulation considers:

- Planned maintenance cost
- Unplanned repair cost
- Downtime duration and cost
- Unnecessary maintenance interventions
- Implementation cost
- Prevention effectiveness

The dashboard dynamically recalculates financial outcomes based on the selected model and simulation assumptions.

## Interactive Prototype

**Live Prototype:** [Open Dashboard]((https://predictive-maintenance-cost-benefit-dashboard-aeozhz8udbpsgmt7.streamlit.app/))

## Dashboard Features

- Interactive model selection
- Model performance comparison
- Reactive vs. predictive maintenance cost comparison
- Net benefit and ROI calculation
- Cost reduction analysis
- Prevention-effectiveness sensitivity analysis
- Adjustable financial assumptions
- Responsive interface for desktop and mobile devices

## Machine Learning Models

The evaluated models are compared using:

- Accuracy
- Precision
- Recall
- F1-score

Because the dataset is highly imbalanced, the analysis emphasizes precision, recall, and F1-score rather than relying only on accuracy.

## Dataset

The project uses the **AI4I 2020 Predictive Maintenance Dataset**, containing:

- 10,000 observations
- Machine operating variables
- Machine failure labels
- 339 failure observations
- 9,661 non-failure observations

Identifier variables and failure-type indicators are excluded from predictive modeling to avoid irrelevant inputs and target leakage.

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Plotly
- Streamlit
- GitHub
- Streamlit Community Cloud

## Financial Simulation

The project compares two maintenance strategies:

**Reactive Maintenance**  
Maintenance occurs only after an actual machine failure.

**Predictive Maintenance**  
A model prediction triggers a maintenance intervention. Financial outcomes depend on the prediction result and the assumed prevention effectiveness.

The main financial indicators include:

- Reactive maintenance cost
- Predictive maintenance cost
- Operating savings
- Net benefit
- Cost reduction
- Return on investment (ROI)

> Financial values used in the simulation are illustrative scenario assumptions rather than observed industrial maintenance costs.

## Team

Developed by:

**Aleen Aloqili**  
**Ghala Alkahtani**  
**Lama Alsuhaibani**  
**Hala Alhamzah**

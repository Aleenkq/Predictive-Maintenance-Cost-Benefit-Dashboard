# =========================================================
# Predictive Maintenance Cost-Benefit Dashboard
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# COLOR PALETTE
# =========================================================

NAVY = "#081B2E"
NAVY_LIGHT = "#102B42"
NAVY_CARD = "#16354D"

TEAL = "#24C6B8"
TEAL_LIGHT = "#4DE7DC"
TEAL_DARK = "#169D96"

SILVER = "#D6E1E8"
TEXT = "#E6F4F1"
MUTED_TEXT = "#AFC9CD"

SUCCESS = "#30C992"
WARNING = "#F4B942"
DANGER = "#E85D75"

CHART_COLORS = [
    TEAL,
    "#38BFD1",
    "#4DE7DC",
    "#7196A8",
    "#9FD9D2"
]


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* -----------------------------------------------------
       All Streamlit alert boxes
    ----------------------------------------------------- */

    div[data-testid="stAlert"] {{
        background-color: #0C3B33 !important;
        border: 1px solid rgba(77, 231, 220, 0.28) !important;
        border-radius: 14px !important;
        color: #E6F4F1 !important;
    }}

    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] div,
    div[data-testid="stAlert"] span {{
        color: #E6F4F1 !important;
    }}

    div[data-testid="stAlert"] svg {{
        color: #4DE7DC !important;
        fill: #4DE7DC !important;
    }}


    /* Force alert colors in both Streamlit light and dark themes */
    .stApp div[data-testid="stAlert"],
    .stApp div[data-testid="stAlertContainer"] {{
        background: #0C3B33 !important;
        background-color: #0C3B33 !important;
        border-color: rgba(77, 231, 220, 0.28) !important;
        color: #E6F4F1 !important;
    }}

    .stApp div[data-testid="stAlert"] *,
    .stApp div[data-testid="stAlertContainer"] * {{
        color: #E6F4F1 !important;
        -webkit-text-fill-color: #E6F4F1 !important;
    }}

    .stApp div[data-testid="stAlert"] svg,
    .stApp div[data-testid="stAlertContainer"] svg {{
        color: #4DE7DC !important;
        fill: #4DE7DC !important;
    }}

    /* -----------------------------------------------------
       Main page
    ----------------------------------------------------- */

    .stApp {{
        background:
            radial-gradient(
                circle at top right,
                rgba(36,198,184,0.08),
                transparent 30%
            ),
            linear-gradient(
                180deg,
                {NAVY} 0%,
                #0A2034 45%,
                #0D263B 100%
            );
        color: {TEXT};
    }}

    .block-container {{
        max-width: 1350px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT} !important;
    }}

    p, label {{
        color: {TEXT};
    }}


    /* -----------------------------------------------------
       Sidebar
    ----------------------------------------------------- */

    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                {NAVY_LIGHT} 0%,
                #0D293F 100%
            );

        border-right:
            1px solid rgba(77,231,220,0.18);
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {TEXT} !important;
    }}


    /* -----------------------------------------------------
       Metric cards
    ----------------------------------------------------- */

    div[data-testid="stMetric"] {{
        background:
            linear-gradient(
                145deg,
                rgba(22,53,77,0.95),
                rgba(16,43,66,0.90)
            );

        border:
            1px solid rgba(36,198,184,0.26);

        padding: 18px;

        border-radius: 18px;

        box-shadow:
            0 10px 28px rgba(0,0,0,0.23);
    }}

    div[data-testid="stMetricLabel"] {{
        color: {MUTED_TEXT} !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {TEXT} !important;
    }}


    /* -----------------------------------------------------
       Hero section
    ----------------------------------------------------- */

    .hero-box {{
        background:
            linear-gradient(
                135deg,
                rgba(36,198,184,0.15),
                rgba(16,43,66,0.85)
            );

        border:
            1px solid rgba(77,231,220,0.22);

        border-radius: 24px;

        padding: 30px;

        box-shadow:
            0 12px 32px rgba(0,0,0,0.26);
    }}

    .hero-title {{
        color: {TEXT};
        font-size: 2.35rem;
        font-weight: 750;
        margin-bottom: 10px;
        line-height: 1.2;
    }}

    .hero-subtitle {{
        color: {MUTED_TEXT};
        font-size: 1.05rem;
        line-height: 1.7;
        margin-bottom: 12px;
    }}

    .model-pill {{
        display: inline-block;
        background: rgba(36,198,184,0.15);
        color: {TEAL_LIGHT};
        border: 1px solid rgba(77,231,220,0.28);
        padding: 7px 14px;
        border-radius: 30px;
        font-size: 0.93rem;
    }}


    /* -----------------------------------------------------
       Tabs
    ----------------------------------------------------- */

    button[data-baseweb="tab"] {{
        background:
            rgba(22,53,77,0.72) !important;

        color: {TEXT} !important;

        border-radius:
            12px 12px 0 0 !important;

        border:
            1px solid rgba(36,198,184,0.16) !important;

        margin-right: 5px;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        background:
            linear-gradient(
                135deg,
                {TEAL_DARK},
                {TEAL}
            ) !important;

        color: white !important;
    }}


    /* -----------------------------------------------------
       Dataframes
    ----------------------------------------------------- */

    [data-testid="stDataFrame"] {{
        border:
            1px solid rgba(36,198,184,0.18);

        border-radius: 15px;

        overflow: hidden;
    }}


    /* -----------------------------------------------------
       Sliders
    ----------------------------------------------------- */

    .stSlider [role="slider"] {{
        background-color: {TEAL_LIGHT} !important;
        border: 2px solid white !important;
    }}


    /* -----------------------------------------------------
       Dividers
    ----------------------------------------------------- */

    hr {{
        border: none;

        border-top:
            1px solid rgba(77,231,220,0.15);

        margin-top: 2rem;
        margin-bottom: 2rem;
    }}


    /* -----------------------------------------------------
       Footer
    ----------------------------------------------------- */

    .footer-box {{
        margin-top: 35px;

        padding: 22px;

        text-align: center;

        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                rgba(22,53,77,0.94),
                rgba(16,43,66,0.94)
            );

        border:
            1px solid rgba(36,198,184,0.20);

        box-shadow:
            0 10px 25px rgba(0,0,0,0.22);

        color: {MUTED_TEXT};
    }}

    .footer-box b {{
        color: {TEAL_LIGHT};
    }}

    .footer-title {{
        color: {TEXT};
        font-weight: 650;
        margin-bottom: 7px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    performance_df = pd.read_csv(
        "model_performance_comparison.csv"
    )

    outcomes_df = pd.read_csv(
        "model_outcomes.csv"
    )

    assumptions_df = pd.read_csv(
        "simulation_assumptions.csv"
    )

    sensitivity_df = pd.read_csv(
        "sensitivity_analysis.csv"
    )

    financial_df = pd.read_csv(
        "financial_model_comparison.csv"
    )

    dataset_df = pd.read_csv(
        "ai4i2020.csv"
    )

    return (
        performance_df,
        outcomes_df,
        assumptions_df,
        sensitivity_df,
        financial_df,
        dataset_df
    )


(
    performance_df,
    outcomes_df,
    assumptions_df,
    sensitivity_df,
    financial_df,
    dataset_df
) = load_data()


# =========================================================
# DEFAULT FINANCIAL ASSUMPTIONS
# =========================================================

default_assumptions = assumptions_df.iloc[0].to_dict()

DEFAULT_PLANNED = float(
    default_assumptions.get(
        "planned_maintenance_cost",
        500
    )
)

DEFAULT_UNPLANNED = float(
    default_assumptions.get(
        "unplanned_repair_cost",
        3000
    )
)

DEFAULT_DOWNTIME_HOURS = float(
    default_assumptions.get(
        "downtime_hours",
        6
    )
)

DEFAULT_DOWNTIME_COST = float(
    default_assumptions.get(
        "downtime_cost_per_hour",
        400
    )
)

DEFAULT_FALSE_ALARM = float(
    default_assumptions.get(
        "false_alarm_cost",
        250
    )
)

DEFAULT_IMPLEMENTATION = float(
    default_assumptions.get(
        "implementation_cost",
        10000
    )
)

DEFAULT_EFFECTIVENESS = float(
    default_assumptions.get(
        "prevention_effectiveness",
        0.80
    )
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <h2 style="
        margin-bottom:0.2rem;
    ">
        ⚙️ Control Panel
    </h2>

    <p style="
        color:#AFC9CD;
        font-size:0.92rem;
    ">
        Adjust the simulation assumptions and
        explore their financial impact.
    </p>
    """,
    unsafe_allow_html=True
)


selected_model = st.sidebar.selectbox(
    "Predictive Model",
    performance_df["Model"].tolist(),
    index=(
        performance_df["Model"]
        .tolist()
        .index("XGBoost")
        if "XGBoost"
        in performance_df["Model"].tolist()
        else 0
    )
)


st.sidebar.markdown("---")

st.sidebar.subheader(
    "Financial Assumptions"
)


planned_cost = st.sidebar.slider(
    "Planned Maintenance Cost (SAR)",
    min_value=0,
    max_value=10000,
    value=int(DEFAULT_PLANNED),
    step=100
)


unplanned_repair_cost = st.sidebar.slider(
    "Unplanned Repair Cost (SAR)",
    min_value=0,
    max_value=30000,
    value=int(DEFAULT_UNPLANNED),
    step=250
)


downtime_hours = st.sidebar.slider(
    "Downtime Hours per Failure",
    min_value=0,
    max_value=48,
    value=int(DEFAULT_DOWNTIME_HOURS),
    step=1
)


downtime_cost_per_hour = st.sidebar.slider(
    "Downtime Cost per Hour (SAR)",
    min_value=0,
    max_value=5000,
    value=int(DEFAULT_DOWNTIME_COST),
    step=50
)


false_alarm_cost = st.sidebar.slider(
    "Unnecessary Maintenance Cost (SAR)",
    min_value=0,
    max_value=10000,
    value=int(DEFAULT_FALSE_ALARM),
    step=50
)


implementation_cost = st.sidebar.slider(
    "Implementation Cost (SAR)",
    min_value=0,
    max_value=100000,
    value=int(DEFAULT_IMPLEMENTATION),
    step=1000
)


prevention_effectiveness = st.sidebar.slider(
    "Prevention Effectiveness",
    min_value=0.0,
    max_value=1.0,
    value=float(DEFAULT_EFFECTIVENESS),
    step=0.05,
    format="%.2f"
)


# =========================================================
# SELECTED MODEL DATA
# =========================================================

selected_performance = (
    performance_df[
        performance_df["Model"]
        == selected_model
    ]
    .iloc[0]
)


selected_outcome = (
    outcomes_df[
        outcomes_df["Model"]
        == selected_model
    ]
    .iloc[0]
)


tp = int(selected_outcome["TP"])
fp = int(selected_outcome["FP"])
fn = int(selected_outcome["FN"])
tn = int(selected_outcome["TN"])


accuracy = float(
    selected_performance["Accuracy"]
)

precision = float(
    selected_performance["Precision"]
)

recall = float(
    selected_performance["Recall"]
)

f1 = float(
    selected_performance["F1-score"]
)


# =========================================================
# FINANCIAL CALCULATIONS
# =========================================================

failure_loss = (
    unplanned_repair_cost
    +
    (
        downtime_hours
        * downtime_cost_per_hour
    )
)


reactive_total_cost = (
    (tp + fn)
    * failure_loss
)


planned_maintenance_total = (
    tp * planned_cost
)


unnecessary_interventions_total = (
    fp * false_alarm_cost
)


missed_failure_loss_total = (
    fn * failure_loss
)


residual_failure_loss_total = (
    tp
    * (1 - prevention_effectiveness)
    * failure_loss
)


predictive_total_cost = (
    planned_maintenance_total
    +
    unnecessary_interventions_total
    +
    missed_failure_loss_total
    +
    residual_failure_loss_total
    +
    implementation_cost
)


net_benefit = (
    reactive_total_cost
    -
    predictive_total_cost
)


operating_savings = (
    reactive_total_cost
    -
    (
        predictive_total_cost
        -
        implementation_cost
    )
)


investment = (
    planned_maintenance_total
    +
    unnecessary_interventions_total
    +
    implementation_cost
)


roi = (
    net_benefit
    / investment
    * 100
    if investment > 0
    else 0
)


cost_reduction = (
    (
        reactive_total_cost
        -
        predictive_total_cost
    )
    / reactive_total_cost
    * 100
    if reactive_total_cost > 0
    else 0
)


failure_detection_rate = (
    tp
    / (tp + fn)
    * 100
    if (tp + fn) > 0
    else 0
)


# =========================================================
# LOGO + HERO SECTION
# =========================================================

logo_col, hero_col = st.columns(
    [1, 3.7],
    vertical_alignment="center"
)

with logo_col:
    st.image(
        "logo.png",
        use_container_width=True
    )

with hero_col:
    st.markdown(
        f"""<div class="hero-box">
<div class="hero-title">Predictive Maintenance Cost-Benefit Dashboard</div>
<div class="hero-subtitle">
Interactive evaluation of predictive maintenance performance,
operational outcomes, and financial impact in smart manufacturing.
</div>
<span class="model-pill">Selected Model: <b>{selected_model}</b></span>
</div>""",
        unsafe_allow_html=True
    )


# =========================================================
# PRIMARY FINANCIAL KPI CARDS
# =========================================================

st.subheader(
    "Financial Overview"
)


k1, k2, k3, k4 = st.columns(4)


k1.metric(
    "Reactive Cost",
    f"{reactive_total_cost:,.0f} SAR"
)


k2.metric(
    "Predictive Cost",
    f"{predictive_total_cost:,.0f} SAR"
)


k3.metric(
    "Net Benefit",
    f"{net_benefit:,.0f} SAR"
)


k4.metric(
    "ROI",
    f"{roi:,.2f}%"
)


# =========================================================
# TABS
# =========================================================

(
    tab1,
    tab2,
    tab3,
    tab4,
    tab5
) = st.tabs(
    [
        "◈ Executive Overview",
        "◉ Model Analytics",
        "◇ Financial Impact",
        "△ Scenario Lab",
        "▦ Project Insights"
    ]
)


# =========================================================
# TAB 1 — EXECUTIVE OVERVIEW
# =========================================================

with tab1:

    st.subheader(
        "Executive Overview"
    )

    st.caption(
        "A concise view of the project's "
        "operational and financial outcome."
    )


    overview_left, overview_right = st.columns(
        [1.3, 1]
    )


    # -----------------------------------------------------
    # Cost comparison
    # -----------------------------------------------------

    with overview_left:

        strategy_df = pd.DataFrame(
            {
                "Strategy": [
                    "Reactive",
                    "Predictive"
                ],

                "Cost (SAR)": [
                    reactive_total_cost,
                    predictive_total_cost
                ]
            }
        )


        fig_strategy = px.bar(
            strategy_df,
            x="Strategy",
            y="Cost (SAR)",
            text="Cost (SAR)",
            color="Strategy",
            color_discrete_map={
                "Reactive": "#7196A8",
                "Predictive": TEAL
            },
            title=(
                "Reactive vs Predictive "
                "Maintenance Cost"
            )
        )


        fig_strategy.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside"
        )


        fig_strategy.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=TEXT
            ),
            showlegend=False,
            height=420
        )


        fig_strategy.update_layout(title_font=dict(color="#FFFFFF"))

        st.plotly_chart(
            fig_strategy,
            use_container_width=True
        )


    # -----------------------------------------------------
    # Insight card
    # -----------------------------------------------------

    with overview_right:

        st.markdown(
            "### Decision Insight"
        )

        st.metric(
            "Failure Detection Rate",
            f"{failure_detection_rate:.2f}%"
        )

        st.metric(
            "Cost Reduction",
            f"{cost_reduction:.2f}%"
        )

        st.metric(
            "Operating Savings",
            f"{operating_savings:,.0f} SAR"
        )


        if net_benefit > 0:

            st.success(
                "Under the selected assumptions, "
                "predictive maintenance provides "
                "a positive simulated financial benefit."
            )

        elif net_benefit < 0:

            st.warning(
                "Under the selected assumptions, "
                "predictive maintenance is not currently "
                "financially favorable."
            )

        else:

            st.info(
                "Both maintenance strategies currently "
                "produce approximately equal costs."
            )


# =========================================================
# TAB 2 — MODEL ANALYTICS
# =========================================================

with tab2:

    st.subheader(
        "Model Analytics"
    )

    st.caption(
        "Comparison of the four predictive "
        "maintenance classification models."
    )


    st.markdown(
        "### Performance Comparison"
    )


    display_performance = (
        performance_df.copy()
    )


    for metric in [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-score"
    ]:

        display_performance[metric] = (
            display_performance[metric]
            * 100
        ).round(2)


    st.dataframe(
        display_performance,
        use_container_width=True,
        hide_index=True
    )


    metric_choice = st.selectbox(
        "Compare models by metric",
        [
            "Accuracy",
            "Precision",
            "Recall",
            "F1-score"
        ]
    )


    fig_metric = px.bar(
        performance_df,
        x="Model",
        y=metric_choice,
        text=metric_choice,
        color="Model",
        color_discrete_sequence=CHART_COLORS,
        title=f"{metric_choice} Comparison"
    )


    fig_metric.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside"
    )


    fig_metric.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=TEXT
        ),
        showlegend=False,
        height=430,
        yaxis=dict(
            range=[0, 1.08]
        )
    )


    fig_metric.update_layout(title_font=dict(color="#FFFFFF"))

    st.plotly_chart(
        fig_metric,
        use_container_width=True
    )


    # -----------------------------------------------------
    # Confusion outcomes
    # -----------------------------------------------------

    st.markdown(
        f"### {selected_model} Decision Outcomes"
    )


    confusion_df = pd.DataFrame(
        {
            "Outcome": [
                "True Positive",
                "False Positive",
                "False Negative",
                "True Negative"
            ],

            "Count": [
                tp,
                fp,
                fn,
                tn
            ],

            "Meaning": [
                "Failure correctly identified",
                "Unnecessary intervention",
                "Failure missed by the model",
                "Correct no-intervention decision"
            ]
        }
    )


    st.dataframe(
        confusion_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 3 — FINANCIAL IMPACT
# =========================================================

with tab3:

    st.subheader(
        "Financial Impact"
    )

    st.caption(
        "Breakdown of the simulated financial "
        "impact of the selected predictive model."
    )


    cost_breakdown_df = pd.DataFrame(
        {
            "Component": [
                "Planned Maintenance",
                "Unnecessary Interventions",
                "Missed Failure Loss",
                "Residual Failure Loss",
                "Implementation"
            ],

            "Cost (SAR)": [
                planned_maintenance_total,
                unnecessary_interventions_total,
                missed_failure_loss_total,
                residual_failure_loss_total,
                implementation_cost
            ]
        }
    )


    fig_breakdown = px.bar(
        cost_breakdown_df,
        x="Component",
        y="Cost (SAR)",
        text="Cost (SAR)",
        color="Component",
        color_discrete_sequence=CHART_COLORS,
        title=(
            "Predictive Maintenance "
            "Cost Breakdown"
        )
    )


    fig_breakdown.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )


    fig_breakdown.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=TEXT
        ),
        showlegend=False,
        height=470
    )


    fig_breakdown.update_layout(title_font=dict(color="#FFFFFF"))

    st.plotly_chart(
        fig_breakdown,
        use_container_width=True
    )


    st.markdown(
        "### Financial Interpretation"
    )


    financial_interpretation = pd.DataFrame(
        {
            "Indicator": [
                "Reactive Maintenance Cost",
                "Predictive Maintenance Cost",
                "Net Benefit",
                "ROI",
                "Cost Reduction",
                "Failure Detection Rate"
            ],

            "Result": [
                f"{reactive_total_cost:,.2f} SAR",
                f"{predictive_total_cost:,.2f} SAR",
                f"{net_benefit:,.2f} SAR",
                f"{roi:.2f}%",
                f"{cost_reduction:.2f}%",
                f"{failure_detection_rate:.2f}%"
            ]
        }
    )


    st.dataframe(
        financial_interpretation,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 4 — SCENARIO LAB
# =========================================================

with tab4:

    st.subheader(
        "Scenario Lab"
    )

    st.caption(
        "Explore how maintenance effectiveness "
        "changes the financial outcome."
    )


    sensitivity_rows = []


    for effectiveness in np.linspace(
        0,
        1,
        21
    ):

        residual_loss_temp = (
            tp
            * (1 - effectiveness)
            * failure_loss
        )


        predictive_cost_temp = (
            planned_maintenance_total
            +
            unnecessary_interventions_total
            +
            missed_failure_loss_total
            +
            residual_loss_temp
            +
            implementation_cost
        )


        net_benefit_temp = (
            reactive_total_cost
            -
            predictive_cost_temp
        )


        sensitivity_rows.append(
            {
                "Prevention Effectiveness (%)":
                    effectiveness * 100,

                "Net Benefit (SAR)":
                    net_benefit_temp,

                "Predictive Cost (SAR)":
                    predictive_cost_temp
            }
        )


    dynamic_sensitivity_df = pd.DataFrame(
        sensitivity_rows
    )


    sensitivity_col1, sensitivity_col2 = (
        st.columns(2)
    )


    with sensitivity_col1:

        fig_net_benefit = px.line(
            dynamic_sensitivity_df,
            x="Prevention Effectiveness (%)",
            y="Net Benefit (SAR)",
            markers=True,
            title=(
                "Net Benefit vs "
                "Prevention Effectiveness"
            )
        )


        fig_net_benefit.update_traces(
            line_color=TEAL,
            marker_color=TEAL_LIGHT
        )


        fig_net_benefit.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=TEXT
            ),
            height=420
        )


        fig_net_benefit.update_layout(title_font=dict(color="#FFFFFF"))

        st.plotly_chart(
            fig_net_benefit,
            use_container_width=True
        )


    with sensitivity_col2:

        fig_predictive_cost = px.line(
            dynamic_sensitivity_df,
            x="Prevention Effectiveness (%)",
            y="Predictive Cost (SAR)",
            markers=True,
            title=(
                "Predictive Cost vs "
                "Prevention Effectiveness"
            )
        )


        fig_predictive_cost.update_traces(
            line_color="#38BFD1",
            marker_color=TEAL_LIGHT
        )


        fig_predictive_cost.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=TEXT
            ),
            height=420
        )


        fig_predictive_cost.update_layout(title_font=dict(color="#FFFFFF"))

        st.plotly_chart(
            fig_predictive_cost,
            use_container_width=True
        )


    st.markdown(
        "### Scenario Interpretation"
    )


    if net_benefit > 0:

        st.success(
            f"Using {selected_model}, the current "
            f"scenario produces a positive net benefit "
            f"of {net_benefit:,.0f} SAR."
        )

    else:

        st.warning(
            f"Using {selected_model}, the current "
            f"scenario produces a net benefit of "
            f"{net_benefit:,.0f} SAR."
        )


# =========================================================
# TAB 5 — PROJECT INSIGHTS
# =========================================================

with tab5:

    st.subheader(
        "Project Insights"
    )


    info_col1, info_col2 = st.columns(2)


    with info_col1:

        st.markdown(
            "### Dataset Information"
        )


        dataset_info = pd.DataFrame(
            {
                "Property": [
                    "Dataset",
                    "Total Records",
                    "Total Columns",
                    "Failure Cases",
                    "Non-Failure Cases",
                    "Failure Rate"
                ],

                "Value": [
                    "AI4I 2020",
                    f"{len(dataset_df):,}",
                    dataset_df.shape[1],
                    int(
                        dataset_df[
                            "Machine failure"
                        ].sum()
                    ),
                    int(
                        (
                            dataset_df[
                                "Machine failure"
                            ]
                            == 0
                        ).sum()
                    ),
                    (
                        f"{dataset_df['Machine failure'].mean()*100:.2f}%"
                    )
                ]
            }
        )


        st.dataframe(
            dataset_info,
            use_container_width=True,
            hide_index=True
        )


    with info_col2:

        st.markdown(
            "### Project Workflow"
        )


        workflow_df = pd.DataFrame(
            {
                "Stage": [
                    "1. Industrial Data",
                    "2. Data Preparation & EDA",
                    "3. Predictive Modeling",
                    "4. Model Evaluation",
                    "5. Maintenance Simulation",
                    "6. Cost-Benefit Analysis",
                    "7. Interactive Dashboard"
                ]
            }
        )


        st.dataframe(
            workflow_df,
            use_container_width=True,
            hide_index=True
        )


    st.info(
        "Financial values are scenario-based "
        "simulation assumptions. Their sources "
        "and justification should be documented "
        "in the final report."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")


st.markdown(
    """<div class="footer-box">
<div class="footer-title">Predictive Maintenance Cost-Benefit Dashboard</div>
<div>
<b>By:</b> Aleen Aloqili • Ghala Alkahtani • Lama Alsuhaibani • Hala Alhamzah
</div>
</div>""",
    unsafe_allow_html=True
)

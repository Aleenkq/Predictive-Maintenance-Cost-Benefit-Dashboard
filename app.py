import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0b1220 0%, #111827 40%, #0f172a 100%);
    color: white;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3, h4 {
    color: white !important;
}
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.25);
}
.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.25);
}
.section-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 22px;
    border-radius: 20px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.22);
    margin-bottom: 18px;
}
.hero-box {
    background: linear-gradient(135deg, rgba(14,165,233,0.20), rgba(99,102,241,0.18));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 26px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.30);
}
.small-note {
    font-size: 0.95rem;
    color: #cbd5e1;
}
hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    performance_df = pd.read_csv("model_performance_comparison.csv")
    outcomes_df = pd.read_csv("model_outcomes.csv")
    assumptions_df = pd.read_csv("simulation_assumptions.csv")
    sensitivity_df = pd.read_csv("sensitivity_analysis.csv")
    financial_df = pd.read_csv("financial_model_comparison.csv")
    dataset_df = pd.read_csv("ai4i2020.csv")
    return performance_df, outcomes_df, assumptions_df, sensitivity_df, financial_df, dataset_df

performance_df, outcomes_df, assumptions_df, sensitivity_df, financial_df, dataset_df = load_data()


# =========================================================
# DEFAULT ASSUMPTIONS
# =========================================================
default_assumptions = assumptions_df.iloc[0].to_dict()

DEFAULT_PLANNED = float(default_assumptions.get("planned_maintenance_cost", 500))
DEFAULT_UNPLANNED = float(default_assumptions.get("unplanned_repair_cost", 3000))
DEFAULT_DOWNTIME_HOURS = float(default_assumptions.get("downtime_hours", 6))
DEFAULT_DOWNTIME_COST = float(default_assumptions.get("downtime_cost_per_hour", 400))
DEFAULT_FALSE_ALARM = float(default_assumptions.get("false_alarm_cost", 250))
DEFAULT_IMPLEMENTATION = float(default_assumptions.get("implementation_cost", 10000))
DEFAULT_EFFECTIVENESS = float(default_assumptions.get("prevention_effectiveness", 0.80))


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("⚙️ Control Panel")

selected_model = st.sidebar.selectbox(
    "Select Predictive Model",
    performance_df["Model"].tolist()
)

st.sidebar.markdown("---")
st.sidebar.subheader("Financial Assumptions")

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
    step=0.05
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Tip: Change the assumptions to test how the financial results "
    "change under different maintenance conditions."
)


# =========================================================
# SELECT MODEL ROWS
# =========================================================
selected_performance = performance_df[performance_df["Model"] == selected_model].iloc[0]
selected_outcome = outcomes_df[outcomes_df["Model"] == selected_model].iloc[0]

tp = int(selected_outcome["TP"])
fp = int(selected_outcome["FP"])
fn = int(selected_outcome["FN"])
tn = int(selected_outcome["TN"])

accuracy = float(selected_performance["Accuracy"])
precision = float(selected_performance["Precision"])
recall = float(selected_performance["Recall"])
f1 = float(selected_performance["F1-score"])


# =========================================================
# FINANCIAL CALCULATIONS
# =========================================================
failure_loss = unplanned_repair_cost + (downtime_hours * downtime_cost_per_hour)

reactive_total_cost = (tp + fn) * failure_loss

planned_maintenance_total = tp * planned_cost
unnecessary_interventions_total = fp * false_alarm_cost
missed_failure_loss_total = fn * failure_loss
residual_failure_loss_total = tp * (1 - prevention_effectiveness) * failure_loss

predictive_total_cost = (
    planned_maintenance_total
    + unnecessary_interventions_total
    + missed_failure_loss_total
    + residual_failure_loss_total
    + implementation_cost
)

net_benefit = reactive_total_cost - predictive_total_cost

operating_savings = reactive_total_cost - (predictive_total_cost - implementation_cost)

investment = planned_maintenance_total + unnecessary_interventions_total + implementation_cost

roi = (net_benefit / investment * 100) if investment > 0 else 0

cost_reduction = (
    (reactive_total_cost - predictive_total_cost) / reactive_total_cost * 100
    if reactive_total_cost > 0 else 0
)

failure_detection_rate = (tp / (tp + fn) * 100) if (tp + fn) > 0 else 0


# =========================================================
# HERO
# =========================================================
st.markdown(f"""
<div class="hero-box">
    <h1 style="margin-bottom:10px;">⚙️ Predictive Maintenance Cost-Benefit Simulation Dashboard</h1>
    <p style="font-size:1.1rem; margin-bottom:6px;">
        An interactive decision-support dashboard for evaluating predictive maintenance performance,
        operational outcomes, and financial impact in smart manufacturing.
    </p>
    <p class="small-note">
        Selected Model: <b>{selected_model}</b>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("")


# =========================================================
# TOP KPI CARDS
# =========================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Reactive Cost", f"SAR {reactive_total_cost:,.0f}")
col2.metric("Predictive Cost", f"SAR {predictive_total_cost:,.0f}")
col3.metric("Net Benefit", f"SAR {net_benefit:,.0f}")
col4.metric("ROI", f"{roi:,.2f}%")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Accuracy", f"{accuracy*100:.2f}%")
col6.metric("Precision", f"{precision*100:.2f}%")
col7.metric("Recall", f"{recall*100:.2f}%")
col8.metric("F1-score", f"{f1*100:.2f}%")


# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Overview",
    "🤖 Model Analytics",
    "💰 Financial Impact",
    "🧪 Scenario Lab",
    "📁 Data & Project Insights"
])


# =========================================================
# TAB 1 - EXECUTIVE OVERVIEW
# =========================================================
with tab1:
    st.subheader("Executive Overview")

    c1, c2 = st.columns([1.2, 1])

    with c1:
        strategy_df = pd.DataFrame({
            "Strategy": ["Reactive", "Predictive"],
            "Cost (SAR)": [reactive_total_cost, predictive_total_cost]
        })

        fig_strategy = px.bar(
            strategy_df,
            x="Strategy",
            y="Cost (SAR)",
            text="Cost (SAR)",
            color="Strategy",
            color_discrete_sequence=["#ef4444", "#22c55e"],
            title="Reactive vs Predictive Maintenance Cost"
        )
        fig_strategy.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_strategy.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=420
        )
        st.plotly_chart(fig_strategy, use_container_width=True)

    with c2:
        fig_roi = go.Figure(go.Indicator(
            mode="gauge+number",
            value=roi,
            number={"suffix": "%"},
            title={"text": "Return on Investment (ROI)"},
            gauge={
                "axis": {"range": [-100, 200]},
                "bar": {"color": "#38bdf8"},
                "steps": [
                    {"range": [-100, 0], "color": "#7f1d1d"},
                    {"range": [0, 50], "color": "#365314"},
                    {"range": [50, 200], "color": "#14532d"},
                ],
            }
        ))
        fig_roi.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=420
        )
        st.plotly_chart(fig_roi, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        outcomes_pie = pd.DataFrame({
            "Outcome": ["True Positive", "False Positive", "False Negative", "True Negative"],
            "Count": [tp, fp, fn, tn]
        })

        fig_outcomes = px.pie(
            outcomes_pie,
            names="Outcome",
            values="Count",
            hole=0.55,
            title="Maintenance Decision Outcomes"
        )
        fig_outcomes.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=420
        )
        st.plotly_chart(fig_outcomes, use_container_width=True)

    with c4:
        summary_df = pd.DataFrame({
            "KPI": ["Failure Detection Rate", "Cost Reduction", "Operating Savings"],
            "Value": [
                f"{failure_detection_rate:.2f}%",
                f"{cost_reduction:.2f}%",
                f"SAR {operating_savings:,.0f}"
            ]
        })

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Key Insights")
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        if net_benefit > 0:
            st.success("Predictive maintenance is financially favorable under the selected assumptions.")
        else:
            st.warning("Predictive maintenance is not financially favorable under the selected assumptions.")
        st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# TAB 2 - MODEL ANALYTICS
# =========================================================
with tab2:
    st.subheader("Model Analytics")

    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.markdown("### Performance Comparison")
        st.dataframe(performance_df, use_container_width=True, hide_index=True)

        metric_choice = st.selectbox(
            "Select metric for comparison",
            ["Accuracy", "Precision", "Recall", "F1-score"],
            key="metric_select"
        )

        fig_metric = px.bar(
            performance_df,
            x="Model",
            y=metric_choice,
            text=metric_choice,
            color="Model",
            title=f"Model Comparison by {metric_choice}"
        )
        fig_metric.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig_metric.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=450
        )
        st.plotly_chart(fig_metric, use_container_width=True)

    with c2:
        radar_df = performance_df.copy()

        fig_radar = go.Figure()

        for _, row in radar_df.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row["Accuracy"], row["Precision"], row["Recall"], row["F1-score"]],
                theta=["Accuracy", "Precision", "Recall", "F1-score"],
                fill='toself',
                name=row["Model"]
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1])
            ),
            title="Radar View of Model Performance",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=500
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("### Selected Model Confusion Outcomes")
    conf_df = pd.DataFrame({
        "Outcome": ["TP", "FP", "FN", "TN"],
        "Count": [tp, fp, fn, tn],
        "Description": [
            "Correctly predicted failure",
            "Unnecessary maintenance",
            "Missed failure",
            "Correctly predicted normal condition"
        ]
    })
    st.dataframe(conf_df, use_container_width=True, hide_index=True)


# =========================================================
# TAB 3 - FINANCIAL IMPACT
# =========================================================
with tab3:
    st.subheader("Financial Impact")

    c1, c2 = st.columns([1.2, 1])

    with c1:
        cost_breakdown_df = pd.DataFrame({
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
        })

        fig_breakdown = px.bar(
            cost_breakdown_df,
            x="Component",
            y="Cost (SAR)",
            text="Cost (SAR)",
            color="Component",
            title="Predictive Maintenance Cost Breakdown"
        )
        fig_breakdown.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_breakdown.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=470
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)

    with c2:
        waterfall = go.Figure(go.Waterfall(
            name="Financial Impact",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "relative", "total"],
            x=[
                "Reactive Cost",
                "Planned Maint.",
                "False Alarms",
                "Missed Failures",
                "Residual Loss",
                "Predictive Cost"
            ],
            y=[
                reactive_total_cost,
                -planned_maintenance_total,
                -unnecessary_interventions_total,
                -missed_failure_loss_total,
                -residual_failure_loss_total,
                0
            ],
            textposition="outside"
        ))
        waterfall.update_layout(
            title="Financial Movement View",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=470
        )
        st.plotly_chart(waterfall, use_container_width=True)

    st.markdown("### Financial Summary Table")
    summary_financial = pd.DataFrame({
        "Metric": [
            "Reactive Maintenance Cost",
            "Predictive Maintenance Cost",
            "Operating Savings",
            "Net Benefit",
            "ROI",
            "Cost Reduction"
        ],
        "Value": [
            f"SAR {reactive_total_cost:,.2f}",
            f"SAR {predictive_total_cost:,.2f}",
            f"SAR {operating_savings:,.2f}",
            f"SAR {net_benefit:,.2f}",
            f"{roi:.2f}%",
            f"{cost_reduction:.2f}%"
        ]
    })
    st.dataframe(summary_financial, use_container_width=True, hide_index=True)


# =========================================================
# TAB 4 - SCENARIO LAB
# =========================================================
with tab4:
    st.subheader("Scenario Lab")

    st.write(
        "This section shows how the financial outcome changes when the "
        "failure prevention effectiveness changes."
    )

    sensitivity_rows = []
    for eff in np.linspace(0, 1, 21):
        residual = tp * (1 - eff) * failure_loss
        predictive_cost_temp = (
            planned_maintenance_total
            + unnecessary_interventions_total
            + missed_failure_loss_total
            + residual
            + implementation_cost
        )
        net_benefit_temp = reactive_total_cost - predictive_cost_temp

        sensitivity_rows.append({
            "Prevention Effectiveness": eff,
            "Net Benefit (SAR)": net_benefit_temp,
            "Predictive Cost (SAR)": predictive_cost_temp
        })

    sensitivity_dynamic_df = pd.DataFrame(sensitivity_rows)

    c1, c2 = st.columns(2)

    with c1:
        fig_sens_nb = px.line(
            sensitivity_dynamic_df,
            x="Prevention Effectiveness",
            y="Net Benefit (SAR)",
            markers=True,
            title="Net Benefit vs Prevention Effectiveness"
        )
        fig_sens_nb.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=420
        )
        st.plotly_chart(fig_sens_nb, use_container_width=True)

    with c2:
        fig_sens_pc = px.line(
            sensitivity_dynamic_df,
            x="Prevention Effectiveness",
            y="Predictive Cost (SAR)",
            markers=True,
            title="Predictive Cost vs Prevention Effectiveness"
        )
        fig_sens_pc.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=420
        )
        st.plotly_chart(fig_sens_pc, use_container_width=True)

    st.markdown("### Scenario Interpretation")
    if net_benefit > 0:
        st.success(
            f"Using {selected_model}, predictive maintenance currently achieves "
            f"a positive net benefit of SAR {net_benefit:,.0f}."
        )
    else:
        st.error(
            f"Using {selected_model}, predictive maintenance currently results "
            f"in a negative net benefit of SAR {net_benefit:,.0f}."
        )


# =========================================================
# TAB 5 - DATA & PROJECT INSIGHTS
# =========================================================
with tab5:
    st.subheader("Data & Project Insights")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Dataset Snapshot")
        st.dataframe(dataset_df.head(10), use_container_width=True)

    with c2:
        st.markdown("### Dataset Information")
        info_df = pd.DataFrame({
            "Property": [
                "Total Records",
                "Total Columns",
                "Failure Cases",
                "Non-Failure Cases"
            ],
            "Value": [
                len(dataset_df),
                dataset_df.shape[1],
                int(dataset_df["Machine failure"].sum()),
                int((dataset_df["Machine failure"] == 0).sum())
            ]
        })
        st.dataframe(info_df, use_container_width=True, hide_index=True)

    st.markdown("### Raw Exported Results")
    st.write("Financial model comparison")
    st.dataframe(financial_df, use_container_width=True)

    st.caption(
        "Note: Financial values are scenario-based assumptions and should be "
        "properly justified with references in the final report."
    )
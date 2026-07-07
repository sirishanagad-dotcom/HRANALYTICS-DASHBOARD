import streamlit as st
import pandas as pd
import plotly.express as px


# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)


# -------------------------------
# LOAD EXCEL FILES
# -------------------------------

@st.cache_data
def load_data():

    employees = pd.read_excel("Employees.xlsx")

    attendance = pd.read_excel("Attendance.xlsx")

    performance = pd.read_excel("Performance.xlsx")

    attrition = pd.read_excel("Attrition.xlsx")


    # Merge tables

    df = employees.merge(attendance,on="EmployeeID",how="left")

    df = df.merge(performance, on="EmployeeID",how="left" )

    df = df.merge(attrition, on="EmployeeID", how="left" )


    return df



df = load_data()



# -------------------------------
# TITLE
# -------------------------------

st.title("📊 HR Analytics Dashboard")



# -------------------------------
# SIDEBAR SLICERS
# -------------------------------

st.sidebar.header("Dashboard Filters")


department = st.sidebar.multiselect("Department",df["Department"].dropna().unique())


jobrole = st.sidebar.multiselect("Job Role",df["JobRole"].dropna().unique())


gender = st.sidebar.multiselect("Gender",df["Gender"].dropna().unique())


city = st.sidebar.multiselect("City",df["City"].dropna().unique())


review_year = st.sidebar.multiselect("Review Year",df["ReviewYear"].dropna().unique())


attrition_status = st.sidebar.multiselect("Attrition Status", df["AttritionStatus"].dropna().unique())



# -------------------------------
# APPLY FILTERS
# -------------------------------

filtered_df = df.copy()


if department:
    filtered_df = filtered_df[filtered_df["Department"].isin(department)]


if jobrole:
    filtered_df = filtered_df[ filtered_df["JobRole"].isin(jobrole)]


if gender:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender)]


if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]


if review_year:
    filtered_df = filtered_df[filtered_df["ReviewYear"].isin(review_year)]


if attrition_status:
    filtered_df = filtered_df[filtered_df["AttritionStatus"].isin(attrition_status)]



# -------------------------------
# KPI CARDS
# -------------------------------

total_employee = filtered_df["EmployeeID"].nunique()

average_salary = filtered_df["Salary"].mean()

average_rating = filtered_df["Rating"].mean()


attrition_rate = (filtered_df["AttritionStatus"].value_counts(normalize=True).get("Yes",0) *100)



c1,c2,c3,c4 = st.columns(4)


c1.metric( "Total Employees",total_employee)


c2.metric("Average Salary", f"{average_salary:,.0f}")


c3.metric("Average Rating", round(average_rating,2))


c4.metric("Attrition %", round(attrition_rate,2))



# -------------------------------
# EMPLOYEE ANALYSIS
# -------------------------------

st.header("Employee Analysis")


col1,col2 = st.columns(2)


department_count = (filtered_df.groupby("Department") ["EmployeeID"] .nunique() .reset_index())



fig = px.bar(department_count, x="Department", y="EmployeeID", title="Employees by Department")


col1.plotly_chart(fig, use_container_width=True)



gender_count = (filtered_df["Gender"].value_counts().reset_index())


gender_count.columns=["Gender", "Count"]


fig = px.pie(gender_count,names="Gender",values="Count", title="Gender Distribution")


col2.plotly_chart(fig,use_container_width=True)



# -------------------------------
# ATTENDANCE ANALYSIS
# -------------------------------

st.header("Attendance Analysis")


col1,col2 = st.columns(2)



attendance_status = (filtered_df["Status"].value_counts().reset_index())


attendance_status.columns=["Status", "Count"]



fig = px.pie(attendance_status,names="Status",values="Count",title="Present vs Absent")


col1.plotly_chart(fig,use_container_width=True)



attendance_department = (filtered_df.groupby("Department")["Status"].apply( lambda x:(x=="Present").mean()*100).reset_index()
)



attendance_department.columns=["Department","Attendance %"]



fig = px.bar(attendance_department,x="Department",y="Attendance %",title="Attendance Percentage")


col2.plotly_chart(fig,use_container_width=True)



# -------------------------------
# PERFORMANCE ANALYSIS
# -------------------------------

st.header("Performance Analysis")


col1,col2 = st.columns(2)



fig = px.histogram(filtered_df,x="Rating",title="Performance Rating Distribution")


col1.plotly_chart(fig,use_container_width=True)



avg_rating_department = (filtered_df.groupby("Department")["Rating"].mean().reset_index())



fig = px.bar(avg_rating_department,x="Department",y="Rating",title="Average Rating by Department")


col2.plotly_chart(fig,use_container_width=True)



# -------------------------------
# BONUS ANALYSIS
# -------------------------------

st.header("Bonus Analysis")


fig = px.scatter(filtered_df,x="Rating",y="Bonus",color="Department",title="Performance Rating vs Bonus")


st.plotly_chart(fig,use_container_width=True)



# -------------------------------
# ATTRITION ANALYSIS
# -------------------------------

st.header("Attrition Analysis")


attrition_chart = pd.crosstab(filtered_df["Department"],filtered_df["AttritionStatus"]
)



fig = px.bar(attrition_chart,barmode="group",title="Attrition by Department")


st.plotly_chart(fig,use_container_width=True)



# -------------------------------
# DATA TABLE
# -------------------------------

st.header("Employee Details")


st.dataframe(filtered_df,use_container_width=True)
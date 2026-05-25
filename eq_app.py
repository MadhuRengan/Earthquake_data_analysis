import streamlit as st
import pymysql
import pandas as pd

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="madhu.1723",
        database="gst"
    )

def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return pd.DataFrame(rows, columns=columns)

st.title("🌍 earthquake data analysis dashboard")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "magnitude & depth", 
    "time analysis", 
    "casualties",
    "event type & quality metrics",
    "tsunami & alerts",
    "seismic patterns & trend analysis",
    "depth, location & distance-based analysis"
])


with tab1:
    st.header("magnitude & depth")
    option = st.radio("choose a query:", [
        "top 10 strongest earthquakes",
        "top 10 deepest earthquakes",
        "shallow earthquakes < 50 km and mag > 7.5",
        "average depth per continent",
        "average magnitude per magnitude type"
    ])

    if option == "top 10 strongest earthquakes":
        df = run_query("select id, place, mag from earthquake_data order by mag desc limit 10;")
        st.table(df.style.hide(axis="index"))

    elif option == "top 10 deepest earthquakes":
        df = run_query("select id, place, depth_km from earthquake_data order by depth_km desc limit 10;")
        st.table(df.style.hide(axis="index"))

    elif option == "shallow earthquakes < 50 km and mag > 7.5":
        df = run_query("select id, place, mag, depth_km, flag_based_on_depth from earthquake_data where depth_km < 50 and mag > 7.5;")
        st.table(df.style.hide(axis="index"))

    elif option == "average depth per continent":
        df = run_query("select round(avg(depth_km),3) as avg_depth, place from earthquake_data group by place;")
        st.table(df.style.hide(axis="index"))

    elif option == "average magnitude per magnitude type":
        df = run_query("select round(avg(mag),3) as avg_magnitude, magtype from earthquake_data group by magtype;")
        st.table(df.style.hide(axis="index"))


with tab2:
    st.header("time analysis")
    option = st.radio("choose a query:", [
        "year with most earthquakes",
        "month with highest number of earthquakes",
        "day of week with most earthquakes",
        "count of earthquakes per hour of day",
        "most active reporting network"
    ])

    if option == "year with most earthquakes":
        df = run_query("select year, count(id) as earthquake_count from earthquake_data group by year order by earthquake_count desc limit 1;")
        st.table(df.style.hide(axis="index"))

    elif option == "month with highest number of earthquakes":
        df = run_query("select month, count(id) as earthquake_count from earthquake_data group by month order by earthquake_count desc limit 1;")
        st.table(df.style.hide(axis="index"))

    elif option == "day of week with most earthquakes":
        df = run_query("select day_of_week, count(id) as earthquake_count from earthquake_data group by day_of_week order by earthquake_count desc limit 1;")
        st.table(df.style.hide(axis="index"))

    elif option == "count of earthquakes per hour of day":
        df = run_query("select hour(time) as hour, count(id) as eq_count from earthquake_data group by hour order by hour;")
        st.table(df.style.hide(axis="index"))

    elif option == "most active reporting network":
        df = run_query("select count(net) as report_count, net from earthquake_data group by net order by report_count desc limit 1;")
        st.table(df.style.hide(axis="index"))


with tab3:
    st.header("casualties")
    option = st.radio("choose a query:", ["top 5 places with highest casualties"])
    if option == "top 5 places with highest casualties":
        df = run_query("select place, sum(felt) as casualties from earthquake_data group by place order by casualties desc limit 5;")
        st.table(df.style.hide(axis="index"))


with tab4:
    st.header("event type & quality metrics")
    option = st.radio("choose a query:", [
        "count of reviewed vs automatic earthquakes",
        "count by earthquake type",
        "number of earthquakes by data type",
        "average rms and gap per continent",
        "events with high station coverage"
    ])

    if option == "count of reviewed vs automatic earthquakes":
        df = run_query("select count(id) as count, status from earthquake_data group by status;")
        st.table(df.style.hide(axis="index"))

    elif option == "count by earthquake type":
        df = run_query("select count(id) as count, type from earthquake_data group by type;")
        st.table(df.style.hide(axis="index"))

    elif option == "number of earthquakes by data type":
        df = run_query("select count(id) as count, types from earthquake_data group by types;")
        st.table(df.style.hide(axis="index"))

    elif option == "average rms and gap per continent":
        df = run_query("select round(avg(rms),3) as avg_rms, round(avg(gap),3) as avg_gap, place from earthquake_data group by place;")
        st.table(df.style.hide(axis="index"))

    elif option == "events with high station coverage":
        df = run_query("select id, nst, place, type from earthquake_data where nst > 79;")
        st.table(df.style.hide(axis="index"))


with tab5:
    st.header("tsunami & alerts")
    option = st.radio("choose a query:", [
        "number of tsunamis triggered per year",
        "count earthquakes by alert levels"
    ])

    if option == "number of tsunamis triggered per year":
        df = run_query("select year, count(*) as tsunami_count from earthquake_data where tsunami = 1 group by year order by year;")
        st.table(df.style.hide(axis="index"))

    elif option == "count earthquakes by alert levels":
        df = run_query("select alert, count(id) as count from earthquake_data group by alert;")
        st.table(df.style.hide(axis="index"))


with tab6:
    st.header("seismic patterns & trend analysis")
    option = st.radio("choose a query:", [
        "top 5 countries with highest avg magnitude (past 5 years)",
        "countries with both shallow & deep earthquakes in same month",
        "year-over-year growth rate globally",
        "3 most seismically active regions"
    ])

    if option == "top 5 countries with highest avg magnitude (past 5 years)":
        df = run_query("select round(avg(mag),2) as mag_avg, place from earthquake_data group by place order by avg(mag) desc limit 5;")
        st.table(df.style.hide(axis="index"))

    elif option == "countries with both shallow & deep earthquakes in same month":
        df = run_query("select place, month from earthquake_data group by place, month having sum(case when flag_based_on_depth = 'shallow' then 1 else 0 end) > 1 and sum(case when flag_based_on_depth = 'deep' then 1 else 0 end) > 1;")
        st.table(df.style.hide(axis="index"))

    elif option == "year-over-year growth rate globally":
        df = run_query("select year, count(id) as event_count, round((count(id) - lag(count(id)) over (order by year)) / lag(count(id)) over (order by year) * 100, 2) as growth_rate from earthquake_data group by year order by year;")
        st.table(df.style.hide(axis="index"))

    elif option == "3 most seismically active regions":
        df = run_query("select place, round(avg(mag),2) as mag, count(id) as frequency, round(avg(mag)*count(id)) as seismic_score from earthquake_data group by place order by seismic_score desc limit 3;")
        st.table(df.style.hide(axis="index"))

with tab7:
    st.header("depth, location & distance-based analysis")

    option = st.radio("choose a query:", [
        "avg depth within ±5° latitude of equator",
        "highest ratio shallow:deep earthquakes",
        "avg magnitude difference tsunami vs non-tsunami",
        "lowest data reliability (gap + rms)",
        "pairs of consecutive earthquakes within 50 km & 1 hour",
        "regions with highest frequency of deep-focus earthquakes"
    ])

    if option == "avg depth within ±5° latitude of equator":
        df = run_query("select place, round(avg(depth_km),2) as avg_depth from earthquake_data where latitude between -5 and 5 group by place;")
        st.table(df.style.hide(axis="index"))

    elif option == "highest ratio shallow:deep earthquakes":
        df = run_query("select place, (sum(case when flag_based_on_depth = 'shallow' then 1 else 0 end) / nullif(sum(case when flag_based_on_depth = 'deep' then 1 else 0 end),0)) as ratio from earthquake_data group by place order by ratio desc limit 10;")
        st.table(df.style.hide(axis="index"))

    elif option == "avg magnitude difference tsunami vs non-tsunami":
        df = run_query("select round(avg(case when tsunami = 0 then mag end),3) as avg_mag_no_tsunami, round(avg(case when tsunami = 1 then mag end),3) as avg_mag_tsunami, round((avg(case when tsunami = 0 then mag end) - avg(case when tsunami = 1 then mag end)),3) as difference from earthquake_data;")
        st.table(df.style.hide(axis="index"))

    elif option == "lowest data reliability (gap + rms)":
        df = run_query("select id, place, gap, rms, 1.0 / (1 + (gap/180.0) + rms) as reliability_score from earthquake_data order by reliability_score limit 10;")
        st.table(df.style.hide(axis="index"))

    elif option == "pairs of consecutive earthquakes within 50 km & 1 hour":
        df = run_query("select * from (select id, time, latitude, longitude, lag(id) over (order by time) as prev_id, lag(time) over (order by time) as prev_time, lag(latitude) over (order by time) as prev_latitude, lag(longitude) over (order by time) as prev_longitude from earthquake_data) t having timestampdiff(minute, t.prev_time, t.time) <= 60 and abs(t.latitude - t.prev_latitude) <= 0.5 and abs(t.longitude - t.prev_longitude) <= 0.5;")
        st.table(df.style.hide(axis="index"))

    elif option == "regions with highest frequency of deep-focus earthquakes":
        df = run_query("select place, count(id) as frequency from earthquake_data where depth_km > 300 group by place order by frequency desc limit 10;")
        st.table(df.style.hide(axis="index"))

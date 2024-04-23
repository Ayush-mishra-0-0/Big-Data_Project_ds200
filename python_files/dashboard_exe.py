import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title="EXE File Analysis", page_icon=":gear:", layout="wide")

st.title(" :bar_chart: EXE File Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)



fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(fl, encoding="ISO-8859-1")  
else:
    df = pd.read_csv("/mnt/c/users/ayush/Project/detection_models/exe/data.csv",sep='|', encoding="ISO-8859-1")


# Display the data
st.write(df.head())

# Sidebar filters
st.sidebar.header("Filters")
# Add sidebar filters for interactive filtering of data
st.sidebar.header("Choose your filter: ")
# Create for Region
region = st.sidebar.multiselect("Pick your type of file", df["Machine"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Machine"].isin(region)]


# Histogram of SizeOfCode
st.subheader("Histogram of SizeOfCode")
hist_fig = px.histogram(df, x="SizeOfCode", nbins=20)
st.plotly_chart(hist_fig)

# Scatter plot of SizeOfCode vs SizeOfOptionalHeader
st.subheader("Scatter Plot: SizeOfCode vs SizeOfOptionalHeader")
scatter_fig = px.scatter(df, x="SizeOfCode", y="SizeOfOptionalHeader", color="Machine", size="SizeOfInitializedData",
                         hover_data=["Name"], title="SizeOfCode vs SizeOfOptionalHeader")
st.plotly_chart(scatter_fig)

# Line chart of MajorLinkerVersion over Name
st.subheader("Line Chart: MajorLinkerVersion over Name")
line_fig = px.line(df, x="Name", y="MajorLinkerVersion", title="MajorLinkerVersion over Name")
st.plotly_chart(line_fig)

# Box plot of Characteristics grouped by Machine
st.subheader("Box Plot: Characteristics by Machine")
box_fig = px.box(df, x="Machine", y="Characteristics", title="Characteristics by Machine")
st.plotly_chart(box_fig)

# Bar chart of MajorSubsystemVersion by Machine
st.subheader("Bar Chart: MajorSubsystemVersion by Machine")
bar_fig = px.bar(df, x="Machine", y="MajorSubsystemVersion", color="Machine", title="MajorSubsystemVersion by Machine")
st.plotly_chart(bar_fig)

# Treemap of SizeOfCode by Name
# st.subheader("Treemap: SizeOfCode by Name")
# treemap_fig = px.treemap(df, path=["Name"], values="SizeOfCode", title="SizeOfCode by Name")
# st.plotly_chart(treemap_fig)

# Radar chart of SizeOfOptionalHeader, SizeOfInitializedData, SizeOfUninitializedData by Machine
st.subheader("Radar Chart: Size Metrics by Machine")
radar_fig = go.Figure()
radar_fig.add_trace(go.Scatterpolar(
    r=df[df["Machine"] == 332][["SizeOfOptionalHeader", "SizeOfInitializedData", "SizeOfUninitializedData"]].mean(),
    theta=["SizeOfOptionalHeader", "SizeOfInitializedData", "SizeOfUninitializedData"],
    fill='toself',
    name='Machine 332'
))
radar_fig.add_trace(go.Scatterpolar(
    r=df[df["Machine"] == 224][["SizeOfOptionalHeader", "SizeOfInitializedData", "SizeOfUninitializedData"]].mean(),
    theta=["SizeOfOptionalHeader", "SizeOfInitializedData", "SizeOfUninitializedData"],
    fill='toself',
    name='Machine 224'
))
radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True,)),
                        title="Size Metrics by Machine",
                        showlegend=True)
st.plotly_chart(radar_fig)

# Download data button
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Data", data=csv_data, file_name="exe_file_data.csv", mime="text/csv")

# Display raw data
st.subheader("Raw Data")
st.write(df)

# Download original dataset
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Raw Data", data=csv, file_name="Raw_Data.csv", mime="text/csv")

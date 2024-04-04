import streamlit as st
import pandas as pd
import os
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Project!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(fl, encoding="ISO-8859-1")  
else:
    os.chdir(r"/mnt/c/users/ayush/Project/python_files/")
    df = pd.read_csv("data.csv", encoding="ISO-8859-1")

st.write(df.head())  

col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date 
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))



def color_by_range(val):
    if val < 500:
        color = 'lightyellow'
    elif 500 <= val < 1000:
        color = 'orange'
    elif 1000 <= val < 1500:
        color = 'lightgreen'
    elif 1500 <= val < 2000:
        color = 'blue'
    else:
        color = 'lightblue'
    
    return f'background-color: {color}; color: black'


st.sidebar.header("Choose your filter: ")
# Create for Region
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# Create for State
state = st.sidebar.multiselect("Pick the State", df2["Province"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["Province"].isin(state)]

category_df = df.groupby(by=["Product Category"], as_index=False)["Sales"].sum()

with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x="Product Category", y="Sales", text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)
with col2:
    st.subheader("Region wise Sales")
    fig = px.pie(df, values="Sales", names="Region", hole=0.5)
    fig.update_traces(text=df["Region"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Product Category_ViewData"):
        st.write(category_df)  # Display DataFrame without background gradient
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="productCategory.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("Region_ViewData"):
        region = df.groupby(by="Region", as_index=False)["Sales"].sum()
        st.write(region)  # Display DataFrame without background gradient
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')



# Create a treem based on Region, category, sub-Category
st.subheader("Hierarchical view of Sales using TreeMap")
fig3 = px.treemap(df, path=["Region", "Product Category", "Product Sub-Category"], values="Sales", hover_data=["Sales"],
                  color="Product Sub-Category")
fig3.update_layout(width=800, height=650)
st.plotly_chart(fig3, use_container_width=True)


      
df["month_year"] = df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')

linechart = pd.DataFrame(df.groupby(df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')



chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(df, values = "Sales", names = "Customer Segment", template = "plotly_dark")
    fig.update_traces(text = df["Customer Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(df, values = "Sales", names = "Product Category", template = "gridon")
    fig.update_traces(text = df["Product Category"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)


import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region","Province","Product Category","Sales","Profit","Order Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Viridis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month wise sub-Category Table")
    df["month"] = df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = df, values = "Sales", index = ["Product Sub-Category"],columns = "month")
    # st.write(sub_category_Year.style.background_gradient())
    styled_df = sub_category_Year.style.applymap(color_by_range)
    st.write(styled_df)



def color_by_range(val):
    if isinstance(val, str):  # Skip strings
        return ''
    elif val < 500:
        return 'color: red'
    else:
        return 'color: green'

# Create a scatter plot
data1 = px.scatter(df, x = "Sales", y = "Profit", size = "Order Quantity")
data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

with st.expander("View Data"):
    styled_df = df.iloc[:500, 1:20:2]
    st.write(styled_df)

# Download original DataSet
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")
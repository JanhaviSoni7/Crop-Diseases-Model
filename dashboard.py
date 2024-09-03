import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Dashboard",page_icon=":bar_chart:",layout="wide")
st.subheader(":bar_chart: Crops in India and Diseases")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)

# Load the dataset
df = pd.read_csv('crop_disease_data.csv', encoding='ISO-8859-1')

#sidebar
st.sidebar.header("Choose your filter: ",'<style>div.block-container{padding-top:3rem;}</style>')

region = st.sidebar.multiselect("Region",df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

state = st.sidebar.multiselect("State",df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

crop = st.sidebar.multiselect("Crop Type",df3["Crop Type"].unique())
if not crop:
    df4 = df3.copy()
else:
    df4 = df3[df3["Crop Type"].isin(crop)]

disease = st.sidebar.multiselect("Disease",df4["Disease"].unique())

if not region and not state and not crop and not disease:
    filtered_df = df
elif region and not state and not crop and not disease:
    filtered_df = df[df["Region"].isin(region)]
elif not region and state and not crop and not disease:
    filtered_df = df[df["State"].isin(state)]
elif not region and not state and crop and not disease:
    filtered_df = df[df["Crop Type"].isin(crop)]
elif not region and not state and not crop and disease:
    filtered_df = df[df["Disease"].isin(disease)]
elif region and state and not crop and not disease:
    filtered_df = df4[df["Region"].isin(region) & df["State"].isin(state)]
elif region and not state and crop and not disease:
    filtered_df = df4[df["Region"].isin(region) & df["Crop Type"].isin(crop)]
elif region and not state and not crop and disease:
    filtered_df = df4[df["Region"].isin(region) & df["Disease"].isin(disease)]
elif not region and state and crop and not disease:
    filtered_df = df4[df["State"].isin(state) & df["Crop Type"].isin(crop)]
elif not region and state and not crop and disease:
    filtered_df = df4[df["State"].isin(state) & df["Disease"].isin(disease)]
elif not region and not state and crop and disease:
    filtered_df = df4[df["Crop Type"].isin(crop) & df["Disease"].isin(disease)]
elif region and state and crop and not disease:
    filtered_df = df4[df["Region"].isin(region) & df["State"].isin(state) & df["Crop Type"].isin(crop)]
elif region and state and not crop and disease:
    filtered_df = df4[df["Region"].isin(region) & df["State"].isin(state) & df["Disease"].isin(disease)]
elif region and not state and crop and disease:
    filtered_df = df4[df["Region"].isin(region) & df["Crop Type"].isin(crop) & df["Disease"].isin(disease)]
elif not region and state and crop and disease:
    filtered_df = df4[df["State"].isin(state) & df["Crop Type"].isin(crop) & df["Disease"].isin(disease)]
else:
    filtered_df = df4[df4["Region"].isin(region) & df4["State"].isin(state) & df4["Crop Type"].isin(crop) & df4["Disease"].isin(disease)]

#visuals
col1, col2 = st.columns((2))
with col1:
    fig = px.bar(filtered_df, x='Crop Type', y='Total Yield in a Year (tons/ha)', title='Cropwise Yield In a Year')
    st.plotly_chart(fig,use_container_width=True)
with col2:
    fig = px.pie(filtered_df, names='Crop Type', title='Diseases by Crop Type', hole=0.5)
    fig.update_traces(text = filtered_df["Crop Type"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)
with st.expander("View Data"):
        st.write(filtered_df.style.background_gradient(cmap="BrBG"))
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data=csv,file_name="Filtered_Data.csv",mime="text/csv",help="Click here to download the data as a CSV file")
fig = px.bar(filtered_df, x='Region', y='Disease', color='Disease', 
             title='Top Diseases by Region', barmode='stack')
st.plotly_chart(fig, use_container_width=True)

corr = filtered_df[['Max Temp (°C)', 'Min Temp (°C)', 'Relative Humidity (%)', 
                    'Rainfall (mm)', 'Wind Speed (kmph)', 'Total Yield in a Year (tons/ha)']].corr()

fig = px.imshow(corr, text_auto=True, title='Correlation Heatmap of Environmental Factors')
st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns((2))
with col3:
    fig = px.scatter(filtered_df, x='Rainfall (mm)', y='Total Yield in a Year (tons/ha)', color='Crop Type', 
                     title='Rainfall vs. Crop Yield',  hover_data=['Region', 'State'])
    st.plotly_chart(fig, use_container_width=True)
with col4:
    fig = px.scatter(filtered_df, x='Max Temp (°C)', y='Total Yield in a Year (tons/ha)', color='Crop Type', 
                     title='Max Temperature vs. Crop Yield',  hover_data=['Region', 'State'])
    st.plotly_chart(fig, use_container_width=True)
col5, col6 = st.columns((2))
with col5:
    fig = px.sunburst(filtered_df, path=['Region', 'State', 'Crop Type', 'Disease'], values='Total Yield in a Year (tons/ha)', 
                      title='Hierarchical View of Crop Data by Region and State')
    st.plotly_chart(fig, use_container_width=True)
with col6:
    fig = px.line(filtered_df, x='Season', y='Total Yield in a Year (tons/ha)', color='Crop Type', 
                  title='Seasonal Yield Trends by Crop Type', markers=True)
    st.plotly_chart(fig, use_container_width=True)


fig = px.treemap(filtered_df,path=['Soil Requirements', 'Water Requirement', 'Crop Type'], values='Total Yield in a Year (tons/ha)', 
                 title='Soil and Water Requirements by Crop Type')
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### **Disease Details**")
st.dataframe(filtered_df[['Disease', 'Pathogens', 'Recommended Practices', 'Treatments']])




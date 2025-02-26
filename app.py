from fileinput import filename
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data sweeper" , layout='wide')

#custom css
st.markdown(
    """
    <style>
    st.App{
      backgruond-color: black;
      color: white;
    }
     </style>
      
      """,


      unsafe_allow_html=True
)

#title   $   description
st.title("DATA STERLING INTEGRATOR BY AREESHA ANWAR")
st.write("Transform your files between CSV and Excel formate with built-in data cleaning and visualization creating the project for quarter 3!")

#file uploader
Uploaded_files = st.file_uploader("Uploade your files (Accepts CSV and Excel):" , type=["Csv" , "Xlsx"] , accept_multiple_files=(True))

if Uploaded_files:
    for file in Uploaded_files:
      file_ext = os.path.splitext(file.name)[-1].lower()
      
      if file_ext == ".csv":
                df = pd.read_csv(file)
      elif file_ext == "xlsx" :
                df = pd.read_excel(file)
      else:
            st.error(f"unsupported file type: {file_ext}")
      continue

      #file detailes
      st.write("preview the head of the Dataframe")
      st.dataframe(df.head())

      #data cleaning

      st.subheader("Data cleaning options")
      st.checkbox(f"cleaning data for{file.name}")
    col1 , col2 = st.columns(2)
      
    with col1:
               if st.button(f"Remove duplicates from the file {file.name}"):
                      df.drop_duplicates(inplace=True)
                      st.write("Duplicates remove!")
    with col2:
              if  st.button(f"fill missing values for {file.name}") :
                      numeric_col = df.select_dtypes(include=["number"]).columns
                      df[numeric_col] = df[numeric_col].fillna(df[numeric_col].mean())
                      st.write("Missing values have been filled!")

    st.subheader("Select columns to keep")
    columns = st.multiselect(f"choose columns for {file.name}",df.columns, default=df.columns)
    df=df[columns]

    #Data visualization
    st.subheader("Data visualization")
    if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

    #conversion option

    st.subheader("conversion option")
    conversion_type = st.audio(f"convert {file.name} to:" ,["CSV" , "Excel"], key=file.name)
    if st.button(f"convert{file.name}"):
            Buffer=BytesIO()
            if conversion_type == "CSV":
                    df.to.to_csv(Buffer , index=False)
                    filename == file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
            elif conversion_type == "Excel":
                    df.to.to_excel(Buffer , index=False)
                    filename == file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformates-officedocument.spreadsheetml.sheet"      
            Buffer.seek(0)

            st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=Buffer,
                    file_name=filename,
                    mime=mime_type
            )

st.success("All files processed successfully!")          
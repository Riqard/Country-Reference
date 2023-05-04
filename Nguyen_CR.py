# -*- coding: utf-8 -*-
"""

@author: Richard Nguyen

"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import webbrowser
from PIL import Image
import zipfile as zp

#unzip the files being used
zpName='Nguyen_FP_Data.zip'
zpfile= zp.ZipFile(zpName,'r').extractall()

#sets page title
st.set_page_config(
        page_title="Country Reference Guide")

# make sidebar menu to switch datasets
with st.sidebar:
    selected = option_menu(
        menu_title='Main Menu',
        options=['Home',"Economy",'Human Development Index','Manufacturing','Military Ependiture','Population'], 
        icons=['house','currency-dollar','mortarboard', 'building' , 'cash-coin', 'people-fill']
        
        )


#MAIN CODE: MAKE DATA CHARTS AND TABLES#------------------------------------------------------------------------------------------------------------------------------------------------

def show_Data(data,cntry1,cntry2,rng1,rng2,yr1,mesr1,mesr2,txt1,txt2):
    
    # header for each data set
    st.header(txt2)
    
    #import the data being defined
    df=data
    
    #Choose what countries you want to examine (Defaulted to China and US)
    countries = st.multiselect("Choose Countries", list(df.index),[cntry1, cntry2])
    countryDB=df.T[countries]
    
    #Choose the range of years to examine (Defaulted to Minimum and Maximum)
    yR = st.slider('Please select a Range of Years',rng1, rng2,(rng1, rng2))
    
    #Creates ranged specified data and displays the data
    rCountryDB=countryDB[str(min(yR)):str(max(yR))]
    st.write(mesr1, rCountryDB.T)
    #Download Main Data
    df1=rCountryDB.T.to_csv().encode('utf-8')
    st.download_button(label='Download Data as CSV',data=df1,file_name=f'{txt2}{countries}{str(min(yR))}-{str(max(yR))}.csv',mime='text/csv')
    

    #Displays Total Percent Change for range
    totPerChange=pd.DataFrame()
    totPerChange[f'{str(min(yR))} - {str(max(yR))}']=rCountryDB.T.apply(lambda row: str((((row.iloc[-1] - row.iloc[0])/row.iloc[0])*100).round(2))+'%', axis=1)
    st.write('\n')
    st.write(f'Total Percent Change for {txt2} from {str(min(yR))} to {str(max(yR))}')
    col1, col2 =st.columns([2,1],gap='large')
    with col1:
        st.dataframe(totPerChange,use_container_width=True)
    with col2:
        "\n"
        "\n"
        #Download DF % Change
        st.download_button(label='Download Data as CSV',data=totPerChange.to_csv().encode('utf-8'),file_name=f'TotPctChange{countries}_{str(min(yR))}-{str(max(yR))}.csv',mime='text/csv')
            
            
    #plots data and interactive map
    plotLine=px.line(rCountryDB, labels={'index':'Years','value':mesr2,'Country':'Countries'}, title=f'Line Chart of {txt2} from {str(min(yR))} to {str(max(yR))}')
    plotScatr=px.scatter(rCountryDB, labels={'index':'Years','value':mesr2,'Country':'Countries'}, title=f'Scatter Chart of {txt2} from {str(min(yR))} to {str(max(yR))}')
    plotArea=px.area(rCountryDB, labels={'index':'Years','value':mesr2,'Country':'Countries'}, title=f'Area Chart of {txt2} from {str(min(yR))} to {str(max(yR))}')
    plotBar=px.bar(rCountryDB, labels={'index':'Years','value':mesr2,'Country':'Countries'}, title=f'Bar Chart of {txt2} from {str(min(yR))} to {str(max(yR))}')

    charts=st.radio('Which Chart do you want to See?',('Line','Scatter','Area','Bar'))
    if charts=='Line':
        st.plotly_chart(plotLine)
    if charts=='Scatter':
        st.plotly_chart(plotScatr)
    if charts=='Area':
        st.plotly_chart(plotArea)
    if charts=='Bar':
        st.plotly_chart(plotBar)
    
    # Start of annual percent change section
    st.divider()
            
    #Displays percent change
    st.subheader(f'Annual Percent Change for {txt2} from {str(min(yR))} to {str(max(yR))}')
    perChange = (rCountryDB.T.pct_change(axis='columns')*100)
    perChangeStr=perChange.round(2).astype(str)+'%'
    perChangeStr
    
    # download annual percent change as csv
    st.download_button(label='Download Data as CSV',data=perChange.to_csv().encode('utf-8'),file_name=f'AnnualPctChange{countries}_{str(min(yR))}-{str(max(yR))}.csv',mime='text/csv')
 
    #Get average % change
    avgPerChange=perChange.mean(axis=1).round(2)
    perChangeAvg=pd.DataFrame()
    perChangeAvg['Average Annual Percent Change'] = avgPerChange
    perChangeStrAvg=perChangeAvg['Average Annual Percent Change'].astype(str)+'%' 
    st.write('\n \n \n \n \n')
    st.write(f'Average Annual Percent Change for {txt2} from {str(min(yR))} to {str(max(yR))}')
    
    col3, col4 =st.columns([2,1],gap='large')
    with col3:
        st.dataframe(perChangeStrAvg,use_container_width=True)
    with col4:
        "\n"
        "\n"
        #download Annual Percent Change as CSV
        st.download_button(label='Download Data as CSV',data=perChangeAvg.to_csv().encode('utf-8'),file_name=f'AnnualPctChange{countries}_{str(min(yR))}-{str(max(yR))}.csv',mime='text/csv')
   
    #plot % change
    perPlot=px.line(perChange.T,labels={'index':'Years','value':'Percent %','Country':'Countries'}, title=f'Line Chart of Average Percent Change for {txt2} from {str(min(yR))} to {str(max(yR))}')
    st.plotly_chart(perPlot) 
    
    # start of comparing specific year section
    st.divider()
    
    #Moves to data for specific year
    st.subheader(txt1)
    
    #Choose specific year
    ySpec=st.slider('Please Choose a Specific Year',rng1,rng2,(yr1))
    ySpecStr=str(ySpec)
    
    #Makes dataframe based on specified year
    ySpecCntry=countryDB.T[str(ySpec)]
    st.write(f'{txt2} at Year {ySpecStr} ({mesr1})')
    
    col5,col6=st.columns([2,1],gap='large')
        
    with col5:
        st.dataframe(ySpecCntry, use_container_width=True)
    with col6:
        "\n"
        "\n"
        "\n"
        st.download_button(label='Download Data as CSV',data=ySpecCntry.to_csv().encode('utf-8'),file_name=f'{txt2} {mesr2} {countries} {str(ySpec)}.csv',mime='text/csv')
    
    #Makes pie data to compare
    pie=px.pie(countryDB.T,values=str(ySpec),names=countries,color=countries,title='Examine Size Makeup at Year '+ySpecStr)    
    
    #Makes bar data to compare
    bar=px.bar(ySpecCntry,color=countries, labels={'value':mesr2,'Country':'Countries','color':'Countries'},title='The Data at Year '+ySpecStr)
    
    #choose to see pie or bar graph
    chartsYspec=st.radio('How do you Want to Compare?',('Pie','Bar'))   
    
    #show pie chart
    if chartsYspec=='Pie':
        st.plotly_chart(pie, use_container_width=True)
        
    #show bar graph
    if chartsYspec=='Bar':
        st.plotly_chart(bar, use_container_width=True)
    

#shoretened reference
cna='China'
usa='United States'




#HOME TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#code for Home section
if selected == 'Home':
    st.balloons()
    
    #Image is the title header
    image=Image.open('pngwing.com.png')
    st.image(image)
    
    # names the creator
    st.markdown(':red[Created by] :blue[Richard Nguyen]')
    
    #Inormation on project
    st.header('Project Description')
    st.markdown("The purpose of this Final Project was to learn how to use Streamlit to make a quick reference guide relating to my applied project on "
                +"**:red[The Developments of the People’s Republic of China,] and the :blue[Need to Reshore American Manufacturing]**. "
                +"This guide will display areas of intrigue relating to a country’s :green[Economic, Human Development, Manufacturing, Military Ependiture, and Population] data. "
                +"It will display only the data for the given selected countries as well as the data at certain time frames. Links to the online sources of the data "
                +"will be given, as well as the option to download the data. "
                )
    #Hide imported libraries and tools used
    with st.expander('Imported Libraries and Tools Used'):
        
        #displays imported libraries and tools
        st.code('''
                
            import pandas as pd \n
            import matplotlib.pyplot as plt \n
            import streamlit as st \n
            import plotly.express as px \n
            from streamlit_option_menu import option_menu \n
            import webbrowser \n
            from PIL import Image \n
            import zipfile as zp
            
            ''', language='python')
    
    urlPaper='https://drive.google.com/file/d/18EnmT0dNU9sLqIjlkL_8kKsp_dnzauwH/view?usp=share_link'
    if st.button('Find the Report Here',use_container_width=True):
        st.write(urlPaper)
        webbrowser.open_new_tab(urlPaper) 
        
    urlGit='https://github.com/Riqard/Country-Reference.git'
    if st.button('Find the GitHub Repository Here',use_container_width=True):
        st.write(urlGit)
        webbrowser.open_new_tab(urlGit) 
        
    urlApp='https://nguyencountryreferenceguide.streamlit.app/'
    if st.button('Go to Online Version',use_container_width=True):
        st.write(urlApp)
        webbrowser.open_new_tab(urlApp) 

      


   
#ECONOMIC TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

# Extract Economic Data
econData= pd.read_csv('WEOApr2023all.csv')
econData=econData.drop(labels=['WEO Country Code','ISO','WEO Subject Code','Subject Notes','Country/Series-specific Notes','Estimates Start After'], axis=1)
econData=econData.set_index(['Country'])
econData.iloc[:,3:]=econData.iloc[:,3:].astype(float)

#Get only Data in terms of USD
econDataUSD=econData[econData['Units']=='U.S. dollars']

#Get only GDP in terms of USD
econDataUSDGDP=econDataUSD[econDataUSD['Subject Descriptor']=='Gross domestic product, current prices']
econDataUSDGDP=econDataUSDGDP.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#Get only GDP/capita in terms of USD
econDataUSDGDPCap=econDataUSD[econDataUSD['Subject Descriptor']=='Gross domestic product per capita, current prices']
econDataUSDGDPCap=econDataUSDGDPCap.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#Get only Data in terms of PPP
econDataPPP=econData[econData['Units']=='Purchasing power parity; international dollars']

#Get only GDP in terms of PPP
econDataPPPGDP=econDataPPP[econDataPPP['Subject Descriptor']=='Gross domestic product, current prices']
econDataPPPGDP=econDataPPPGDP.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)

#Get only GDP/Capita in terms of PPP
econDataPPPGDPCap=econDataPPP[econDataPPP['Subject Descriptor']=='Gross domestic product per capita, current prices']
econDataPPPGDPCap=econDataPPPGDPCap.drop(labels=['Subject Descriptor','Units','Scale'],axis=1)


#Code for Economics Section
if selected == 'Economy':
    st.title('Economy')
    #Give Tab Description
    st.write("This tab will display the global economic data ranging from 1980 to the projected data in 2028. " +"A country's Gross Domestic Product (GDP), is a measure of how much economic output a country generated, typically measured in US Dollars. " 
             +"A country's GDP per capita measures the economic output of a nation per resident. Purchasing Power Parity (PPP) is a metric that adjusts the US Dollar to more closely match how much a dollar is worth in a given country. "
             + "These metrics are based on items such as a nation's standard of living, currency, and more, taking a 'basket of goods' approach. "
             +"The data past year 2022 are the International Monetary Fund's projected figures.")

    econDataTb, econLink=st.tabs(['Data','Source'])
    
    #Display data
    with econDataTb:
              
       #Choose what type of economic data will be displayed
       choice=[]
       sel=st.selectbox('Choose what Data you Wish to See',('GDP-USD','GDP-USD per Capita','GDP-PPP','GDP-PPP per Capita'))
       choice.append(sel)
       
       # GDP - USD
       if choice == ['GDP-USD']:
           USDGDP=show_Data(econDataUSDGDP,cna,usa,1980,2028,2022,'Measured in Millions USD (2021 Prices)','Millions USD (2021 Prices)','Compare GDP for a Specific Year',"Country's GDP in USD")
       
        # GDP/Capita - USD
       if choice == ['GDP-USD per Capita']:
           USDGDPCap=show_Data(econDataUSDGDPCap,cna,usa,1980,2028,2022,'Measured in USD (2021 Prices)','USD (2021 Prices)','Compare GDP/Capita for a Specific Year',"Country's GDP per Capita in USD")
       
        # GDP - PPP
       if choice == ['GDP-PPP']:
           PPPGDP=show_Data(econDataPPPGDP,cna,usa,1980,2028,2022,'Measured in Purchasing Power Parity; Millions International Dollars', 'Millions International Dollars' , 'Compare GDP-PPP for a Specific Year',"Country's GDP in PPP")
      
        # GDP/Capita - PPP
       if choice == ['GDP-PPP per Capita']:
           PPPGDPCap=show_Data(econDataPPPGDPCap,cna,usa,1980,2028,2022,'Measured in Purchasing Power Parity; International Dollars', 'International Dollars', 'Compare GDP/Capita in PPP for a Specific Year',"Country's GDP per Capita in PPP")
    
    # Go to original data source
    with econLink:
        st.write("This Data originated from the International Monetary Fund")
        econURL='https://www.imf.org/en/Publications/WEO/weo-database/2023/April/download-entire-database'
        if st.button('International Monetary Fund'):
            st.write(econURL)
            webbrowser.open_new_tab(econURL)
 
    


#HUMAN DEVELOPMENT INDEX TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Extract HDI Data
hdiDF=pd.read_csv('HDR21-22_Composite_indices_complete_time_series.csv').set_index('Country')


#Code for HDI section
if selected == 'Human Development Index':
    st.title('Human Development Index')
    
    #Give Tab Description
    st.write("The Human Development Index (HDI) is a summary measure of the average achievement in key dimensions of human development. "
             + "These achievements include but are not limited to an individual’s life expectancy, education, standard of living and more. "
             +"Generally a higher score means that a country is more developed and ranges from 0 to 1."
             +"This data was retrieved from the United Nations Development Program")
    
    # makes data and source tabs
    hdiDataTb, hdiLink=st.tabs(['Data','Source'])
    
    #Display data
    with hdiDataTb:
        
        # runs hdi data
        hdiData=show_Data(hdiDF,cna,usa,1990,2021,2021,'Scores','Scores','Compare HDI for a Specific Year',"Country's Human Development Index")

    # Go to original data source
    with hdiLink:
        st.write('This Data originated from the United Nations')
        hdiURL='https://hdr.undp.org/data-center/documentation-and-downloads'
        if st.button('United Nations Development Program'):
            st.write(hdiURL)
            webbrowser.open_new_tab(hdiURL)
        


#MANUFACTURING TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Extract and Clean Manufacturing Data
mfgData=pd.read_csv('API_NV.IND.MANF.CD_DS2_en_csv_v2_5363423.csv')
mfgData=mfgData.rename(columns={"Country Name": "Country"})
mfgData=mfgData.set_index(['Country'])
mfgData=mfgData.drop(labels=['Country Code','Indicator Code','Indicator Name'], axis=1)

#Wage Data
wage=pd.read_csv('EAR_4MTH_SEX_ECO_CUR_NB_A-filtered-2023-05-02 (1).csv')
wage=wage[wage['classif1.label'].apply(lambda econ: 'Manufacturing' in econ)]
wage=wage[(wage['sex.label']=='Sex: Total')*(wage['classif2.label']=='Currency: U.S. dollars')]
wage=wage.rename(columns={"ref_area.label": "Country"}).set_index('Country')
wage['time']=wage['time'].astype(str)
wage=wage.loc[:,['time','obs_value']]
wage=wage.pivot_table(values='obs_value', index='Country', columns='time', aggfunc='first')

#wage general
totwage=pd.read_csv('EAR_4MTH_SEX_ECO_CUR_NB_A-filtered-2023-05-02 (2).csv')
totwage=totwage.rename(columns={"ref_area.label": "Country"}).set_index('Country')
totwage['time']=totwage['time'].astype(str)
totwage=totwage.loc[:,['time','obs_value']]
totwage=totwage.pivot_table(values='obs_value', index='Country', columns='time', aggfunc='first')


# Code for Manufacturing section
if selected == 'Manufacturing':
    st.title('Manufacturing')
    
    #Give Tab Description
    st.write("The following data will display the value added by manufacturing per country in 2021 US dollars, with data orgininating from the World Bank. "
             + "It will also display the average wages for manufacturing workers in US dollars with data originating from the International Labor Organization.")
    
    # makes data and source tabs
    mfgDataTb, mfgLink=st.tabs(['Data','Source'])
    
    #Display data
    with mfgDataTb:
        mfgChoice=[]
        selMfg=st.selectbox('Choose what Data you Wish to See',('Total Output','Average Monthly Manufacturing Wage', 'Average General Wage'))
        mfgChoice.append(selMfg)
        
        if mfgChoice==['Total Output']:
            # runs mfg data
            mfgShow=show_Data(mfgData,cna,usa,1975,2021,2021,'Amount of Output in US Dollars', 'US Dollars' , 'Compare Amount of Output for a Specific Year', "Country's Manufacturing Output")
        
        if mfgChoice==['Average Monthly Manufacturing Wage']:
            wageShow=show_Data(wage,cna,usa,1969,2022,2020,'Average Wage in US Dollars', 'US Dollars' , 'Compare Average Wage for a Specific Year', "Country's Average Manufacturing Wage")
        
        if mfgChoice==['Average General Wage']:
            genwWgeShow=show_Data(totwage,cna,usa,1969,2022,2020,'Average Wage in US Dollars', 'US Dollars' , 'Compare Average Wage for a Specific Year', "Country's Average Wage")
        
                    
        
    # Go to original data source  
    with mfgLink:
        mfgURL='https://data.worldbank.org/indicator/NV.IND.MANF.CD?end=2021&start=1960&view=chart'
        wageURL='https://www.ilo.org/shinyapps/bulkexplorer16/?lang=en&id=EAR_4MTH_SEX_ECO_CUR_NB_A'
        st.write('This Data for Manufacturing Output originated from the World Bank')
        if st.button('World Bank'):
            st.write(mfgURL)
            webbrowser.open_new_tab(mfgURL)      
        st.write('This Data for Manufacturing Wages and General Wages originated from the International Labor Organization')
        if st.button('International Labor Organization'):
            st.write(wageURL)
            webbrowser.open_new_tab(wageURL)      

#MILITARY TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Get annual Military Expenditure Data
milExp=pd.read_csv('milExp.csv').set_index('Country')

#Get MilExp as share of GDP
milExpPer=pd.read_csv('milPercent.csv').set_index('Country')
milExpPer=milExpPer.mul(100)


# Code for Military section    
if selected == 'Military Ependiture':
    st.title('Military Ependiture')
    
    #Give Tab Description
    st.write("The following data will display the Military Expenditures of each selected country as well as how much that spending is related to gross domestic product. "
             +"The following data originated from the Stockholm International Peace Research Institute.")
    
    # makes data and source tabs
    milTb, milLink=st.tabs(['Data','Source'])
    
    # Display data
    with milTb:
                
        # Choose annual military expenditure or military expenditure as a share of gdp
        choice1=[]
        sel1=st.selectbox('Choose what Data you Wish to See',('Annual Military Expenditures','Annual Military Expenditures as a Share of GDP'))
        choice1.append(sel1)
        
        # annual military expenditure
        if choice1 == ['Annual Military Expenditures']:
            milExpData=show_Data(milExp,cna,'United States of America',1949,2022,2021,'Measured in Millions USD (2021 prices)', 'Millions US Dollars (2021 prices)' ,'Compare Military Expenditure for a Specifc Year', 'Annual Military Expenditure')
        
        # mil exp as a percent of GDP
        if choice1 == ['Annual Military Expenditures as a Share of GDP']:
            milExpPerData=show_Data(milExpPer,cna,'United States of America',1949,2022,2021,'Measured as a Percent Makeup', 'Percentage of GDP' ,'Compare Share of GDP for a Specifc Year', 'Annual Military Expenditure as a Share of GDP')
            
    # Go to original data source
    with milLink:
        milURL='https://milex.sipri.org/sipri'
        st.write('This Data originated from the Stockholm International Peace Research Institute')
        if st.button('Stockholm International Peace Research Institute'):
            st.write(milURL)
            webbrowser.open_new_tab(milURL)



#POPULATION TAB#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Extract population data
popData=pd.read_csv('totpopmf.csv')
popData['Time']=popData['Time'].astype(str)
popData=popData.rename(columns={"Location": "Country"})

#get only total population
totPopData=popData.drop(labels=['PopMale','PopFemale'], axis=1).pivot_table(values='PopTotal', index='Country', columns='Time', aggfunc='first')*1000

#get only male population
mPopData=popData.drop(labels=['PopTotal','PopFemale'], axis=1).pivot_table(values='PopMale', index='Country', columns='Time', aggfunc='first')*1000

#get only female population 
fPopData=popData.drop(labels=['PopTotal','PopMale'], axis=1).pivot_table(values='PopFemale', index='Country', columns='Time', aggfunc='first')*1000

# Code for Population section    
if selected == 'Population':
    st.title('Population')
    
    #Give Tab Description
    st.write("The following data will display the Total, Male, and Female Populations for the selected countries within a given time frame. "
             +"The data past year 2022 are the United Nations’ projected figures. "
             +"This data originated from the United Nations Department of Economic And Social Affairs.")
    
    # makes data and source tabs
    popDataTb,popLink=st.tabs(['Data','Source'])
    
    #Displays data
    with popDataTb:
        
        # Choose Total, Male, or Female population
        choice2=[]
        sel2=st.selectbox('Choose what Data you Wish to See',('Total Population','Male Population','Female Population'))
        choice2.append(sel2)
        
        # Total Population
        if choice2==['Total Population']:
            totPopData=show_Data(totPopData,'China (and dependencies)','United States of America (and dependencies)',1950,2100,2022,'Measured in Amount of People', 'People' ,   'Compare Populations for a Specific Year', 'Total Populations of Countries')
        
        # Male Population
        if choice2==['Male Population']:
            totPopData=show_Data(mPopData,'China (and dependencies)','United States of America (and dependencies)',1950,2100,2022,'Measured in Amount of People', 'People' ,   'Compare Populations for a Specific Year', 'Total Male Populations of Countries')
        
        # Female Population
        if choice2==['Female Population']:
            totPopData=show_Data(fPopData,'China (and dependencies)','United States of America (and dependencies)',1950,2100,2022,'Measured in Amount of People', 'People' ,  'Compare Populations for a Specific Year', 'Total Female Populations of Countries')

    # Go to original data source
    with popLink:
        st.write('This Data originated from the United Nations Department of Economic And Social Affairs')
        popURL='https://population.un.org/wpp/Download/Standard/CSV/'
        if st.button('United Nations Department of Economic And Social Affairs'):
            st.write(popURL)
            webbrowser.open_new_tab(popURL)



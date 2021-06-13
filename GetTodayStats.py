#Importing libraries
import re 
import requests
import pandas as pd
from datetime import datetime

#Scraping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

#____________________________________________________________________________________________________________#

                                                    #Functions#

def getWebPage():
    """
    A Function to read and load Ministry of Health webpage and return the container of the data.
    """
    # Create browser obj
    driver = webdriver.Chrome(executable_path='chromedriver/chromedriver')

    # request url
    driver.get('https://www.moh.gov.sa/Pages/Default.aspx')

    # Driver should wait for a given duration, for the element to load.
    driver.implicitly_wait(5) #5 is in seconds

    # Download the page
    html = driver.page_source
    
    # Close the browser
    driver.close()

    return BeautifulSoup(html,'html.parser').find_all('div', attrs={'class':'col-sm-4 mb-4'})


def Collect_data():

    """
    A Function to collect the data from the returned webapge and return the data for each one.
    """

    # Get webpage
    WebPage = getWebPage()

    # Total Examinations
    Examinations = int(WebPage[5].find('div', attrs={'class':'counter red'}).string.replace(',', ''))

    # Total Vaccinations
    Vaccinations = int(WebPage[0].find('div', attrs={'class':'counter red'}).string.replace(',', ''))

    # Total Active cases
    Active_cases = int(WebPage[4].find('div', attrs={'class':'counter red'}).string.replace(',', ''))

    # Total confirmed cases
    Total_conf_cases = int(re.sub(r"\D", "", WebPage[1].find('h6', attrs={'class':'funfact-title'}).string))

    # New cases
    New_cases = int(WebPage[1].find('div', attrs={'class':'counter red'}).string.replace(',', ''))

    # Total recoveries
    Total_recoveries = int(re.sub(r"\D", "",WebPage[2].find('h6', attrs={'class':'funfact-title'}).string))

    # New recoveries
    New_recoveries = int(WebPage[2].find('div', attrs={'class':'counter red'}).string.replace(',', ''))

    # Total deaths
    Total_deaths = int(re.sub(r"\D", "",WebPage[3].find('h6', attrs={'class':'funfact-title'}).string))

    # New deaths
    New_deaths = int(WebPage[3].find('div', attrs={'class':'counter red'}).string.replace(',', ''))

    return [Examinations, Vaccinations, Active_cases, Total_conf_cases, New_cases, Total_recoveries, New_recoveries, Total_deaths, New_deaths]

def getData():
    """
    A Function to group the data and return dataframe with new status.
    """

    covid_status = Collect_data()

    COVID_moh = pd.DataFrame([{'Total_Examinations':    covid_status[0],
                               'Total_Vaccinations':    covid_status[1],
                               'New cases':             covid_status[2],
                               'Total_Active_cases':    covid_status[3],
                               'Total_confirmed_cases': covid_status[4],
                               'New_recoveries':        covid_status[5],
                               'Total_recoveries':      covid_status[6],
                               'New_deaths':            covid_status[7],
                               'Total_deaths':          covid_status[8]
                               }], 
                               index = pd.to_datetime([datetime.now().strftime("%d/%m/%Y")])
                            )
    return COVID_moh

def Append_to_file(data, file_path):
    try:
        data.to_csv(f'{file_path}', mode='a', header=False)

    except:
        print('The file either in use by other appications or the path is wrong.')


def switcher(user_input):
    """
    A Switcher function for user-input
    """

    if user_input == 1:
        print(getData())

    elif user_input == 2:
        getData().to_csv(f'.//COVID_19_status_{datetime.now().strftime("%d_%m")}.csv')

    elif user_input == 3:
        Append_to_file(getData(), input('Full path for the file to append (Must be .CSV): '))
    
    else:
        print('Please select a valid option!')
    

def main():
 print(f"""{'='*50}

 Please enter one of the follwoing options:

 1- Get today's status.
 2- Export today's status into a '.CSV' file.
 3- Append today's status into a '.CSV' file.

{'='*50}
 """)
 try:
     inpt = int(input(' Waiting for an input: '))
     switcher(inpt)

 except:
    print(' Please enter a valid option.')


if __name__ == "__main__":
    main() # Call main
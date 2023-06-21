import os
import pandas as pd
import openpyxl
from selenium import webdriver
import getpass
import requests
from bs4 import BeautifulSoup
from time import sleep
import os 

# Importing Selenium Libraries 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium import webdriver

# importing ChromeDriverManager to install the chrome Driver
from webdriver_manager.chrome import ChromeDriverManager

import re


# Creating a function get_driver to get all the drivers related to Chrome 
def get_driver():
    # PATH = r"C:\Users\singh\OneDrive\Desktop\Python Projects\Glassdoor\chromedriver"

    # Let's creates an instance of ChromeOptions, which allows you to set various options and preferences for the Chrome browser.

    chrome_options = webdriver.ChromeOptions() 

    # chrome_options.add_argument("--start-maximized") # This adds an argument to maximize the Chrome browser window when it is launched.

    # chrome_options.add_argument("--disable-gpu") # This adds an argument to disable the GPU (graphics processing unit) acceleration.

    # chrome_options.add_argument("--no-sandbox") # This adds an argument to disable the sandbox mode, which provides additional security measures.

    # chrome_options.add_argument("--disable-notifications") # This adds an argument to disable notifications from the browser.

    chrome_options.add_argument('--headless')
    
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # This adds an experimental option to exclude the "enable-logging" switch, which prevents logging in the ChromeDriver logs.

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) # This adds an experimental option to exclude the "enable-automation" switch, which helps in preventing detection of WebDriver automation.
    
    chrome_options.add_experimental_option('useAutomationExtension', False) # This adds an experimental option to disable the use of the Chrome Automation Extension.

    #driver = webdriver.Chrome(options=chrome_options, executable_path=PATH)
    
    #Automatically download and install the appropriate version of ChromeDriver based on the installed Chrome browser version. This ensures compatibility between Chrome and ChromeDriver.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver = webdriver.Chrome(options=chrome_options)

    return driver

#Opens a new chrome window

driver=get_driver()

# driver.get('https://www.glassdoor.co.in/Job/bengaluru-data-analyst-jobs-SRCH_IL.0,9_IC2940587_KO10,22.htm?suggestCount=0&suggestChosen=false&typedKeyword=Data%2520Analyst%2520&dropdown=0&Autocomplete=INDIA')
driver.get('https://www.glassdoor.co.in/')
sleep(0.5)



driver.get('https://www.glassdoor.co.in/')
sleep(0.5)

# finding the sign- in button and entering the email 

my_email = os.getenv('user_name_glassdoor')
my_pass = os.getenv('user_pass_glassdoor')


driver.find_element(By.CLASS_NAME,'e1h5k8h92').send_keys(my_email)

# Clicking on the continue with the email button 
sign_in_button=driver.find_element(By.XPATH,'//*[@type="submit"]')

#.click() to open sign_in through gmail
sign_in_button.click()
sleep(2)  

# Finding the password element and entering the password 
driver.find_element(By.CLASS_NAME,'css-1kmcde.e1h5k8h92').send_keys(my_pass)

# clicking on continue to Glassdoor element button
continue_to_glassdoor= driver.find_element(By.XPATH,'//*[@type="submit"]')
continue_to_glassdoor.click()
sleep(2)



data_analyst='https://www.glassdoor.co.in/Job/bengaluru-data-analyst-jobs-SRCH_IL.0,9_IC2940587_KO10,22.htm?suggestCount=0&suggestChosen=false&typedKeyword=Data%2520Analyst%2520&dropdown=0&Autocomplete=INDIA'
B_A="https://www.glassdoor.co.in/Job/india-business-analysts-jobs-SRCH_IL.0,5_IN115_KO6,23.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Business%2520Analyst&typedLocation=India&context=Jobs&dropdown=0"
P_A="https://www.glassdoor.co.in/Job/india-product-analyst-jobs-SRCH_IL.0,5_IN115_KO6,21.htm"
# changing the url and calling a new windows with the preset keywords for the job posting 

driver.get('https://www.glassdoor.co.in/Job/bengaluru-data-analyst-jobs-SRCH_IL.0,9_IC2940587_KO10,22.htm?suggestCount=0&suggestChosen=false&typedKeyword=Data%2520Analyst%2520&dropdown=0&Autocomplete=INDIA')
sleep(2)

urls=[data_analyst,B_A,P_A]
#finding the date dropdown filter for job posting in the last 24 hours
# dropdown=driver.find_element(By.XPATH,'//*[@id="filter_fromAge"]/span[2]')
# sleep(10)
# selecting the 24 hour filter
# last_24_hours= driver.find_element(By.CLASS_NAME," css-1p9640h.ew8xong2").click()
# sleep(10)
# last_24_hours= driver.find_element(By.XPATH,'//*[@type=""]').click()

# //*[@id="PrimaryDropdown"]/ul/li[2]/button/div/span
# //*[@id="filter_fromAge"]/span[2]
# //*[@id="PrimaryDropdown"]/ul/li[2]/button/div/span

# Most Recent Jobs
filter= driver.find_element(By.CLASS_NAME,"css-150lexj.e1gtdke60")

filter.click()
sleep(2)

#clicking the most recent one 
recent= driver.find_elements(By.CLASS_NAME,"dropdownLabel")[1].click()
sleep(2)

# Page scroller 
def scroll_down():
    # find the body element and the Page_Down key
    body= driver.find_element(By.TAG_NAME,"body")
    body.send_keys(Keys.PAGE_DOWN)



# Creating an empty list to store the information 
details=[]

# Searching for the element that contains all the information
elements= driver.find_elements(By.CLASS_NAME,'d-flex.justify-content-between.p-std.jobCard ')
#print(elements)
# for url in urls:
# Running the loop over the main element page that stores all the information to get the required detail and append the value to the list
for element in elements:
    element.click()
    sleep(0.5)

        # Finding the title for the job posted 
    title= driver.find_element(By.CLASS_NAME,"css-1vg6q84.e1tk4kwz4").text
    print(title)
    sleep(0.5)

   # Organisation name 
    org_name = driver.find_element(By.CLASS_NAME,'css-87uc0g.e1tk4kwz1').text
    Org = org_name
        # print(f'Organisation Name',Org)
    sleep(0.5)

        # Finding the Job link from the web-content
    link= driver.find_element(By.CLASS_NAME,'p-std.jobCard')
    job_link= link.get_attribute('href')
    # print(job_link)
    sleep(0.5)

        
        #location 
    location = driver.find_element(By.CLASS_NAME,'css-56kyx5.e1tk4kwz5').text
        # print(f"Location :",location)
    sleep(0.5)

        #Salary Range
    try:
        salary = driver.find_element(By.CLASS_NAME,'css-1xe2xww.e1wijj242').text
        sal= salary.split()[2]
            # print(f'Salary:',sal)
    except:
        sal = "NA"
        sleep(0.5)

    j_d= driver.find_element(By.CLASS_NAME,'jobDescriptionContent.desc').text
        #print(j_d)
    sleep(0.5)
            
    details.append({
                'Job Title': title,
                'Organisation Name' : Org, 
                'Job Link' : job_link,
                'Location' : location,
                'Salary' : sal,
                'Job Description' : j_d

        })

df = pd.DataFrame.from_dict(details)
file_path= r'C:\Users\singh\OneDrive\Desktop\Python Projects\New folder\2023-6-13\glassdoor_jobs.csv'
# add it in the enviorment varianle
df.to_csv(file_path,index=None)
df.to_excel("Glassdoor_jobs.xlsx",index=None)
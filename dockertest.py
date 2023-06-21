import os 
import pandas as pd
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from time import sleep
import os 
from dotenv import load_dotenv
import re



from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium import webdriver
# # ...
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'



# Setting up the chromium options 
def set_chrome() -> Options:
    # setting up the options for the chromium 
    options = webdriver.ChromeOptions() #newly added 
    options.headless = True  
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    options.add_argument('--disable-usb-discovery')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-features=InterestCohort')
    # chrome_prefs={}
    # options.experimental_options["prefs"]= chrome_prefs
    # chrome_prefs["profile.default_content_settings"]={"images":2}
    
    return options

def scrape_jobs():
        driver =webdriver.Chrome(options=set_chrome())
        
        driver.get("https://www.glassdoor.co.in")

        load_dotenv()

        email= os.getenv('user_name')
        password= os.getenv('password')

        driver.find_element(By.XPATH,'//*[@id="inlineUserEmail"]').send_keys(email)
        sleep(2)
    
        sign_in_button=driver.find_element(By.XPATH,'//*[@type="submit"]')
        sign_in_button.click()
        sleep(2)  

        # Finding the password element and entering the password 
        # driver.find_element(By.XPATH,'//*[@id="inlineUserPassword"]').send_keys(password)

        password_input = driver.find_element(By.ID,"inlineUserPassword")  # Replace "password_field_id" with the actual ID of the input field
        password_input.send_keys(password)

        # clicking on continue to Glassdoor element button
        continue_to_glassdoor= driver.find_element(By.XPATH,'//*[@type="submit"]')
        continue_to_glassdoor.click()
        sleep(2)

        data_analyst= "https://www.glassdoor.co.in/Job/bengaluru-data-analyst-jobs-SRCH_IL.0,9_IC2940587_KO10,22.htm?suggestCount=0&suggestChosen=false&typedKeyword=Data%2520Analyst%2520&dropdown=0&Autocomplete=INDIA"
    
        # changing the url and calling a new windows with the preset keywords for the job posting 
        driver.get(data_analyst)
        sleep(2)

        # Most Recent Jobs
        filter= driver.find_element(By.CLASS_NAME,"css-150lexj.e1gtdke60")
        filter.click()
        sleep(2)

        #clicking the most recent one 
        recent= driver.find_elements(By.CLASS_NAME,"dropdownLabel")[1].click()
        sleep(2)

        url="https://www.glassdoor.co.in/Job/data-analyst-jobs-SRCH_IL.0,9_IC2940587_KO10,22.htm?sortBy=date_desc"
        driver.get(url)
        sleep(2)

        # Creating an empty list to store the information of all the job-Ids 
        details=[]
        id_elements=driver.find_elements(By.CLASS_NAME,'react-job-listing')

        for element in id_elements:
             sleep(0.5)
             data_id = element.get_attribute("data-id")

             #getting location
             try:
                 Location = element.find_element(By.CSS_SELECTOR,'[data-test="emp-location"]')
                 location= Location.text
                #  print(location)
             except:
                 location ="NA"

             #  Getting the title for each job
             try:
                Title = element.find_element(By.ID,"job-title-"+data_id)
                title=Title.text
                # print(title_text)
             except:
                title= "NA"

             #Salary Range
             try:
                salary = element.find_element(By.CSS_SELECTOR,'[data-test="detailSalary"]').text
                sal= salary.split()[2]
                # print(f'Salary:',sal)
             except:
                sal = "NA"
                # print(sal)

             # Getting the organisation name 
             try:
                Company = element.find_element(By.CLASS_NAME,'ml-xsm.job-search-1bgdn7m')   

                co_name= Company.text
                org = co_name 
                Org=  org.split(" ")[0]
             except:
                Org="NA"
            
             # getting the job link 
             try:
                hrr=element.find_element(By.CSS_SELECTOR,'[data-test="job-link"]')
                href_value = hrr.get_attribute('href')
             except:
                  href_value= "NA"
    
             details.append({
                        'Job Title': title,
                        'Organisation Name' : Org, 
                        'Job Link' : href_value,
                        'Location' : location,
                        'Salary' : sal,

                })
            # find the body element and the Page_Down key
             body= driver.find_element(By.TAG_NAME,"body")
             body.send_keys(Keys.PAGE_DOWN)

        driver.quit()
        df = pd.DataFrame.from_dict(details)
        df.to_csv("Glassdoor_jobs.CSV",index=None)
        df.to_excel("Glassdoor_jobs.xlsx", index= None)

if __name__=="__main__":
        
        
        import file_sharing
        file_sharing.send_message()
        file_sharing.send_file()
            

            
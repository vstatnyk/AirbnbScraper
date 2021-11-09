from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
import csv
import datetime     #needed for time opperations
import schedule


def job():

    # airbnb link
    checkInLink = "https://www.airbnb.com/s/Sacramento--CA--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=december&flexible_trip_dates%5B%5D=november&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&query=Sacramento%2C%20CA%2C%20United%20States&place_id=ChIJ-ZeDsnLGmoAR238ZdKpqH5I&checkin="
    checkOutLink = "&checkout="
    restLink = "&adults=2&source=structured_search_input_header&search_type=filter_change&room_types%5B%5D=Entire%20home%2Fapt"

    # driver setup
    PATH = "/Users/vstatnyk/Documents/GitHub/AirbnbScraper/chromedriver"
    chrome_options = Options()                          # this will allow for script to run in the background
    chrome_options.set_headless(headless=True)          # this will allow for script to run in the background
    driver = webdriver.Chrome(PATH,chrome_options=chrome_options)

    # time setup
    DELTA_PST = datetime.timedelta(hours = 7)           # time conversion interval
    intervals = [   
                    datetime.timedelta(days = 1),   #ONE DAY
                    datetime.timedelta(days = 2),   #TWO DAY
                    datetime.timedelta(days = 5),   #FIVE DAY
                    datetime.timedelta(days = 10),  #TEN DAY
                    datetime.timedelta(days = 15),  #FIFTEEN DAY
                    datetime.timedelta(days = 25),  #TWENTY FIVE DAY
                ]
        
    today = datetime.datetime.now()
    today = today - DELTA_PST
    checkInDate = str(today.strftime('%Y-%m-%d'))       #format for dates = yyyy-mm-dd

    output.append(checkInDate)

    for i in intervals:

        checkOutDate = today + i
        checkOutDate = str(checkOutDate.strftime('%Y-%m-%d'))


        # main body
            #creating link to get
        link = checkInLink + checkInDate + checkOutLink + checkOutDate + restLink
        driver.get(link)
        sleep(3)
        try:
            result = str(driver.find_element_by_xpath('//*[@id="site-content"]/div[1]/div/div/div/div/div/section/h1/div').text)
            result = result.split()
            print(result[0])
            output.append(result[0])
        except:
            try:
                result = str (driver.find_element_by_xpath('//*[@id="site-content"]/div[1]/div/div/div/div/div/h1').text)
                result = result.split()
                print(result[0])
                output.append(result[0])
            except:
                print("error found")
                output.append("error, please contact developer")
        
    with open("output.csv", 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow('\n')
        writer.writerow(output)
        output.clear
    driver.quit()


# output list 
output = []

schedule.every().day.at("11:29").do(job)
schedule.every().day.at("11:28").do(job)
schedule.every().day.at("11:27").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://dse.com.bd/latest_PE.php'

driver = webdriver.Chrome(executable_path=r'C:\webdrivers\chromedriver.exe')
driver.get(url)

print('check 1')

driver.maximize_window()

# print('check 2')
driver.find_element("link text", "Recent Market Information").send_keys("\n")

time.sleep(0.5)
driver.find_element("link text", "More recent market information").send_keys("\n")

time.sleep(0.5)

#("01/01/2015")
driver.find_element("xpath", '//*[@id="startDate"]').send_keys("01")
driver.find_element("xpath", '//*[@id="startDate"]').send_keys("01")
driver.find_element("xpath", '//*[@name="startDate"]').send_keys(Keys.ARROW_RIGHT)
driver.find_element("xpath", '//*[@id="startDate"]').send_keys("2015")
time.sleep(0.5)

# 1/9/2022
driver.find_element("xpath", '//*[@id="endDate"]').send_keys("01")
driver.find_element("xpath", '//*[@id="endDate"]').send_keys("09")
driver.find_element("xpath", '//*[@name="endDate"]').send_keys(Keys.ARROW_RIGHT)
driver.find_element("xpath", '//*[@id="endDate"]').send_keys("2022")
time.sleep(0.5)

driver.find_element("name", "searchRecentMarket").send_keys("\n")

h = driver.page_source
with open("dse_index.html","w") as f:
    f.write(h)

# Downloading contents of the web page
data = open("dse_index.html", "r")
data = data.read()

# Create BeautifulSoup object
soup = BeautifulSoup(data, 'html5lib')

# Get table
table = soup.find('table', _id='data-table')

contents = []
df = pd.DataFrame(columns=['Date', 'Total Trade', 'Total Volume', 'Total Value in Taka (mn)', 'Total Market Cap in Taka (mn)', 'DSEX Index', 'DSES Index',
                            'DS30 Index', 'DGEN Index'])
    
# Getting all rows
#for row in table.find_all('th')

for row in table.tbody.find_all('tr'):    
# Find all data for each column
    columns = row.find_all('td')
    if(columns != []):
        date = columns[0].text.strip()
        ttrade = columns[1].text.strip()
        tvol = columns[2].text.strip()
        tvt = columns[3].text.strip()
        tmc = columns[4].text.strip()
        dsex = columns[5].text.strip()
        dses = columns[6].text.strip()
        ds30 = columns[7].text.strip()
        dgen = columns[8].text.strip()

        df = df.append({'Date': date,  'Total Trade': ttrade, 'Total Volume': tvol, 'Total Value in Taka (mn)': tvt, 'Total Market Cap in Taka (mn)': tmc,
                            'DSEX Index': dsex, 'DSES Index': dses, 'DS30 Index': ds30, 'DGEN Index': dgen}, ignore_index=True)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y').dt.date
    #df = df.set_index("Date")
    #df.to_csv('test.csv', sep=',', date_format='%d-%m-%Y', index = True, encoding='utf-8') # True: included index
df.to_excel("dse_index.xlsx", index=False)
print(df)

    
    
#Click on Link and Redirect to another page
driver.find_element("link text", "Home").send_keys("\n")

time.sleep(0.5)
driver.find_element("link text", "P/E: at a Glance").send_keys("\n")
time.sleep(0.5)
    
h = driver.page_source
with open("current_trade.html","w") as f:
    f.write(h)
driver.close()

# Downloading contents of the web page
data = open("current_trade.html", "r")
data = data.read()
    
list_of_dfs = pd.read_html('https://dse.com.bd/latest_PE.php')
#print(list_of_dfs)
size = len(list_of_dfs)
print("DFS Size:",size)
position = size - 2
print("Position of the table in DFS:",position)
table = list_of_dfs[position]
table = table.fillna('')
print(table)
table.to_excel("current_trade.xlsx", index=False)

print('Extraction done')
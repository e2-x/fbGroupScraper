import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

id_list_file = "id_list.txt"  # Name of file with list of IDs (Should be in working directory)
username = ""  # Enter a valid Facebook user name
password = ""  # Enter a password
url_list = []
group_list = []

page = "https://www.facebook.com"

driver = webdriver.PhantomJS()
driver.get(page)
print("Opening Facebook...")

user_name_form = driver.find_element_by_id('email')
user_name_form.send_keys(username)

password_form = driver.find_element_by_id('pass')
password_form.send_keys(password)

log_in = driver.find_element_by_id('loginbutton')
log_in.click()
print("Logged In!")

wait = WebDriverWait(driver, 1)
with open(id_list_file, "r") as f:

    for line in f:

        new_line = str(line).lstrip().replace('\n', '').replace(' ', '')
        searchUrl = 'https://www.facebook.com/search/' + new_line + '/groups'

        # Goto webpage using headless browser
        driver.get(searchUrl)

        print("\n##########################################\n")
        print("User groups page reached. - ", line)
        print(searchUrl)
        body = driver.find_element_by_tag_name('body')
        csv_id = line + ".csv"

        time.sleep(2)
        body.click()
        time.sleep(1)

        lenOfPage = driver.execute_script\
        ("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False

        while not match:
            lastCount = lenOfPage
            time.sleep(1)
            lenOfPage = driver.execute_script\
            ("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

            if lastCount == lenOfPage:
                match = True
                time.sleep(1)

                # # let's parse our html
                soup = BeautifulSoup(driver.page_source, "html.parser")
                div = soup.find_all(attrs={'class': '_3u1 _gli _5und'})

                for item in div:

                    group_id = item.select('._gll')

                    for id in group_id:

                        id_element = id.next_element
                        group_url = id_element.attrs['href']
                        group_name = id_element.text
                        group_list.append(group_name)
                        url_list.append(group_url)

                        with open(csv_id, 'w') as mycsv:
                            # mycsv = open(csv_id, 'w')
                            writer = csv.writer(mycsv, dialect='excel')
                            writer.writerow(['Group Name', 'Group URL'])

                            for group, url in zip(group_list, url_list):

                                writer.writerow([group, (page + url)])

        del group_list[:]
        del url_list[:]


print("Done")
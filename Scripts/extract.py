from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import lxml
import re
import csv
from selenium.webdriver.chrome.options import Options
chormeOptions = Options()
chormeOptions.add_argument('--headless')
driver = webdriver.Chrome(options=chormeOptions)


def loginToWebsite(username, password):
    driver.get(url='https://code.ptit.edu.vn/login')
    nameField = driver.find_element(by=By.NAME, value='username')
    nameField.send_keys(username)
    passwordField = driver.find_element(by=By.NAME, value='password')
    passwordField.send_keys(password)
    login_button = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div/div[3]/div/form/button')
    login_button.click()


def directToState():
    state = driver.find_element(by=By.LINK_TEXT, value='Trạng thái')
    state.click()


pages = []


def extractWebpageHtml():
    global pages
    for p in range(9):
        pages.append(driver.page_source)
        next_page_button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div/div/div[3]/ul/li[12]/a')
        next_page_button.click()
    pages.append(driver.page_source)
    driver.close()


def parseHtmlContentAndExtractData():
    records = []
    pattern = re.compile(r'^\s*(\w+)\s+\((.+)\)\s*$')

    def tr_tag_has_no_class_att(tag):
        return tag.name == 'tr' and not tag.has_attr('class')

    for page in pages:
        tags = BeautifulSoup(page, 'lxml').findAll(tr_tag_has_no_class_att)
        for tag in tags:
            submit = {}
            result = tag.find('span')
            if result is None:
                continue
            else:
                result = result.string
            soup = BeautifulSoup(str(tag), 'lxml')
            submit["submit_id"] = tag.find('td', attrs={'class': 'text--middle link_solution_ids'}).string
            submit['date'] = tag.find(attrs={'class': 'status__table__date'}).string
            submit['time'] = tag.find(attrs={'class': 'status__table__time'}).string
            id_and_name_tag = soup.select_one(selector='tr > td:nth-child(3)')
            match = re.search(pattern=pattern, string=str(id_and_name_tag.string))
            submit['student_id'], submit['student_name'] = match.groups()
            submit['exercise'] = soup.select_one(selector='tr > td:nth-child(4) > a:nth-child(1)').string
            submit['result'] = result
            if result == "TLE":
                submit['run_time'] = None
                submit['memory'] = tag.find(id=re.compile('^memory')).string
            elif result == "CE":
                submit['run_time'] = None
                submit['memory'] = None
            else:
                submit['run_time'] = tag.find(id=re.compile('^run_time')).string
                submit['memory'] = tag.find(id=re.compile('^memory')).string
            submit['language'] = soup.select_one(selector='tr > td:nth-child(8)').string
            records.append(submit)
    return records


def saveRawData(data):
    with open('Data/RawData/raw_data.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def main():
    print('Extracting...')
    loginToWebsite('B21DCCN435', '24082003')
    directToState()
    extractWebpageHtml()
    data = parseHtmlContentAndExtractData()
    saveRawData(data)
    print('Extracted successfully')

"""
if __name__ == "__main__":
    main()"""

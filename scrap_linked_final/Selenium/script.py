import csv
import paramaters
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# function for field validation
def field_validation(field):
    if field:
        pass
    else:
        field = ''
    return field

# chrome is opened
f = open(paramaters.file_name, 'w')
fnames = ['Name', 'Job Title', 'URL', 'e-mail']

writer = csv.DictWriter(f, fieldnames=fnames)
writer.writeheader()

driver = webdriver.Chrome('/Users/balaji/Documents/chromedriver')
driver.get('https://www.linkedin.com')
sleep(2)

username = driver.find_element_by_class_name('login-email')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_id('login-password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(5)

input_search_box = driver.find_element_by_xpath("//input[@placeholder='Search']")
sleep(2)

input_search_box.send_keys(paramaters.search_query)
sleep(2)

#For pressing enter
input_search_box.send_keys(u'\ue007')
sleep(5)

sel = Selector(text=driver.page_source)
# list = sel.xpath('//ul[@class="search-results__list "]/li')
list = sel.xpath('//ul[@class="search-results__list list-style-none"]/li')

for list_1 in list:
    try:
        main_url = "https://www.linkedin.com"+list_1.xpath('.//*[@class="search-result__info pt3 pb4 ph0"]/a/@href').extract_first()
    except:
        pass
    profile_name = list_1.xpath('.//span[@class="name actor-name"]/text()').extract_first()
    driver.get(main_url)
    sleep(2)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//h1/text()').extract_first().strip()
    sleep(0.5)

    job_title = sel.xpath('//h2/text()').extract_first().strip()
    sleep(0.5)

    linkedin_url = driver.current_url.strip()

    email_id=""


    name = field_validation(name)
    job_title = field_validation(job_title)
    # location = field_validation(location)
    linkedin_url = field_validation(linkedin_url)
    # fnames = ['Name', 'Job Title', 'URL', 'e-mail']
    writer.writerow({'Name' : name, 'Job Title' : job_title, 'URL' : linkedin_url, 'e-mail' : email_id })
    print ('\n')
    print ('Name: ' + name)
    print ('Job Title: ' + job_title)
    # print ('Location: ' + location)
    print ('URL: ' + linkedin_url)
    print ('email :' + email_id)
    print ('\n')


    try:
        driver.find_element_by_xpath('//span[text()="Connect"]').click()
        sleep(3)

        driver.find_element_by_xpath('//*[@class="button-primary-large ml1"]').click()
        sleep(3)

    except:
        location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first().strip()
        contact_information_url = "https://www.linkedin.com" + sel.xpath('//a[@data-control-name="contact_see_more"]/@href').extract_first().strip()
        sleep(1)
        if contact_information_url:
            driver.get(contact_information_url)
            sleep(0.5)
            sel = Selector(text=driver.page_source)
            email_id = sel.xpath('.//*[contains(@href, "mail")]/text()')[0].extract().strip()
        # driver.get(main_url)
        pass

sel.xpath('.//*[contains(@href, "mail")]/text()')[0].extract()
sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__contact-info")]/text()').extract_first()

driver.quit()

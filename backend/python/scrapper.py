# import from environment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from dotenv import load_dotenv
import os
import sys

# import from other .py files
from api import Gpt
from sleep import sleep
from _wd import scrollToBottom, getExperience
from prompt import prompt_summarize_woking_info, prompt_email


def runScrapper(username, password, save_csv, send_email):
    # test
    print("running")

    while True:
        try:
            # start the selenium driver and feed the Linkedin url to it
            wd = webdriver.Chrome(r'/Users/tingkangzhao/SeleniumDriver/chromedriver') # path to your chromedriver
            wd.implicitly_wait(21)

            url = "https://www.linkedin.com"
            wd.get(url)

            username_box = wd.find_element(By.CSS_SELECTOR, "#session_key")
            password_box = wd.find_element(By.CSS_SELECTOR, "#session_password")

            # send the username and password
            username_box.send_keys(username)
            sleep()
            password_box.send_keys(password)

            # click the login button to login
            sleep()
            wd.find_element(By.CSS_SELECTOR, "#main-content > section.section.min-h-\[560px\].flex-nowrap.pt-\[40px\].babybear\:flex-col.babybear\:min-h-\[0\].babybear\:px-mobile-container-padding.babybear\:pt-\[24px\] > div > div > form:nth-child(7) > div.flex.justify-between.sign-in-form__footer--full-width > button").click()
            break
        except:
            continue
    
    # test
    sleep(21, 29)
    wd.quit()
    return

    while True:
        try:
            # go to My Network Page
            my_network_button = wd.find_element(By.CSS_SELECTOR, "ul.global-nav__primary-items>li:nth-child(2)")
            my_network_button.click()
            sleep(21, 29)
            break
        except:
            continue
    
    while True:
        try:
            # go to Connections
            connections_button = wd.find_element(By.CSS_SELECTOR, "div.mn-community-summary__section.artdeco-dropdown a:nth-child(1)")
            connections_button.click()
            sleep()
            break
        except:
            continue

    # scroll to the bottom
    scrollToBottom(wd)

    while True:
        try:
            # get each connection of the user
            urls = []
            all_info = []
            all_connections_form = wd.find_element(By.CSS_SELECTOR, "div.scaffold-finite-scroll__content")
            sleep()
            all_connections = all_connections_form.find_elements(By.CSS_SELECTOR, "li")
            for connection in all_connections:
                connection_url = connection.find_element(By.TAG_NAME, "a").get_attribute("href")
                urls.append(connection_url)
                sleep(1, 4)
                # test
                if len(urls) > 10:
                    break
            break
        except:
            print("failed at getting connections\nrebooting...")
            continue

    for url in urls:
        try:
            gpt = Gpt()
            person = {}
            person["url"] = url
            # check the detailed information on a new tab
            wd.execute_script(f"window.open('{url}');")
            wd.switch_to.window(wd.window_handles[1])
            person["name"] = wd.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words").text
            sleep(3, 9)
            info = getExperience(wd)
            prompt = prompt_summarize_woking_info(info)
            person["working_info"] = gpt.chat(prompt) # chatgpt

            # use ChatGPT generate message
            prompt = prompt_email(str(person))
            message = gpt.chat(prompt) # chatgpt
            # store the info
            person["message"] = message
            all_info.append(person)

            if send_email:
                wd.find_element(By.CSS_SELECTOR, "div.pv-top-card-v2-ctas button.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view").click()
                # send the message
                wd.find_element(By.CSS_SELECTOR, "div.msg-form__contenteditable.t-14.t-black--light.t-normal.flex-grow-1.full-height.notranslate").send_keys(person["message"])
                wd.find_element(By.CSS_SELECTOR, "footer.msg-form__footer.flex-shrink-zero>.msg-form__right-actions.display-flex.align-items-center button").click()
                sleep()

            # quit current tab
            wd.switch_to.window(wd.window_handles[1])
            wd.close()
            wd.switch_to.window(wd.window_handles[0])
            sleep()

            if save_csv:
                # save person's contact info into csv
                df_urls = pd.DataFrame(all_info)
                df_urls.to_csv("test.csv", index=False)
        except:
            print(f"we failed on the url: {url}")
            pass



# Execute!!!
args = sys.argv[1:]

username = args[0]
password = args[1]
save_csv = args[2]
send_email = args[3]

runScrapper(username, password, save_csv, send_email)

sys.stdout.flush()
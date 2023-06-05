# import from environment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pandas as pd
from dotenv import load_dotenv
import os
import sys

# import from other .py files
from api import Gpt
from sleep import sleep
from _wd import scrollToBottom, getExperience
from prompt import prompt_summarize_woking_info, prompt_email


def runScrapper(username, password, save_csv, send_message):

    if save_csv == "true":
        save_csv = True
    else:
        save_csv = False

    if send_message == "true":
        send_message = True
    else:
        send_message = False


    while True:
        try:
            # start the selenium driver and feed the Linkedin url to it
            # wd = webdriver.Chrome(r'/Users/tingkangzhao/SeleniumDriver/chromedriver') # path to your chromedriver
            service = Service('/Users/tingkangzhao/SeleniumDriver/chromedriver') # path to your chromedriver
            wd = webdriver.Chrome(service=service)
            wd.implicitly_wait(21)

            url = "https://www.linkedin.com"

            while True:
                try:
                    username_box = wd.find_element(By.CSS_SELECTOR, "#session_key")
                    password_box = wd.find_element(By.CSS_SELECTOR, "#session_password")
                    break
                except:
                    wd.get(url)
                    # incase the page doesn't load
                    while True:
                        try:
                            wd.find_element(By.CSS_SELECTOR, ".google-auth")
                            break
                        except:
                            pass
                        try:
                            wd.find_element(By.CSS_SELECTOR, "[data-test-id='hero']")
                            break
                        except:
                            wd.refresh()

                    # incase we goes to the LinkedIn SingUp page
                    try:
                        wd.find_element(By.CSS_SELECTOR, "button.authwall-join-form__form-toggle--bottom.form-toggle").click()
                    except:
                        pass
                sleep()


            # send the username and password
            username_box.send_keys(username)
            sleep()
            password_box.send_keys(password)
        
            # click the login button to login
            sleep()
            wd.find_element(By.CSS_SELECTOR, "#main-content > section.section.min-h-\[560px\].flex-nowrap.pt-\[40px\].babybear\:flex-col.babybear\:min-h-\[0\].babybear\:px-mobile-container-padding.babybear\:pt-\[24px\] > div > div > form:nth-child(7) > div.flex.justify-between.sign-in-form__footer--full-width > button").click()

            # if the user send the wrong username or password
            try:
                wd.find_element(By.CSS_SELECTOR, "iframe#captcha-internal")
                print("wrong username or password")
                return
            except:
                pass
            try:
                wd.find_element(By.CSS_SELECTOR, "div[error-for]")
                print("wrong username or password")
                wd.quit()
                return
            except:
                pass

            break
        except:
            continue

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
    t = 0 #test
    while True:
        try:
            # get each connection of the user
            urls = []
            all_info = []
            all_connections_form = wd.find_element(By.CSS_SELECTOR, "div.scaffold-finite-scroll__content")
            sleep()
            all_connections = all_connections_form.find_elements(By.CSS_SELECTOR, "li")
            for connection in all_connections:
                t += 1 #test
                connection_url = connection.find_element(By.TAG_NAME, "a").get_attribute("href")
                urls.append(connection_url)
                sleep(1, 4)
                if t >= 3: #test
                    break
            break
        except:
            print("failed at getting connections\nrebooting...")
            continue
        

    for url in urls:
        while True:
            try:
                gpt = Gpt()
                person = {}
                person["url"] = url
                # check the detailed information on a new tab
                wd.execute_script(f"window.open('{url}');")
                wd.switch_to.window(wd.window_handles[1])
                # name
                person["name"] = wd.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words").text
                sleep(3, 9)
                # experiences
                info = getExperience(wd)
                prompt = prompt_summarize_woking_info(info)
                person["working_info"] = gpt.chat(prompt) # chatgpt
                sleep(1, 3)
                # email address
                wd.find_element(By.CSS_SELECTOR, "div.pv-text-details__left-panel.mt2>span.pv-text-details__separator.t-black--light>a").click()
                try:
                    email = wd.find_element(By.CSS_SELECTOR, ".pv-contact-info__contact-type.ci-email>div.pv-contact-info__ci-container.t-14>a").text
                except:
                    email = None
                sleep()
                wd.find_element(By.CSS_SELECTOR, "li-icon>svg").click()
                person["email"] = email

                # use ChatGPT generate message
                prompt = prompt_email(str(person))
                message = gpt.chat(prompt) # chatgpt
                # store the info
                person["message"] = message
                all_info.append(person)

                if send_message:
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
                break

            except:
                if len(wd.window_handles) > 1:
                    for window_index in range(len(wd.window_handles)):
                        if window_index == 0:
                            continue
                        wd.switch_to.window(wd.window_handles[1])
                        wd.close()
                wd.switch_to.window(wd.window_handles[0])
                continue

    wd.quit()



# Execute!!!
args = sys.argv[1:]

username = args[0]
password = args[1]
save_csv = args[2]
send_message = args[3]

runScrapper(username, password, save_csv, send_message)

sys.stdout.flush()
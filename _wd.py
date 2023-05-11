import time
from sleep import sleep
from selenium.webdriver.common.by import By

# scroll to the bottom
def scrollToBottom(wd):
    last_height = wd.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new content to load
        time.sleep(1)

        # Calculate new page height and check if it has changed
        new_height = wd.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        sleep()


def getExperience(wd):
    wd.implicitly_wait(1)
    wd.switch_to.window(wd.window_handles[1])
    for element in wd.find_elements(By.CSS_SELECTOR, "section.artdeco-card.ember-view.relative.break-words.pb3.mt2"):
        try:
            element.find_element(By.CSS_SELECTOR, "#experience")
            return element.text
        except:
            pass
        sleep(1,3)
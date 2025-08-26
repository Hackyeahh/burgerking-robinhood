from typing import Literal
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
import re

start_time = time.time()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

PLATFORM: Literal["desktop"] | Literal["mobile"] = "desktop"
BK_URL = r"https://www.mybkexperience.com/"

driver.get(BK_URL)
driver.maximize_window()


TIMEOUT_SECONDS = 10
wait = WebDriverWait(driver, TIMEOUT_SECONDS)


form_iframe = driver.find_element(By.CLASS_NAME, r"Home_iframe__T3nfU")
driver.switch_to.frame(form_iframe)


# @lru_cache(maxsize=100)
def get_id(element_id: str):
    return wait.until(EC.element_to_be_clickable((By.ID, element_id)))


# 00 STORE INFO
get_id("QR~QID114").send_keys("5079")
get_id("NextButton").click()


# 01 MORE DETAILS

ONTARIO_OPTION = "46"
Select(get_id("QR~QID6")).select_by_value(ONTARIO_OPTION)

VISIT_DATETIME = datetime.now() - timedelta(minutes=5)

driver.execute_script(
    f"arguments[0].value = '{VISIT_DATETIME.strftime('%m/%d/%Y')}';",
    get_id("QR~QID118~2"),
)
get_id("QR~QID8#1~1").send_keys(VISIT_DATETIME.strftime("%I"))
get_id("QR~QID8#2~1").send_keys(VISIT_DATETIME.strftime("%m"))
get_id("QR~QID8#3~1").send_keys(VISIT_DATETIME.strftime("%p"))
get_id("NextButton").click()


# 02 OVERALL SATISFACTION RATING
get_id("QID18-22-label").click()
get_id("NextButton").click()


# user_response = input("Give a 3 sentence answer to your experience at BK: ")

# if len(user_response) < 40:
if True:
    OVERALL_SATISFACTION_RESPONSE = "everything was good, no issues with the order! service was fast & efficient like usual. restaurant was clean and experience met expectations"
else:
    OVERALL_SATISFACTION_RESPONSE = user_response

# 03 OVERALL SATISFACTION NATURAL LANGUAGE RESPONSE
get_id("QR~QID120").send_keys(OVERALL_SATISFACTION_RESPONSE)
get_id("NextButton").click()


# 04 ORDER TYPE
get_id("QID13-2-label").click()
get_id("NextButton").click()


# 05 ORDER PLACEMENT LOCATION
get_id("QID12-2-label").click()
get_id("NextButton").click()


# 06 ORDER PLACEMENT LOCATION
# get_id("QID83-1-label").click() # this is YES to ROYAL PERKS
get_id("QID83-2-label").click()
get_id("NextButton").click()


# 07 CUSTOMER RITUALS
get_id("QID123-3-label").click()  # i dont remember
get_id("QID124-3-label").click()  # i dont remember
get_id("NextButton").click()


# 08 CATEGORY SATISFACTION


def get_radio_clickable(label_id: str):
    return wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"label[for='{label_id}']"))
    )


match PLATFORM:
    case "mobile":
        # TODO test this:
        get_id("header~QID21~1").click()  # friendliness
        get_id("QID21-11-12-col-label").click()  # highly satisfied
        time.sleep(0.5)

        get_id("header~QID21~2").click()  # interior cleanliness
        get_id("QID21-7-12-col-label").click()  #  highly satisfied
        time.sleep(0.5)

        get_id("header~QID21~3").click()  # taste
        get_id("QID21-1-12-col-label").click()  #  highly satisfied
        time.sleep(0.5)

        get_id("header~QID21~4").click()  # ease
        get_id("QID21-13-12-col-label").click()  #  highly satisfied
        time.sleep(0.5)

        get_id("header~QID21~5").click()  # speed
        get_id("QID21-4-12-col-label").click()  #  highly satisfied
        time.sleep(0.5)

        get_id("header~QID21~6").click()  # exterior cleanliness
        get_id("QID21-9-12-col-label").click()  #  highly satisfied
        time.sleep(0.5)

        get_id("header~QID21~7").click()  # temperature
        get_id("QID21-2-12-col-label").click()  #  highly satisfied
        time.sleep(0.5)

        get_id("header~QID21~8").click()  # accuracy
        get_id("QID21-16-12-col-label").click()  #  highly satisfied
        time.sleep(0.5)

    case "desktop":
        get_radio_clickable("QR~QID21~11~12").click()
        get_radio_clickable("QR~QID21~1~12").click()
        get_radio_clickable("QR~QID21~13~12").click()
        get_radio_clickable("QR~QID21~7~12").click()
        get_radio_clickable("QR~QID21~16~12").click()
        get_radio_clickable("QR~QID21~4~12").click()
        get_radio_clickable("QR~QID21~9~12").click()
        get_radio_clickable("QR~QID21~2~12").click()


get_id("NextButton").click()


# 09 RETURN & RECOMMEND NEXT MONTH
get_radio_clickable("QR~QID41~1~6").click()
get_radio_clickable("QR~QID41~2~6").click()
get_id("NextButton").click()


# 10 PROBLEM ENCOUNTERED IN VISIT
get_id("QID38-2-label").click()
get_id("NextButton").click()


# 11 ORDER ITEMS
get_id("QID103-1-label").click()
get_id("QID103-2-label").click()
get_id("QID103-3-label").click()
get_id("NextButton").click()


# 11.a BEEF ITEMS
get_id("QID46-22-label").click()
get_id("NextButton").click()


# 11.b SIDE ITEMS
get_id("QID47-3-label").click()
get_id("NextButton").click()


# 11.c DRINK ITEMS
get_id("QID107-14-label").click()
get_id("NextButton").click()


# 12 WHOPPER SATISFACTION
get_id("QID48-12-label").click()
get_id("NextButton").click()


# 13 WHOPPER CATEGORY SATISFACTION
match PLATFORM:
    case "mobile":
        raise NotImplementedError()

    case "desktop":
        get_radio_clickable("QR~QID49~1~12").click()
        get_radio_clickable("QR~QID49~2~12").click()
        get_radio_clickable("QR~QID49~3~12").click()
        get_radio_clickable("QR~QID49~4~12").click()
        get_radio_clickable("QR~QID49~5~12").click()
        get_radio_clickable("QR~QID49~6~12").click()
        get_radio_clickable("QR~QID49~7~12").click()
        get_radio_clickable("QR~QID49~9~12").click()


get_id("NextButton").click()


# 14 WHOPPER REPURCHASE LIKELINESS
get_id("QID50-1-label").click()
get_id("NextButton").click()


# 15 WHOPPER REPURCHASE LIKELINESS
get_id("QID121-2-label").click()
get_id("NextButton").click()


# 16 WHOPPER REPURCHASE LIKELINESS
get_id("QID60-1-label").click()
get_id("NextButton").click()


# 17 REASON FOR VISITING
get_id("QID62-4-label").click()
get_id("NextButton").click()


# 18 SANDWICH CUSTOMIZATION
get_id("QID57-2-label").click()
get_id("NextButton").click()


# 19 SANDWICH CUSTOMIZATION
get_id("QID94-2-label").click()
get_id("NextButton").click()


# 20 PARTY SIZE
get_id("QID55-1-label").click()
get_id("NextButton").click()


# 21 SEE SURVEY SOURCE
get_id("QID97-1-label").click()
get_id("NextButton").click()


# 22 OUTSTANDING SERVICE?
get_id("QID78-2-label").click()  # no
get_id("NextButton").click()


# 23 FUTURE PROMOTIONAL OPPORTUNITIES?
get_id("QID100-2-label").click()  # no
get_id("NextButton").click()


get_id("EndOfSurvey").text


final_text_blurb = get_id("EndOfSurvey").text
VALIDATION_CODE_PATTERN = r"Validation Code:\s*([A-Z0-9]+)"
code_match = re.search(VALIDATION_CODE_PATTERN, final_text_blurb)

end_time = time.time()

print(f"Robinhood took {end_time - start_time:.1f}s")

if code_match is None:
    print("failed to get code automatically, see webpage and extract manually")
    input("waiting for user to close the page")
else:
    print(f"SUCCESS! {code_match.group(0)}")

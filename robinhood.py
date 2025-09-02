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
from loguru import logger
from tqdm import tqdm

logger.remove()
logger.add(
    lambda msg: tqdm.write(msg, end=""),
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
)

start_time = time.time()
logger.info("🚀 Starting Burger King Survey Automation")

logger.info("🔧 Installing Chrome WebDriver")
service = Service(ChromeDriverManager().install())
logger.success("✅ Chrome WebDriver installed successfully")

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

logger.info("🌐 Launching headless Chrome browser")
driver = webdriver.Chrome(service=service, options=options)
logger.success("✅ Chrome browser launched in headless mode")

PLATFORM: Literal["desktop"] | Literal["mobile"] = "desktop"
BK_URL = r"https://www.mybkexperience.com/"

logger.info(f"📍 Navigating to Burger King survey: {BK_URL}")
driver.get(BK_URL)
driver.maximize_window()
logger.success("✅ Successfully loaded survey page")


TIMEOUT_SECONDS = 10
wait = WebDriverWait(driver, TIMEOUT_SECONDS)


logger.info("🇫️ Switching to survey iframe")
form_iframe = driver.find_element(By.CLASS_NAME, r"Home_iframe__T3nfU")
driver.switch_to.frame(form_iframe)
logger.success("✅ Successfully switched to iframe")

total_stages = 23
progress_bar = tqdm(total=total_stages, desc="🍔 Survey Progress", unit="stage", colour="green", position=0, leave=True)


# @lru_cache(maxsize=100)
def get_id(element_id: str):
    return wait.until(EC.element_to_be_clickable((By.ID, element_id)))


logger.info("🏢 Stage 00: Entering store information")
get_id("QR~QID114").send_keys("5079")
get_id("NextButton").click()
logger.success("✅ Store information submitted")
progress_bar.update(1)


logger.info("📅 Stage 01: Filling visit details and datetime")

ONTARIO_OPTION = "46"
Select(get_id("QR~QID6")).select_by_value(ONTARIO_OPTION)

VISIT_DATETIME = datetime.now() - timedelta(minutes=5)
logger.debug(f"Visit datetime set to: {VISIT_DATETIME.strftime('%m/%d/%Y %I:%M %p')}")

driver.execute_script(
    f"arguments[0].value = '{VISIT_DATETIME.strftime('%m/%d/%Y')}';",
    get_id("QR~QID118~2"),
)
get_id("QR~QID8#1~1").send_keys(VISIT_DATETIME.strftime("%I"))
get_id("QR~QID8#2~1").send_keys(VISIT_DATETIME.strftime("%m"))
get_id("QR~QID8#3~1").send_keys(VISIT_DATETIME.strftime("%p"))
get_id("NextButton").click()
logger.success("✅ Visit details submitted")
progress_bar.update(1)


logger.info("⭐ Stage 02: Setting overall satisfaction rating")
get_id("QID18-22-label").click()
get_id("NextButton").click()
logger.success("✅ Overall satisfaction rating submitted")
progress_bar.update(1)


# user_response = input("Give a 3 sentence answer to your experience at BK: ")

# if len(user_response) < 40:
if True:
    OVERALL_SATISFACTION_RESPONSE = "everything was good, no issues with the order! service was fast & efficient like usual. restaurant was clean and experience met expectations"
else:
    OVERALL_SATISFACTION_RESPONSE = user_response

logger.info("📝 Stage 03: Entering satisfaction feedback")
logger.debug(f"Feedback text: {OVERALL_SATISFACTION_RESPONSE[:50]}...")
get_id("QR~QID120").send_keys(OVERALL_SATISFACTION_RESPONSE)
get_id("NextButton").click()
logger.success("✅ Satisfaction feedback submitted")
progress_bar.update(1)


logger.info("🍽️ Stage 04: Selecting order type")
get_id("QID13-2-label").click()
get_id("NextButton").click()
logger.success("✅ Order type selected")
progress_bar.update(1)


logger.info("📍 Stage 05: Selecting order placement location")
get_id("QID12-2-label").click()
get_id("NextButton").click()
logger.success("✅ Order placement location selected")
progress_bar.update(1)


logger.info("👑 Stage 06: Royal Perks membership question")
# get_id("QID83-1-label").click() # this is YES to ROYAL PERKS
get_id("QID83-2-label").click()
get_id("NextButton").click()
logger.success("✅ Royal Perks question answered")
progress_bar.update(1)


logger.info("🤔 Stage 07: Customer ritual questions")
get_id("QID123-3-label").click()  # i dont remember
get_id("QID124-3-label").click()  # i dont remember
get_id("NextButton").click()
logger.success("✅ Customer ritual questions answered")
progress_bar.update(1)


logger.info("📊 Stage 08: Category satisfaction ratings")


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
logger.success("✅ Category satisfaction ratings completed")
progress_bar.update(1)


logger.info("🔁 Stage 09: Return & recommendation likelihood")
get_radio_clickable("QR~QID41~1~6").click()
get_radio_clickable("QR~QID41~2~6").click()
get_id("NextButton").click()
logger.success("✅ Return & recommendation questions answered")
progress_bar.update(1)


logger.info("⚠️ Stage 10: Problems encountered during visit")
get_id("QID38-2-label").click()
get_id("NextButton").click()
logger.success("✅ Problem question answered")
progress_bar.update(1)


logger.info("🍔 Stage 11: Order items selection")
get_id("QID103-1-label").click()
get_id("QID103-2-label").click()
get_id("QID103-3-label").click()
get_id("NextButton").click()
logger.success("✅ Order items selected")
progress_bar.update(1)


logger.info("🥩 Stage 11a: Beef items specification")
get_id("QID46-22-label").click()
get_id("NextButton").click()
logger.success("✅ Beef items specified")
progress_bar.update(1)


logger.info("🍟 Stage 11b: Side items specification")
get_id("QID47-3-label").click()
get_id("NextButton").click()
logger.success("✅ Side items specified")
progress_bar.update(1)


logger.info("🥤 Stage 11c: Drink items specification")
get_id("QID107-14-label").click()
get_id("NextButton").click()
logger.success("✅ Drink items specified")
progress_bar.update(1)


logger.info("🍔 Stage 12: Whopper satisfaction rating")
get_id("QID48-12-label").click()
get_id("NextButton").click()
logger.success("✅ Whopper satisfaction rated")
progress_bar.update(1)


logger.info("🍔 Stage 13: Whopper category satisfaction ratings")
match PLATFORM:
    case "mobile":
        raise NotImplementedError()

    case "desktop":
        logger.debug("Filling desktop Whopper category ratings")
        get_radio_clickable("QR~QID49~1~12").click()
        get_radio_clickable("QR~QID49~2~12").click()
        get_radio_clickable("QR~QID49~3~12").click()
        get_radio_clickable("QR~QID49~4~12").click()
        get_radio_clickable("QR~QID49~5~12").click()
        get_radio_clickable("QR~QID49~6~12").click()
        get_radio_clickable("QR~QID49~7~12").click()
        get_radio_clickable("QR~QID49~9~12").click()


get_id("NextButton").click()
logger.success("✅ Whopper category satisfaction completed")
progress_bar.update(1)


logger.info("🔁 Stage 14: Whopper repurchase likelihood")
get_id("QID50-1-label").click()
get_id("NextButton").click()
logger.success("✅ Whopper repurchase likelihood rated")
progress_bar.update(1)


logger.info("🔁 Stage 15: Additional Whopper preference question")
get_id("QID121-2-label").click()
get_id("NextButton").click()
logger.success("✅ Additional Whopper question answered")
progress_bar.update(1)


logger.info("🔁 Stage 16: Final Whopper preference question")
get_id("QID60-1-label").click()
get_id("NextButton").click()
logger.success("✅ Final Whopper question answered")
progress_bar.update(1)


logger.info("🎯 Stage 17: Reason for visiting BK")
get_id("QID62-4-label").click()
get_id("NextButton").click()
logger.success("✅ Visit reason selected")
progress_bar.update(1)


logger.info("⚙️ Stage 18: Sandwich customization preferences")
get_id("QID57-2-label").click()
get_id("NextButton").click()
logger.success("✅ Customization preferences set")
progress_bar.update(1)


logger.info("⚙️ Stage 19: Additional customization question")
get_id("QID94-2-label").click()
get_id("NextButton").click()
logger.success("✅ Additional customization answered")
progress_bar.update(1)


logger.info("👥 Stage 20: Party size information")
get_id("QID55-1-label").click()
get_id("NextButton").click()
logger.success("✅ Party size specified")
progress_bar.update(1)


logger.info("📱 Stage 21: Survey source information")
get_id("QID97-1-label").click()
get_id("NextButton").click()
logger.success("✅ Survey source answered")
progress_bar.update(1)


logger.info("⭐ Stage 22: Outstanding service question")
get_id("QID78-2-label").click()  # no
get_id("NextButton").click()
logger.success("✅ Outstanding service question answered")
progress_bar.update(1)


logger.info("🎁 Stage 23: Promotional opportunities question")
get_id("QID100-2-label").click()  # no
get_id("NextButton").click()
logger.success("✅ Promotional opportunities answered")
progress_bar.update(1)


logger.info("🏁 Survey completion - extracting validation code")
get_id("EndOfSurvey").text

final_text_blurb = get_id("EndOfSurvey").text
VALIDATION_CODE_PATTERN = r"Validation Code:\s*([A-Z0-9]+)"
code_match = re.search(VALIDATION_CODE_PATTERN, final_text_blurb)

end_time = time.time()
execution_time = end_time - start_time

progress_bar.close()
logger.info(f"⏱️ Total execution time: {execution_time:.1f} seconds")

if code_match is None:
    logger.error("❌ Failed to extract validation code automatically")
    logger.warning("👀 Please check the webpage and extract the code manually")
    input("Press Enter when ready to close the page...")
else:
    validation_code = code_match.group(1)
    logger.success(f"🎉 SUCCESS! Validation Code: {validation_code}")
    logger.success("✅ Survey automation completed successfully!")

logger.info("🖼️ Cleaning up browser session")
driver.quit()
logger.success("✅ Browser closed successfully")

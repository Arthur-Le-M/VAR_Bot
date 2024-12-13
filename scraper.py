from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

class Scraper:

    def __init__(self) -> None:

        service = Service("./assets/drivers/chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)
    
    def break_cookie(self):
        """
        Close cookie modal and close ads
        """
        wait = WebDriverWait(self.driver, 15)

        cookie_button = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "CybotCookiebotDialogBodyButtonDecline")
            )
        )

        cookie_button.click()

        #Ads modal
        close_modal_button = self.driver.find_element(By.CSS_SELECTOR, ".modal-body > div")

        close_modal_button.click()

        
    def scrap_five_website(self, url: str):
        """
        Get the website page and gather links of videos
        """
        self.driver.get(url)

        wait = WebDriverWait(self.driver, 15)

        self.break_cookie()
        
        timeline_events = self.driver.find_elements(By.CLASS_NAME, "lf-video-timeline-event.container")
        links = []

        for event in timeline_events:

            self.driver.execute_script("arguments[0].scrollIntoView(true);", event)
    
            event.click()
            
            wait.until(EC.visibility_of_element_located((By.ID, "videoModal___BV_modal_outer_")))
            
            share_container = self.driver.find_element(By.CLASS_NAME, "lf-share-buttons-container")
            
            first_a_element = share_container.find_element(By.TAG_NAME, "a")
            link = first_a_element.get_attribute("href")
            
            links.append(link.split("u=")[1])

            modal_outer = self.driver.find_element(By.ID, "videoModal___BV_modal_body_")
            ActionChains(self.driver).move_to_element_with_offset(modal_outer, 300, 300).click().perform()
            wait.until(
                EC.invisibility_of_element_located((By.ID, "videoModal___BV_modal_outer_"))
            )
        
        with open("playlist.txt", "w", encoding="utf-8") as f:
            for l in links:
                f.write(l + "\n")
        
        self.driver.close()
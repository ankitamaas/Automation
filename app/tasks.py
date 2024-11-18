from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.models import Category, Keyword, ScrapedResult
from django.utils import timezone
import logging
from celery import shared_task
logger = logging.getLogger(__name__)


@shared_task
def periodic_scraping_task():
    # Path to ChromeDriver
    chrome_service = Service()  # Update this path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        categories = Category.objects.all()
        current_time = timezone.now()

        for category in categories:
            if current_time >= category.schedule_time:
                keywords = Keyword.objects.filter(category=category)

                for keyword in keywords:
                    try:
                        driver.get(f'https://www.google.com/search?q={keyword.name}')

                        # Wait for results to load
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.tF2Cxc'))  # Update selector
                        )

                        # Extract the first result
                        search_results = driver.find_elements(By.CSS_SELECTOR, '.tF2Cxc')  # Update selector
                        if search_results:
                            first_result = search_results[0].find_element(By.CSS_SELECTOR, 'a')
                            url = first_result.get_attribute('href')

                            if not ScrapedResult.objects.filter(keyword=keyword, url=url).exists():
                                ScrapedResult.objects.create(
                                    keyword=keyword,
                                    url=url,
                                    page_number=1,
                                    position=1,
                                    scrape_time=current_time
                                )
                        else:
                            logger.warning(f"No results found for keyword '{keyword.name}'.")

                    except Exception as e:
                        logger.warning(f"Error while scraping keyword '{keyword.name}': {e}")
                        continue

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        driver.quit()

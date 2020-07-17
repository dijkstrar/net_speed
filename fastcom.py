from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from contextlib import contextmanager

@contextmanager
def get_chrome() -> Chrome:
    # https://docs.python.org/3.7/library/contextlib.html#contextlib.contextmanager
    opts = ChromeOptions()
    opts.headless = True
    driver = Chrome(options=opts,executable_path=r'/usr/lib/chromium-browser/chromedriver')
    yield driver
    driver.close()


def wait_visible(driver: Chrome, selector: str, timeout: int = 2):
    cond = EC.visibility_of_any_elements_located((By.CSS_SELECTOR, selector))
    try:
        WebDriverWait(driver, timeout).until(cond)
    except TimeoutException as e:
        raise LookupError(f'{selector} is not visible after {timeout}s') from e


def extract_speed_info(soup: BeautifulSoup) -> dict:
    dl_speed = float(soup.select_one('#speed-value').text)
    upload_speed = float(soup.select_one('#upload-value').text)
    if soup.select_one('#upload-units').text == 'Kbps':
        upload_speed/=1000
    if soup.select_one('#speed-units').text == 'Kbps':
        dl_speed/=1000
        
    return {
        'upload': float(upload_speed),
        'download': float(dl_speed)
    }


def run_speed_test() -> dict:
    with get_chrome() as driver:
        print('visit page')
        driver.get('https://fast.com/en')
        
        # Obtain download speeds
        download_done_selector = '#speed-value.succeeded'
        wait_visible(driver, download_done_selector, timeout=60)
        print('VISIBLE')
        # Obtain upload speed
        link = driver.find_element_by_link_text('Show more info')
        link.click()
        print('CLICKED')
        upload_done_selector = '#upload-value.succeeded'
        wait_visible(driver, upload_done_selector, timeout=60)
        
        
        # Select the resulting speeds
        print('SELECT RESULTS')
        results_selector = '.speed-controls-container'
        results_el = driver.find_element_by_css_selector(results_selector)
        results_html = results_el.get_attribute('outerHTML')

    soup = BeautifulSoup(results_html, 'html.parser')
    info = extract_speed_info(soup)
    print(info)
    return info

if __name__ == '__main__':
    run_speed_test()

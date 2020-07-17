from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from contextlib import contextmanager
import time


@contextmanager
def get_chrome() -> Chrome:
    # https://docs.python.org/3.7/library/contextlib.html#contextlib.contextmanager
    opts = ChromeOptions()
    opts.headless = False
    opts.add_argument('disable-infobars')
    opts.add_argument('disable-extensions')
    opts.add_argument('no-sandbox')
    opts.add_argument('disable-dev-shm-usage')
    driver = Chrome(options=opts,executable_path=r'/usr/lib/chromium-browser/chromedriver')
    yield driver
    driver.close()
    driver.quit()


def wait_visible(driver: Chrome, selector: str, timeout: int = 2):
    cond = EC.visibility_of_any_elements_located((By.CSS_SELECTOR, selector))
    try:
        WebDriverWait(driver, timeout).until(cond)
    except TimeoutException as e:
        raise LookupError(f'{selector} is not visible after {timeout}s') from e


def extract_speed_info(soup: BeautifulSoup) -> dict:
    ping = float(soup.select_one('.ping-speed').text)
    ping_unit = soup.select_one('.result-item-ping .result-data-unit').text 
    
    dl_speed = float(soup.select_one('.download-speed').text)
    dl_unit = soup.select_one('.result-item-download .result-data-unit').text
    
    upload_speed = float(soup.select_one('.upload-speed').text)
    upload_unit = soup.select_one('.result-item-upload .result-data-unit').text
    return {
        'upload': float(upload_speed),
        'download': float(dl_speed),
        'ping': float(ping)
    }


def run_speed_test() -> dict:
    with get_chrome() as driver:
        driver.get('https://speedtest.net/run')
        # Obtain download speeds
        download_done_selector = '.result-container-speed-active'
        wait_visible(driver, download_done_selector, timeout=300)
        
        # Select the resulting speeds
        results_selector = '.result-container-data'
        results_el = driver.find_element_by_css_selector(results_selector)
        results_html = results_el.get_attribute('outerHTML')
    # we're finished with chrome, let it close (by exiting with block)
    soup = BeautifulSoup(results_html, 'html.parser')
    info = extract_speed_info(soup)
    print(info)
    return info
if __name__ == '__main__':
    start_time=time.time()
    print('FETCHING SPEEDS')
    run_speed_test()
    print("--- %s seconds ---"% (time.time()-start_time))

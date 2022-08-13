import spacy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import logging
from settings import TARGET_URL
import sys

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('outputs.log')
    ]
)
logger = logging.getLogger()

nlp = spacy.load('ja_ginza')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

analyze_urls = {
    TARGET_URL: False
}


def analyze():
    try:
        filtered_urls = dict(filter(lambda item: not item[1], analyze_urls.items()))
        url, _ = filtered_urls.popitem()
        analyze_urls[url] = True
        driver.get(url)
        logger.warning(url)
        root = driver.find_element(by=By.CLASS_NAME, value='notion-root')
        elements = root.find_elements(by=By.CLASS_NAME, value='notion-semantic-string')
        for element in tqdm(elements, desc='analyzing'):
            content = element.get_attribute('innerHTML')
            extract(content)

        link_elements = root.find_elements(by=By.CLASS_NAME, value='notion-link')
        urls = map(lambda link_element: link_element.get_attribute('href'), link_elements)
        for url in urls:
            if url is None:
                continue
            if should_add_analyze_urls(url):
                analyze_urls[url] = False
    except WebDriverException as e:
        logger.error(e.msg)

    if any(analyze_urls.values()):
        analyze()


def should_add_analyze_urls(url: str) -> bool:
    if not url.startswith(TARGET_URL):
        return False
    if url in analyze_urls:
        return False
    return True


def extract(content):
    doc = nlp(content)
    for ent in doc.ents:
        if ent.label_.__eq__('Person'):
            logger.warning(ent.text)


if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    analyze()

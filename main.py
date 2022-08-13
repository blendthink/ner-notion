import spacy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from typing import List
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import logging
from settings import TARGET_URL
import sys

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        # logging.FileHandler('outputs.log')
        logging.FileHandler('outputs.electra.log')
    ]
)
logger = logging.getLogger()

# nlp = spacy.load('ja_ginza')
nlp = spacy.load('ja_ginza_electra')

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
            contents = element.get_attribute('innerHTML')
            extracts(contents)

        link_elements = root.find_elements(by=By.CLASS_NAME, value='notion-link')
        urls = map(lambda link_element: link_element.get_attribute('href'), link_elements)
        for url in urls:
            if url is None:
                continue
            if should_add_analyze_urls(url):
                analyze_urls[url] = False
    except WebDriverException as e:
        logger.warning(e.msg)

    if not all(analyze_urls.values()):
        analyze()


def should_add_analyze_urls(url: str) -> bool:
    if not url.startswith(TARGET_URL):
        return False
    if url in analyze_urls:
        return False
    return True


def extracts(contents):
    split_contents = split_content(contents)
    if type(split_contents) is str:
        extract(split_contents)
    else:
        for content in tqdm(split_contents, leave=False, desc='analyzing split_contents'):
            extract(content)


def extract(content):
    doc = nlp(content)
    for ent in doc.ents:
        if ent.label_.__eq__('Person'):
            logger.error(ent.text)


# Tokenization error: Input is too long, it can't be more than 49149 bytes, was 83630
def split_content(content, max_length=5000) -> str | List[str]:
    if len(content) < max_length:
        return content

    return [content[i:i + 5000] for i in range(0, len(content), 5000)]


if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    analyze()
    print('Complete!')

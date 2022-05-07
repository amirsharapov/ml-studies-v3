from enum import Enum


class Reports(Enum):
    ScrapeHtml = 'scrape_htmls'
    ExtractTexts = 'extract_texts'
    ProcessTexts = 'process_texts'


class OutputPaths(Enum):
    SCRAPE_HTMLS = 'data/cnn_articles_html/{}.html'
    EXTRACT_TEXTS = 'data/cnn_articles_extracted_texts/{}.json'
    PROCESS_TEXTS = 'data/cnn_articles_processed_texts/{}.csv'

    def format(self, filename):
        return self.value.format(filename)


class Status(Enum):
    FAILURE = 'FAILURE'
    SUCCESS = 'SUCCESS'

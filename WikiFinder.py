import wikipedia
from bs4 import BeautifulSoup


# This is the object that can find the information in Wikipedia
class WikiFinder:
    def __init__(self, query: str):
        self.query = query

    def __call__(self):
        is_rus = self.is_russian(self.query)
        if is_rus:
            wikipedia.set_lang("ru")
            author_page = self.get_author_from_russian_wikipedia()
        else:
            wikipedia.set_lang("en")
            author_page = self.get_author_from_english_wikipedia()

        if not author_page:
            result = "Unfortunately, query is not founded"
            return result
        result = author_page
        return result

    # Get the url of author's image from page in Wikipedia
    @staticmethod
    def get_author_image(author_page):
        soup = BeautifulSoup(author_page.html(), "html.parser")
        image = soup.find("a", attrs={"class": "image"})
        image = image.find("img")["src"]
        if not image.startswith("https:"):
            image = "https:" + image
        return image

    # Define in what language the given request
    @staticmethod
    def is_russian(text, alphabet=set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")):
        return not alphabet.isdisjoint(text.lower())

    # Firstly, if the query has a spelling mistake, we correct it. Secondly, we find 2 first page's titles of our query
    def search_in_wikipedia(self):
        suggestion = wikipedia.suggest(self.query)
        if suggestion:
            self.query = suggestion
        search_result = wikipedia.search(self.query, 2)
        if len(search_result) == 0:
            return None
        return search_result

    # Find information about our author on English
    def get_author_from_english_wikipedia(self):
        search_result = self.search_in_wikipedia()
        if not search_result:
            return None, None
        for result in search_result:
            try:
                page = wikipedia.WikipediaPage(result)
                if page:
                    return page, wikipedia.summary(result)
                else:
                    continue
            except wikipedia.DisambiguationError:
                continue
        return None, None

    # Find information about our author on Russian
    def get_author_from_russian_wikipedia(self):
        search_result = self.search_in_wikipedia()
        if not search_result:
            return None, None
        for result in search_result:
            try:
                page = wikipedia.WikipediaPage(result)
                if page:
                    return page, wikipedia.summary(result)
                else:
                    continue
            except wikipedia.DisambiguationError:
                continue
        return None, None

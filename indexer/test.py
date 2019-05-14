from nltk.tokenize import word_tokenize
from stopwords import stop_words_slovene
from bs4 import BeautifulSoup


example_text = "»Program projektov eProstor« (en prostor za vse) ima specifični cilj zagotoviti večjo preglednost in učinkovitost pri urejanju prostora, graditvi objektov in upravljanju nepremičnin. Osnovni namen je pospešiti in izboljšati procese pri prostorskem načrtovanju, graditvi objektov in upravljanju z nepremičninami, kar je mogoče doseči s povezljivimi, enostavno dostopnimi in zanesljivimi zbirkami prostorskih podatkov."

soup = BeautifulSoup(open('data/e-prostor.gov.si/e-prostor.gov.si.1.html', 'rb'), 'html.parser')
body = soup.find('body')

htmlText = body.get_text()

word_tokens = word_tokenize(htmlText)
word_tokens = [token.lower() for token in word_tokens]


filtered_text = [w for w in word_tokens if w not in stop_words_slovene]

print(len(word_tokens))
print(len(filtered_text))
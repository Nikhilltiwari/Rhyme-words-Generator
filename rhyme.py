import requests
from bs4 import BeautifulSoup


# Datamuse API to fetch rhyming words
def get_rhyming_words(word):
    url = f"https://api.datamuse.com/words?rel_rhy={word}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return [entry['word'] for entry in response.json()]
    else:
        print(f"Failed to fetch rhyming words for {word}. Status code: {response.status_code}")
        return []

# Function to fetch word meaning from an online dictionary
def get_meaning(word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        definition = soup.find('span', {'class': 'dtText'})
        if definition:
            return definition.text.strip().replace(': ', '')
        else:
            return "Meaning not found."
    else:
        return "Meaning not found."

# Integrate rhyming words and meanings
def get_rhymes_with_meanings(word):
    rhyming_words = get_rhyming_words(word)
    rhymes_with_meanings = []
    for rw in rhyming_words:
        meaning = get_meaning(rw)
        rhymes_with_meanings.append((rw, meaning))
    return rhymes_with_meanings

# Example usage
word = "cat"
rhymes_with_meanings = get_rhymes_with_meanings(word)
for rw, meaning in rhymes_with_meanings:
    print(f"Word: {rw}, Meaning: {meaning}")

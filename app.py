from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)

# Function to fetch rhyming words using Datamuse API
def get_rhyming_words(word):
    url = f"https://api.datamuse.com/words?rel_rhy={word}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return [entry['word'] for entry in response.json()]
    else:
        print(f"Failed to fetch rhyming words for {word}. Status code: {response.status_code}")
        return []

# Function to fetch word meanings by scraping Merriam-Webster
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

# Function to integrate rhyming words and their meanings
def get_rhymes_with_meanings(word):
    rhyming_words = get_rhyming_words(word)
    rhymes_with_meanings = []
    for rw in rhyming_words:
        meaning = get_meaning(rw)
        rhymes_with_meanings.append({"word": rw, "meaning": meaning})
    return rhymes_with_meanings

@app.route('/api/rhyme', methods=['GET'])
def rhyme():
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "Please provide a word."}), 400
    
    rhymes_with_meanings = get_rhymes_with_meanings(word)
    return jsonify(rhymes_with_meanings)

if __name__ == '__main__':
    app.run(debug=True)

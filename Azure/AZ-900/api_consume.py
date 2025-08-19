'''Consuming an API with Python Requests'''

import json
import requests


def get_joke(code=False):
    ''' Consuming API Endpoint. Return Random Joke '''
    api_end_point = "https://official-joke-api.appspot.com/jokes/random"
    joke = requests.get(api_end_point)
    json_data = json.loads(joke.text)
    if code:
        print(joke.status_code)
    joke_data = f"Joke about {json_data['type']} with ID {json_data['id']}:\n"
    joke_format = f"\t{json_data['setup']}\n\t{json_data['punchline']}"
    return joke_data + joke_format


def get_joke_by_category(category="programming", code=False):
    ''' Consuming API Endpoint. Return Random Joke by Category '''
    api = "https://official-joke-api.appspot.com/jokes/" + category + "/random"
    joke = requests.get(api)
    json_data = json.loads(joke.text)[0]
    if code:
        print(joke.status_code)
    joke_data = f"Joke about {json_data['type']} with ID {json_data['id']}:\n"
    joke_format = f"\t{json_data['setup']}\n\t{json_data['punchline']}"
    return joke_data + joke_format


if __name__ == "__main__":
    print(get_joke())
    print(get_joke_by_category("general"))

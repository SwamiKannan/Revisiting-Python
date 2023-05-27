import requests



def get_motivational_quote():
    URL = 'https://zenquotes.io'
    params = {
        'api': 'random'
    }

    req = requests.get(url=URL, params=params)
    req.raise_for_status()
    res = req.json()
    quote = res[0]['q']
    author = res[0]['a']
    return(quote, author)



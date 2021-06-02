import wikipedia
def search(toSearch, amount=3):
    first, *middle, last = toSearch.get_string().split()
    results = wikipedia.summary(last, sentences = amount)
    print(results)
    return results

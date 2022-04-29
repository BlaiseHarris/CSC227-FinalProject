from bs4 import BeautifulSoup
import requests
from matplotlib import pyplot as plt

if __name__ == '__main__':
    chars = {}
    keys_removed = (' ', '_', '\n', '-', "'", '©', '"', '%')
    url = input("Input website you want analyzed: ")
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.get_text())
    for i in soup.get_text():
        if i in chars:
            chars[i] += 1
        else:
            chars[i] = 1
    for x in keys_removed:
        chars.pop(x, None)
    print("Website chosen:", r.url)
    print("------------------------------------------------------------------------------")
    print("Characters Sorted: ", sorted(chars.items(), key=lambda kv: (kv[1], kv[0])))

    plt.figure(figsize=(5,5))
    graphChars = sorted(chars.items(), key=lambda kv: (kv[1], kv[0]))
    graphChars = graphChars[-10::1]
    x, y = zip(*graphChars)

    plt.title("Character Amount on Page", fontsize = 20)
    plt.xlabel("Character", fontsize=14)
    plt.ylabel("Occured", fontsize=14)
    plt.plot(x, y)
    plt.show()
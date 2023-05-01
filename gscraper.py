import re, os, random
import urllib.request

"""
TODO: 
change to bs4
Improve Pattern
Option to parse to JSON
"""
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 OPR/75.0.3969.267",
]
start = 1
end = 75000
timeout=0

def scrapeText():
    pat3 = r'\*\*\*(?: |    )START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.{1,90}\*\*\*(.+)\*\*\*(?: |    )END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.{1,90}\*\*\*'
    pat4 = re.compile('[^a-zA-Z0-9"\s\':.;,]')
    
    for i in range(start, end):
        url = f"https://www.gutenberg.org/cache/epub/{i}/pg{i}.txt"
        print(f"Scraping URL: {url}")
        try:
            useragent = random.choice(user_agents)
            headers = {'User-Agent': useragent}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                try:
                    text = response.read().decode('utf-8')
                except UnicodeDecodeError:
                    print("Decoding Format couldn't be applied. This might happen because the 'IP blocked Page' has a different Format. \n=> No Book to scrap - Continue")
                    continue
                text = text.replace('\r', ' ').replace('\n', ' ')
                match = re.search(pat3, text)
                if match:
                    text = match.group(1)
                    text = text.replace('  ', ' ')
                    while text != text.replace('  ', ' '):
                        text = text.replace('  ', ' ')
                    text = pat4.sub('', text)
                    filename = f"book{i}.txt"
                    with open(f"./texts/{filename}", "w", encoding="utf-8") as file:
                        file.write(text)
                    print(f"File '{filename}' written.")
                else:
                    print("Pattern not found in the text.")
                    continue
        except urllib.error.HTTPError as e:
            print(f"Error fetching URL: {url}. \n{e}")


def main():
    os.makedirs("./books", exist_ok=True)
    scrapeText()

    print("----------------Program completed the task successfully----------------")


if __name__ == "__main__":
    main()

from os import environ

from bs4 import BeautifulSoup as bs

soup = bs(html_content, "lxml")

title = soup.find("title")
print(title)
print(type(title))
print(title.text)

# print(soup.body.text)
print(soup.body.p)

pList = soup.body.find_all("p")
for p in enumerate(pList):
    print(p.text)
    print("---------------")

print([bullet.text for bullet in soup.body.find_all("li")])

p2 = soup.find(id="paragraph 2")
print(p2.text)

divAll = soup.find_all("div")
print(divAll)
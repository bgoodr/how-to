from bs4 import BeautifulSoup
# Just print out the __dict__ but don't actually use it. This is just for example:
print "BeautifulSoup.__dict__ {}".format(BeautifulSoup.__dict__)
import sys
print 'sys.path {}'.format(sys.path)

# Tutorial: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
print
print(soup.prettify())
print
print soup.title
print
print soup.title.name
print
print soup.title.string
print
print soup.title.parent.name
print
print soup.p
print
print soup.p['class']
print
print soup.a
print
print soup.find_all('a')
print
print "<{}>".format(soup.find_all('a')[0])

print
print soup.find(id="link3")
print

for link in soup.find_all('a'):
    print(link.get('href'))

print(soup.get_text())

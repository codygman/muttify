#!/usr/bin/env python
from optparse import OptionParser
from BeautifulSoup import BeautifulSoup, SoupStrainer, Tag
from urlparse import urlparse

parser = OptionParser()
parser.add_option("-i", "--html", dest="input_html", help="read html data")
parser.add_option("-f", "--file", dest="input_file", help="read html data from file")
(options, args) = parser.parse_args()

def validate_link(link):
    try:
        parsed_link = urlparse(link.get('href'))
        if parsed_link.scheme == "http" and parsed_link.netloc != "":
            return True
    except Exception:
        pass
    return None


def make_links_readable(html):
    soup = BeautifulSoup(html)
    for link in soup.findAll('a'):#links:
        print link.text
        if validate_link(link) and link.get('href', None):
            if not link.text:
                link.replaceWith(link.get('href'))
            else:
                div = Tag(soup, 'div')
                div.setString(link.text)
                br = Tag(soup, 'br')
                new_link = Tag(soup, 'a')
                new_link.setString("(%s)" % (link.get('href')) )
                div.append(br)
                div.append(new_link)
                link.replaceWith(div)
            print

    return soup

if options.input_html != None:
    new_html = make_links_readable(options.input_html)
    print new_html

if options.input_file != None:
    content = None
    print content
    with open(options.input_file, 'r') as f:
        content = f.read()
    new_html = make_links_readable(content)
    print new_html


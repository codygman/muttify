#!/usr/bin/env python
from optparse import OptionParser
import ConfigParser
from BeautifulSoup import BeautifulSoup, SoupStrainer, Tag
from urlparse import urlparse
import googl

parser = OptionParser()
parser.add_option("-i", "--html", dest="input_html", help="read html data")
parser.add_option("-f", "--file", dest="input_file", help="read html data from file")
parser.add_option("-s", "--use-short-links", dest="use_short_links", default=False, help="Do you want to use short links?")
(options, args) = parser.parse_args()

config = ConfigParser.SafeConfigParser()
config.read('config.cfg')
API_KEY = config.get('googl api', 'api_key') 

def validate_link(link):
    try:
        parsed_link = urlparse(link.get('href'))
        if parsed_link.scheme == "http" and parsed_link.netloc != "":
            return True
    except Exception:
        pass
    return None

def shorten_link(soup, link):
    api = googl.Googl(API_KEY)
    googl_link = api.shorten(link.get('href'))
    new_link = Tag(soup, 'a')
    new_link['href'] = googl_link.get('id', None)
    if new_link.get('href', None):
        new_link.setString(link.text)
        return new_link
    else:
        return None

def make_links_readable(html):
    """
    Goes through links making them readable
    If they are too long, they are turned into goo.gl links
    timing stats:
    before multiprocess = 0m18.063s
    """
    soup = BeautifulSoup(html)
    for link in soup.findAll('a'):#links:
        oldlink = link
        if link and len(link.get('href', '')) > 90 and options.use_short_links:
            #make into goo.gl link
            short_link = shorten_link(soup, link)
            if short_link != None:
                link = short_link

        if validate_link(link) and link.get('href', None):
            if not link.text:
                oldlink.replaceWith(link.get('href', "No href link to replace with"))
            else:
                div = Tag(soup, 'div')
                div.setString(link.text)
                br = Tag(soup, 'br')
                new_link = Tag(soup, 'a')
                new_link.setString("(%s)" % (link.get('href')) )
                div.append(br)
                div.append(new_link)
                oldlink.replaceWith(div)
            print

    return soup

if options.input_html != None:
    new_html = make_links_readable(options.input_html)
    print new_html

if options.input_file != None:
    content = None
    with open(options.input_file, 'r') as f:
        content = f.read()
    new_html = make_links_readable(content)
    print new_html


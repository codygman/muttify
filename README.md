This was made to turn email links from html messages from this:
    <a href="http://www.google.com">Google</a>

To this:
    Google
    (http://www.google.com)

I use mutt and encountered limitations when converting html to text with w3m... the links were gone!
So I came up with this, so my urxvt terminal would see the link, parse it, and make it clickable.

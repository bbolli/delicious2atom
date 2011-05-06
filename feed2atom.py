# encoding: utf-8

from time import strftime
import xmltramp


def isodate(time):
    return strftime('%Y-%m-%dT%H:%M:%SZ', time)

class FeedToAtom:
    """Convert a feedparser feed to an Atom 1.0 XML document"""

    atom = xmltramp.Namespace('http://www.w3.org/2005/Atom')

    def convert(self, feed):
	f = self.feed = xmltramp.Element(self.atom.feed, prefixes=self.atom._prefix(None))
	f.title = feed.feed.title
	f.link = feed.feed.link
	u = feed.get('updated') or feed.feed.get('updated_parsed')
	if u:
	    f.updated = isodate(u)
	f.id = feed.href
	f.link = {'rel': 'self', 'href': feed.href}
	for entry in feed.entries:
	    if not self.filter(entry):
		continue
	    e = self.entry = f._new('entry')
	    e._new('author').name = entry.author
	    e.title = entry.title
	    e.updated = isodate(entry.updated_parsed)
	    e.id = entry.id
	    e.link = {'rel': 'alternate', 'type': 'text/html', 'href': entry.link}
	    if 'summary' in entry:
		e.summary = entry.summary
	    for t in entry.tags:
		e['category':] = {'scheme': t.scheme, 'term': t.term}
	    self.post_process(entry)
	return f.__repr__(1, 1)

    def filter(self, entry):
	"""Override to filter the entries"""
	return True

    def post_process(self, entry):
	"""Override to post-process the entries"""
	pass


if __name__ == '__main__':
    import sys, feedparser
    c = FeedToAtom()
    for url in sys.argv[1:]:
	print c.convert(feedparser.parse(url)).encode('utf-8')

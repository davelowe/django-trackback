import xmlrpclib, urllib, urllib2
from xml.sax import parseString, SAXParseException
from xml.sax.handler import ContentHandler
import re

PINGBACK_RE = re.compile('<link rel="pingback" href="([^"]+)" ?/?>')
TRACKBACK_RE = re.compile(r'(<rdf:RDF .*?</rdf:RDF>)', re.MULTILINE)




class RdfHandler(ContentHandler):
    """
    Copyright (c) 2008, Bruce Kroeze http://solidsitesolutions.com
    
    Released under New BSD License
    
    xml -> dictionary of {dc:identifier => trackback:ping|rdf:about}

    Parse a given html page, and retrieve the rdf:about information associated
    with a given href.
    
    """

    link = {'preferred' : None}
    
    def best_link(self):
        for k in ('trackback:ping', 'about', 'rdf:about'):
            if self.link.has_key(k):
                return self.link[k]
    
    def startElement(self, name, attributes):
        if name == 'rdf:Description':
            for k in attributes.getNames():
                if k in ('trackback:ping', 'about', 'rdf:about'):
                    self.link[k] =attributes.getValue(k)
            
            self.link['preferred'] = self.best_link()
            
            
            
def discover_trackback_url(url):
    """
    Copyright (c) 2008, Bruce Kroeze http://solidsitesolutions.com
    
    Released under New BSD License
    
    Loads a remote document and searches for the trackback url as of
    http://www.sixapart.com/pronet/docs/trackback_spec
    
    """
    try:
        remote = urllib2.urlopen(url)
    except urllib2.URLError, e:
        return None
        
    link = None
    body = remote.read()
    body = body.replace('\n',' ')
    body = body.replace('\r',' ')
    for rdf in TRACKBACK_RE.findall(body):
        try:
            doc = parseString(rdf, RdfHandler())
            link = RdfHandler.link['preferred']
            if link:
                break
        except SAXParseException:
            pass

    return link
    
    
    
def discover_pingback_url(url):
    """
    Load a remote document and search for the pingback url as of
    http://www.hixie.ch/specs/pingback/pingback

    TODO: this is not very robust, just a proof-of-concept for now

    TODO: should be DOS safe, i.e. only loading a defined portion of the
    remote document.

    """
    try:
        remote = urllib2.urlopen(url)
    except urllib2.URLError:
        return None
    
    try:
        # first look for a X-Pingback header
        pingurl = remote.info().getheader('X-Pingback')
        return pingurl
    except:
        pass
        
    try:
        # then try to find a <link> element
        pingurl = PINGBACK_RE.findall(remote.read())
        return pingurl[0]
    except:
        pass
        
    return None
    

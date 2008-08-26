"""
http://www.sixapart.com/pronet/docs/trackback_spec

TrackBack Technical Specification

This document describes TrackBack, a framework for peer-to-peer communication 
and notifications between web sites. The central idea behind TrackBack is the 
idea of a TrackBack ping, a request saying, essentially, "resource A is 
related/linked to resource B." A TrackBack "resource" is represented by a 
TrackBack Ping URL, which is just a standard URI.

Using TrackBack, sites can communicate about related resources. For example, 
if Weblogger A wishes to notify Weblogger B that he has written something 
interesting/related/shocking, A sends a TrackBack ping to B. This accomplishes
two things:

   1. Weblogger B can automatically list all sites that have referenced a 
   particular post on his site, allowing visitors to his site to read all 
   related posts around the web, including Weblogger A's.

   2. The ping provides a firm, explicit link between his entry and yours, as 
   opposed to an implicit link (like a referrer log) that depends upon outside
   action (someone clicking on the link).

Sending a TrackBack Ping

TrackBack uses a REST model, where requests are made through standard HTTP 
calls. To send a TrackBack ping, the client makes a standard HTTP request to 
the server, and receives a response in a simple XML format (see below for 
more details).

In the TrackBack system, the URL that receives TrackBack pings is the 
TrackBack Ping URL. A typical TrackBack Ping URL looks like 
http://www.example.com/trackback/5, where 5 is the TrackBack ID. Server 
implementations can use whatever format makes sense for the TrackBack Ping 
URL; client implementations should not depend on a particular format.

To send a ping, the client sends an HTTP POST request to the TrackBack Ping 
URL. The client MUST send a Content-Type HTTP header, with the content type 
set to application/x-www-form-urlencoded. The client SHOULD include the 
character encoding of the content being sent (title, excerpt, and weblog name)
in the charset attribute of the Content-Type header.

For example, a ping request might look like:

    POST http://www.example.com/trackback/5
    Content-Type: application/x-www-form-urlencoded; charset=utf-8
    
    title=Foo+Bar&url=http://www.bar.com/&excerpt=My+Excerpt&blog_name=Foo

The possible parameters in the request content are the following:

    * title

      The title of the entry.

      Optional.
      
      
    * excerpt

      An excerpt of the entry.

      Optional.
      
      
    * url

      The permalink for the entry. Like any permalink, this should point as 
      closely as possible to the actual entry on the HTML page, as it will 
      be used when linking to the entry in question.

      Required. If a client neglects to send a url, the server MUST respond 
      with an error message.
      
      
    * blog_name

      The name of the weblog to which the entry was posted.

      Optional.
      

All of the fields provided MUST be in the character encoding specified in 
charset.

There are no length restrictions on the above fields inherent in the TrackBack
protocol, but server implementations are free to crop or ignore any of the 
above fields.

In the event of a succesful ping, the server MUST return a response in the 
following format:

    <?xml version="1.0" encoding="utf-8"?>
    <response>
    <error>0</error>
    </response>

In the event of an unsuccessful ping, the server MUST return an HTTP response 
in the following format:

    <?xml version="1.0" encoding="utf-8"?>
    <response>
    <error>1</error>
    <message>The error message</message>
    </response>

Auto-Discovery of TrackBack Ping URLs

TrackBack clients need a method of determining the TrackBack Ping URL for a 
particular URL or weblog entry. Server implementations should include embedded
RDF in the pages they produce; the RDF represents metadata about an entry, 
allowing clients to auto-discover the TrackBack Ping URL.

Sample RDF looks like this:

    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:dc="http://purl.org/dc/elements/1.1/"
             xmlns:trackback="http://madskills.com/public/xml/rss/module/trackback/">
    <rdf:Description
        rdf:about="http://www.foo.com/archive.html#foo"
        dc:identifier="http://www.foo.com/archive.html#foo"
        dc:title="Foo Bar"
        trackback:ping="http://www.foo.com/tb.cgi/5" />
    </rdf:RDF>

Note: because current validators choke on RDF embedded in XHTML, if you want 
your pages to validate you may wish to enclose the above RDF in HTML comments:

    <!--
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    ...
    </rdf:RDF>
    -->

This is not a perfect solution, but it works as a temporary fix.

The dc: elements are standard Dublin Core elements; the trackback:ping element
comes from the TrackBack Module for RSS 1.0/2.0 at 
http://madskills.com/public/xml/rss/module/trackback/.

Given a URL my_url, clients should follow these steps:

   1. Send an HTTP GET request to retrieve the contents of the page at my_url.

   2. Scan the page contents for embedded RDF. Pages can contain multiple 
   instances of embedded RDF--clients should pick the block whose 
   dc:identifier matches my_url.

   3. Extract the trackback:ping value from the block of RDF. This is the 
   TrackBack Ping URL.

Once the client has determined the TrackBack Ping URL, it can send a 
TrackBack ping (see "Sending a TrackBack Ping").

Example auto-discovery code is below in "Examples".
Examples
Sample TrackBack Implementation

To aid perspective developers in implementing TrackBack in their own systems, 
we are releasing a standalone implementation of TrackBack that is not 
dependent on Movable Type. It accepts pings sent through HTTP requests, stores
the pings locally in the filesystem, and can return a list of pings sent on a 
particular TrackBack item in RSS format. It also generates RSS files 
statically, if you want it to. This can be useful for including a list of the 
last 15 TrackBack pings on a sidebar on your site, for example.

The standalone implementation can be downloaded from 
http://www.movabletype.org/downloads/tb-standalone.tar.gz.

It is released under the Artistic License. The terms of the Artistic License 
are described at http://www.perl.com/language/misc/Artistic.html.

Installation and usage instructions are at 
http://www.movabletype.org/docs/tb-standalone.html.

Sample Auto-Discovery

The Net::TrackBack Perl module provides an easy interface for doing TrackBack 
auto-discovery.

    use Net::TrackBack::Client;
    my $url = 'http://www.example.com/weblog/';
    my $client = Net::TrackBack::Client->new;
    my $data = $client->discover($url);
    if (Net::TrackBack->is_message($data)) {
        ## An error occurred trying to fetch $url.
        die $data->message;
    } else {
        ## $data is a reference to an array of Net::TrackBack::Data objects.
        for my $resource (@$data) {
            print $resource->ping, "\n";
        }
    }

Authors

Six Apart, http://www.sixapart.com/
Version

1.2
History
1.2 (August 1, 2004)

    * Clients SHOULD send the character encoding of the content being sent in 
    the charset attribute to the Content-Type HTTP header.

    * Removed the Retrieving TrackBack Pings section, which was not standard 
    and implemented only in a couple of servers. It will return, in a 
    different format, in a future revision of the spec (2.0).

    * Cleaned up a lot of the language in the specification and made it more 
    specification-like.

    * Converted autodiscovery example to use Net::TrackBack.

1.1 (October 10, 2002)

    * TrackBack pings should now be sent using HTTP POST instead of GET. 
    The old behavior is deprecated, and support for GET will be removed in 
    January 2003.

    * In the RDF, the TrackBack Ping URL should now be stored in the 
    trackback:ping element, rather than rdf:about.

    * Changed the format of the sample TrackBack Ping URL to use the PATH_INFO
    instead of the query string.

    * The embedded RDF used for auto-discovery no longer causes pages to fail 
    validation.

    * Added sample code for auto-discovery.

1.0 (August 28, 2002)

Initial release.
Credits

Thanks to Paul Prescod and others for their guidance on making TrackBack more 
REST-like.






http://www.hixie.ch/specs/pingback/pingback


"""
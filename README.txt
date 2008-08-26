A reuseable trackback/pingback app for the django web-framework
===============================================================

Django-trackback aims to implement the trackback_ and pingback_ specifications
and provide both as a reuseable app, which can be plugged into any django
project. Although blog applications will see the greatest benefit of this app,
it's also possible to use it in any other project to make sending and
receiving trackbacks and pingbacks possible.

_`trackback` : http://www.sixapart.com/pronet/docs/trackback_spec
_`pingback` : http://www.hixie.ch/specs/pingback/pingback


Other Implementations
---------------------

Many django-based blogging apps already provide a way of receiving and/or
sending trackbacks and/or pingbacks. But except for django-pingback_, which
only implements xml-rpc pingbacks (based on the code from the 
`byteflow project`_) I was not able to find any resueable solution.

_`django-pingback` : http://code.google.com/p/django-pingback/
_`byteflow project` : http://byteflow.su/

The following django-based blogging apps/projects at least provide any of
the four combinations of sending/receiving trackbacks/pingbacks, so you 
might want to read their source, if you are interested in the topic:

  * banjo : http://code.google.com/p/banjo/
  * blogmaker : http://code.google.com/p/blogmaker/
  * byteflow : http://byteflow.su/
   


from distutils.core import setup

setup(
    name='django-trackback',
    version='0.1.0',
    description='A generic trackback and pingback app for Django',
    author='Arne Brodowski',
    author_email='arne@rcs4u.de',
    url='http://code.google.com/p/django-trackback/',
    download_url='http://code.google.com/p/django-trackback/downloads/list',
    zip_safe = False,
    packages=(
        'trackback',
        'trackback.templatetags',
        'trackback.utils',
    ),
    package_data={
        'trackback': [
            'templates/trackback/*',
        ]
    },
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Framework :: Django',
    ),
)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geoip2_extras']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<4.0', 'geoip2>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'django-geoip2-extras',
    'version': '2.0b0',
    'description': 'Additional functionality using the GeoIP2 database.',
    'long_description': '**The master branch of this project is now Python 3.7+ and Django 3.2+ only. Legacy Python and Django versions are tagged.**\n\n# Django GeoIP2 Extras\n\nUseful extras based on the `django.contrib.gis.geoip2` module, using\nthe [MaxMind GeoIP2 Lite](http://dev.maxmind.com/geoip/geoip2/geolite2/) database.\n\nThe first feature in this package is a Django middleware class that can\nbe used to add city, country level information to inbound requests.\n\n## Requirements\n\nThis package wraps the existing Django functionality, and as a result\nrelies on the same underlying requirements:\n\n    In order to perform IP-based geolocation, the GeoIP2 object\n    requires the geoip2 Python library and the GeoIP Country and/or City\n    datasets in binary format (the CSV files will not work!). Grab the\n    GeoLite2-Country.mmdb.gz and GeoLite2-City.mmdb.gz files and unzip\n    them in a directory corresponding to the GEOIP_PATH setting.\n\nThis package requires Django 3.2 or above.\n\n## Installation\n\nThis package can be installed from PyPI as `django-geoip2-extras`:\n\n```\n$ pip install django-geoip2-extras\n```\n\nIf you want to add the country-level information to incoming requests,\nadd the middleware to your project settings.\n\n```python\n# settings.py\nMIDDLEWARE = (\n    ...,\n    \'geoip2_extras.middleware.GeoIP2Middleware\',\n)\n```\n\nThe middleware will not be active unless you add a setting for the\ndefault `GEOIP_PATH` - this is the default Django GeoIP2 behaviour:\n\n```python\n# settings.py\nGEOIP_PATH = os.path.dirname(__file__)\n```\n\nNB Loading this package does *not* install the (MaxMind\ndatabase)[http://dev.maxmind.com/geoip/geoip2/geolite2/]. That is your\nresponsibility. The Country database is 2.7MB, and could be added to\nmost project comfortably, but it is updated regularly, and keeping that\nup-to-date is out of scope for this project. The City database is 27MB,\nand is probably not suitable for adding to source control. There are\nvarious solutions out on the web for pulling in the City database as\npart of a CD process.\n\n## Usage\n\nOnce the middleware is added, you will be able to access City and / or\nCountry level information on the request object.\n\nThe raw data is added to the request and response headers:\n\n```\n$ curl -I -H "x-forwarded-for: 142.250.180.3" localhost:8000\nHTTP/1.1 200 OK\nDate: Sun, 29 Aug 2021 15:47:22 GMT\nServer: WSGIServer/0.2 CPython/3.9.4\nContent-Type: text/html\nX-GeoIP2-City:\nX-GeoIP2-Continent-Code: NA\nX-GeoIP2-Continent-Name: North America\nX-GeoIP2-Country-Code: US\nX-GeoIP2-Country-Name: United States\nX-GeoIP2-Dma-Code:\nX-GeoIP2-Is-In-European-Union: False\nX-GeoIP2-Latitude: 37.751\nX-GeoIP2-Longitude: -97.822\nX-GeoIP2-Postal-Code:\nX-GeoIP2-Region:\nX-GeoIP2-Time-Zone: America/Chicago\nX-GeoIP2-Remote-Addr: 142.250.180.3\nContent-Length: 10697\n```\n\nThis is available from your code via the `request.headers` object (the\nkeys are case insensitive):\n\n```python\n>>> request.headers["x-geoip2-city"]\n\'Beverley Hills\'\n>>> request.headers["x-geoip2-postal-code"]\n\'90210\'\n>>> request.headers["x-geoip2-region"]\n\'California\'\n>>> request.headers["x-geoip2-country-code"]\n\'US\'\n>>> request.headers["x-geoip2-country-name"]\n\'United States\'\n>>> request.headers["x-geoip2-latitude"]\n\'34.0736\'\n>>> request.headers["x-geoip2-longitude"]\n\'118.4004\'\n```\n\nMissing / incomplete data will be and empty string "".\n\nIf the IP address cannot be found (e.g. \'127.0.0.1\'), then a default\n\'unknown\' country is used, with a code of \'XX\'.\n\n## Tests\n\nThe project tests are run through `pytest`.\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-geoip2-extras',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

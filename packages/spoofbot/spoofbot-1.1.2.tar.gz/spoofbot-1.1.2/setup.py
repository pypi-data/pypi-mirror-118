# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spoofbot', 'spoofbot.adapter', 'spoofbot.util']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'Pillow>=8.3.1,<9.0.0',
 'bs4>=0.0.1,<0.0.2',
 'loguru>=0.5.3,<0.6.0',
 'mitmproxy>=7.0.2,<8.0.0',
 'publicsuffix2>=2.20191221,<3.0',
 'requests>=2.26.0,<3.0.0',
 'toposort>=1.6,<2.0',
 'urllib3>=1.26.6,<2.0.0']

setup_kwargs = {
    'name': 'spoofbot',
    'version': '1.1.2',
    'description': 'A python requests wrapper that forms requests like real browsers and offers caching',
    'long_description': "# Spoofbot\nWeb bot for spoofing browser behaviour when using python requests.\nSupports Firefox and Chrome browser on most generic Windows, MacOS and Linux spoofing.\n\n## Example usage\n```py\nfrom spoofbot.browser import Chrome\nfrom spoofbot.adapter import FileCache\n\nbrowser = Chrome()\nbrowser.adapter = FileCache()\n\nbrowser.navigate('https://httpbin.org/')\nspec = browser.get('https://httpbin.org/spec.json').json()\nprint(spec['info']['description'])\n# A simple HTTP Request & Response Service.<br/> <br/> <b>Run locally: </b> <code>$ docker run -p 80:80 kennethreitz/httpbin</code>\nheaders = browser.navigate(\n    'https://httpbin.org/headers',\n    headers={'Accept': 'mime/type'}\n).json()\nprint(headers['headers']['Accept'])\n# mime/type\n```\n\n## Browsers\n\n`spoofbot` allows for useragents to be generate using information like the platform and browser version. Currently, only Firefox and Chrome are supported, but through inheritance one can add more browsers. The browser classes are derived from the `requests.Session` class and extend it by additional features.\n\n### Brotli encoding\n\nFirefox indicates that brotli encoding (`br`) is acceptable, but that might lead to issues when parsing the responses. It is possible to change that default header:\n\n```py\nfrom spoofbot.browser import Firefox\n\nff = Firefox()\nff._accept_encoding = ['deflate', 'gzip']  # brotli (br) is cumbersome\n``` \n\n### Request timeout for lower server load\n\nThe browsers have an automatic request delay built in which can be controlled with the `request_timeout` and `honor_timeout`. After requests have been made, `did_wait` and `waiting_period` provide further information.\n\n## Cache adapters\n\nFor more info refer to [the adapter module](src/spoofbot/adapter).\n\n### File Cache\n\nUsing `FileCache`, one can store responses (without metadata such as headers or cookies) in the filesystem. The cache indicates whether the last made request got a cache hit. If there is a request that should be cached that cannot be adequately stored with only hostname and path, one can specify and alternative url to use instead of the request's prior to the request using the adapter's `next_request_cache_url`\nproperty. This is also supported when deleting the last request from the cache. By using the `backup` method, the cache will backup the subsequent requests' original cached responses inside a new `Backup` object. If it is then determined that the backup should be restored, the `restore_all`/`restore` methods can be used. The backup process can be stopped explicitly with `stop_backup` or by using a `with` block on the\nbackup object.\n\n### Archive Cache\n\nUsing `ArchiveCache`, one is able to load `.har` and [MITMProxy](https://mitmproxy.org/) flow files to use as cache. This cache does not make actual HTTP requests to the net, but fails if no matching request could be found. It can be specified whether matching a request should be strict (must match all headers) or not. When matching for requests, one can toggle rules to use (such as matching headers, header order or\npost data) when looking for a match using the adapter's properties.\n\n## Example usage\n\nPlease take a look at the [tests](tests). Take note that the loggers provide helpful data when testing from matches in the cache on the `DEBUG` level.\n\n### Tips\n\nTurn off logging of other libraries:\n\n```py\nimport logging\n\nlogging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)\nlogging.getLogger('chardet.charsetprober').setLevel(logging.INFO)\nlogging.getLogger('chardet.universaldetector').setLevel(logging.INFO)\n```",
    'author': 'raember',
    'author_email': 'raember@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/spoofbot/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

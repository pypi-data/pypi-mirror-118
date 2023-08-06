# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangorestframework_kicksaw_auth']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.51,<2.0.0', 'djangorestframework>=3.12.4,<4.0.0']

setup_kwargs = {
    'name': 'djangorestframework-kicksaw-auth',
    'version': '1.0.0',
    'description': 'Provides DRF auth classes that are backed by various AWS resources',
    'long_description': '# Installation\n\n```\npip install djangorestframework-kicksaw-auth\n```\n\nOr with poetry\n\n```\npoetry add djangorestframework-kicksaw-auth\n```\n\n# Usage\n\n## BasicApiGatewayApiKeyAuth\n\n```python\nfrom djangorestframework_kicksaw_auth import BasicApiGatewayApiKeyAuth\n\n@authentication_classes([BasicApiGatewayApiKeyAuth])\ndef endpoint(request: HttpRequest):\n    # ...\n```\n\nThis authenticator reads basic auth and ensures the username and password\nmatch an API Gateway key\n\n```\ncurl -u username:password -v localhost:8000/api/your/endpoint\n```\n\nWhere `username` is the name of your API key and `password` is the API key\n',
    'author': 'Alex Drozd',
    'author_email': 'alex@kicksaw.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kicksaw-Consulting/djangorestframework-kicksaw-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

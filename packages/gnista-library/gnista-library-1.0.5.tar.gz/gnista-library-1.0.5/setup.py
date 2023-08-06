# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_point_client',
 'data_point_client.api',
 'data_point_client.api.data_export',
 'data_point_client.api.data_point',
 'data_point_client.api.files',
 'data_point_client.models',
 'gnista_library']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.1.0,<3.0.0',
 'attrs>=20.1.0,<22.0.0',
 'colorama>=0.4.4,<0.5.0',
 'httpx>=0.15.4,<0.19.0',
 'oauth2-client>=1.2.1,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'structlog>=21.1.0,<22.0.0']

setup_kwargs = {
    'name': 'gnista-library',
    'version': '1.0.5',
    'description': 'A client library for accessing gnista.io',
    'long_description': '# gnista-library\nA client library for accessing gnista.io\n\n## Tutorial\n### Create new Poetry Project\nNavigate to a folder where you want to create your project and type\n```shell\npoetry new my-gnista-client\ncd my-gnista-client\n```\n\n### Add reference to your Project\nNavigate to the newly created project and add the PyPI package\n```shell\npoetry add gnista-library\n``` \n\n### Your first DataPoint\nCreate a new file you want to use to receive data this demo.py\n\n```python\nfrom gnista_library import GnistaConnection, GnistaDataPoint\n\nconnection = GnistaConnection()\ndataPoint = GnistaDataPoint(connection=connection)\ndata = dataPoint.get_data_point(data_point_id="DATA_POINT_ID")\nprint(data)\n```\n\nYou need to replace the `DataPointId` with an ID from your gnista.io workspace.\n\nFor example the DataPointId of this DataPoint `https://aws.gnista.io/secured/dashboard/datapoint/4684d681-8728-4f59-aeb0-ac3f3c573303` is `4684d681-8728-4f59-aeb0-ac3f3c573303` making your line read `data = dataPoint.get_data_point(id="4684d681-8728-4f59-aeb0-ac3f3c573303")`\n\n### Run and Login\nRun your file in poetry\'s virtual environment\n```console\n$ poetry run python demo.py\n2021-09-02 14:51.58 [info     ] Authentication has been started. Please follow the link to authenticate with your user: [gnista_library.gnista_connetion] url=https://aws.gnista.io/authentication/connect/authorize?client_id=python&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fhome&response_type=code&scope=data-api%20openid%20profile%20offline_access&state=myState\n```\nIn order to login copy the `url` into your Browser and Login to gnista.io if you use aws.gnista.io you can use this [link](https://aws.gnista.io/authentication/connect/authorize?client_id=python&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fhome&response_type=code&scope=data-api%20openid%20profile%20offline_access&state=myState)\n\n\n## Links\n**Website**\n[![gnista.io](https://www.gnista.io/assets/images/gnista-logo-small.svg)](gnista.io)\n\n**PyPi**\n[![PyPi](https://pypi.org/static/images/logo-small.95de8436.svg)](https://pypi.org/project/gnista-library/)\n\n**GIT Repository**\n[![Gitlab](https://about.gitlab.com/images/icons/logos/slp-logo.svg)](https://gitlab.com/campfiresolutions/public/gnista.io-python-library)',
    'author': 'Markus Hoffmann',
    'author_email': 'markus@campfire-solutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

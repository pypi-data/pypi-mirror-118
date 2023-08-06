# gnista-library
A client library for accessing gnista.io

## Tutorial
### Create new Poetry Project
Navigate to a folder where you want to create your project and type
```shell
poetry new my-gnista-client
cd my-gnista-client
```

### Add reference to your Project
Navigate to the newly created project and add the PyPI package
```shell
poetry add gnista-library
``` 

### Your first DataPoint
Create a new file you want to use to receive data this demo.py

```python
from gnista_library import GnistaConnection, GnistaDataPoint

connection = GnistaConnection()
dataPoint = GnistaDataPoint(connection=connection)
data = dataPoint.get_data_point(data_point_id="DATA_POINT_ID")
print(data)
```

You need to replace the `DataPointId` with an ID from your gnista.io workspace.

For example the DataPointId of this DataPoint `https://aws.gnista.io/secured/dashboard/datapoint/4684d681-8728-4f59-aeb0-ac3f3c573303` is `4684d681-8728-4f59-aeb0-ac3f3c573303` making your line read `data = dataPoint.get_data_point(id="4684d681-8728-4f59-aeb0-ac3f3c573303")`

### Run and Login
Run your file in poetry's virtual environment
```console
$ poetry run python demo.py
2021-09-02 14:51.58 [info     ] Authentication has been started. Please follow the link to authenticate with your user: [gnista_library.gnista_connetion] url=https://aws.gnista.io/authentication/connect/authorize?client_id=python&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fhome&response_type=code&scope=data-api%20openid%20profile%20offline_access&state=myState
```
In order to login copy the `url` into your Browser and Login to gnista.io if you use aws.gnista.io you can use this [link](https://aws.gnista.io/authentication/connect/authorize?client_id=python&redirect_uri=http%3A%2F%2Flocalhost%3A4200%2Fhome&response_type=code&scope=data-api%20openid%20profile%20offline_access&state=myState)


## Links
**Website**
[![gnista.io](https://www.gnista.io/assets/images/gnista-logo-small.svg)](gnista.io)

**PyPi**
[![PyPi](https://pypi.org/static/images/logo-small.95de8436.svg)](https://pypi.org/project/gnista-library/)

**GIT Repository**
[![Gitlab](https://about.gitlab.com/images/icons/logos/slp-logo.svg)](https://gitlab.com/campfiresolutions/public/gnista.io-python-library)
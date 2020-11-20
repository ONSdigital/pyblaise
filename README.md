# pyblaise

This is a simple wrapper for the [Blaise](https://blaise.com/products/blaise-5) SOAP interface.

The SOAP interface is well defined and reasonably intuitive if you are familiar with Blaise concepts.

This package allows connections to a Blaise host from a python host environment (VM, Kubernetes pod, GCP Cloud-Function, AWS Lambda, etc.).

## Installation

```
pip install git+https://github.com/ONSdigital/pyblaise.git
```
*pypi package coming soon*

## Usage

```python
import pyblaise

username = os.getenv("BLAISE_USERNAME")
password = os.getenv("BLAISE_PASSWORD")

with Blaise("https", "my.blaise.com", 8031, username, password) as blaise:
  roles = blaise.get_roles()
  users = blaise.get_users()
  server_parks = blaise.get_server_park_definitions()
```

## Development

### Testing

`pytest` tests are defined in the module

for development:
+ create a virtualenv `virtualenv -p python3 venv; source venv/bin/activate`
+ install the package locally `pip install -e pyblaise`
+ run `pytest .`

The same tests are run by GithubActions on push.


### Versioning

Follow the [PEP440 specification](https://www.python.org/dev/peps/pep-0440).
i.e.:
```
v0.1.4      # actual version 0.1.4
v2.4.1rc1   # release candidate 1
v1.3.4dev3  # developer version 3
```

This is handled in the `setup.py` function.

Process:
+ develop in branch
```
git checkout -b my-branch
git add ...
git commit ...
```

+ push to github
```
git push origin my-branch
```

+ pull automated changes from github
```
git pull origin my-branch
```

+ tag the release
```
git tag -a <my-tag-name> -m "<my tag message>"
```

+ push the tag
```
git push origin --tags
```



## Blaise SOAP Interface Overview

Blaise has five resources, each with a [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)
interface accessed via a `POST` request with a header `SOAPAction` set to the following values:
1) Roles
    + create: `http://www.blaise.com/security/2016/06/ISecurityManagementService/CreateRole`
    + read: `http://www.blaise.com/security/2016/06/ISecurityManagementService/GetRoles`
    + update: `http://www.blaise.com/security/2016/06/ISecurityManagementService/UpdateRole`
    + delete: `http://www.blaise.com/security/2016/06/ISecurityManagementService/DeleteRole`
1) Skills
    + tbd
1) Users
    + create: `http://www.blaise.com/security/2018/12/ISecurityManagementService/CreateUser201812`
    + read: `http://www.blaise.com/security/2018/12/ISecurityManagementService/GetAllUsers201812`
1) Instruments
    + create: ?
    + read: `http://www.blaise.com/deploy/2013/03/IDeployService/GetListOfInstruments`
    + update: ?
    + delete: `http://www.blaise.com/deploy/2013/03/IDeployService/RemoveInstrument`
1) Server Parks
    + tbd

There are further operations to support:
+ Authentication
    + `http://www.blaise.com/security/2016/06/ISecurityTokenService/RequestToken`
    + `http://www.blaise.com/security/2016/06/ISecurityTokenService/RefreshToken`
+ Version
    + `http://www.blaise.com/deploy/2014/09/IDeployService/GetVersionResponse`
    + `http://www.blaise.com/deploy/2019/06/IDeployService/GetServerVersion`
+ File upload
    + this is the only part of the interface which is not a SOAP action and is a standard
      `POST` request with the file data included in the body.
    + `POST /Blaise/Administer/Services/REST/<server-park>/<survey-name>/<survey-uuid>/uploadpackage`
    + The `REST` element in the URL suggests a REST API exists, which is exciting.

It is unfortunate that the interface is exposed via the poorly supported SOAP protocol, which
makes working with the interface more difficult than the good, consistent design deserves.

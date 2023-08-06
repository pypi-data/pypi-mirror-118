**PyJazzClient** is a simple python package for communicating with IBM Jazz.

```python
>>> from pyjazzclient.jazzclient import JazzClient
>>> from pyjazzclient.testcase import TestCase
>>> server_url = "https://jazz.net/jazz"
>>> default_projects = {"qm": "__JVJ8e2eEeuHyM9xpDtK0B", "rm": "__JVJ8e2eEeuHyM9xpDtK0C"}
>>> jazz = JazzClient(server_url, "username", "password", default_projects)
>>> testcase = jazz.testcase(web_id=16197)
>>> print(testcase.title)
'The handheld device shall allow the meter reader to enter information about meters relocated on a particular route.'
```

Pyjazzclient allows you to create, edit, update, delete, lock, and unlock various artifacts within IBM Jazz with little need to understand the RqmAPI or OSLCS.

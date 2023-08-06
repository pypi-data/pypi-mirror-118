import requests
import xml.etree.ElementTree as ET

from .testcase import TestCase
from .exceptions import JazzClientRequestError


class JazzClient():
    RQM_REQUEST_HEADER = {
        "OSLC-Core-Version": "2.0",
        "Accept": "application/xml",
        "Content-Type": "application/rdf+xml"
    }

    TESTCASE_URL = ("/service/com.ibm.rqm.integration.service.IIntegrationService/"
                    "resources/{project}/testcase")

    WEB_ID_OR_SLUG_REQUIRED = "web_id or slug must be provided"
    TESTCASE_MUST_BE_VALID = "testcase must be a valid TestCase"

    def __init__(self, server_url: str, username: str, password: str, default_projects: dict = None):
        """Constructor"""
        self.__server_url = server_url
        self.__session = requests.session()
        self.__username = username
        self.__password = password
        self.__default_projects = default_projects or {"qm": "", "rm": ""}

    def __request(self, method: str = "GET", url: str = None, data: str = None,
                  headers: dict = None, auth: tuple = ("", "")) -> requests.Response:
        try:

            response = self.__session.request(method=method, url=url, data=data, headers=JazzClient.RQM_REQUEST_HEADER,
                                              allow_redirects=True, auth=auth)
            # check if we got a exception worthly response
            # response.raise_for_status()
            if (response.status_code not in [200, 201]):
                raise JazzClientRequestError(None, response)
        except Exception as err:
            raise err

        return response

    def testcase(self, web_id: str = None, slug: str = None, revision: int = None, calm_links: bool = None,
                 oslc_links: bool = None, meta_data: bool = None, abbreviate: bool = None,
                 sort: str = None, fields: str = None, project: dict = None) -> TestCase:
        """
        """
        # ensure we have either a web_id or a slug
        if (web_id is None and slug is None):
            raise ValueError(JazzClient.WEB_ID_OR_SLUG_REQUIRED)

        # use the provided project, if one is not provided use default_projects qm
        project = project or self.__default_projects["qm"]

        # create url string
        url = self.__server_url + \
            JazzClient.TESTCASE_URL.format(project=project)

        # append web_id or slug to url
        if (web_id is not None):
            url += f"/urn:com.ibm.rqm:testcase:{web_id}"
        if (slug is not None):
            url += f"/{slug}"

        # attempt to make GET request for testcase
        try:
            response = self.__request(method="GET", url=url,
                                      headers=JazzClient.RQM_REQUEST_HEADER, auth=(self.__username, self.__password))
        except Exception as err:
            raise err

        # convert response payload to xml element
        xml = ET.fromstring(response.text)

        # create a TestCase object containing the results of our request
        testcase = TestCase(xml)

        # return testcase to caller
        return testcase

    def update_testcase(self, testcase: TestCase) -> None:
        if (isinstance(testcase, TestCase) == False):
            raise ValueError(JazzClient.TESTCASE_MUST_BE_VALID)

        try:
            response = self.__session.put(url=testcase.identifier, data=testcase.to_string(),
                                          headers=JazzClient.RQM_REQUEST_HEADER, allow_redirects=True,
                                          auth=(self.__username, self.__password))
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

    def create_testcase(self, testcase: TestCase, project: str = None) -> str:
        # use the provided project, if one is not provided use default_projects qm
        project = project or self.__default_projects["qm"]

        # create url string
        url = self.__server_url + \
            JazzClient.TESTCASE_URL.format(project=project)

        try:
            response = self.__request(method="POST", url=url, data=testcase.to_string(),
                                      headers=JazzClient.RQM_REQUEST_HEADER, auth=(self.__username, self.__password))
        except requests.exceptions.HTTPError:
            raise

        return response.headers["Content-Location"]

    def delete_testcase(self, web_id: int = None, slug: str = None, project: str = None) -> None:
        # ensure we have either a web_id or a slug
        if (web_id is None and slug is None):
            raise ValueError(JazzClient.WEB_ID_OR_SLUG_REQUIRED)

        # use the provided project, if one is not provided use default_projects qm
        project = project or self.__default_projects["qm"]

        # create url string
        url = self.__server_url + \
            JazzClient.TESTCASE_URL.format(project=project)

        # append web_id or slug to url
        if (web_id is not None):
            url += f"/urn:com.ibm.rqm:testcase:{web_id}"
        if (slug is not None):
            url += f"/{slug}"

        # attempt to make GET request for testcase
        try:
            response = self.__request(method="DELETE", url=url,
                                      headers=JazzClient.RQM_REQUEST_HEADER, auth=(self.__username, self.__password))
        except requests.exceptions.HTTPError:
            raise

    def lock_testcase(self, web_id: int = None, slug: str = None, project: str = None) -> None:
        # ensure we have either a web_id or a slug
        if (web_id is None and slug is None):
            raise ValueError(JazzClient.WEB_ID_OR_SLUG_REQUIRED)

        # use the provided project, if one is not provided use default_projects qm
        project = project or self.__default_projects["qm"]

        # create url string
        url = self.__server_url + \
            JazzClient.TESTCASE_URL.format(project=project)

        # append web_id or slug to url
        if (web_id is not None):
            url += f"/urn:com.ibm.rqm:testcase:{web_id}"
        if (slug is not None):
            url += f"/{slug}"

        # attempt to make GET request for testcase
        try:
            response = self.__request(method="LOCK", url=url,
                                      headers=JazzClient.RQM_REQUEST_HEADER, auth=(self.__username, self.__password))
        except requests.exceptions.HTTPError:
            raise

    def unlock_testcase(self, web_id: int = None, slug: str = None, project: str = None) -> None:
        # ensure we have either a web_id or a slug
        if (web_id is None and slug is None):
            raise ValueError(JazzClient.WEB_ID_OR_SLUG_REQUIRED)

        # use the provided project, if one is not provided use default_projects qm
        project = project or self.__default_projects["qm"]

        # create url string
        url = self.__server_url + \
            JazzClient.TESTCASE_URL.format(project=project)

        # append web_id or slug to url
        if (web_id is not None):
            url += f"/urn:com.ibm.rqm:testcase:{web_id}"
        if (slug is not None):
            url += f"/{slug}"

        # attempt to make GET request for testcase
        try:
            _ = self.__request(method="UNLOCK", url=url,
                                      headers=JazzClient.RQM_REQUEST_HEADER, auth=(self.__username, self.__password))
        except requests.exceptions.HTTPError:
            raise

    def search_testcase(self, fields: str = None, modified_since: str = None, revision: bool = None,
                        calm_links: bool = None, oslc_links: bool = None, meta_data: bool = None,
                        abbreviate: bool = None, sort: bool = None, project: str = None) -> None:
        # use the provided project, if one is not provided use default_projects qm
        project = project or self.__default_projects["qm"]

        # create url string
        url = self.__server_url + \
            JazzClient.TESTCASE_URL.format(project=project)

        # attempt to make GET request for testcase
        try:
            _ = self.__request(method="GET", url=url,
                                      headers=JazzClient.RQM_REQUEST_HEADER, auth=(self.__username, self.__password))
        except requests.exceptions.HTTPError:
            raise

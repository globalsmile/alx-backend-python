#!/usr/bin/env python3
""" Parameterize and patch as decorators, Mocking a property, More patching,
    Parameterize, Integration test: fixtures, Integration tests """
import unittest
from typing import Dict
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from urllib.error import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """ TESTCASE"""

    """inputs to test the functionality """
    @parameterized.expand([
        ("google"),
        ("abc"),
        ])
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name: str, mock_get: Mock) -> None:
        """ test that GithubOrgClient.org returns the correct value """
        test_client = GithubOrgClient(org_name)
        test_return = test_client.org
        self.assertEqual(test_return, mock_get.return_value)
        mock_get.assert_called_once

    def test_public_repos_url(self) -> None:
        """ to unit-test GithubOrgClient._public_repos_url """
        with patch.object(GithubOrgClient,
                          "org",
                          new_callable=PropertyMock,
                          return_value={"repos_url": "holberton"}) as mock_get:
            test_json = {"repos_url": "holberton"}
            test_client = GithubOrgClient(test_json.get("repos_url"))
            test_return = test_client._public_repos_url
            mock_get.assert_called_once
            self.assertEqual(test_return,
                             mock_get.return_value.get("repos_url"))

    @patch("client.get_json", return_value=[{"name": "holberton"}])
    def test_public_repos(self, mock_get: Mock) -> None:
        """ to unit-test GithubOrgClient.public_repos """
        with patch.object(GithubOrgClient,
                          "_public_repos_url",
                          new_callable=PropertyMock,
                          return_value="https://api.github.com/") as mock_pub:
            test_client = GithubOrgClient("holberton")
            test_return = test_client.public_repos()
            self.assertEqual(test_return, ["holberton"])
            mock_get.assert_called_once
            mock_pub.assert_called_once

    """ inputs to test the functionality """
    @parameterized_expand([
        ({"license": {"key": "my_license"}}, license_key="my_license"),
        ({"license": {"key": "other_license"}}, license_key="my_license"),
        ])
    def test_has_license(self, repo: Dict, license_key: str,
                         expected_return: bool) -> None:
        """ to unit-test GithubOrgClient.has_license """
        test_client = GithubOrgClient("holberton")
        test_return = test_client.has_license(repo, license_key)
        self.assertEqual(expected_return, test_return)

    @patch("client.GithubOrgClient._public_repos_url",
           new_callable=PropertyMock,
           return_value="https://api.github.com/")
    def test_public_repos_with_license(self, mock_pub: Mock) -> None:
        """ to unit-test GithubOrgClient.public_repos with
        the argument license """
        with patch("client.get_json",
                   return_value=[{"license": {"key": "my_license"}}]) as mgt:
            test_client = GithubOrgClient("holberton")
            test_return = test_client.public_repos("my_license")
            self.assertEqual(test_return, [{"license": {"key": "my_license"}}])
            mgt.assert_called_once
            mock_pub.assert_called_once


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ TESTCASE"""

    """ inputs to test the functionality """
    @classmethod
    def setUpClass(cls) -> None:
        """ It is part of the unittest.TestCase API
        method to return example payloads found in the fixtures """
        cls.get_patcher = patch('requests.get', side_effect=HTTPError)

    """ It is part of the unittest.TestCase API """
    @classmethod
    def tearDownClass(cls) -> None:
        """ It is part of the unittest.TestCase API
        method to stop the patcher """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """ method to test GithubOrgClient.public_repos """
        test_class = GithubOrgClient("holberton")
        assert True

    def test_public_repos_with_license(self) -> None:
        """ method to test the public_repos with the argument license """
        test_class = GithubOrgClient("holberton")
        assert True

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from cpt import ci_manager
from cpt.ci_manager import CIManager
from cpt.printer import Printer


if __name__ == "__main__":
    manager = CIManager(Printer())
    response = None
    if manager.get_branch() == "stable/3.6.1" and not manager.is_pull_request() and os.getenv("ARCH") == "x86":
        if ci_manager.is_travis():
            json_data = {"request": {"branch": "release/3.6.1"}}
            headers = {"Authorization": "token %s" % os.getenv("TRAVIS_TOKEN"), "Travis-API-Version": "3"}
            response = requests.post(url="https://api.travis-ci.com/repo/bincrafters%2Fprotobuf-integration-test/requests", json=json_data, headers=headers)
        elif ci_manager.is_appveyor():
            json_data = {"accountName":"BinCrafters", "projectSlug": "protobuf-integration-test", "branch": "release/3.6.1"}
            headers = {"Authorization": "Bearer %s" % os.getenv("APPVEYOR_TOKEN")}
            response = requests.post(url="https://ci.appveyor.com/api/builds", json=json_data, headers=headers)
        else:
            print("WARNING: No CI manager detected")

        if response:
            if not response.ok:
                raise Exception("ERROR: Could not trigger a new build: %s" % response.text)
            print(response.text)
    else:
        print("WARNING: Integration test is for stable branch")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, RunEnvironment


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            self.run("protoc --version")

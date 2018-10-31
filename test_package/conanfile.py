#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def test(self):
        self.run("protoc --version", run_environment=True)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile, CMake


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run("protoc --version", run_environment=True)

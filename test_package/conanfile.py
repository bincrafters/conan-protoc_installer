#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile, CMake


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.definitions["protobuf_VERBOSE"] = True
        cmake.definitions["protobuf_MODULE_COMPATIBLE"] = True
        cmake.configure()
        cmake.build()

    def test(self):
        self.run("protoc --version", run_environment=True)

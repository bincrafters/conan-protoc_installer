#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class ProtobufConan(ConanFile):
    name = "protoc_installer"
    version = "3.6.1"
    url = "https://github.com/bincrafters/conan-protoc_installer"
    homepage = "https://github.com/protocolbuffers/protobuf"
    topics = ("protocol-buffers", "protocol-compiler", "serialization", "rpc")
    author = "Bincrafters <bincrafters@gmail.com>"
    description = ("protoc is a compiler for protocol buffers definitions files. It can can "
                   "generate C++, Java and Python source code for the classes defined in PROTO_FILE.")
    license = "BSD-3-Clause"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os_build", "arch_build"
    short_paths = True
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = "protobuf-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        if self.settings.arch_build == "x86":
            cmake.definitions["CMAKE_C_FLAGS"] = "-m32"
            cmake.definitions["CMAKE_CXX_FLAGS"] = "-m32"
        elif self.settings.arch_build == "x86_64":
            cmake.definitions["CMAKE_C_FLAGS"] = "-m64"
            cmake.definitions["CMAKE_CXX_FLAGS"] = "-m64"
        cmake.definitions["protobuf_BUILD_TESTS"] = False
        cmake.definitions["protobuf_WITH_ZLIB"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        # INFO: CMake install is not used intentionally - copy only executable file
        self.copy(pattern="protoc", src=os.path.join(self._build_subfolder, "bin"), dst="bin")
        self.copy(pattern="protoc.exe", src=os.path.join(self._build_subfolder, "bin"), dst="bin")
        self.copy(pattern="*.proto", src=os.path.join(self._source_subfolder, "src"), dst="include")
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        protoc = "protoc.exe" if self.settings.os_build == "Windows" else "protoc"
        self.env_info.PROTOC_BIN = os.path.normpath(os.path.join(self.package_folder, "bin", protoc))

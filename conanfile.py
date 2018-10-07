#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ProtobufConan(ConanFile):
    name = "protoc_installer"
    version = "3.5.2"
    url = "https://github.com/bincrafters/conan-protoc_installer"
    homepage = "https://github.com/protocolbuffers/protobuf"
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "protoc is a compiler for protocol buffers definitions files. It can can generate C++, Java " \
                  "and Python source code for the classes defined in PROTO_FILE."
    license = "BSD"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    settings = "os_build", "arch_build"
    short_paths = True

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = "protobuf-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        if self.settings.arch_build == 'x86':
            cmake.definitions['CMAKE_C_FLAGS'] = '-m32'
            cmake.definitions['CMAKE_CXX_FLAGS'] = '-m32'
        elif self.settings.arch_build == 'x86_64':
            cmake.definitions['CMAKE_C_FLAGS'] = '-m64'
            cmake.definitions['CMAKE_CXX_FLAGS'] = '-m64'
        cmake.definitions["CMAKE_INSTALL_LIBDIR"] = "lib"
        cmake.definitions["protobuf_BUILD_TESTS"] = False
        cmake.definitions["protobuf_WITH_ZLIB"] = False
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        # CMake install is not used intentionally - copy only executable file
        self.copy(pattern='protoc*', src=os.path.join(self.build_subfolder, 'bin'), dst='bin')
        self.copy(pattern='*.proto', src=os.path.join(self.source_subfolder, 'src'), dst='include')
        self.copy("LICENSE", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, 'bin'))
        protoc = 'protoc.exe' if self.settings.os_build == 'Windows' else 'protoc'
        self.env_info.PROTOC_BIN = os.path.normpath(os.path.join(self.package_folder, 'bin', protoc))

cmake_minimum_required(VERSION 2.8.11)
project(test_package CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_VERBOSE_MAKEFILE ON)


string(FIND ${CONAN_SETTINGS_ARCH} "arm" CROSS_BUILDING)
if ((CROSS_BUILDING GREATER -1 OR WIN32)AND CMAKE_SIZEOF_VOID_P EQUAL 4)
    message(STATUS "Cross Building")
    set(CMAKE_SIZEOF_VOID_P 8)
    find_package(protoc CONFIG REQUIRED)
else()
    find_package(protoc CONFIG REQUIRED)
endif()

message(STATUS "Using Protocol Buffers ${protobuf_VERSION}")

if(protobuf_MODULE_COMPATIBLE)
    PROTOBUF_GENERATE_CPP(PROTO_SRCS PROTO_HDRS addressbook.proto)
    message(STATUS "PROTO_SRCS: ${PROTO_SRCS}")
    message(STATUS "PROTO_HDRS: ${PROTO_HDRS}")
endif(protobuf_MODULE_COMPATIBLE)
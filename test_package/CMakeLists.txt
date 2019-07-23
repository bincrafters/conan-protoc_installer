cmake_minimum_required(VERSION 2.8.11)
project(test_package CXX)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

set(CMAKE_VERBOSE_MAKEFILE ON)

find_package(Protobuf REQUIRED)

message(STATUS "Using Protocol Buffers ${Protobuf_VERSION}")

protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS addressbook.proto)
message(STATUS "PROTO_SRCS: ${PROTO_SRCS}")
message(STATUS "PROTO_HDRS: ${PROTO_HDRS}")

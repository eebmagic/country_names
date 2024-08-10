cmake_minimum_required(VERSION 3.4)
project(example)

add_subdirectory(pybind11)
pybind11_add_module(example example.cpp)

#!/bin/bash

conan remove soralog/0.2.3 -c
conan create . --version=0.2.3 --name=soralog --build=missing --update
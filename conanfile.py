import os
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy
from conan.tools.scm import Git


class PackageConan(ConanFile):
    name = "soralog"
    version = "0.2.3"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/simbahebinbo/conan-soralog.git"
    requires = (
        "gtest/1.13.0",
        "yaml-cpp/0.6.3",
        "fmt/10.1.1"
    )

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        git = Git(self)
        if not os.path.exists(os.path.join(self.source_folder, ".git")):
            git.clone("https://github.com/simbahebinbo/soralog.git", target=".")
        else:
            self.run("git pull")

        branch_name = "develop"
        git.checkout(branch_name)

    def build(self):
        build_script_folder = os.path.join(self.source_folder)
        self.run(f"cmake {build_script_folder}")
        self.run("cmake --build .")

    def package(self):
        cmake = CMake(self)
        cmake.install()

        # 头文件路径
        include_folder = os.path.join(self.source_folder, "include")
        # 库文件路径
        lib_folder = os.path.join(self.build_folder, "src")

        # 使用 conan.tools.files.copy 替代 self.copy
        copy(self, "*.hpp", dst=os.path.join(self.package_folder, "include"), src=include_folder)
        copy(self, "*.a", dst=os.path.join(self.package_folder, "lib"), src=lib_folder)

    def package_info(self):
        # 使用别名来指定库
        self.cpp_info.libs = [
            "soralog",  # 对应 add_library(soralog ALIAS soralog)
            "configurator_yaml",  # 对应 add_library(yaml ALIAS configurator_yaml)
            "fallback_configurator",  # 对应 add_library(fallback ALIAS fallback_configurator)
            "logger",
            "sink_to_console",
            "sink_to_syslog",
            "sink_to_file",
            "group",
            "multisink",
            "sink_to_nowhere"
        ]

        # 也可以使用别名来添加库到 cpp_info.libs
        self.cpp_info.names["cmake_find_package"] = "soralog"
        self.cpp_info.names["cmake_find_package_multi"] = "soralog"

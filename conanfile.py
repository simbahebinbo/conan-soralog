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
        self.cpp_info.libs = [
            "soralog",
            "configurator_yaml",  # 这个对应 `yaml` 目标
            "fallback_configurator",
            "logger",
            "sink_to_console",
            "sink_to_syslog",
            "sink_to_file",
            "group",
            "multisink",
            "sink_to_nowhere"
        ]

        # 添加 `yaml` 别名
        self.cpp_info.components["yaml"].libs = ["configurator_yaml"]
        self.cpp_info.components["yaml"].requires = ["yaml-cpp::yaml-cpp"]
        # self.cpp_info.components["yaml"].names["cmake_find_package"] = "yaml"
        # self.cpp_info.components["yaml"].names["cmake_find_package_multi"] = "yaml"

        self.cpp_info.components["fmt"].libs = []
        self.cpp_info.components["fmt"].requires = ["fmt::fmt"]

        # 添加 `fallback` 别名
        self.cpp_info.components["fallback"].libs = ["fallback_configurator"]
        # self.cpp_info.components["fallback"].names["cmake_find_package"] = "fallback"
        # self.cpp_info.components["fallback"].names["cmake_find_package_multi"] = "fallback"

        # 添加 `soralog` 别名
        self.cpp_info.names["cmake_find_package"] = "soralog"
        self.cpp_info.names["cmake_find_package_multi"] = "soralog"

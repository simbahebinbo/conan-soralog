CMAKE_MINIMUM_REQUIRED(VERSION 3.12)

PROJECT(example_simple LANGUAGES CXX VERSION 1.0.0)

set(CMAKE_POSITION_INDEPENDENT_CODE TRUE)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(soralog CONFIG REQUIRED)
#find_package(yaml-cpp REQUIRED)
#find_package(fmt REQUIRED)
#find_package(Threads REQUIRED)

add_executable(${PROJECT_NAME}
        main.cpp
        #        logging_object.cpp
)

target_include_directories(${PROJECT_NAME}
        PRIVATE ${CMAKE_SOURCE_DIR}/include
)
target_link_libraries(${PROJECT_NAME}
        soralog::soralog
        #        soralog::yaml
        #        soralog::fallback
        #        yaml-cpp::yaml-cpp
        #        fmt::fmt
        #        Threads::Threads
)

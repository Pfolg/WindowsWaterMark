cmake_minimum_required(VERSION 3.16)

project(ActivateWindows VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# 确保包含项目根目录
include_directories(${CMAKE_SOURCE_DIR})
find_package(Qt6 REQUIRED COMPONENTS Widgets Core Network)
qt_standard_project_setup()

qt_add_executable(ActivateWindows
        main.cpp
        widget.cpp
        widget.h
        json.hpp
        doconfig.cpp
        doconfig.h
)
target_link_libraries(ActivateWindows PRIVATE Qt6::Widgets Qt6::Core Qt6::Network)

set_target_properties(ActivateWindows PROPERTIES
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

include(GNUInstallDirs)
install(TARGETS ActivateWindows
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

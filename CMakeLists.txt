cmake_minimum_required(VERSION 3.12)
project(dnf-plugin-kpatchfilter NONE)
include(GNUInstallDirs)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

add_subdirectory(plugin)
install(DIRECTORY "etc/" DESTINATION "${CMAKE_INSTALL_FULL_SYSCONFDIR}")


cmake_minimum_required(VERSION 3.10)
project(radioDriver)

set(HEADER_FILES
	components.hpp
	#radioDriver.hpp
	)

set(SOURCE_FILES
	main.cpp
	components.cpp
	#radioDriver.cpp
	)

add_executable(radioDriver
	${SOURCE_FILES}
	${HEADER_FILES})



set_property(TARGET radioDriver PROPERTY CXX_STANDARD 17)


if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
	target_compile_options(radioDriver PRIVATE -Wall -Wextra -pedantic -l sqlite3)
	find_package(SQLite3)
	include_directories(${SQLite3_INCLUDE_DIRS})
	target_link_libraries(radioDriver ${SQLite3_LIBRARIES})
endif()

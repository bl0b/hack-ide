PROJECT(hackide NONE)

cmake_minimum_required(VERSION 2.8)


SET(PY_FILES py/base.py py/hackide.py py/layout.py py/main.py py/rc_file.py py/startup.py py/task.py py/tmux.py)
SET(TT tasks)
SET(CT contexts)

SET(CMAKE_VERSION_MAJOR 0)
SET(CMAKE_VERSION_MINOR 1)
SET(CMAKE_VERSION_PATCH beta)

SET(HACKIDE_NAME hackide)

INSTALL(FILES ${PY_FILES} DESTINATION share/hack-ide/py)
INSTALL(FILES hackide.1 DESTINATION share/man/man1)
INSTALL(FILES COPYING README.md default.tmuxrc DESTINATION share/hack-ide)
INSTALL(DIRECTORY ${TT} DESTINATION share/hack-ide)
INSTALL(DIRECTORY ${CT} DESTINATION share/hack-ide)
SET(FRONTEND ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_PREFIX}/hackide)
CONFIGURE_FILE(hackide.in ${FRONTEND} @ONLY)
INSTALL(PROGRAMS ${FRONTEND} DESTINATION bin)

INCLUDE(CMakeCPack.cmake)

@echo off
setlocal
set "PYTHONPATH=%~dp0src"
py -3 -m minhtri %*

echo off
set TEMPLATE=%1
SET scriptpath=%~dp0
%scriptpath%venv\Scripts\python.exe %scriptpath%%TEMPLATE%.py
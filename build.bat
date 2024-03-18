@echo off

:: check if PyInstaller is installed
pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 2 (
    echo PyInstaller is not installed.
    echo You can install it by running "pip install pyinstaller"
    exit /b 1
)

:: check if the version is specified in the arguments
if "%~1" == "" (
    echo Specify the version as the first argument.
    echo > build X.X.X
    exit /b 1
)

set "version=%1"
set "filename=TextureRestorer-%version%.zip"

mkdir tmp
cd tmp

set "iconpath=..\src\assets\arrow.ico"
set "entrypoint=..\src\TextureRestorer.py"

:: generate executable
pyinstaller --onefile --windowed --icon=%iconpath% %entrypoint%

cd ..

set "exe=.\tmp\dist\TextureRestorer.exe"
set "assets=.\src\assets"
set "data=.\src\data"

:: zip files
powershell -Command "Compress-Archive -LiteralPath %exe% -DestinationPath %filename%"
powershell -Command "Compress-Archive -Path %assets%, %data% -Update -DestinationPath %filename%"

:: clean
rmdir /s /q tmp
::rmdir /s /q build
::del *.spec

echo.
echo Generated %filename%

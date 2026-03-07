@echo off
chcp 65001 >nul
echo 开始打包...

REM 清理旧的打包文件
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM 执行打包
pyinstaller class-toolkit.spec

REM 复制外部配置文件
mkdir "dist\config" 2>nul
mkdir "dist\files" 2>nul
mkdir "dist\tools" 2>nul
mkdir "dist\tools\log" 2>nul

copy "config\config.json" "dist\config\"
copy "tools.json" "dist\"
copy "files\names.txt" "dist\files\"
copy "tools\*.py" "dist\tools\"

echo 打包完成！
echo 输出目录: dist\
pause
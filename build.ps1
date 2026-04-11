Write-Host "开始打包..." -ForegroundColor Green

# 清理
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue build, dist

# 打包
pyinstaller class-toolkit.spec

# 创建目录并复制文件
@('dist/config', 'dist/files', 'dist/tools', 'dist/tools/log') | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_ | Out-Null
}

Copy-Item 'config/config.json' 'dist/config/'
Copy-Item 'tools.json' 'dist/'
Copy-Item 'files/names.txt' 'dist/files/'
Copy-Item 'tools/*.py' 'dist/tools/'

Write-Host "打包完成！输出目录: dist\" -ForegroundColor Green
pause
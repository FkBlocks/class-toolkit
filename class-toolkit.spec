# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        ('pics', 'pics'),               # 图片目录
        # 不打包以下文件，保持外部可修改：
        # - config/ (配置文件)
        # - files/ (名单文件)
        # - tools/ (工具脚本)
        # - tools.json (工具配置)
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'tkinter',
        'pycaw.pycaw',
        'comtypes',
        'psutil',
        'winshell',
        'tools.logger',
        'tools.consts',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='class-toolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='pics/ball.png',  # 应用图标
)
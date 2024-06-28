# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['click_green_objects.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('E:\\Blum2\\ice_cube.png', '.'),
        ('E:\\Blum2\\play_button.png', '.'),
        ('E:\\Blum2\\close_button.png', '.'),
        ('E:\\Blum2\\green_object.png', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='click_green_objects.py',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='click_green_objects.py'
)

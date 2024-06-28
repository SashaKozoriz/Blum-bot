# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['click_green_objects.py'],
    pathex=[],
    binaries=[],
    datas=[('E:\\Blum2\\ice_cube.png', '.'), ('E:\\Blum2\\play_button.png', '.'), ('E:\\Blum2\\close_button.png', '.'), ('E:\\Blum2\\green_object.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='click_green_objects',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

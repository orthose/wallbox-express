# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/wallbox_express.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("src/gui/assets/*", "gui/assets/"),
        ("src/gui/fonts/Ubuntu/*.ttf", "gui/fonts/Ubuntu/"),
    ],
    hiddenimports=[
        "PIL._tkinter_finder",
    ],
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
    [],
    exclude_binaries=True,
    name='wallbox_express',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='wallbox_express',
)

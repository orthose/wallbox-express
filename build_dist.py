import shutil
import PyInstaller.__main__


PyInstaller.__main__.run([
    "--noconfirm",
    "wallbox_express.spec",
])
shutil.copyfile("./config.toml", "./dist/wallbox_express/config.toml")
shutil.make_archive("./dist/wallbox_express", 'zip', "./dist/wallbox_express")

from distutils.core import setup

setup(
    name = "ScreenAPI",
    packages = ["ScreenAPI"],
    version = "0.1.0",
    description = "A python library used for making custom screens easier.",
    author = "IKings",
    author_email = "adking08@hotmail.com",
    url = "https://github.com/KingsMMA/ScreenAPI",
    download_url = "https://github.com/KingsMMA/ScreenAPI/archive/refs/tags/beta_v1_0.tar.gz",
    keywords = ["screen", "api", "screenapi", "utility", "tkinter"],
    install_requires = [
        "tkinter",
        "math"
    ],
    classifiers =[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)

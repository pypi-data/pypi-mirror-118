from setuptools import setup

with open("requirements.txt") as reqs_file:
    reqs = reqs_file.readlines()

setup(
    name ="zbxtool-cfomp",
    version ="0.4.2",
    packages = ['lib'],
    include_package_data=True,
    zip_safe=True,
    install_requires = reqs,

    entry_points={
        'console_scripts':[
            'zbxtool = lib.cli:main'
        ],
    },
)


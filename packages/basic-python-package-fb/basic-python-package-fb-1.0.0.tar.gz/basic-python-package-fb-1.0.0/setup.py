import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="basic-python-package-fb",
    version="1.0.0",
    packages=["package"],
    include_package_data=True,
    install_requires=["django-socio-grpc"],
    entry_points={
        "console_scripts": [
            "basic-python-package-fb=package.__main__:main"
        ]
    }
)

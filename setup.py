from setuptools import setup, find_packages
import pathlib
import pkg_resources
import setuptools

with pathlib.Path('requirements.txt').open() as requirements_txt:
    reqs = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="napalm_influx",
    version="0.1",
    packages=find_packages(),
    author="elisa",
    author_email="elisa",
    description="napalm_influx",
    include_package_data=True,
    install_requires=reqs,
    entry_points={
        'console_scripts': [
            'napalm_influx = napalm_influx.__main__:main'
        ]
    }
)

import uuid

from setuptools import setup, find_packages
from pip.req import parse_requirements

__author__ = 'elisa'

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs if ir.req]

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

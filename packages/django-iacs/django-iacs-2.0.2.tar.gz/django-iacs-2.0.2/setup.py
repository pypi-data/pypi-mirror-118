import subprocess
import sys

from setuptools import setup, find_namespace_packages

version = '2.0.2'
name = 'django-iacs'


def write_svn_info():
    code, stdout = subprocess.getstatusoutput("svn info")
    with open("iacs/SVN", "wb") as f:
        f.write(stdout.encode("utf-8"))


if sys.argv[1] == "sdist":
    write_svn_info()

setup(
    name=name,
    version=version,
    packages=find_namespace_packages(include=["iacs"]),
    install_requires=[
        "redis>=3.5.3",
        "deprecated>=1.2.12",
        "mysqlclient>=2.0.3",
        "django>=3.2.5,<4.0.0",
        "djangorestframework>=3.12.4,<4.0.0",
        "channels>=3.0.4,<4.0.0",
        "channels-redis>=3.0.3,<4.0.0"
        "daphne>=3.0.2,<4.0.0",
        "django-filter>=2.4.0,<3.0.0",
        "channels-redis>=3.3.0,<4.0.0",
        "drf-yasg>=1.20.0"
    ],
    include_package_data=True,
    url='https://broadtech.com.cn',
    license='GNU General Public License v3.0',
    author='Lee',
    author_email='canyun@live.com',
    description=f'iacs',
)

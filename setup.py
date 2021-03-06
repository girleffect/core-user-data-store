from setuptools import setup, find_packages
from user_data_store import __version__

LONG_DESCRIPTION_FILES = ["README.rst", "AUTHORS.rst", "CHANGELOG.rst"]

setup(
    name="core-user-data-store",
    version=__version__,
    description="Girl Effect Core User Data Store",
    long_description="".join(open(filename, "r").read() for filename in LONG_DESCRIPTION_FILES),
    author="Praekelt Consulting",
    author_email="dev@praekelt.com",
    license="BSD",
    url="http://github.com/girleffect/core-user-data-store",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)

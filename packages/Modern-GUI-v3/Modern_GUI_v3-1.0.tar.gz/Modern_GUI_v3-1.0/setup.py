from setuptools import setup, find_packages
setup_args=dict(
    name="Modern_GUI_v3",
    version='1.0',
    author="Sancho Godinho",
    description="A Module to Build Modern GUI Source Files Without Internet Connection!",
    long_description="Please See More Info on: https://github.com/sancho1952007/Modern-GUI-v3.0",
    packages=["Modern_GUI_v3"],
    keywords=['build'],
    url="https://github.com/sancho1952007/Modern-GUI-v3.0",
    license_files = ('LICENSE.txt'),
    project_urls={
        "Bug Tracker": "https://github.com/sancho1952007/Modern-GUI-v3.0/issues"
    }
)
install_requires=[]

setup(**setup_args, install_requires=install_requires)
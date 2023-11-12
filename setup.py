from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

console_scripts = '''
[console_scripts]
mcadmin=mcadmin:cli
'''

setup(
    name = 'mcadmin',
    version = '0.3.4',
    author = 'J. Alex Long',
    license = 'GPLv3',
    description = 'A minecraft server administration tool.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/JAlexLong/mcadmin',
    py_modules = ['mcadmin'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points=console_scripts,
)
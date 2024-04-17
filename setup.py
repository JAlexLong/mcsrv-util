from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

console_scripts = '''
[console_scripts]
minecraftctl=minecraftctl:cli
'''

setup(
    name = 'minecraftctl',
    version = '0.4.3',
    author = 'J. Alex Long',
    license = 'GPLv3',
    description = 'A minecraft server administration tool.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/JAlexLong/minecraftctl',
    py_modules = ['minecraftctl'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    entry_points=console_scripts,
)
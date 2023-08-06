from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'AminoLab',
    version = '1.0',
    url = 'https://github.com/LilZevi/AminoLab',
    download_url = 'https://github.com/LilZevi/AminoLab/archive/refs/heads/main.zip',
    license = 'MIT',
    author = 'LilZevi',
    author_email = 'elegantlyakaintelligent@gmail.com',
    description = 'A library for aminoapps.com to create Amino bots.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = [
        'aminoapps',
        'amino-py',
        'amino',
        'amino-bot',
        'narvii',
        'api',
        'python',
        'python3',
        'python3.x',
        'lilzevi',
        'botamino'
    ],
    install_requires = [
        'setuptools',
        'requests',
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
from setuptools import setup, find_packages

with open('README.md') as readme:
    long_description = readme.read().strip()

setup(
    name="linkparser",
    version="1.0",
    description="A Simple Python Package to Extract All Links from a Target Domain or URL.",
    author="Gaurav Raj",
    url="https://github.com/thehackersbrain/linkparser",
    author_email="techw803@gmail.com",
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['linkparser', 'thehackersbrain',
              'hacking', 'web scraping', 'python', 'python3'],
    packages=find_packages(),
    install_requires=['requests', 'rich', 'pyfiglet', 'bs4'],
    entry_points={
        'console_scripts': ['linkparser = linkparser.linkparser:main']
    },

    zip_safe=False,
)

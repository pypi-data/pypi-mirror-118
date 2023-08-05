# LinkParser

> Written in Python3 by Gaurav Raj [TheHackersbrain](https://google.com/search?q=thehackersbrain)

## Description

**LinkParser** is a tool written in Python 3 for scrapping or grabbing all the links from a targeted website, domain or URL.

**NOTE:** This Project was written during Practice session.

## Version

#### LinkParser 1.0

## Requirements

-   [Requests](#)
-   [Rich](#)
-   [BeautifulSoup4](#)
-   [PyFiglet](#)

## Installation and Uses

### Installation

-   Install this tool from **PyPi** using **PIP**
    ```shell
    pip3 install linkparser
    ```

or

-   Build it from source

    -   clone this repo

    ```shell
    git clone https://github.com/thehackersbrain/linkparser.git
    ```

    -   change the directory

    ```shell
    cd linkparser
    ```

    -   Now Run the `setup.py` script

    ```shell
    python setup.py install
    ```

### Uses

-   For Grabbing All links from a targeted URL.

    ```shell
    linkparser -u 'https://blog.gauravraj.tech/'
    ```

-   For Grabbing Links from a specific path

    ```shell
    linkparser -u 'https://blog.gauravraj.tech' -p '/about'
    ```

-   For Writting all of the finding in a file
    ```shell
    linkparser -u 'https://blog.gauravraj.tech' -p '/about' -o output.log
    ```

## About Author

-   [Portfolio](https://gauravraj.tech/)
-   [Blog](https://blog.gauravraj.tech/)
-   [Github](https://github.com/thehackersbrain/)
-   [Twitter](https://twitter.com/thehackersbrain)
-   [LinkedIn](https://linkedin.com/thehackersbrain)
-   [Instagram](https://instagram.com/thehackersbrain)
-   [More Projects](https://github.com/thehackersbrain?tab=repositories)

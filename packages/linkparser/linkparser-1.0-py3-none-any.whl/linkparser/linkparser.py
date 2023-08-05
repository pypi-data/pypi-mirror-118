import argparse
import requests
from rich import print
import pyfiglet
from bs4 import BeautifulSoup
import re


# required variables
initial_links = []
links = []


def banner():
    """
    ASCII Art Banner
    """
    banner = pyfiglet.figlet_format('Link Grabber', font='slant')
    print("[bold green]{}[/bold green]".format(banner))


def validate_urls(baseUrl):
    """
    Function for validating Entered Urls.
    """
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, baseUrl)
    initUrl = [i[0] for i in url]
    baseUrl = baseUrl.join(initUrl)
    if not baseUrl.endswith('/'):
        return baseUrl + '/'
    return baseUrl


def find_urls(baseUrl, urls):
    """
    Finding all links from the Website and appending them to list named initial_links
    """
    for i in urls:
        req = requests.get(baseUrl+i)
        soup = BeautifulSoup(req.text, "html.parser")
        link = soup.find_all('a', href=True)
        for i in link:
            if i['href'] == '#' or i['href'] == "":
                pass
            else:
                initial_links.append(i['href'])


def sort_list():
    """
    This function is for sorting for removing duplicates links from the links list. while originally
    found all links is stored in initial_links list.
    """
    for i in initial_links:
        if i not in links:
            links.append(i)


def outputData(output_file, links):
    with open(output_file, 'a') as data_file:
        for i in links:
            data_file.write(i+"\n")


def getlinks(baseUrl, urls, output, outfile):
    """
    Running All the Function in order
    """
    try:
        banner()
        print(
            "[[bold yellow]*[/bold yellow]] Target: [green]{}[/green]\n".format(baseUrl))
        print("[[bold yellow]*[/bold yellow]] Path Links: {}\n".format(urls))
        print("[[bold yellow]*[/bold yellow]] Loading Links...\n")
        find_urls(validate_urls(baseUrl), urls)
        sort_list()
        url_count = 0
        for i in links:
            url_count += 1
            print(f"[[bold green]+[/bold green]] Link: [green]{i}[/green]")
        print(
            "\n[[bold green]+[/bold green]] Total Links Found: [green]{}[/green]".format(str(url_count)))
        if (output == 1):
            outputData(outfile, links)
    except Exception:
        print("[[bold red]-[/bold red]] Unexpected Error Encountered, Exiting...\n")
    except KeyboardInterrupt:
        print("Programm Terminated, Exiting...")


def main():
    parser = argparse.ArgumentParser(description="Link Parser")
    parser.add_argument(
        '-u', '--url', help='Specify the Target URL', required=True)
    parser.add_argument(
        '-p', '--path', help='Specify the URL Path seperated with \',\'', default='/')
    parser.add_argument("-o", '--output', help="Specify Output File", type=str)
    arg = parser.parse_args()
    baseURL = arg.url
    urls = arg.path
    write_output = 0
    if (arg.output):
        write_output = 1
    getlinks(baseURL, urls.split(','), write_output, arg.output)


# Initializing the main function
if __name__ == '__main__':
    main()

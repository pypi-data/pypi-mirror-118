import argparse
from argparse import Namespace
from json import dump
from os import getcwd
from os.path import join
from random import randint

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from requests import get


def args() -> Namespace:
    parser = argparse.ArgumentParser(
        prog="Programming Languages",
        description="A Python project to get a list of programming languages from Wikipedia. The default behavior prints a random programming language to the console.",
    )

    parser.add_argument(
        "-o",
        "--download-only",
        action="store_true",
        required=False,
        help="Flag to download only a JSON file of the list of programming languages",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        help="Flag to enable verbosity",
    )

    parser.add_argument(
        "-d",
        "--directory",
        nargs=1,
        type=str,
        required=False,
        default=".",
        help="Directory where to store downloaded files",
    )

    return parser.parse_args()


def getPage(page: str) -> BeautifulSoup:
    page = get(url=page).text

    return BeautifulSoup(markup=page, features="lxml")


def getProgrammingLanguage(soup: BeautifulSoup) -> dict:
    data: dict = {}

    letters: ResultSet = soup.findChildren(name="div", attrs={"class": "div-col"})

    letter: Tag
    for letter in letters:

        languages: ResultSet = letter.findAll("li")

        language: Tag
        for language in languages:
            url: str
            try:
                url = "https://en.wikipedia.org" + language.findChild("a").get(
                    key="href"
                )
            except AttributeError:
                url = ""
            data[language.text] = url

    return data


def exportProgrammingLanguages(
    data: dict, filepath: str = join(getcwd(), "languages.json")
) -> None:
    with open(file=filepath, mode="w") as file:
        dump(obj=data, fp=file)
        file.close()


def getRandomLanguage(data: dict) -> dict:
    languages: list = list(data.keys())
    index: int = randint(0, len(languages) - 1)
    key: str = languages[index]
    return {key: data[key]}


def _verboseRun() -> dict:
    wikipediaPage: str = (
        "https://en.wikipedia.org/wiki/List_of_programming_languages"
    )
    print(f"Getting HTML from {wikipediaPage}")
    soup: BeautifulSoup = getPage(page=wikipediaPage)
    print("Scraping programming languages from the downloaded HTML")
    languages: dict = getProgrammingLanguage(soup=soup)

    if args().download_only is False:
        print("Randomly selecting a programming language")
        langURL: dict = getRandomLanguage(data=languages)
        lang: str = list(langURL.keys())[0]
        print("\n" + lang + " : " + langURL[lang] + "\n")

    filepath: str = join(args().directory[0], "languages.json")
    print(f"Saving programming languages to {filepath}")
    exportProgrammingLanguages(data=languages, filepath=filepath)
    return languages

def _quietRun() -> dict:
    soup: BeautifulSoup = getPage(
        page="https://en.wikipedia.org/wiki/List_of_programming_languages"
    )
    languages: dict = getProgrammingLanguage(soup=soup)

    if args().download_only is False:
        langURL: dict = getRandomLanguage(data=languages)
        lang: str = list(langURL.keys())[0]
        print(lang + " : " + langURL[lang])

    filepath: str = join(args().directory[0], "languages.json")
    exportProgrammingLanguages(data=languages, filepath=filepath)
    return languages

def main()  ->  dict:
    if args().verbose:
        _verboseRun()
    else:
        _quietRun()

if __name__ == "__main__":
    main()

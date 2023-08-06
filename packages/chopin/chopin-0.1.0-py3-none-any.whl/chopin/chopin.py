# -*- coding: utf-8 -*-

__all__ = (
    "Chopin",
)

import asyncio
import copy
import json
import os
import random
import subprocess
from dataclasses import dataclass, field
from typing import List, TypedDict, Union

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

LinkArg:TypedDict = TypedDict("LinkArg", {"url":str, "id":str, "artists":str})

@dataclass
class Link(object):
    """
    Attributes
    ----------
    url : str
        Youtube url of the video
    id : str
        YouTube video id
    artists : List[str]
        List of artists in the video
    """
    url :str
    id :str
    artists :List[str]

    @classmethod
    def _link_class(cls, url:str, id:str, artists:str):
        return cls(url, id, artists.split(","))

    def download(self, path:str=None, delete:bool=False) -> str:
        """
        Downloading audio using the `youtube-dl` library.

        Parameters
        ----------
        path : str
            path to save to, if None, audio
        delete : bool
            delete the file if it has been saved in the past
        """
        path = f"/tmp/{self.id}.mp3" if path is None else path

        if not path.endswith(".mp3"):
            path = f"{path}.mp3"

        if delete and os.path.exists(path):
            os.remove(path)

        cmd = f"youtube-dl -o {path.replace('mp3','%(ext)s')} -x -f bestaudio --audio-format mp3 --audio-quality 0 {self.url}"
        subprocess.check_call(cmd.split())

        return path

    def delete(self, path:str=None) -> None:
        """
        delete a saved audio file
        """
        path = f"/tmp/{self.id}.mp3" if path is None else path
        if os.path.exists(path):
            os.remove(path)
        return

    def get_json(self) -> dict:
        return {"url":self.url, "id":self.id, "artists":",".join(self.artists)}

@dataclass
class Composition(object):
    """
    Chopin's composition data.

    Attributes
    ----------
    title : str
        Title of composition
    wiki : str
        Link to the github wiki
    opus : str
        Opus number (Op)
    no : str
        The number of the work (No) if there is an identical Opus number
    links : List[Link]
        List of links to videos
    """
    title :str
    wiki :str
    opus :str = None
    no :str = None
    links :List[Link] = field(default_factory=list)

    @classmethod
    def _class_composition(cls, title:str, wiki:str, opus:str=None, no:str=None, link_list:List[LinkArg]=[]):
        return cls(title, wiki, opus, no, [Link._link_class(**link) for link in link_list])

    def __str__(self) -> str:
        text = f"{self.title} "
        text += f"Op.{self.opus} " if self.opus is not None else ""
        text += f"No.{self.no} " if self.no is not None else ""
        return text

    def get_file_name(self, index:int) -> str:
        """
        Generates a song file name consisting of the song title, composition number and artist name.

        Parameters
        ----------
        index : int
            index of lists to video links
        """
        link = self.links[index]
        name = f"{self.title}_"
        name += f"{self.opus}_" if self.opus is not None else "_"
        name += f"{self.no}_" if self.no is not None else "_"
        name += f"{'&'.join(link.artists)}&"
        name = name.replace(" ", "_")
        return name

    def get_json(self) -> dict:
        return {"title":self.title, "wiki":self.wiki, "opus":self.opus, "no":self.no, "link_list":[link.get_json() for link in self.links]}

class Chopin(object):
    """
    class on Chopin's compositions

    Attributes
    ----------
    compositions : List[Composition]
        list of Chopin's compositions
    """
    _json_path = "/tmp/chopin.json"
    GENRE = (
        "Ballade",
        "Bolero",
        "Etude",
        "Fantasie",
        "Impromptu",
        "Mazurka",
        "Nocturne",
        "Concerto",
        "Sonata",
        "Scherzo",
        "Polonaise",
        "Prelude",
        "Rondo",
        "Variations",
        "Waltz",
    )

    def __init__(self, force:bool=False, output:bool=False, semaphore:int=5) -> None:
        """
        Parameters
        ----------
        force : bool
            `True` when getting data from the web, even if there is a temporary file that holds the wiki data.
        output : bool
            `True` when displaying the status of access to the wiki
        semaphore : int
            Semaphore to control the number of parallelism
        """
        super().__init__()

        if force or not os.path.exists(self._json_path):
            it = Init(output=output, semaphore=semaphore)
            it.run()
            json_data = it.arg_list
            with open(self._json_path, "w") as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
        else:
            with open(self._json_path, "r") as f:
                json_data = json.load(f)

        self.compositions:List[Composition] = []
        for data in json_data:
            self.compositions.append(Composition._class_composition(**data))

        return

    def _list_in_list(self, list1:List[str], list2:List[str]) -> bool:
        for el in list1:
            if el in list2:
                return True
        return False

    def _get_by_genre(self, genre:str) -> List[Composition]:
        if genre not in self.GENRE:
            genre = "Others"

        output_list:List[Composition] = []

        if genre != "Others":
            for compo in self.compositions:
                if genre in compo.title:
                    output_list.append(copy.deepcopy(compo))
        else:
            for compo in self.compositions:
                if not self._list_in_list(self.GENRE, compo.title):
                    output_list.append(copy.deepcopy(compo))

        return output_list

    def get_by_genre_list(self, genre_list:List[str]=list(GENRE)+["Others"]) -> List[Composition]:
        """
        Get a list of compositions by genre.

        Parameters
        ----------
        genre_list : List[str]
            list of genres
        """

        output_list:List[Composition] = []

        for genre in genre_list:
            output_list.extend(self._get_by_genre(genre))

        return output_list

    def random_get(self) -> Composition:
        """
        Return `Composition` class with multiple link destination.
        """
        output:Composition = None

        while output is None:
            compo = random.choice(self.compositions)
            if compo.links != []:
                output = copy.deepcopy(compo)
                output.links = [random.choice(compo.links)]

        return output

    def random_gets(self) -> Composition:
        """
        Return `Composition` class with a single link destination.
        """
        output:Composition = None

        while output is None:
            compo = random.choice(self.compositions)
            if compo.links != []:
                output = copy.deepcopy(compo)

        return output

class Init(object):
    url = "https://github.com/ster-phys/chopin/wiki"

    def __init__(self, output=False, semaphore=5) -> None:
        super().__init__()
        self.arg_list:List[dict] = self._init_arg_list()
        self.output:bool = output
        self.semaphore:int = semaphore

    def _init_arg_list(self) -> List[dict]:
        soup = BeautifulSoup(requests.get(self.url).text, "lxml")
        tr_list:List[Tag] = soup.find_all("div", class_="markdown-body")[0].find_all("tr")[1:]
        arg_list = []
        for tr in tr_list:
            td_list:List[Tag] = tr.find_all("td")
            wiki:str = td_list[0].find('a').get("href")
            title:str = str(td_list[1].string)
            opus = str(td_list[2].string)
            no = str(td_list[3].string)
            opus:Union[None,str] = None if opus == "ㅤ" else opus
            no:Union[None,str] = None if no == "ㅤ" else no
            arg_list.append({"title":title, "opus":opus, "no":no, "wiki":wiki})
        return arg_list

    def _get_link(self, i:int) -> None:
        url = self.arg_list[i]["wiki"]

        if self.output:
            print(f"{i+1:>3}/{len(self.arg_list)} Connect to {url}")
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        try:
            tr_list:List[Tag] = soup.find_all("div", class_="markdown-body")[0].find_all("tr")[1:]
        except IndexError:
            return

        if self.output:
            print(f"{i+1:>3}/{len(self.arg_list)} Found Youtube {len(tr_list)} ids")

        link_arg_list = []
        for tr in tr_list:
            td_list:List[Tag] = tr.find_all("td")
            url = td_list[0].find('a').get("href")
            id = str(td_list[1].string)
            artists = str(td_list[2].string)
            link_arg_list.append({"url":url, "id":id, "artists":artists})

        self.arg_list[i]["link_list"] = link_arg_list
        return

    async def _query(self, loop:asyncio.AbstractEventLoop):
        sem = asyncio.Semaphore(self.semaphore)

        async def _task(i:int):
            async with sem:
                return await loop.run_in_executor(None, self._get_link, i)

        tasks = [_task(i) for i in range(len(self.arg_list))]
        return await asyncio.gather(*tasks)

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._query(loop))

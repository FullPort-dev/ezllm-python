import time
from typing import TYPE_CHECKING, Generic, TypeVar, overload

from ezllm.SubDoc import SubDocs
from ezllm.constants import UPLOAD_TIMEOUT

if TYPE_CHECKING:
    from ezllm.methods.Base import MethodBase
    from ezllm.methods import ExtractionMethod, QAMethod
    from ezllm.response import ExtractionMethodResponse, QAMethodResponse

import requests
from ezllm.types import DocumentStateTypes, GroupTypes, MetadataFilterType

from ezllm.errors import FileProcessingError, NotFound
from .Client import Client

S = TypeVar('S', bound=SubDocs)

class Document(Generic[S]):
    SubDocsClass: S = SubDocs
    def __init__(
            self,
            id = None,
            client:Client = None,
            cid = None,
            data = None,
        ):
        
        self.client = client or Client()
        self.data = data or {}
        self._id = id or self.data.get('_id')
        self._cid = cid or self.data.get('cid')
        self.subdocs = None
        if self.data.get('subdocs'):
            self.subdocs = self.SubDocsClass(self.data.get('subdocs'))
        
        
    def get_state(self) -> DocumentStateTypes:
        res = requests.get(
            f'{self.url}/state',
            headers=self.client.headers,
        )
        state = res.json()
        self.data['state'] = state
        return state

    @classmethod
    def from_data(cls, data, client = None):
        return Document(
            data['_id'],
            client=client,
            cid=data['cid'],
            data=data,
        )
    
    @property
    def url(self):
        return f'{self.client.workspace_api_url}/d/{self._id}'
    
    def get(self):
        response = requests.get(
            self.url,
            headers=self.client.headers,
        )
        if response.status_code == 200:
            # TODO format this into a Document
            data = response.json()
            self.data = data

            # TODO should this return self?
            return Document.from_data(data, self.client)
        else:
            print("ERROR FETCHING DOCUMENT", response.status_code)
            raise NotFound("Document")

    def get_cache(self):
        if len(self.data) == 0:
            self.get()
        
        return self.data

    def filter(self,
            metadata: 'MetadataFilterType' = {}
        ):

        from .Filter import Filter
        return Filter(documents=[self], metadata=metadata)

    @overload
    def run(
        self,
        method: 'ExtractionMethod' = None,
        group: GroupTypes = GroupTypes.all,
    ) -> 'ExtractionMethodResponse': ...

    @overload
    def run(
        self,
        method: 'QAMethod' = None,
        group: GroupTypes = GroupTypes.all,
    ) -> 'QAMethodResponse': ...
        
    def run(
            self,
            method: 'MethodBase' = None,
            group: GroupTypes = GroupTypes.all,
        ):
        return self.scan(group).run(method)

    def search(self, query, n_docs = 10):
        from .Search import SearchRetrieval
        return SearchRetrieval(
            client=self.client,
            query=query,
            n_docs=n_docs,
            filter=self.filter()
        )

    def scan(
            self,
            group: GroupTypes = GroupTypes.all
        ):
        from .Scan import ScanRetrieval
        return ScanRetrieval(
            client=self.client,
            filter=self.filter()
        )
    

    def delete(self):

        headers = {
            "Content-Type": "application/json",
            **self.client.headers  
        }
        res = requests.delete(
            self.url,
            headers=headers,
        )
        self.data = res.json()
        return self

    def await_processed(self):
        MAX_POLLING_INTERVAL = 10
        interval = 1
        start = time.time()
        while True:
            if time.time() - start > UPLOAD_TIMEOUT:
                raise TimeoutError("Polling timed out")
            time.sleep(interval)
            state = self.get_state()
            interval = min(interval*2, MAX_POLLING_INTERVAL)  # Double the interval

            if state == 'active':
                break
            if state == 'error':
                raise FileProcessingError()

    @property
    def name(self) -> str:
        data = self.get_cache()
        return data['name']
    
    @property
    def id(self) -> str:
        if self._id:
            return self._id
        data = self.get_cache()
        return data['_id']
    
    @property
    def state(self) -> str:
        data = self.get_cache()
        return data['state']
    

    # @property
    # def file(self) -> DocumentFile:
    #     pass # TODO STEPHEN


"""
# {
#     "type": "all",
#     "id": "",
#     "docs": [
#         {
#             "_id": "659a54a5d9569e7b627dea93",
#             "updatedOn": "2024-01-08T07:51:56.570000",
#             "createdOn": "2024-01-08T07:51:54.430000",
#             "name": "Reddit Test File",
#             "wid": "test",
#             "cid": "659a54a5d9569e7b627dea93",
#             "state": "active",
#             "errorMessage": None,
#             "metadata": {
#                 "type": "text"
#             },
#             "file": {
#                 "contentType": "text/plain",
#                 "filename": "reddit.txt",
#                 "size": 3299
#             },
#             "parser": {},
#             "link": {
#                 "type": "default",
#                 "href": None,
#                 "external": False
#             },
#             "users": [],
#             "groups": [],
#             "visibility": "private",
#             "deletedTime": None,
#             "subdocs": [
#                 {
#                     "page_content": "jump to content\nMY SUBREDDITS\n\t\t\t\tPOPULAR-ALL-RANDOM-USERS\u00a0|\u00a0ASKREDDIT-PICS-GAMING-FUNNY-MOVIES-MILDLYINTERESTING-WORLDNEWS-DATAISBEAUTIFUL-DIY-NEWS-EXPLAINLIKEIMFIVE-TODAYILEARNED-OLDSCHOOLCOOL-VIDEOS-NOTTHEONION-BOOKS-TIFU-SHOWERTHOUGHTS-TWOXCHROMOSOMES-AWW-FUTUROLOGY-MUSIC-JOKES-LIFEPROTIPS-ASKSCIENCE-SCIENCE-IAMA-SPACE-GADGETS-SPORTS-UPLIFTINGNEWS-FOOD-NOSLEEP-HISTORY-GIFS-INTERNETISBEAUTIFUL-GETMOTIVATED-WRITINGPROMPTS-ANNOUNCEMENTS-PHILOSOPHY-DOCUMENTARIES-EARTHPORN-CREEPY-PHOTOSHOPBATTLES-LISTENTOTHIS-BLOG\nMORE \u00bb\n\t\treddit.com\u00a0hotnewrisingcontroversialtopwiki\n\t\tWant to join?\u00a0Log in\u00a0or\u00a0sign up\u00a0in seconds.|English\n\n\nremember mereset password\nlogin\n\n\nSubmit a new link\n\nSubmit a new text post\n\n\nGet an ad-free experience with special benefits, and directly support Reddit.\nGet Reddit Premium\n\nWelcome to Reddit.\nCome for the cats, stay for the empathy.\nBECOME A REDDITOR\nand start exploring.\n\u00d7\npopular in:\u00a0Canada\n\n1\n\n7792\n\n\nWhat was the \u201c\u2026seriously?\u201d gift you opened this Christmas?\u00a0(self.AskReddit)\nsubmitted\u00a011 hours ago\u00a0by\u00a0Leading_War_5847\u00a0to\u00a0r/AskReddit\n\t\t10166 commentssharesavehidereport\n\n\n\n\n\n2\n\n\u2022\n\n\n[Post Game Thread] The Brooklyn Nets (15-15) defeat the Detroit Pistons (2-28), 118 - 112 behind 21/4/3 from Mikal Bridges as the Pistons break the record for the most consecutive losses by a team in a single seasonPost Game Thread\u00a0(self.nba)\n\nsubmitted\u00a0an hour ago\u00a0*\u00a0by\u00a0UnbiasedNBAFan_[\ud83c\udf70]\u00a0to\u00a0r/nba\n\t\t821 commentssharesavehidereport\n\n\n\n\n3\n\n2937\n\n\n[Serious] What's the scariest fact you wish you didn't know?Serious Replies Only\u00a0(self.AskReddit)\nsubmitted\u00a09 hours ago\u00a0by\u00a0Msjann\u00a0to\u00a0r/AskReddit\n\t\t3188 commentssharesavehidereport\n\n\n\n\n4\n\n44.4k\n\n\ufffc\nA daughter wrote a brutal \"rot in hell\" kind of obituary about her mom in a newspaper in Michigan.\u00a0(i.redd.it)\n\nsubmitted\u00a08 hours ago\u00a0by\u00a0Lifegoesonforever\u00a0to\u00a0r/pics\n\t\t2153 commentssharesavehidereport\n\n\n\n\n5\n\n8455\n\n\ufffc\n\"Calling Eminem the greatest at rap is white supremacy\"\u00a0\ud83c\uddf2 \ud83c\uddee \ud83c\uddf8 \ud83c\udde8 \u00a0(i.redd.it)\n\nsubmitted\u00a04 hours ago\u00a0by\u00a0Visqo\u00a0to\u00a0r/facepalm\n\t\t2302 commentssharesavehidereport\n\n\n\n\n6\n\n342\n\n\ufffc\nCanadians aren\u2019t actually that interested in the economy, and that\u2019s a problemOpinion Piece\u00a0(theglobeandmail.com)\nsubmitted\u00a04 hours ago\u00a0by\u00a0joe4942\u00a0to\u00a0r/canada\n\t\t299 commentssharesavehidereport\n\n\n\n\n7\n\n859\n\n\ufffc\nWell this is the most accurate map legend everMeme\u00a0(i.redd.it)\n\nsubmitted\u00a02 hours ago\u00a0by\u00a0Alternative-Pay6464\u00a0to\u00a0r/nhl\n\t\t97 commentssharesavehidereport\n\n\n\n\n8\n\n4982\n\n\ufffc\nWoman with 6 kids upset at this year\u2019s haul\u00a0(i.redd.it)\n\nsubmitted\u00a08 hours ago\u00a0by\u00a0adelltfm\u00a0to\u00a0r/ChoosingBeggars\n\t\t1452 commentssharesavehidereport\n\n\n\n\n9\n\n\u2022\n\n\ufffc\n'Parasite' actor Lee Sun-kyun found dead amid investigation over drug allegationsNews\u00a0(koreatimes.co.kr)\nsubmitted\u00a0an hour ago\u00a0by\u00a0mcfw31\u00a0to\u00a0r/movies\n\t\t155 commentssharesavehidereport\n\n\n\n\n10\n\n11.7k\n\n\ufffc\nTIL on 9/11/01 a guest at the Marriott World Trade Center hotel, located at the base of the towers, awoke to the first plane crashing but went back to bed. He then got up, turned on the news, took a shower, packed his things, and only decided to evacuate when the South Tower collapsed onto the hotel\u00a0(voanews.com)\nsubmitted\u00a05 hours ago\u00a0by\u00a0minerman30\u00a0to\u00a0r/todayilearned\n\t\t334 commentssharesavehidereport",
#                     "metadata": {
#                         "cid": "659a54a5d9569e7b627dea93",
#                         "did": "659a54a5d9569e7b627dea93",
#                         "index": 0,
#                         "wid": "test"
#                     },
#                     "score": None
#                 }
#             ]
#         }
#     ]
# }
"""
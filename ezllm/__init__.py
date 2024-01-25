from __future__ import annotations
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(usecwd=True))

from io import BufferedReader
from typing import Optional

# from ezllm.Workspace import Workspace
from .Client import Client
from .Collection import Collection, FileTypes
from .Document import  Document
from .Documents import  Documents
from .Filter import Filter
from .Search import SearchRetrieval
from .Collections import Collections
from .methods import *
from .types import *


def upload(
    file: Optional[BufferedReader] = None,
    path: Optional[str] = None,
    name: Optional[str] = None,
    type: Optional[FileTypes] = 'auto'
):
    """
    Upload to the Default Collection
    """
    col = Collection(name="Default Collection")
    return col.upload(file=file, path=path, name=name, type=type)


    
def filter(
    documents: DocumentFilterType = [],
    collections: CollectionFilterType = [],
    metadata: MetadataFilterType = {}
):
    from .Filter import Filter
    return Filter(documents=documents, collections=collections, metadata=metadata)

__version__ = "0.1.4"
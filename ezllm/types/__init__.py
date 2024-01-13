from enum import Enum
from typing import List, Dict, Any, Literal

DocumentFilterType = List[str]
CollectionFilterType = List[str]
MetadataFilterType = Dict[str, Any]

# TODO : figure this out one day w/ out the circular deps
# DocumentFilterType = List[Union[Document, str]]
# CollectionFilterType = List[Union[Collection, str]]
# MetadataFilterType = Dict[str, Any]


GroupTypes = Literal['all', 'collection', 'document']



class DocumentStateTypes(Enum):
    unprocessed = 'unprocessed'
    processing = 'processing'
    active = 'active'
    error = 'error'
    deleted = 'deleted'

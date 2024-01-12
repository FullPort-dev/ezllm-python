from enum import Enum
from typing import List, Dict, Any

DocumentFilterType = List[str]
CollectionFilterType = List[str]
MetadataFilterType = Dict[str, Any]

# TODO : figure this out one day w/ out the circular deps
# DocumentFilterType = List[Union[Document, str]]
# CollectionFilterType = List[Union[Collection, str]]
# MetadataFilterType = Dict[str, Any]

class GroupTypes(Enum):
    all='all'
    collection='collection'
    document='document'



class DocumentStateTypes(Enum):
    unprocessed = 'unprocessed'
    processing = 'processing'
    active = 'active'
    error = 'error'
    deleted = 'deleted'
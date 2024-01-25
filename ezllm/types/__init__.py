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
AggTypes = Literal['all', 'collection', 'document', 'accumulate']
LLMTypes = Literal['gpt-4', 'gpt-3.5', 'gpt-3.5-turbo-1106']



class DocumentStateTypes(Enum):
    unprocessed = 'unprocessed'
    processing = 'processing'
    active = 'active'
    error = 'error'
    deleted = 'deleted'


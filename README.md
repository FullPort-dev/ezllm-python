# ezllm-python
The goal of EzLLM is to provide the simplest interface for creating LLM based applications

EzLLM simplifies the process of 
1. File parsing
2. Storage
3. Retrieval
4. LLM optimization
5. LLM output parsing

## [Read The Docs](https://docs.ezllm.io)

for more information




# Quick Start
## Install
```bash
pip install ezllm
```

## Authenticate the SDK
1. go to the API keys page in the developer dashboard
2. create an API key
3. save the API key and API secret to a `.env` file

```bash
EZLLM_KEY=abc
EZLLM_SECRET=xyz
```
by saving it to a .env file, ezllm will authenticate itself

alternatively you can pass the key and secret to ezllm to create a client

```py
from ezllm import Client

client = Client(key='...', secret='...')
```

## Upload Documents
```py
import ezllm
# or
from ezllm import Collection

col = ezllm.Collection("documentation")



# Upload a single file
file = open('./file.pdf', 'r')
await col.upload(file)

# Upload an array of files
files = [open('./file1.pdf'), open('./file2.txt')]
await col.upload(files)
```

## Retrieve Relevant Documents
for more information on document retrieval [click here](</retrieval/Retrieval>)

```py
response = col.search('search query').get()

print(response)

SearchResponse(
    costs=ResponseCosts(
        total_cost=10.0,
        costs=[
            ResponseCost(
                cost=10,
                date='2024-01-12T05:38:08.266074',
                step='retrieve',
                usage=1,
                limitType='search',
                limitId='search',
                desc=None,
                reportedCost=None
            )
        ]
    )
    doc_groups=SearchDocOutputGroups(
        groups=[
            SearchDocOutputGroup(
                id="collection_id",
                type="collection",
                data=SearchResponseDocs(
                    docs=[
                        SearchResponseDoc(
                            name="Test File",
                            SubDocs=1
                        )
                    ]
                )
            )
        ]
    )
)

# it's heavily nested from the aggregation step
# so you can reference all of the underlying docs with .docs
print(response.docs)

ResponseDocs(
    docs=[
        SearchResponseDoc(
            name="Test File"
            SubDocs=1
        )
    ]
)

for doc in response.docs:
    print(doc)

    SearchResponseDoc(
        name="Test File"
        SubDocs=1
    )
```


# you can iterate through the results

for result in realted_documents:
    print(result)
```


## Run Methods against a Retrieval
```py
from ezllm.methods import Summarization

col.search('search query').run(Summarization())
```


## Tests
tests are located in the /test directory and can be a good resource for understanding how to interact with entities in the SDK.

[Read more about tests here ](<./tests/README.md>)

to run tests, you need to provide a .env file with the following values.
```bash
EZLLM_ACCESS_KEY = access_key
EZLLM_SECRET = secret
EZLLM_API_URL = https://api.ezllm.io # optional
EZLLM_RUN_URL = https://run.ezllm.io # optional
```
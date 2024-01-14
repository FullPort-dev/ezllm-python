# ezllm-python
The goal of EzLLM is to provide the simplest interface for creating LLM based applications

EzLLM simplifies the process of 
1. File parsing
2. Storage
3. Retrieval
4. LLM optimization
5. LLM output parsing

## [Home Page](https://ezllm.io) --- [Docs](https://docs.ezllm.io) --- [Developer Console](https://console.ezllm.io)

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

# Upload by path
await col.upload(path='./file.pdf')
# Or
await col.upload(path='./file.pdf', name="My File Name", type='pdf')
```

## Retrieve Relevant Documents
for more information on document retrieval [click here](</retrieval/Retrieval>)

```py
response = col.search('search query').get()

print(response)

# Output
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

# Output
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

    # Output
    SearchResponseDoc(
        name="Test File"
        SubDocs=1
    )
```


## Run Methods against a Retrieval
```py
from ezllm.methods import QAMethod

col.search('search query').run(QAMethod(questions=["Is this document relevant to my research in XYZ"]))

# Output
QAMethodResponse(
    costs=ResponseCosts(
        total_cost=0.08994,
        costs=[
            ResponseCost(cost=0.01061, date='2023-12-27T18:11:18.722257', step='method', usage=835, limitType='llm', limitId='gpt-4-1106-preview', desc=None, reportedCost=None)
            ...
        ]
    )
    # add the include_docs=True argument to return docs
    doc_groups=DocOutputGroups(
        groups=[

        ]
    )
    output_groups=QAOutputGroups(
        groups=[
            QAOutputGroup(
                type="document"
                id="658b4e441f41ead7592562de"
                output=QAOutputData(
                    data=[
                        {
                            "question": "Who are the authors?",
                            "answer": "Sylvain Burns, Joseph Brehaut, Jamie Britton",
                            "relevant": 100
                        },
                        {
                            "question": "What organizations is this document from?",
                            "answer": "Journal of Professional Engineering, University of Ottawa",
                            "relevant": 100
                        }
                    ]
                )
            )
            ...
        ]
    )
)
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


## Deploy
```bash
pip show ezllm

# 1. Build
python3 setup.py sdist bdist_wheel

2. # Install
## local
pip3 install --upgrade dist/ezllm-0.1-py3-none-any.whl

## test-pypi
pip3 install --index-url https://test.pypi.org/simple/ ezllm

## pypi
pip3 install ezllm

## Uninstall (necessary to test each version)
pip3 uninstall ezllm 

3. # Upload
## test-pypi
python3 -m twine upload --repository testpypi dist/*

## pypi
python3 -m twine upload dist/*
```
# SDK Testing

```bash
pytest
# or
python3 -m pytest # I was having trouble with pytest resolving the sdk

# run a specific test file
pytest tests/test_name.py

# run a specific test function
pytest tests/test_name.py::function_name

pytest -s # if you want console prints
```

## Auth
```bash
cd knowledgeshare/scripts
python3 setup_test_env.py
```


# Strategy
constants
- workspace `test`
- collection name=`test` cid=`659a54a5d9569e7b627dea93`
- document name=`Reddit Test File` did=`659a54a5d9569e7b627dea93`
- collection name=`Default Collection` cid=`659a54a5d9569e7b627dea99`


We will test upload, updated, delete ... files in the Default Collection and leave the test collection immutable

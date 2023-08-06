# JSONCHICK
Get paths to a value in JSON data.

## Install
`pip install jsonchick`

## Use

```
from jsonchick import jsonchick


data = [{'k1': 'v1'}, [{'k2': ['v1']}]]
value = 'v1'

assert ((0, 'k1'), (1, 0, 'k2', 0)) == jsonchick.get_tuples(value, data)
assert [[0, 'k1'], [1, 0, 'k2', 0]] == jsonchick.get_lists(value, data)
assert ['[0]["k1"]', '[1][0]["k2"][0]'] == jsonchick.get_strings(value, data)
```

## Credits
The lib is a modified version of a Stackoverflow answer on the question:
https://stackoverflow.com/questions/31010299/json-get-key-path-in-nested-dictionary


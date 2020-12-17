# sunburst_kit
Testing tools for analysis of the Sunburst backdoor reported by FireEye (Written for Python3)

**sunburst_FNV.py**

_Requirements: pip install fnvhash_

This script can be used to attempt to decode the hardcoded values from within SUNBURST backdoor. This can be done by either passing a file of guess strings (bit like a dictionary attack):
```
python3 sunburst_FNV.py -f processes.txt --values hardcodedVal.txt
```
Or via bruteforce:
```
python3 sunburst_FNV.py -b --values hardcodedVal.txt
```
_**Note that this is rudimentary bruteforce and is not fully optimised!**_

processes.txt populated from https://github.com/fireeye/sunburst_countermeasures/blob/main/fnv1a_xor_hashes.txt

# sunburst_kit
Testing tools for analysis of the Sunburst backdoor reported by FireEye (Written for Python3)

## sunburst_FNV.py

_Requirements: pip install fnvhash_

This script can be used to attempt to decode the hardcoded values from within SUNBURST backdoor. This can be done by either passing a file of guess strings (bit like a dictionary attack) or via bruteforce.

**Usage**

Passing process file
```
python3 sunburst_FNV.py -f processes.txt --values hardcodedVal.txt
```
Bruteforce
```
python3 sunburst_FNV.py -b --values hardcodedVal.txt
```
_**Note that this is rudimentary bruteforce and is not fully optimised!**_

processes.txt populated from https://github.com/fireeye/sunburst_countermeasures/blob/main/fnv1a_xor_hashes.txt

## sunburst_b64.py

This script pulls out the encoded strings within _OrionImprovementBusinessLayer_ that use the DeflateStream Class of the .NET's System.IO.Compression library and base64 encoding. It then removes any duplicate base64 values before inflating to return the decoded string value.

**Usage**
```
python3 sunburst_b64.py -f <decompiled OrionImprovementBusinessLayer>
```

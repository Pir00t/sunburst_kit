import argparse
import base64
import binascii
import re
import sys
import zlib

__author__ = 'Pir00t'
__date__ = 20201217

def extractor(content):
    
    results = []

    # regex for base64 strings - repurposed from another script of mine
    sig = re.compile(r"^\b(?!\(\")(?:[A-Za-z0-9+/]{4})+(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?(?<!\"\))$|(?!')(?:[A-Za-z0-9+/]{4})+(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?(?=\"\))|[a-zA-Z0-9/+]{30,}={0,2}")
    
    for line in content:
        if "ZipHelper.Unzip" in line:
            result = re.findall(sig, line)
            for r in result:
                if r == '': # ignore null values for output
                    continue
                else:
                    results.append(r)

    return results

def dedup(strings):
   
    matches = [] # hold unique lines seen

    for line in strings:
        if line not in matches: # not a duplicate
            matches.append(line)

    return matches

def decoder(b64_str):

    try:
        decoded = zlib.decompress(base64.b64decode(b64_str), -zlib.MAX_WBITS)
        return decoded

    except binascii.Error as err:
        print ('[!] {}'.format(err))
        print ('[*] Attempting to fix and decode...')
        try:
            missing_pad = len(b64_str) % 4
            b64_str += '='* (4 - missing_pad)
            decoded = zlib.decompress(base64.b64decode(b64_str), -zlib.MAX_WBITS)
            return decoded

        except binascii.Error as e:
            err_string = ('[!] {} or Invalid base64 string...Skipping'.format(e))
            result = err_string.encode()
            return result


def main():

    parser = argparse.ArgumentParser(description="Find and decode the encoded variable names within Sunburst backdoor code.")
    parser.add_argument("-f", help="Sunburst decompiled file name/location")

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    sunFile = args.f

    with open(sunFile, "r") as f:
        content = f.read().splitlines()

    print ("\n[*] Searching for encoded strings...")
    found = extractor(content)
    uniqueb64 = dedup(found)
    
    with open("b64decoded_strings.txt", "w+") as output:
        print ('[*] Attempting to decode strings...') 
        for b64str in uniqueb64:
            if b64str.isdigit() or b64str.islower() or b64str.isalpha(): # attempt to filter out ordinary/numeric strings
                pass
            else:
                decoded = decoder(b64str)
                #print ("[+] Successfully decoded {} : {}\n".format(b64str, decoded.decode()))
                output.write(b64str + " : " + decoded.decode() + "\n")

    print("[+] Done. Check text file for output")
if __name__ == '__main__':
    main()
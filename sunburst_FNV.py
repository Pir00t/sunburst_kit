# This script was developed in order to gain an understanding of the encoding methods used in the Solwarwinds/SUNBURST backdoor DLL
# Feel free to use it for learning/understanding as per the licence included in the main repo: https://github.com/Pir00t/sunburst_kit/blob/main/LICENSE

import argparse
import sys
from fnvhash import fnv1a_64 # needs installed via PyPi
from itertools import combinations_with_replacement 
from itertools import permutations
from string import ascii_lowercase, digits

__author__ = 'Pir00t'
__date__ = 20201217

def readFiles(procDoc, valDoc): # reads txt files of process names to try and hardcoded values txt file
    
    with open(procDoc, "r") as f:
        procs = f.read().splitlines()

    with open(valDoc, "r") as f:
        values = f.read().splitlines()

    return procs, values

#
def GetHash(svc):

    # encode proc/service using FNV-1a 64bit hash function
    fnv_val = fnv1a_64(svc.encode())

    return fnv_val ^ 6605813339339102567

def encCheck(enc_val, hardValues):

    match = False
    if str(enc_val) in hardValues: # check if computed value is a match in the hardcoded values list
        match = True
        
    return enc_val, match

def nameGenerator(length):

    charset = ascii_lowercase + digits + " _-." # bruteforce using charset from backdoor DLL
    gen_names = []
    name_gen = combinations_with_replacement(charset, length)
    for n in name_gen:
        perms = permutations("".join(n))
        for p in perms:
            gen_names.append("".join(p))

    length += 1

    return gen_names

def main():

    parser = argparse.ArgumentParser(description="Can bruteforce FNV-1a 64-bit hash or be provided with list of suspected process to compare against hardcoded values")
    parser.add_argument("-f", default="", help="Process file name/location")
    parser.add_argument("--values", default="", help="Hardcoded values file name/location")
    parser.add_argument("-b", default=False, action='store_true', help="Enable bruteforce mode")
    
    if len(sys.argv) <=1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.f and args.values:
        procs = args.f
        vals = args.values

        # read file contents required for attempting the "decoding"
        processes, hardVals = readFiles(procs, vals)
        with open("decoded.txt", "w+") as decoded:
            for proc in processes:
                check = GetHash(proc)
                enc_val, match = encCheck(check, hardVals)

                if match == True:
                    print ("\n[!] Match found\n[+] {} : {}".format(enc_val, proc))
                    decoded.write(str(enc_val) + " : " + proc + "\n")
                    

    elif args.b and args.values:
        print ("\n[*] Starting Bruteforce Mode")
        vals = args.values
        with open(vals, "r") as f:
            hardVals = f.read().splitlines()

        length = 2
        while length <= 5:
            print ("\n\t-------------------------------------------\n[*] Trying {} character length".format(length))
            gen_names = nameGenerator(length)
            length += 1
            for name in gen_names:
                check = GetHash(name)
                enc_val, match = encCheck(check, hardVals)

                if match == True:
                    print ("\n[!] Match found\n[+] {} : {}".format(enc_val, name))
                
    else:
        parser.print_help()
        sys.exit(0)
        
if __name__ == '__main__':
    main()
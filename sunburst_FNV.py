# This script was developed in order to gain an understanding of the encoding methods used in the Solwarwinds/SUNBURST backdoor DLL
# Feel free to use it for learning/understanding as per the licence included in the main repo: https://github.com/Pir00t/sunburst_kit/blob/main/LICENSE

from fnvhash import fnv1a_64 # needs installed via PyPi

__author__ = 'Pir00t'
__date__ = 20201217

def readFiles():
    
    with open("processes.txt", "r") as f:
        procs = f.read().splitlines()

    with open("hashes.txt", "r") as f:
        hashes = f.read().splitlines()

    return procs, hashes

#
def GetHash(svc):

    # encode proc/service using FNV-1a 64bit hash function
    fnv_val = fnv1a_64(svc.encode())
    #print ("[+] FNV1a(64-bit) for Message:\t", fnv_val)
    #print ("[+] XOR'd FNV1a Hash:\t", fnv_val ^ 6605813339339102567)

    return fnv_val ^ 6605813339339102567

def encCheck(enc_val, hashes, proc):

    match = False
    if str(enc_val) in hashes:
        
        match = True
        
    return enc_val, match

def main():

    # read file contents required for attempting the "decoding"
    procs, hashes = readFiles()

    with open("decoded.txt", "w+") as decoded:
        for proc in procs:
            check = GetHash(proc)
            enc_val, match = encCheck(check, hashes, proc)
            if match == True:
                print ("\n[!] Match found\n[+] {} : {}".format(enc_val, proc))
                decoded.write(str(enc_val) + " : " + proc + "\n")

        
if __name__ == '__main__':
    main()

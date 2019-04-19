from typing import List, Dict, Tuple

from collections import defaultdict
from hookFile import HookFile
from hookFileType import HookFileType
from standardizedFile import StandardizedFile
from plagiarismOccurence import PlagiarismOccurence
from match import Match

class AnHash:
    startLine: int = -1
    endLine: int = -1
    hashVal: int = -1
    origFile: HookFile

FNV_OFFSET_BASIS = 0xcbf29ce484222325
FNV_PRIME        = 0x00000100000001b3
MAX_64           = 0xffffffffffffffff

def winnow(hashes: List[AnHash], w: int) -> List[AnHash]:
    if w > len(hashes):
        print("Error: window length can't be less than number of hashes")
        exit(1)
    
    hashesIndex:int  = 0
    h: List[AnHash] = []
    fingerPrints: List[AnHash] = []

    for i in range(w):
        h.append(AnHash())

    for i in range(w):
        h[(i+1)%w] = hashes[hashesIndex]
        hashesIndex+=1


    minHash: int = 0
    minHashVal: int = MAX_64
    for i in range(w):
        if h[i].hashVal <= minHashVal:
            minHash = i
            minHashVal = h[i].hashVal

    fingerPrints.append(h[minHash])
    r: int = 0

    while hashesIndex < len(hashes):
        r = (r+1)%w
        h[r] = hashes[hashesIndex]
        hashesIndex += 1

        if minHash == r:
            i = (r-1)%w
            while i != r:
                if h[i].hashVal < h[minHash].hashVal:
                    minHash = i

                i = (i-1+w)%w
            fingerPrints.append(h[minHash])
        else:
            if h[r].hashVal < h[minHash].hashVal:
                minHash = r
                fingerPrints.append(h[minHash])
        
    return fingerPrints

def kGramHash(k: int, data: str, origFile: HookFile) -> List[AnHash]:
    
    # Create map of how many linebreaks before each literal char
    nNewLinesPrior: Dict[int] = {}
    nNewLines: int = 0
    nLiterals: int = 0

    for i in range(len(data)):
        if data[i] == '\n':
            nNewLines += 1
        else:
            nNewLinesPrior[nLiterals] = nNewLines
            nLiterals+=1
    
    data = data.replace('\n','')

    kGramList: List[AnHash] = []

    for i in range(len(data)-k+1):
        hashVal: int = FNV_OFFSET_BASIS
        for c in data[0+i:k+i]:
            hashVal = (hashVal * FNV_PRIME) & MAX_64
            hashVal = (hashVal ^ ord(c)) & MAX_64

        aHash = AnHash()
        aHash.startLine = nNewLinesPrior[0+i]+1
        aHash.endLine = nNewLinesPrior[k+i-1]+1
        aHash.hashVal = hashVal
        aHash.origFile = origFile

        kGramList.append(aHash)

    return kGramList

def getMatches(work: List[StandardizedFile], whiteList: List[StandardizedFile], matchCountStart:int = 0) -> List[Match]:
    k: int = 45
    w: int = 12

    matchCount = matchCountStart

    hashDB: Dict[List[AnHash]] = defaultdict(list)
    matchList: List[Match] = []

    for aFile in work:
        fingerPrints = winnow(kGramHash(k, aFile.standardizedData, aFile.origFile), w)

        for aHash in fingerPrints:
            hashDB[aHash.hashVal].append(aHash)

    # Remove hashes that have been white listed
    for white in whiteList:
        fingerPrints = winnow(kGramHash(k, aFile.standardizedData, aFile.origFile), w)

        for aHash in fingerPrints:
            if aHash.hashVal in hashDB:
                del hashDB[aHash.hashVal]

    for _, hashes in hashDB.items():
        if len(hashes) > 1:
            occurenceList: List[PlagiarismOccurence] = []

            for aHash in hashes:
                occurenceList.append(PlagiarismOccurence(aHash.origFile, aHash.startLine, aHash.endLine))

            matchList.append(Match(matchCount, occurenceList))
            matchCount += 1

    #Remove any matches that contain only one file
    nonDupeList : List[Match] = []
    for ocurList in matchList:
        firstFile = ocurList.plagiarismList[0].hookFile.fileName
        firstOwner = ocurList.plagiarismList[0].hookFile.fileOwner
        multiFiles = False

        for ocur in ocurList.plagiarismList[1:]:
            if ocur.hookFile.fileName != firstFile and ocur.hookFile.fileOwner != firstOwner:
                multiFiles = True
                break

        if multiFiles:
            nonDupeList.append(ocurList)


    #Remove any matches that contain plagiarism of previous years
    matchList.clear()
    for ocurList in nonDupeList:
        for ocur in ocurList.plagiarismList:
            if ocur.hookFile.fileType == HookFileType.CURRENT_YEAR:
                matchList.append(ocurList)
                break

    return matchList


import sys
import time
from typing import List

# --- Utils

def addToKB(kb, kbSearch, representation: List[str], parentClauses: List[int], searchSet=None):
    signature = tuple(sorted(representation))
    
    # Protection 1: Clause already in knowledge base
    if signature in kbSearch:
        return
    
    # Protection 2: Check true clauses
    search = searchSet if searchSet else set(representation)
    for literal in search:
        if negate(literal) in search:
            return

    kbSearch.add(signature)

    kb.append({
        'rep': representation,
        'parents': parentClauses,
        'search': search # search set
    })

def negate(literal: str):
    if literal[0] == '~':
        return literal[1:]
    return '~' + literal

# --- Parser

def parseInput(inputPath: str):
    kb = []
    kbSearch = set()
    lines = []
    
    with open(inputPath, 'r') as reader:
        while line := reader.readline():
            lines.append(line)

    # Read every line but ignore last line since that's target
    for line in lines[:-1]:
        lineArr = line.strip().split(' ')
        addToKB(kb, kbSearch, lineArr, [])
        
    # Reverse target and add to knowledge base
    target = lines[-1].strip().split(' ')
    for literal in target:
        addToKB(kb, kbSearch, [negate(literal)], [])
    
    return {
        'kb': kb,
        'kbSearch': kbSearch,
    }

# --- Resolver

def resolve(kb, kbSearch):
    i = 0
    while i < len(kb):
        curClause = kb[i]

        for j in range(i):
            prevClause = kb[j]

            merge = []
            parents = [i+1, j+1]
            mergeSet = set()
            
            """
            Rules:
            - [x] Generated clauses should not have redundant (repeated) literals.
            - [x] Clauses that evaluate to True should not be added to the KB.
            - [x] Redundant generated clauses should not be added to the KB. A clause is redundant if the KB 
                contains another clause which is logically equivalent to it.
            """

            resolvePointCur = ''

            # TEST
            # print(' '.join(curClause['rep']), '+', ' '.join(prevClause['rep']))

            for literal in curClause['rep']:
                # Repeated literal -> Ignore
                if literal in mergeSet or literal == resolvePointCur:
                    continue

                # Only find one resolve point, if there are multiple pairs, then the merged clause will be true
                # -> addToKB() will handle that and not add to knowledge base
                if resolvePointCur == '' and negate(literal) in prevClause['search']:
                    resolvePointCur = literal
                else:
                    merge.append(literal)
                    mergeSet.add(literal)

            if resolvePointCur == '':
                # This pair cannot resolve, skip to next pair
                
                # TEST
                # print("NONE")

                continue

            for literal in prevClause['rep']:
                # Repeated literal -> Ignore
                if literal in mergeSet or literal == negate(resolvePointCur):
                    continue

                merge.append(literal)
                mergeSet.add(literal)
            
            addToKB(kb, kbSearch, merge, parents, mergeSet)

            # TEST
            # print('=>', end=' ')
            # for clause in kb:
            #     print(' '.join(clause['rep']), end=' || ')
            # print()
            # time.sleep(2)

            # Contradiction when merged clause does not have any literals left
            if len(merge) == 0:
                return
    
        i += 1

#  --- Main

def main():
    inputPath = sys.argv[1]
    
    # Read input file   
    parsed = parseInput(inputPath)
    kb = parsed['kb']
    kbSearch = parsed['kbSearch']

    # TEST
    # for clause in kb:
    #     print(clause)

    # Resolve knowledge base
    resolve(kb, kbSearch)

    # Print result
    success = False
    for i in range(len(kb)):
        rep = kb[i]['rep']
        parents = kb[i]['parents']
        
        if len(rep) != 0:
            print('%d. %s' % (i+1, ' '.join(rep)), end=' ')
        else:
            success = True
            print("%d. Contradiction" % (i+1), end=' ')
        
        if len(parents) == 0:
            print('{}')
        else:
            print('{%d,%d}' % (parents[0], parents[1]))

    if success:
        print("Valid")
    else:
        print("Fail")

main()
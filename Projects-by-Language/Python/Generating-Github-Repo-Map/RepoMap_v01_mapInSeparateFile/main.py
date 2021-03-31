import os

"""
Notes:
- Splitting on a folder name to find root, is fragile.

TODO:
- Find a better way to convert to unix paths.
"""

def pathToUnix(path):
    return path.replace('\\','/')

def getRootPath(repoRootFolderName):
    repoRootFolder = f"/{repoRootFolderName}"
    currentWorkingDirectory = pathToUnix(os.getcwd())
    rootDir = currentWorkingDirectory.split(repoRootFolder)[0] + repoRootFolder
    return rootDir

def getOsWalkForRootRepoFolder(rootDir):
    """
    Note: Because os.walk() returns a generator, it is fast to run initially,
    but the files and paths will not be retrived before the "walk" is
    iterated/looped through.
    """
    walk = os.walk(rootDir, topdown=True)
    return walk

def pruneDirectoriesFromWalk(walk):
    """
    Note: This might be a heavy process depending on how large the directory is.
    The walk is being iterated/looped over, and some folders are excluded from
    the iteration to avoid spending time with files and folders which might not
    be of interest.
    """
    foldersToSkip = set(['.git'])
    prunedWalk = []
    for root, dirs, files in walk:
        dirs[:] = [d for d in dirs if d not in foldersToSkip]
        walkElement = (root, dirs, files)
        prunedWalk.append(walkElement)
    return prunedWalk

def convertWalkToUnixPaths(walk):
    return [(pathToUnix(root), dirs, files) for root, dirs, files in walk]

def generateReadmeTree(walk, rootDir):
    """
    TODO: Make case insensitive for readme-files.
    """
    outLines = []

    def converteToRelativePath(path, rootDir):
        """
        Note: One usually would like to avoid nested functions.
        Note: Slightly unsafe.
        """
        return path.replace(rootDir,'')
        
    walk = [(converteToRelativePath(root, rootDir), dirs, files)
            for root, dirs, files in walk]
    
    for root, dirs, files in walk:
        # TODO: If no readme, add as text (not link)
        if "README.md" in files:
            splitRoot = root.split('/')
            indents = len(splitRoot)-1
            name = splitRoot[-1]
            if indents == 0:
                name = "root"
            relativeFip = f"{root}/README.md"
            textLine = f"{indents*'    '}- [{name}]({relativeFip})"
            outLines.append(textLine)

    print(outLines)
    return "\n".join(outLines)
    # [print(e) for e in walk]
    # pass

def writeToRoot(readmeText, outFileName, rootDir):
    print(readmeText)
    fip = f"{rootDir}/{outFileName}"
    with open(fip, 'w') as o:
        o.write(readmeText)

def main():
    repoRootFolderName = 'Coding-Somewhere'
    rootDir = getRootPath(repoRootFolderName)
    walk = getOsWalkForRootRepoFolder(rootDir)
    prunedWalk = pruneDirectoriesFromWalk(walk)
    prunedWalk = convertWalkToUnixPaths(prunedWalk)
    readmeText = generateReadmeTree(prunedWalk, rootDir)
    writeToRoot(readmeText, "map.md", rootDir)
    # [print(e) for e in prunedWalk]


if __name__ == '__main__':
    main()

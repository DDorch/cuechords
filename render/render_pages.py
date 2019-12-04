sIndexTitle = "Live karaoké - Noël ADAS-ASC 2019"

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Read model
with open("model.html", encoding="utf-8") as f:
    sModel = f.read()

# Read list of files
import glob
txtFiles = glob.glob("../*.txt")

# Generate index
files = [os.path.basename(f).replace(".txt", "") for f in txtFiles]
# Compute font size
maxLen = len(max(files, key=len))
fontSize = 100 / maxLen * 1.7
# Inject index into the model
def renderHtml(sModel, dContent):
    for key, value in dContent.items():
        sModel = sModel.replace("$%s$" % key, value)
    return sModel

sBody = ["<p><a href=\"{0}.html\">{0}</a></p>".format(s) for s in files]
dContent = {
    "TITLE": sIndexTitle,
    "CONTENT": "\n".join(sBody),
    "SIZE": str(fontSize)
}

sHtml = renderHtml(sModel, dContent)
# Write page
with open("index.html", "w", encoding="utf-8") as f:
    f.write(sHtml)

# Generate pages
for sF in txtFiles:
    sTitle = os.path.basename(sF).replace(".txt", "")
    print(sTitle)
    # Read content
    with open(sF, encoding="utf-8") as f:
        sCnt = f.read()
    # Complete scores
    lCnt = sCnt.split("\n")
    i = 0
    sCurrentBlock = ""
    iRep = 1
    dBlocks = {}
    lOut = []
    import re
    while i < len(lCnt):
        bDisplay = True
        z = re.match("^\[([a-zA-Z\s\d]+)\]", lCnt[i])
        if z: # Memorize current block
            sCurrentBlock = z.group(1)
            bFirst = True
            print("Found block {}".format(sCurrentBlock))
            z = re.match("^\[[a-zA-Z\s\d]+\] \(x(\d)\)", lCnt[i])
            iRep = 1
            if z:
                iRep = int(z.group(1))
                print("Repeat block {} times".format(iRep))
            if sCurrentBlock not in dBlocks.keys():
                print("Create block {}".format(sCurrentBlock))
                dBlocks[sCurrentBlock] = [lCnt[i]]
        else:
            if sCurrentBlock != "":
                if lCnt[i] != "":
                    bFirst = False
                    # Record current line in block
                    dBlocks[sCurrentBlock].append(lCnt[i])
                else: # exit from block
                    if bFirst:
                        # Empty block to fill with previous recorded
                        if sCurrentBlock in dBlocks.keys():
                            lOut.pop()
                            bDisplay = False
                            for j in range(iRep):
                                lOut = lOut + dBlocks[sCurrentBlock]
                                lOut.append("")
                                print("Fill empty block {}".format(sCurrentBlock))
                    sCurrentBlock = ""
        if bDisplay: lOut.append(lCnt[i])
        i += 1
    sCnt = ("\n").join(lOut)
    # ^\[[a-zA-Z]*\]$|^\[[a-zA-Z]*\] \(x\d\)
    # Compute font size
    maxLen = len(max(sCnt.split("\n"), key=len))
    print("Max length:"+str(maxLen))
    fontSize = min(100 / maxLen * 1.7, 3.5)
    # Format content
    sCnt = sCnt.replace("\n", "<br/>\n")
    sCnt = sCnt.replace(" ", "&nbsp;")
    # Inject content in the model

    dContent = {
        "TITLE": sTitle,
        "CONTENT": sCnt,
        "SIZE": str(fontSize)
    }
    sHtml = renderHtml(sModel, dContent)
    # Write page
    with open("{0}.html".format(sTitle), "w", encoding="utf-8") as f:
        f.write(sHtml)

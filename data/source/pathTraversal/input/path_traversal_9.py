#
#

def getFileTypes(fileName):
    if '.png' in fileName or '.jpg' in fileName:
        fileType = 'Image'
    elif '.csv' in fileName:
        fileType = 'CSV'
    elif '.xls' in fileName or '.xlsx' in fileName:
        fileType = 'Excel'
    elif '.txt' in fileName:
        fileType = 'Text'
    else:
        fileType = 'Unidentified'
    return fileType

def getFullFilePath(imFileList, dirName):
    fullFilePath = []
    for fileName in fnmatch.filter(imFileList, '*.*'):
        fullFilePath.append(os.path.join(dirName, fileName))
    return fullFilePath
    
def getCouponName(fileName):
    regex = re.compile("[0-9]{0,}[\\-_][0-9]{0,}[\\-_][0-9]{0,}")
    matchArray = regex.findall(fileName)
    if(matchArray):
        return matchArray[0].replace('_', '-')
    else:
        return ''
        
def getImageAttributes(fileName):
    if '.png' in fileName or '.jpg' in fileName:
        name = fileName.split('.')[0]
        nameTypes = name.split('-')
        series = nameTypes[0]
        panel = nameTypes[1]
        coupon = nameTypes[2]
        attributes = [series, panel, coupon]
        return attributes
    else:
        return []
        
def getSeries(dirName):
    if 'DOE_I/' in dirName or 'DOE_I_' in dirName:
        return 'Series 2'
    elif 'DOE_II/' in dirName or 'DOE_II_' in dirName:
        return 'Series 6'
    elif 'DOE_IV/' in dirName or 'DOE_IV_' in dirName:
        return 'Series 10'

def setNamesOfFilesinParamsTTl(pathOfParamTTl, nameOfParamTTl, nameOfCSV, nameOfResultTTl):
    regexCSV = re.compile("^[ \t]*[p][r][o][v][:]+[0-9A-Za-z ]+[<]+[0-9A-Za-z]+[.][0-9A-Za-z]+[>][ ]*[;]")
    regexTTL = re.compile("^[ \t]*[<][ 0-9A-Za-z]+[.][t][t][l][>][ ]*[a][ ]*[p][v][:][0-9A-Za-z ]+[;]")
    replacementStringCSV = "prov:used <"+nameOfCSV+">;"
    replacementStringTTL = "<"+nameOfResultTTl+"> a pv:File;"
    results = os.path.join(os.path.dirname(__file__), "Results", nameOfParamTTl)
    fp = open(pathOfParamTTl, "r")
    lines = fp.readlines()
    toWrite = ''
    l = []
    for line in lines:
        try:
            matchArrayCSV = regexCSV.findall(line.strip())
            if(matchArrayCSV[0] in line):
                line = replacementStringCSV
        except:
            pass
        try:
            matchArrayTTL = regexTTL.findall(line.strip())
            if(matchArrayTTL[0] in line):
                line = replacementStringTTL
        except:
            pass
        toWrite = toWrite.rstrip() + line.rstrip()
        l.append(line.rstrip())
        l.append("\n")
    fp.close()
    fp = open(results, "w+")
    for i in l:
        fp.write(i)
    fp.close()

def invokeSetlr(rawArchiveParam, rawArchiveDomainparam, instanceLevelDomainParam):
    os.chdir(os.path.join(os.path.dirname(__file__), "Results"))
    setlr.mainFunc("setlr_params.ttl")
    setlr.mainFunc("setlr_params_domain.ttl")
    setlr.mainFunc("setlr_params_instancelevel.ttl")

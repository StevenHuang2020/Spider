#python3 steven
import os

def pathsFileFolders(dir, subFolder=False): #Traverse the folders under the path
    for dirpath, dirnames, filenames in os.walk(dir):
        dirnames.sort()
        #print(dirnames)
        for dirName in dirnames:
            yield os.path.join(dirpath, dirName) #dirpath+'\\'+filename
        if not subFolder:
            break
            
def pathsFiles(dir, filter='', subFolder=False): #Traverse the files under the path
    #filter: cpp h txt jpg
    def getExtFile(file):
        return file[file.find('.')+1:]
    
    def getFmtFile(path):
        #/home/User/Desktop/file.txt    /home/User/Desktop/file     .txt
        root_ext = os.path.splitext(path) 
        return root_ext[1]

    fmts = filter.split()  
    #print('pathsFiles().......')  
    if fmts:
        for dirpath, dirnames, filenames in os.walk(dir):
            filenames.sort()
            #print(filenames)
            for filename in filenames:
                if getExtFile(getFmtFile(filename)) in fmts:
                    yield os.path.join(dirpath, filename) #dirpath+'\\'+filename
            if not subFolder:
                break
    else:
        for dirpath, dirnames, filenames in os.walk(dir):
            filenames.sort()
            for filename in filenames:
                yield os.path.join(dirpath, filename) #dirpath+'\\'+filename  
            if not subFolder:
                break    

def deleteFile(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)        

def createPath(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)

def deleteFolder(file_path):
    if os.path.exists(file_path):
        #shutil.rmtree(file_path)
        for lists in os.listdir(file_path):
            f = os.path.join(file_path, lists)
            if os.path.isfile(f):
                os.remove(f)
                       
def getFileName(path):  
    return os.path.basename(path)
   
def getFileNameNo(path):
    base=os.path.basename(path)
    return os.path.splitext(base)[0]
 
import os
import random
import subprocess
import time

########################################inputfiles#######################################################
def inputfiles(folderPathString):
    f1 = open (folderPathString+"/FileNames.txt", "r")
    link_filenames = f1.read ()
    filenames = link_filenames.split ("\t")
    f1.close ()

    f2 = open (folderPathString+"/FilePathNames.txt", "r")
    filepathnames = []
    while 1:
        link_filepathnames = f2.readline ()
        if link_filepathnames == "":
            break
        temp_filepathnames = link_filepathnames.split ("\t")
        temp_filepathnames[1] = temp_filepathnames[1][:-1] + temp_filepathnames[2][1:]
        del (temp_filepathnames[2])
        temp_filepathnames[2] = temp_filepathnames[2][:-1]
        filepathnames.append (temp_filepathnames)
    f2.close ()
    filepathnames[len (filepathnames) - 1][2] = filepathnames[len (filepathnames) - 1][2] + \
                                                filepathnames[len (filepathnames) - 2][2][-1]
    
        
    del link_filenames
    del link_filepathnames
    del temp_filepathnames
    
    size = len (filenames)
    callMatrix = [[0 for i in range (size)] for i in range (size)]  
    f3 = open (folderPathString+"/CDG.txt", "r")

    for i in range(size):
        link_CDG = f3.readline ()     
        if link_CDG == "":
            break
        
        k = 0
        for j in range(len(link_CDG)):
            if link_CDG[j] == '1':
                callMatrix[i][k] = 1
                k = k + 1
            
            elif link_CDG[j] == '0':
                k = k + 1
    
    del link_CDG        
            
    return filenames, filepathnames, callMatrix


########################################motagharen#######################################################
def motagharen(callMatrix):
    tempMatrix = [[0 for i in range (len (callMatrix))] for i in range (len (callMatrix))]
    i = 0
    while i < len (callMatrix):
        j = 0
        while j < len (callMatrix):
            if i != j:
                tempMatrix[j][i] = callMatrix[i][j]
            j = j + 1
        i = i + 1

    i = 0
    while i < len (callMatrix):
        j = 0
        while j < len (callMatrix):
            tempMatrix[i][j] = callMatrix[i][j] + tempMatrix[i][j]
            j = j + 1
        i = i + 1
    return tempMatrix

########################################shortestPathFloydWarshall#######################################################
def shortestPathFloydWarshall(callMatrix):
    inf = 100    
    pathMatrix = [[0 for i in range (len (callMatrix))] for i in range (len (callMatrix))]
    tempCallMatrix = [[0 for i in range (len (callMatrix))] for i in range (len (callMatrix))]
    v = len (callMatrix)

    for i in range (0, v):
        for j in range (0, v):
            tempCallMatrix[i][j] = callMatrix[i][j]
   
    for i in range (0, v):
        for j in range (0, v):
            pathMatrix[i][j] = i
            if i != j and tempCallMatrix[i][j] == 0:
                pathMatrix[i][j] = -1
                tempCallMatrix[i][j] = inf  # set zeros to any large number which is bigger then the longest way

    for k in range (0, v):
        for i in range (0, v):
            for j in range (0, v):
                if tempCallMatrix[i][j] > tempCallMatrix[i][k] + tempCallMatrix[k][j]:
                    tempCallMatrix[i][j] = tempCallMatrix[i][k] + tempCallMatrix[k][j]
                    pathMatrix[i][j] = pathMatrix[k][j]

    for i in range (0, v):
        tempCallMatrix[i][i] = 0 #faseleye har raas ba khodash = 0
    
    for i in range (0, v): #set 0 to array[i][j] that is no path between them 
        for j in range (0, v):
             if i != j and tempCallMatrix[i][j] == inf:
                 tempCallMatrix[i][j] = 0 
                 
    return pathMatrix, tempCallMatrix
    
    
########################################createSimilarityMatrix#######################################################
def createSimilarityMatrix(shortestCallMatrix):
    tempMatrix = [[0 for i in range (len (shortestCallMatrix))] for i in range (len (shortestCallMatrix))]
    v = len (tempMatrix)
    
    maximum = -1    
    for i in range(0,v):
        max_temp = max(shortestCallMatrix[i])
        if maximum < max_temp:
            maximum = max_temp

    if maximum == 0:
        print("all classes are in its own cluster!")
        exit()
    
    for i in range (0, v):
        for j in range (0, v):
            if shortestCallMatrix[i][j] == 0 and i !=j:
                tempMatrix[i][j] = maximum
            else:
                tempMatrix[i][j] = shortestCallMatrix[i][j]
        
    for i in range (0,v):
        for j in range (0, v):
            tempMatrix[i][j] = 1 - tempMatrix[i][j]/maximum
    return tempMatrix


########################################input####################################################### 
def input_k():
    k = int(input ("Please input #Clusters:  "))
    return k
  

########################################initializing#######################################################
def initializing(k , n, similarityMatrix):
    
    centers = generateRandomCenter(k, n)
    #print(centers)    
    
    clusters = fillClustersBasedOnCenter(k, n, similarityMatrix, centers)
    
    return clusters

########################################generateRandomCenter#######################################################
def fillClustersBasedOnCenter(k, n, similarityMatrix, centers):
    
    for i in range(n): # initialize base step, center of a cluster remains in index 0 of each list
        index = 0
        clusterNumber = centers[0][0]
        tempMax = similarityMatrix[i][clusterNumber]
        for j in range(1,k):
            clusterNumber = centers[j][0]
            if tempMax < similarityMatrix[i][clusterNumber]:
                tempMax = similarityMatrix[i][clusterNumber]
                index = j

        temp = []
        temp = centers[index]
        if i != temp[0]:
            temp.append(i)
            
        centers.pop(index)  
        centers.insert(index,temp)  
        #print("i:", i, "index:", index, "sim:", tempMax, "centers:", centers)
    return centers


########################################generateRandomCenter#######################################################
def generateRandomCenter(k, n):
    clusters = []
    
    center = random.sample(range(n), k) #create k random center of k-means
    #print(center)
    
    for j in range(k):  #transform k centers to 2 dimentionals array
        c = center.pop(0)  
        clusters.append([c])

    del(center) 
    #print(clusters)
    return clusters
    
########################################copy#######################################################
def copy(matrix):
    l = len(matrix)
    temp = []

    for i in range(0,l):
        temp.append([])
        m = len(matrix[i])
        for j in range(0,m):
            temp[i].append(matrix[i][j])
    return temp
    
########################################correctCenter#######################################################   
def correctCenter(clusters, similarityMatrix):
    clustersUpdateCenter = []
    for counter in range(k):
        tempClusters = copy(clusters)
        temp = tempClusters.pop(counter)
        #print("temp:", temp)
        
        
        sameSimIndex = [0]
        tempMax = 0
        
        for i in range(0, len(temp)):
            
            sumSimilarity = 0    
            for j in range(0, len(temp)):
                sumSimilarity = sumSimilarity + similarityMatrix[temp[i]][temp[j]]
            #print(temp[i], ":" , sumSimilarity)
            if sumSimilarity > tempMax:
                tempMax = sumSimilarity
                sameSimIndex.clear()        
                sameSimIndex.append(i)
            elif sumSimilarity == tempMax:
                sameSimIndex.append(i)
        
        #print("sameSimIndex: ", sameSimIndex, "tempMax: ",tempMax)
        
        if len(sameSimIndex) == 1:
            val = temp[sameSimIndex[0]]
        #    print(temp)    
            temp.remove(val) 
        #    print(temp)
            temp.insert(0, val)
        #    print(temp)    
            clustersUpdateCenter.append(temp)
        #    print("OK, clustersUpdateCenter: ",clustersUpdateCenter,"\n")
        
        elif len(sameSimIndex) > 1:
            tempMinOtherSim = n    
            for i in range(len(sameSimIndex)):
                sumOtherSimilarity = 0       
                val = temp[sameSimIndex[i]]
                for j in range(k-1):
                    for m in range(len(tempClusters[j])):
                        sumOtherSimilarity = sumOtherSimilarity + similarityMatrix[val][tempClusters[j][m]]
                #print("val:" ,val, "sumOtherSimilarity:",sumOtherSimilarity)
                if tempMinOtherSim > sumOtherSimilarity:
                    tempMinOtherSim = sumOtherSimilarity
                    tempVal = val
            #print("tempVal:", tempVal)
            temp.remove(tempVal)
            temp.insert(0, tempVal)
            clustersUpdateCenter.append(temp)
            #print("NOK, clustersUpdateCenter: ",clustersUpdateCenter,"\n")
    return clustersUpdateCenter

################################################computeSimilarityFunction################################################
def computeSimilarityFunction(matrix , similarityMatrix):#sum of similarity of all clusters 
    function = 0
    for i in range(k):
        for j in range(1, len(matrix[i])):
            function = function + similarityMatrix[matrix[i][0]][matrix[i][j]]
    return function

################################################clustering################################################
def clustering(k, n, similarityMatrix, clustersUpdateCenter):
    
    clusterOld = copy(clustersUpdateCenter) 

    iteration = 0
    flag = 0

    while iteration <1000 and flag < 5:

        iteration = iteration + 1
        clusterNew = []
        
    #    print("old:", id(clusterOld), "new:", id(clusterNew) , "d:", id(clusterOld)-id(clusterNew),"\n")    
        
        for i in range(k):
            clusterNew.append([clusterOld[i][0]]) 
        
        #print(centerUpdate)
        clusterNew = fillClustersBasedOnCenter(k, n, similarityMatrix, clusterNew)
#        print("clusterNew: ",clusterNew)
        
    #    similarityFunctionUpdate = computeSimilarityFunction(clusterNew, similarityMatrix)  
    #    print("similarityFunctionUpdate: ",similarityFunctionUpdate,"\n")
        
        
        clusterNew = correctCenter(clusterNew, similarityMatrix)
#        print("clustersUpdateCenter: ",clusterNew)
        
        # similarityFunctionUpdate = computeSimilarityFunction(clusterNew, similarityMatrix)  
#        print("similarityFunctionUpdate: ",similarityFunctionUpdate,"\n")
        
        #check for continuing    
        tempNew = copy(clusterNew)
        tempOld = copy(clusterOld)
    #    print(id(tempNew),id(tempOld),id(clusterNew),id(clusterOld))
        for i in range(len(tempNew)):
            tempNew[i].sort()
        tempNew.sort()   
#        print("Sorted New: ", tempNew)
    
        for i in range(len(tempOld)):
            tempOld[i].sort()
        tempOld.sort()   
#        print("Sorted Old: ", tempOld)
#        print()
        
        if(tempNew == tempOld):
            flag = flag + 1
    
        
        del(tempNew)
        del(tempOld)
    
        clusterOld = copy(clusterNew) 
    
    return clusterNew
   
   
################################################exportingToMoJoFormatAlgorithmManual################################################
def exportingToMoJoFormatAlgorithmManual(k, n, clustersFinal):
    
    for i in range(k):
        clustersFinal[i].sort()
    clustersFinal.sort()
    f1 = open ("MoJoAlgorithmManual.txt", "w")
    for counter in range(k):
        for i in range(len(clustersFinal[counter])):
            f1.write("contain ")
            f1.write("hulu")
            f1.write(str(counter))
            f1.write(" ")
            f1.write(str(clustersFinal[counter][i]))
            f1.write("\n")
    f1.close()
    

################################################exportingToMoJoFormatExpert################################################
def exportingToMoJoFormatExpert(fileNames, filePathNames, folderPathResult):

    temp = []

    for i in range(len(fileNames)):
#        temp[i][1] = fileNames[i]
        indexCluster = findInTofilePtheNames (fileNames[i], filePathNames)
        
        if indexCluster == -1:
            print("Cluster Conflict class ", fileNames[i])
            return
        
#        temp[i][0] = filePathNames[indexCluster][0]
        temp.append([filePathNames[indexCluster][0], fileNames[i]])
    temp.sort()
    f1 = open (folderPathResult + "/MoJoExpert.txt", "w")
    for i in range(len(fileNames)):
        f1.write("contain ")
        f1.write(temp[i][0])
        f1.write(" ")
        f1.write(temp[i][1])
        f1.write("\n")
    f1.close()
    del(temp)
    

    
################################################findInTofilePtheNames################################################
def findInTofilePtheNames (className, filePathNames):
    index = -1
    for i in range(len(filePathNames)):
        if className == filePathNames[i][1] or className == filePathNames[i][2]:
            if index == -1:
                index = i
            else:
                return -1
    return index
        

################################################findInTofilePtheNames################################################
def exportingToMoJoFormatAlgorithm(k, n, clustersFinal, fileNames, filePathNames, run_no, folderPathResult):
    f1 = open (folderPathResult + "/MoJoAlgorithm" + str(k) + "_" + str(run_no) + ".txt" , "w")
    for counter in range(k):
        for i in range(len(clustersFinal[counter])):
            f1.write("contain ")
            f1.write("hulu")
            f1.write(str(counter))
            f1.write(" ")
            f1.write(fileNames[clustersFinal[counter][i]])
            f1.write("\n")
    f1.close()
    

################################################Start################################################
pathString = []
pathString.append("Case Studies/accessible")
pathString.append("Case Studies/browser")
pathString.append("Case Studies/build")
pathString.append("Case Studies/content")
pathString.append("Case Studies/db")
pathString.append("Case Studies/dom")
pathString.append("Case Studies/extensions")
pathString.append("Case Studies/gfx")
pathString.append("Case Studies/intl")
pathString.append("Case Studies/ipc")

if not os.path.isdir("result"):
    os.mkdir("result")

pathResultString = []
pathResultString.append("result/accessible")
pathResultString.append("result/browser")
pathResultString.append("result/build")
pathResultString.append("result/content")
pathResultString.append("result/db")
pathResultString.append("result/dom")
pathResultString.append("result/extensions")
pathResultString.append("result/gfx")
pathResultString.append("result/intl")
pathResultString.append("result/ipc")

for i in range (len(pathResultString)):
    if not os.path.isdir(pathResultString[i]):
        os.mkdir(pathResultString[i])


for folderNumber in range (0,len(pathString)):
        
    timeInit = 0
    timeClustering = 0
    timeTotal = 0

    fileNames, filePathNames, callMatrix = inputfiles (pathString[folderNumber])
    print("\n\n" + pathString[folderNumber]+":\tinput files completed :)")

    exportingToMoJoFormatExpert(fileNames, filePathNames, pathResultString[folderNumber])
    print(pathString[folderNumber]+":\texporting to MoJo format for expert completed :)")

    time1 = time.time()
    callMatrixMotaghren = motagharen (callMatrix)
    time2 = time.time()
    timeInit = time2 - time1
    print(pathString[folderNumber]+":\tgenerating call matrix to symmetric completed :)")

    #callMatrixMotaghren=[[0,3,5,0],[2,0,4,0],[6,1,0,0],[0,0,3,0]]
    #callMatrixMotaghren = [[0,1,1,1,0,0,0,0],[1,0,0,1,0,0,0,0],[1,0,0,0,1,0,0,0],[1,1,0,0,0,0,0,0],[0,0,1,0,0,1,0,0],[0,0,0,0,1,0,1,1],[0,0,0,0,0,1,0,1],[0,0,0,0,0,1,1,0]]
    #callMatrixMotaghren = [[1,1,0,1,0,0,0,0,0,0,0,0],[1,1,0,1,1,0,0,0,0,0,0,0],[0,0,1,0,1,1,1,0,0,1,0,0],[1,1,0,1,0,0,1,1,0,0,0,0],[0,1,1,0,1,1,0,1,1,1,0,0],[0,0,1,0,1,1,0,0,0,1,0,0],[0,0,1,1,0,0,1,0,0,0,0,0],[0,0,0,1,1,0,0,1,1,0,0,0],[0,0,0,0,1,0,0,1,1,0,0,0],[0,0,1,0,1,1,0,0,0,1,1,0],[0,0,0,0,0,0,0,0,0,1,1,1],[0,0,0,0,0,0,0,0,0,0,1,1]]
    #callMatrixMotaghren = [[1,1,1,1,0,0,0,0],[1,1,1,1,1,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[0,1,0,0,1,1,1,1],[0,0,0,0,1,1,1,1],[0,0,0,0,1,1,1,1],[0,0,0,0,1,1,1,1]]
    #callMatrixMotaghren = [[1,1,1,1,1,1,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1],[0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1],[0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1],[0,0,0,0,0,1,1,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1]]
    #print(callMatrixMotaghren)

    time1 = time.time()
    shortestPathMatrix, shortestCallMatrix = shortestPathFloydWarshall (callMatrixMotaghren)
    time2 = time.time()
    timeInit = timeInit + time2 - time1
    print(pathString[folderNumber]+":\tcalculating shortest path matrix completed :)")

    #print (shortestCallMatrix)
    #print (shortestPathMatrix)

    time1 = time.time()
    similarityMatrix = createSimilarityMatrix(shortestCallMatrix)
    time2 = time.time()
    timeInit = timeInit + time2 - time1
    print(pathString[folderNumber]+":\tforming similarity completed :)")

    #print(similarityMatrix)

    n = len(callMatrixMotaghren) # number of elements
    result = []
    maxRunNo = 30
    maxK = int(min (int(n/3) , 100))

    for run_no in range (1,maxRunNo+1):
        for k in range (2,maxK + 1):

            time1 = time.time()
            clustersInit = initializing(k , n, similarityMatrix)
        #    print("After initializing:\nclusters: ",clustersInit)
            # print("initializing culsters completed :)")
            
            
            # similarityFunction = computeSimilarityFunction(clustersInit, similarityMatrix)  
        #    print("similarityFunction:",similarityFunction,"\n")
            
                        
            clustersUpdateCenter = correctCenter(clustersInit, similarityMatrix)
        #    print("clustersUpdateCenter: ",clustersUpdateCenter)
            
            # similarityFunctionUpdate = computeSimilarityFunction(clustersUpdateCenter, similarityMatrix)  
        #    print("similarityFunctionUpdate: ",similarityFunctionUpdate)
                    
            clustersFinal = clustering(k, n, similarityMatrix, clustersUpdateCenter)
            time2 = time.time()
            timeClustering = time2 - time1

            timeTotal = timeInit + timeClustering

            print("\n" + pathString[folderNumber]+ ":\tclustering completed at k = " + str(k)+ " and in run = " + str(run_no) + " :)")
            
            #exportingToMoJoFormatAlgorithmManual(k, n, clustersFinal)
            #print("exporting to MoJo format algorithm manually completed :)")
            
            exportingToMoJoFormatAlgorithm(k, n, clustersFinal, fileNames, filePathNames, run_no, pathResultString[folderNumber])
            # print("exporting to MoJo format algorithm completed :)")

            MoJoAlgorithmString = pathResultString[folderNumber] + "/MoJoAlgorithm"+ str(k) +"_"+str(run_no) +".txt"
            proc = subprocess.Popen(["java", "mojo/MoJo", MoJoAlgorithmString , pathResultString[folderNumber] + "/MoJoExpert.txt"], stdout=subprocess.PIPE)
            outs, errs = proc.communicate()
            mojoMeasure =  int(outs[:-1])
            # print(mojoMeasure)
            proc = subprocess.Popen(["java", "mojo/MoJo", MoJoAlgorithmString ,  pathResultString[folderNumber] + "/MoJoExpert.txt","-fm"], stdout=subprocess.PIPE)
            outs, errs = proc.communicate()
            mojoFmMeasure =  float(outs[:-1])
            # print(mojoFmMeasure)
            result.append([run_no,k,mojoMeasure,mojoFmMeasure,timeInit,timeClustering,timeTotal])
    # print(result)

    outputFileResult = open (pathResultString[folderNumber] + "/result.txt", "w")

    outputFileResult.write("RunNO"+"\t"+"K"+"\t"+"MoJo"+"\t"+"MoJo fm"+"\t"+"Time Init"+"\t"+"Time Clustering"+"\t"+"Time Total"+"\n")
    for i in range (0, maxRunNo * (maxK-1)):
        outputFileResult.write(str(result[i][0])+"\t"+str(result[i][1])+"\t"+str(result[i][2])+"\t"+str(result[i][3])+"\t"+str(result[i][4])+"\t"+str(result[i][5])+"\t"+str(result[i][6])+"\n")

    outputFileResult.close()

    del fileNames
    del filePathNames
    del callMatrix
    del callMatrixMotaghren
    del similarityMatrix
    del shortestCallMatrix
    del shortestPathMatrix
    del clustersFinal
    del clustersInit
    del clustersUpdateCenter

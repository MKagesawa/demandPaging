import sys

machineSize = sys.argv[1]
pageSize = sys.argv[2]
processSize = sys.argv[3]
jobMix = sys.argv[4]
numRef = sys.argv[5]
replacementAlgo = sys.argv[6]
debugLevel = sys.argv[7]

randomNumbers = None
with open("random-numbers.txt") as f:
    randomNumbers = f.readlines()

counter = 0
def randomOS(counter):
    num = int(randomNumbers[int(counter)])
    if debugLevel == "11":
        print(int(randomNumbers[int(counter)]))
    return num


class Process:
    def __init__(self, processSize, processNum):
        self.processSize = processSize
        self.numFault = 0
        self.numEvict = 0
        self.resTime = 0
        self.nextRef = (111 * processNum) % processSize

    def nextRef(self, A, B, C):
        global counter
        randomNum = randomOS(counter)
        counter += 1
        ratio = randomNum / 2147483648
        if ratio < A:
            self.nextRef = (self.nextRef + 1) % self.processSize
        elif ratio < A + B:
            self.nextRef = (self.nextRef -5 + self.processSize) % self.processSize
        elif ratio < A + B + C:
            self.nextRef = (self.nextRef + 4) % self.processSize
        else:
            self.nextRef = randomNum % self.processSize
            counter += 1


class FrameTable:
    def __init__(self, frameNum, type):
        self.frameNum = frameNum
        self.type = type
        self.table = []
        for i in range(4):
            self.table.append([])

    def hasFault(self, pageNum, processNum, time):
        hasF = True
        for page in self.table:
            if page[0] == pageNum and page[1] == processNum:
                if self.type == "lru":
                    page[2] = time
                hasF = False

        return hasF

    def replace(self, plist, pageNum, processNum, time):
        if self.type == "fifo":
            fifoIndex = -1

            for i in range(len(self.table)):
                if self.table[i][0] == 0 and self.table[i][1] == 0:
                    fifoIndex = i
                    break

            if fifoIndex == -1:
                evictedF = self.table[0]
                evictedP = plist[evictedF[1] - 1]
                resTime = time - evictedF[2]
                evictedP.numEvict += 1
                evictedP.resTime += resTime
                temp = []
                for i in range(len(self.table)):
                    temp.append([])
                for i in range(len(self.table)-1):
                    temp[i] = self.table[i + 1]
                self.table = temp
                fifoIndex = len(self.table) - 1

            self.table[fifoIndex] = [pageNum, processNum, time, time]

        else:
            LRUTime = time
            evictedF = 0

            for i in range(self.frameNum - 1, -1, -1): #check
                if self.table[i][0] == 0 and self.table[i][1] == 0:
                    self.table[i] = [pageNum, processNum, time, time]
                    return
                elif self.type == "lru" and LRUTime > self.time[i][2]:
                    evictedF = i
                    LRUTime = self.table[i][2]

            evictedP = None
            resTime = None
            if self.type == "lru":
                evictedP = plist[self.table[evictedF][1] - 1]
                resTime = time - self.table[evictedF][3]
            else:
                global counter
                evictedF = randomOS(counter) % self.frameNum
                evictedP = plist[self.table[evictedF][1] - 1]
                resTime = time - self.table[evictedF][2]

            evictedP.numEvict += 1
            evictedP.resTime += resTime

            self.table[evictedF] = [pageNum, processNum, time, time]


def main():
    global machineSize
    global pageSize
    global processSize
    global jobMix
    global numRef
    global replacementAlgo
    global debugLevel

    print("The machine size is " + machineSize + ".")
    print("The page size is " + pageSize + ".")
    print("The process size size is " + processSize + ".")
    print("The job mix number is " + jobMix + ".")
    print("The number of references per process is " + numRef + ".")
    print("The replacement algorithm is " + replacementAlgo + ".")
    print("The level of debugging output is " + debugLevel + ".")

    quantum = 3
    totalFault = 0
    totalEvict = 0
    totalRes = 0
    A = []
    B = []
    C = []
    maxIteration = numRef / quantum
    frameNum = machineSize / pageSize
    frameTable = FrameTable(frameNum, replacementAlgo)

    if jobMix == 1:
        plist = []
        plist[0] = Process(processSize, 1)
        for i in range(numRef):
            pageNumber = plist[0].nextRef / pageSize
            if frameTable.hasFault(pageNumber, 1, i+1):
                frameTable.replace(plist, pageNumber, 1, i+1)
                plist[0].numFault += 1

            plist[0].nextRef(1, 0, 0)
    else:
        plist = []
        for i in range(4):
            plist.append([])
            plist[i] = Process(processSize, i+1)

        if jobMix == 2:
            A = [1, 1, 1, 1]
            B = [0, 0, 0, 0]
            C = [0, 0, 0, 0]

        elif jobMix == 3:
            A = [0, 0, 0, 0]
            B = [0, 0, 0, 0]
            C = [0, 0, 0, 0]

        elif jobMix == 4:
            A = [0.75, 0.75, 0.75, 0.5]
            B = [0.25, 0, 0.125, 0.125]
            C = [0, 0.25, 0.125, 0.125]

        for i in range(maxIteration + 1): #check
            for j in range(4):
                count = None
                if i == maxIteration:
                    count = numRef % quantum
                else:
                    count = quantum
                for k in range(counter):
                    pageNumber = plist[j].nextRef / pageSize
                    time = (quantum * i * 4) + k + 1 + (j * counter)
                    if frameTable.hasFault(pageNumber, j+1, time):
                        frameTable.replace(plist, pageNumber, j + 1, time)
                        plist[j].numFault += 1
                    plist[j].nextRef(A[j], B[j], C[j])

    indexTrack = 1

    for p in plist:
        if p.numEvict == 0:
            print("Process ", indexTrack, " had ", p.numFault, " faults.")
            print("\tWith no evictions, the average residence is undefined.")
        else:
            print("Process ", indexTrack, " had ", p.numFault, " faults and ", p.resTime/p.numEvict, " average residency.")

        totalFault += p.numFault
        totalRes += p.resTime
        totalEvict += p.numEvict
        indexTrack += 1

    if totalEvict == 0:
        print("The total number of faults is ", totalFault, ".")
        print("\tWith no evictions, the overall average residency is undefined.")
    else:
        print("The total number of faults is ", totalFault, " and the overall average residency is ", totalRes/totalEvict, ".")


main()

































import sys

#M
machineSize = int(sys.argv[1])
#P
pageSize = int(sys.argv[2])
#S
processSize = int(sys.argv[3])
#J
jobMix = int(sys.argv[4])
#N
numRef = int(sys.argv[5])
#R
replacementAlgo = sys.argv[6]

debugLevel = int(sys.argv[7])

randomNumbers = None
with open("random-numbers.txt") as f:
    randomNumbers = f.readlines()

# a global counter to keep track of index of random number from txt file
counter = 0
def randomOS(counter):
    num = int(randomNumbers[int(counter)])
    if debugLevel == "11":
        print(int(randomNumbers[int(counter)]))
    return num


class Process:
    def __init__(self, processSize, processNum):
        self.processSize = int(processSize)
        self.numFault = 0
        self.numEvict = 0
        # residence time
        self.resTime = 0
        # given on instruction
        self.nextRef = int((111 * processNum) % processSize)

    def nRef(self, A, B, C):
        global counter
        randomNum = randomOS(counter)
        counter += 1
        ratio = randomNum / 2147483648
        if ratio < A:
            self.nextRef = int((self.nextRef + 1) % self.processSize)
        elif ratio < A + B:
            self.nextRef = int((self.nextRef -5 + self.processSize) % self.processSize)
        elif ratio < A + B + C:
            self.nextRef = int((self.nextRef + 4) % self.processSize)
        else:
            self.nextRef = int(randomNum % self.processSize)
            counter += 1


class FrameTable:
    def __init__(self, frameNum, type):
        self.frameNum = frameNum
        # algorithm type being used
        self.type = type
        self.table = []
        for i in range(int(frameNum)):
            self.table.append([])
        for p in self.table:
            p.append(0)
            p.append(0)
            p.append(0)
            p.append(0)

    # check page fault
    def hasFault(self, pageNum, processNum, time):
        hasF = True
        for page in self.table:
            # if page demand is in the table, then there's no fault
            if page[0] == pageNum and page[1] == processNum:
                if self.type == "lru":
                    page[2] = time
                hasF = False

        return hasF

    def replace(self, plist, pageNum, processNum, time):
        if self.type == "fifo":
            # find empty frames
            emptyFrames = -1

            for i in range(len(self.table)):
                if self.table[i][0] == 0 and self.table[i][1] == 0:
                    # store the empty frame
                    emptyFrames = i
                    break

            # evict if there's no empty frame
            if emptyFrames == -1:
                evictedFrame = self.table[0]
                evictedProcess = plist[int(evictedFrame[1]) - 1]
                resTime = int(time - evictedFrame[2])
                evictedProcess.numEvict += 1
                evictedProcess.resTime += resTime
                # hold previous values
                temp = []
                for i in range(len(self.table)):
                    temp.append([])
                for i in range(len(self.table)-1):
                    temp[i] = self.table[i + 1]
                # remove just the first frame
                self.table = temp
                emptyFrames = len(self.table) - 1

            # add new values
            self.table[emptyFrames] = [pageNum, processNum, time, time]

        else:
            LRUTime = int(time)
            evictedFrame = 0
            # check for frames not used, starting from highest address
            for i in range(int(self.frameNum) - 1, -1, -1):
                if self.table[i][0] == 0 and self.table[i][1] == 0:
                    # empty frame found
                    self.table[i] = [pageNum, processNum, time, time]
                    return
                elif self.type == "lru" and LRUTime > self.table[i][2]:
                    # index of evicted frame
                    evictedFrame = i
                    LRUTime = self.table[i][2]

            evictedProcess = None
            resTime = None
            if self.type == "lru":
                evictedProcess = plist[self.table[evictedFrame][1] - 1]
                resTime = time - self.table[evictedFrame][3]
            else:
                global counter
                evictedFrame = int(randomOS(counter) % int(self.frameNum))
                counter += 1
                evictedProcess = plist[self.table[int(evictedFrame)][1] - 1]
                resTime = time - self.table[evictedFrame][2]

            evictedProcess.numEvict += 1
            evictedProcess.resTime += resTime

            # add replacement to the evicted frame
            self.table[evictedFrame] = [pageNum, processNum, time, time]


def main():
    global machineSize
    global pageSize
    global processSize
    global jobMix
    global numRef
    global replacementAlgo
    global debugLevel

    print("The machine size is " + str(machineSize) + ".")
    print("The page size is " + str(pageSize) + ".")
    print("The process size size is " + str(processSize) + ".")
    print("The job mix number is " + str(jobMix) + ".")
    print("The number of references per process is " + str(numRef) + ".")
    print("The replacement algorithm is " + str(replacementAlgo) + ".")
    print("The level of debugging output is " + str(debugLevel) + ".")

    quantum = 3
    totalFault = 0
    totalEvict = 0
    totalRes = 0
    A = []
    B = []
    C = []
    maxIteration = int(int(numRef) / int(quantum))
    frameNum = int(machineSize / pageSize)
    frameTable = FrameTable(frameNum, replacementAlgo)

    if jobMix == 1:
        plist = []
        plist.append(Process(processSize, 1))
        for i in range(numRef):
            pageNumber = int(plist[0].nextRef / pageSize)
            if frameTable.hasFault(pageNumber, 1, i+1):
                frameTable.replace(plist, pageNumber, 1, i+1)
                plist[0].numFault += 1
            plist[0].nRef(1, 0, 0)
    else:
        plist = []
        for i in range(4):
            plist.append([])
            plist[i] = Process(processSize, i+1)

        # given values in the instruction
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

        count = None
        for i in range(maxIteration + 1):
            for j in range(4):
                # check for final iteration
                if i == maxIteration:
                    count = numRef % quantum
                else:
                    count = quantum
                for k in range(count):
                    pageNumber = int(plist[j].nextRef / pageSize)
                    time = (quantum * i * 4) + k + 1 + (j * count)
                    if frameTable.hasFault(pageNumber, j+1, time):
                        frameTable.replace(plist, pageNumber, j + 1, time)
                        plist[j].numFault += 1
                    plist[j].nRef(A[j], B[j], C[j])

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

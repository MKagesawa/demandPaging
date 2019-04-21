import sys

machineSize = sys.argv[1]
pageSize = sys.argv[2]
processSize = sys.argv[3]
jobMix = sys.argv[4]
numRef = sys.argv[5]
replacementAlgo = sys.argv[6]
debugLevel = sys.argv[7]

print("The machine size is " + machineSize + ".")
print("The page size is " + pageSize + ".")
print("The process size size is " + processSize + ".")
print("The job mix number is " + jobMix + ".")
print("The number of references per process is " + numRef + ".")
print("The replacement algorithm is " + replacementAlgo + ".")
print("The level of debugging output is " + debugLevel + ".")

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
            self.nextRef = (self.nextRef + 1) % processSize
        elif ratio < A + B:
            self.nextRef = (self.nextRef -5 + processSize) % processSize
        elif ratio < A + B + C:
            self.nextRef = (self.nextRef + 4) % processSize
        else:
            self.nextRef = randomNum % processSize
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






































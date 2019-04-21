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



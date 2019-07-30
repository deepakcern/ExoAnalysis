import os
import sys


os.system('condor_q dkumar > mycondorJobs.txt')

f=open('mycondorJobs.txt', 'r')

for line in f:
    if 'query' in line:
        #print (line.split())
        totalJobs=line.split()[3]
        idle=line.split()[9]
        run=line.split()[11]
        held=line.split()[-4]

print "\n"
print "===========Status of your jobs============"+'\n'
print "TotalJobs: ",totalJobs
print "Idle:      ",idle
print "Running:   ",run
print "Held:      ",held
print "\n"
f.close()
os.system('rm -rf mycondorJobs.txt')
print "Thanks for using this script "
print "\n"

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
os.system('rm -rf mycondorJobs.txt')
#print "Thanks for using this script; We are sending status upadte to the email in some interval "
print "\n"

fout=open('SendEmail.txt','w')

fout.write("=====Status of condor jobs======"+'\n')
fout.write("TotalJobs: "+str(totalJobs)+'\n')
fout.write("Idle:      "+str(idle)+'\n')
fout.write("Running:   "+str(run)+'\n')
fout.write("Held:      "+str(held)+'\n')
#fout.write('\n'+'\n'+'\n')
#fout.write('Regards,'+'\n')
#fout.write('Deepak Kumar')

fout.close()
os.system('mail -s '+' "Status of condorJobs" '+' dpv0011@gmail.com < SendEmail.txt')
#os.system('rm -rf SendEmail.txt')
f.close()

if int (totalJobs) ==0 and int (run) ==0:
	fout2=open('stop.txt','w')
	fout2.write("=====Status of condor jobs======"+'\n')
	fout2.write("All Jobs have been finished"+'\n')
	fout2.write('\n'+'\n'+'\n')
	fout2.write("Regards,"+'\n')
	fout2.write("Deepak Kumar")
	fout2.close()
	fout3=open('StopRun.txt','w')
        fout3.close()
	os.system('mail -s '+' "Finished condorJobs" '+' dpv0011@gmail.com < stop.txt')

	os.system('rm -rf SendEmail.txt stop.txt')
print "Thanks for using this script; We have emailed upadte "



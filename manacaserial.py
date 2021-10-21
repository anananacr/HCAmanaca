import subprocess as sub
import numpy as np
import os
import sys
import plot_fast
import shuffle
import time
import summary
from progress.bar import ChargingBar
#import ccCalc.py

#Startup message
#ASCII art inspired by Adam at Caltech

print("""Starting MANACÁ SSX data processing
        .-~~-.--.
       :         )
 .~ ~ -.\       /.- ~~ .
 >       `.   .'       <
(         .- -.         )	MANACÁ - SIRIUS
 `- -.-~  `- -'  ~-.- -'
   (        :        )           _ _ .-:
    ~--.    :    .--~        .-~  .-~  }        
        ~-.-^-.-~ \_      .~  .-~   .~
                 \ \'     \ '_ _ -~
                  `.`.    //
         . - ~ ~-.__`.`-.//
     .-~   . - ~  }~ ~ ~-.~-.
   .' .-~      .-~       :/~-.~-./:
  /_~_ _ . - ~                 ~-.~-._
                                   ~-.<
""")

sub.call("beep -f 587 -l 110 -n", shell = True)
inp =input("Insert data directory (test_cccluster/data):")
inp= '../test_cccluster/data/'+inp
sub.call("beep -f 587 -l 110 -n", shell = True)
meudiretorio=input("Insert output directory:")
sub.call("beep -f 587 -l 110 -n", shell = True)
dist=input("Distance based on cc or cell:")  
if dist=="cc":
    sub.call("beep -f 587 -l 110 -n", shell = True)
    points=input("# thresholds between 0 and 1:")
    xmax=0.95
    xmin=0.05
sub.call("beep -f 587 -l 110 -n", shell = True)
on=input("Turn on shuffle mode? y/n:")
shuf=0
if on=="y":
    shuf=1
s=""


files= sub.check_output(("find", inp,"-name","XDS_ASCII.HKL"))

files=files.decode()
lista=[]
listacc=[]

for i in files:
	if i=="\n":
		lista.append(s)
		s=""	
	else:
		s=s[0:]+i
meustring = ''
if dist=='cell':
    meustring += 'ccCalc.py -u -f '+inp+'/*/XDS_ASCII.HKL'
else:
    meustring += 'ccCalc.py -f '+inp+'/*/XDS_ASCII.HKL'
print("----------------------PROCESSING STATUS----------------------\nRunning ccCalc")	
sub.check_output((meustring), shell=True)

cont=1
print("ccCalc finished\n")
if dist=='cell':
    resumo=sub.check_output(("ccCluster.py -i "+dist+"ClusterLog.txt -e"), shell=True)
    f=open("threst.tab","w+")
    f.write(resumo.decode())
    f.close()

    resumo=sub.check_output("sed -n '/flag/ {n;p}' threst.tab", shell=True)
    xmax=round(float(resumo.decode()), 3)

    resumo=sub.check_output("sed -n '/HKL/ {n;p}' threst.tab", shell=True)
    est=round(float(resumo.decode()), 2)


    print("Your max variation is: "+str(xmax))
    sub.call("beep -f 587 -l 110 -n", shell = True)
    points=input("Choose # thresholds between 0 and your max:")
    xmin=0.001
    print("\n")

resumo=sub.check_output(("ccCluster.py -i "+dist+"ClusterLog.txt -e"), shell=True)
f=open("thr_estimated.tab","w+")
f.write(resumo.decode())
f.close()

x=np.linspace(xmin, xmax,int(points)) 
x= np.around(x, decimals=3)
x=list(x)
'''
del(x[11])
del(x[11])
del(x[11])
del(x[11])
del(x[11])
del(x[13])
del(x[13])
'''
f=open("x.tab","w+")
f.write("Threshold\n")
for i in x:
	f.write(str(i)+"\n")
f.close()

f=open("xunit.tab","w+")
f.write("Threshold\n")
for i in x:
	f.write(str(i)+"\n")
f.close()

print("Starting ccCluster")
bar = ChargingBar('Running ccCluster:', max = len(x))
for i in x:
	bar.next()
	sub.check_output(("ccCluster.py", "-i", dist+"ClusterLog.txt", "-t", str(i), "-p"))
	cont+=1
bar.finish()
filescc=sub.check_output(("ls -d cc*/"), shell=True)
filescc=filescc.decode()
home=os.getcwd()
for i in filescc:
	if i=="\n":
		s=home+'/'+s
		listacc.append(s)
		s=""	
	else:
		s=s[0:]+i

point=[]
print('\n')
bar = ChargingBar('Running Pointless:', max = len(listacc))

for i in range(len(listacc)):
    os.chdir(listacc[i])
    f=open("bkeys.dat","w+")
    f.write("HKLIN clustered.mtz\nHKLOUT clustered_aim.mtz\nEND")
    f.close()
    sub.check_output(('cd '+listacc[i]), shell=True)
    f=open("pointless.log","w+")
    sub.check_output('chmod +x launch_pointless.sh', shell=True)	
    result=sub.check_output('./launch_pointless.sh', shell=True)
    bar.next()    
    f.write(result.decode())
    f.close()
    f=open("check_cc.tab","w+")
    resumo=sub.check_output('grep -B7 -A22 "Best Solution:" pointless.log', shell=True)
    f.write(resumo.decode())
    f.close()
    sub.check_output('cd ..', shell=True)
bar.finish()

os.chdir(home)
f=open("check.tab", "w+")
resumo=sub.check_output('grep -B7 -A22 "Best Solution:" cc*/pointless.log', shell=True)
f.write(resumo.decode())
f.close()

print('\n')
bar = ChargingBar('Running Aimless:', max = len(listacc))

for i in range(len(listacc)):
    os.chdir(listacc[i])
    f=open("aimless.log","w+")
    result_aim=sub.check_output('aimless<bkeys.dat', shell=True)
    bar.next()
    f.write(result_aim.decode())
    f.close()
    sub.check_output('cd ..', shell=True)
bar.finish()

os.chdir(home)
f=open("summary.tab","w+")
resumo=sub.check_output('grep -A21 "SUMMARY_BEG" cc*/aimless.log', shell=True)
f.write(resumo.decode())
f.close()

f=open("unit.tab","w+")
resumo=sub.check_output("grep 'UNIT' cc*/XSCALE.LP| awk '{print $3, $4, $5, $6, $7, $8}'", shell=True)
f.write("a b c alfa beta gamma\n"+resumo.decode())
f.close()

thresh=[]
for i in range(len(listacc)):
    resumo=0
    os.chdir(listacc[i])
    resumo=sub.check_output(("find . -name XSCALE.LP -exec grep -c 'COMPLETENESS' XSCALE.LP \;"),shell=True)
    resumo=int(resumo.decode())
    if resumo!=0:
        thresh.append(x[i])
    os.chdir(home)
f=open("threshold.tab","w+")
f.write("Threshold\n")
for i in thresh:
	f.write(str(i)+"\n")
f.close()

print("Plot Unit Cell Parameters")
plot_fast.unit("fast",0)

sub.call("mv unit.tab unit_xscale.tab", shell=True)
sub.call("mv unit_par.png unit_xscale_par.png", shell=True)

f=open("unit.tab","w+")
resumo=sub.check_output("grep 'Unit' <check.tab | awk '{print $4, $5, $6, $7, $8, $9}'", shell=True)
f.write("a b c alfa beta gamma\n"+resumo.decode())
f.close()
f=open("prob.tab","w+")
resumo=sub.check_output("grep 'Total' <check.tab | awk '{print $4}'", shell=True)
f.write("total\n"+resumo.decode())
f.close()
f=open("summary_xscale.tab","w+")
resumo=sub.check_output('grep -A23 "COMPLETENESS" cc*/XSCALE.LP', shell=True)
f.write(resumo.decode())
f.close()
f=open("completeness.tab","w+")

resumo=sub.check_output(("grep 'Completeness' <summary.tab | awk '{print $2,$3,$4}'"),shell=True)
f.write("Overall Outer Inner\n"+resumo.decode())
f.close()
f=open("cc.tab","w+")

resumo=sub.check_output(("grep 'CC(1/2)' <summary.tab | awk '{print $5,$6, $7}'"),shell=True)
f.write("Overall Outer Inner\n"+resumo.decode())
f.close()

f=open("r.tab","w+")

resumo=sub.check_output(("grep 'Rmeas (all I+ & I-)' <summary.tab | awk '{print $6, $7, $8}'"),shell=True)
f.write("Overall Outer Inner\n"+resumo.decode())
f.close()
warning=[]

for i in range(len(listacc)):
    resumo=0
    os.chdir(listacc[i])
    resumo=sub.check_output(("find . -name check_cc.tab -exec grep -c 'WARNING!' check_cc.tab \;"),shell=True)
    resumo=int(resumo.decode())
    if resumo!=0:
        pro=sub.check_output("grep 'Total' <check_cc.tab | awk '{print $3}'", shell=True)
        warning.append(str(x[i])+' '+pro.decode())
    os.chdir(home)

f=open("warning.tab","w+")
f.write("Threshold Prob\n")
for i in warning:
	f.write(str(i)+"\n")
f.close()


print("Plot Completeness")
plot_fast.plot('completeness', 'full',0)

print("Plot CC1/2")
plot_fast.plot('cc', 'full',0)

print("Plot Rmeas")
plot_fast.plot('r', 'full',0)

sub.call(("mkdir "+meudiretorio),shell=True)
sub.call("mv *.png "+meudiretorio, shell=True)

print("Plot CC1/2 vs Compl (Inner)")
plot_fast.map("full",dist, "Inner",0)

print("Plot CC1/2 vs Compl (Outer)")
plot_fast.map("full",dist, "Outer",0)

print("Dynamic plot")
plot_fast.dyn_plot('full', 'cc', 'Inner',0)
plot_fast.dyn_plot('full', 'cc', 'Outer',0)

print("Plot Unit Cell Parameters")
plot_fast.unit('full',0)
sub.call("mv *.png "+meudiretorio, shell=True)

sub.call("mv -t "+meudiretorio+" cc*/ ", shell=True)
sub.call("mv *.tab "+meudiretorio, shell=True)
sub.call("mv imagesOverall/ "+meudiretorio, shell=True)
sub.call("mv imagesOuter/ "+meudiretorio, shell=True)
sub.call("mv *.gif "+meudiretorio, shell=True)
sub.call("mv images_*/ "+meudiretorio, shell=True)
if(shuf==1):
    shuffle.run(dist, meudiretorio)

sub.call("mv "+dist+"* "+meudiretorio, shell=True)
er=sub.check_output("mv "+meudiretorio+" ../test_cccluster/results_script", shell=True)
sub.call("beep -f 587 -l 110 -n", shell = True)
sub.call("beep -f 587 -l 110 -n", shell = True)
sub.call("beep -f 587 -l 110 -n", shell = True)
sub.call("xdg-open ../test_cccluster/results_script/"+meudiretorio, shell=True)

import subprocess as sub
import numpy as np
import os
import sys
import shuffle
import plot_fast
import summary
import time
from progress.bar import ChargingBar
from progress.spinner import PieSpinner
import meritplot


def hcarun(inp,out,points,dist):

	'''inp =input("Insert data directory (test_cccluster/data):")
	inp= '../test_cccluster/data/'+inp
	meudiretorio=input("Insert output directory:")
	dist=input("Distance based on cc or cell:")  
	if dist=="cc":
    		points=input("# thresholds between 0 and 1:")
		xmax=0.95
    		xmin=0.05
	on=input("Turn on shuffle mode? y/n:")
	shuf=0
	if on=="y":
    		shuf=1
	'''
	home=os.getcwd()
	#os.chdir(inp)
	#sub.check_output(("rm", "-r", meudiretorio))
	meudiretorio=out
	if dist=="cc":
		xmax=0.98
		xmin=0.18

	files= sub.check_output(("find",".","-name","XDS_ASCII.HKL"))

	files=files.decode()
	lista=[]
	listacc=[]
	listap=[]
	s=""

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
	
	#sub.check_output((meustring), shell=True)

	cont=1
	print("ccCalc finished\n")
	#sub.call("cp *.txt "+home, shell=True)
	#os.chdir(home)
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
    		xmax=float(input("Highest unit cell variation:"))  
    		points=input("Choose number of thresholds between 0 and your max:")
    		xmin=0.001
    		print("\n")
	'''
	resumo=sub.check_output(("ccCluster.py -i "+dist+"ClusterLog.txt -e"), shell=True)
	f=open("thr_estimated.tab","w+")
	f.write(resumo.decode())
	f.close()
	'''
	x=np.linspace(xmin, xmax,int(points))
	#x=[]
	x= np.around(x, decimals=3)
	x=list(x)
	#print(x)
	f=open("xunit.tab","w+")
	f.write("Threshold\n")
	for i in x:
		f.write(str(i)+"\n")
	f.close()
	print("Starting ccCluster")

	bar = ChargingBar('Running ccCluster:', max = len(x))
	for i in x:
		bar.next()
		#sub.call(("ccCluster.py -i"+ dist+"ClusterLog.txt -t "+str(i)+" -p"), shell=True)
		cont+=1
		filescc=sub.check_output(("ls -d */"), shell=True)
		filescc=filescc.decode()
		print(filescc)
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

	thresh=[]

	for i in range(len(listacc)):
		resumo=0
		os.chdir(listacc[i])
		resumo=sub.check_output(("find . -name XSCALE.LP -exec grep -c 'COMPLETENESS' XSCALE.LP \;"),shell=True)
		resumo=int(resumo.decode())
		if resumo!=0:
			thresh.append(x[i])
		os.chdir(home)
	plot_fast.WriteHeader()
	index=plot_fast.WriteTab(6)

	f=open("threshold.tab","w+")
	f.write("Threshold\n")
	for i in index:
		f.write(str(thresh[i-1])+"\n")
	f.close()

	#f=open(".cc_cluster.log")
	#g=open("temp.log","w+")
	#lines=f.readlines()
	#for i in index:
	#    g.write(str(lines[i-1]))
	#f.close()
	#g.close()
	#sub.call("mv temp.log .cc_cluster.log", shell=True)


	sub.call("mv cc_i.tab cc.tab", shell=True)
	sub.call("mv completeness_i.tab completeness.tab", shell=True)
	sub.call("mv r_i.tab r.tab", shell=True)

	'''
	print("Plot Completeness")
	plot_fast.plot('completeness', 'fast', 0)

	print("Plot CC1/2")
	plot_fast.plot('cc', 'fast', 0)

	print("Plot Rmeas")
	plot_fast.plot('r', 'fast', 0)
	'''
	meritplot.plot_fig()
	
	sub.call(("mkdir "+meudiretorio),shell=True)
	sub.call("mv *.png "+meudiretorio, shell=True)
	'''
	print("Plot CC1/2 vs Compl (Inner)")
	plot_fast.map("fast",dist, "Inner",0)
	print("Plot CC1/2 vs Compl (Outer)")
	plot_fast.map("fast",dist, "Outer",0)

	print("Dynamic plot")
	plot_fast.dyn_plot('fast', dist, 'Inner',0)
	plot_fast.dyn_plot('fast', dist, 'Outer',0)
	'''
	print("Plot Unit Cell Parameters")
	plot_fast.unit("fast",0)
	sub.call("mv *.png "+meudiretorio, shell=True)
	#summary.main()

	sub.call("mv -t "+meudiretorio+" cc*/ ", shell=True)
	#sub.call("mv .cc_summary.txt cc_summary.tab", shell=True)
	#sub.call("mv .cc_cluster.log cc_cluster.tab", shell=True)
	sub.call("mv *.tab "+meudiretorio, shell=True)
	

	#sub.call("mv imagesInner/ "+meudiretorio, shell=True)
	#sub.call("mv imagesOuter/ "+meudiretorio, shell=True)

	sub.call("mv *.gif "+meudiretorio, shell=True)
	#sub.call("mv images_*/ "+meudiretorio, shell=True)
	'''
	if(shuf==1):
    		shuffle.run(dist, meudiretorio)
	'''
	
	sub.call("mv "+dist+"* "+meudiretorio, shell=True)
	er=sub.check_output("cp -r "+meudiretorio+" ../test_cccluster/results_script; rm -r "+meudiretorio, shell=True)
	#sub.call("xdg-open ../test_cccluster/results_script/"+meudiretorio, shell=True)
	

def main():
	print("""Starting SX HCA data processing MANACÁ - Sirius (LNLS) """)
	#inp='../test_cccluster/data/20200227_lys_hr_n2_w5'
	inp='../ame_n2_w5'
	out='/home/ABTLUS/up.arodrigues7/script/20210815_ame_test'
	number=5
	dist='cc'
	hcarun(inp,out,number,dist)

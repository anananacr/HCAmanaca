import matplotlib.pyplot as plt
import sys
import os
import time
import subprocess as sub
import numpy as np
import plot_fast
from PIL import Image, ImageDraw

    
def main():
    print("""Starting HCA pipeline 
               __/)
            .-(__(=:
            |    \)
      (\__  |
     :=)__)-|  __/)
      (/    |-(__(=:
    ______  |  __\)
   /_/    \ | /_/  
        ___\|/___ 
       [         ]
        \       /      MANACÁ - SIRIUS
         \     /
          \___/
    """)
    
    sub.call("beep -f 587 -l 110 -n", shell = True)
    inp =input("Insert data directory (test_cccluster/data):")
    sub.call("mkdir runs_"+inp, shell=True)
    workdir= '../test_cccluster/data/'+inp
    plot_fast.WriteHeader()
    loop=1    
    shouldContinue='True'
    
    while shouldContinue=='True':
        time.sleep(2)
        print("NEW LOOP: #%d"%loop)
        
        crystals = np.arange(0,loop)
        sub.check_output('ccCalc.py -f '+workdir+'/*/XDS_ASCII.HKL', shell=True)
        sub.check_output('ccCluster.py -i ccClusterLog.txt -p', shell=True)
        plot_fast.WriteTab(5)
        filescc=sub.check_output(("ls -d cc*/"), shell=True)
        filescc=filescc.decode()
        home=os.getcwd()
        s=''   
        listacc=[]     
        for i in filescc:
	        if i=="\n":
		        s=home+'/'+s		
		        listacc.append(s)
		        s=""	
	        else:
		        s=s[0:]+i
        files=listacc[0]
        thresh=[]
        for i in range(len(listacc)):
            resumo=0
            os.chdir(listacc[i])
            resumo=sub.check_output(("find . -name XSCALE.LP -exec grep -c 'COMPLETENESS' XSCALE.LP \;"),shell=True)
            resumo=int(resumo.decode())
            if resumo!=0:
                thresh.append(crystals[i])
            os.chdir(home)  
     
        sub.call("chmod -R 777 .", shell=True)
        sub.call("mv "+str(files[:-1])+" "+str(files[:-1])+"_"+str(loop), shell=True)        
        sub.call("mv "+str(files[:-1])+"_"+str(loop)+" runs_"+inp, shell=True)
                
        print('loop %d finished'%loop)
        os.chdir(home)
        
        f=open("threshold.tab","a")
        f.write("\n"+str(loop))
        f.close()
       
        print("Plot Completeness")
        plot_fast.plot('completeness', 'fast', 0)

        print("Plot CC1/2")
        plot_fast.plot('cc', 'fast', 0)

        print("Plot Rmeas")
        plot_fast.plot('r', 'fast', 0)
        
        sub.call(("mv cc_fast.png cc_fast_"+str(loop)+".png"), shell=True)
        sub.call(("mv completeness_fast.png completeness_fast_"+str(loop)+".png"), shell=True)
        sub.call(("mv r_fast.png r_fast_"+str(loop)+".png"), shell=True)
        if loop==10:        
            shouldContinue='False'
        else:
            loop+=1
    #gif plot parameters evolution per iteration
    
    parameters=["cc", "r", "completeness"]
    im=[]
    xmax=loop*200
    for par in parameters:
        images=[]    
        for i in range(loop):
            im=Image.open(par+"_fast_"+str(i+1)+'.png')	
            images.append(im)
            images[0].save('evolution_'+par+'.gif', save_all=True, append_images=images[1:], optimize=False, duration=xmax, loop=0)
    sub.call("rm -r *.tab", shell=True)
    sub.call("rm -r *.png", shell=True)
    sub.call("mv *.gif runs_"+inp, shell=True)

    


main()
  

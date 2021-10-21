import subprocess as sub
import numpy as np
import os
import sys
import HCAplot

def run(dist, meudiretorio):
    #dist cell or cc
    print("\nStarting ccCluster (shuffle mode)")
    sub.check_output(("ccCluster.py -i "+ dist+"ClusterLog.txt -s"), shell=True)

    f=open("summary.tab","w+")
    resumo=sub.check_output('grep -B4 "STATISTICS OF INPUT DATA SET " thr*/XSCALE.LP', shell=True)
    f.write(resumo.decode())
    f.close()

    f=open("summary_xscale.tab","w+")
    resumo=sub.check_output('grep -A23 "COMPLETENESS" thr*/XSCALE.LP', shell=True)
    f.write(resumo.decode())
    f.close()

    f=open("unit.tab","w+")
    resumo=sub.check_output("grep 'UNIT' thr*/XSCALE.LP| awk '{print $3, $4, $5, $6, $7, $8}'", shell=True)
    f.write("a b c alfa beta gamma\n"+resumo.decode())
    f.close()

    f=open("completeness_test.tab","w+")
    resumo=sub.check_output(("grep -B1 "+'"total" <summary.tab | awk ' "'{print $6}'"),shell=True)
    resumo=resumo.decode()
    s=''

    for i in range(len(resumo)-2):
	    flag=0
	    if resumo[i]=='%':
		    s=s[0:]+' '
		    flag=1
	    if resumo[i]=='\n' and resumo[i+1]=='\n':
		    s=s[0:]+'\n'
		    i+=1
		    flag=1
	    if resumo[i]=='\n' and resumo[i+1]!='\n':
		    s=s[0:]
		    flag=1
	    if flag==0:
		    s=s[0:]+ resumo[i]


    f.write("Outer Overall\n"+s+"  ")
    f.close()

    f=open("compin.tab","w+")
    resumo=sub.check_output(("grep -A3 'COMPLETENESS' <summary_xscale.tab | awk '{print $6}'"),shell=True)
    resumo=resumo.decode()
    s=''

    i=0
    while i <(len(resumo)-2):
        flag=0
        if resumo[i]=='C':
            i=i+17
            s=s[0:]
            flag=1
        if resumo[i]=='%':
            flag=1
            s=s[0:]+'\n'
            i=i+3
        if flag==0:
            s=s[0:]+ resumo[i]
            i=i+1
    f.write("Inner \n"+s)
    f.close()

    f=open("rin.tab","w+")
    resumo=sub.check_output(("grep -A3 'COMPLETENESS' <summary_xscale.tab | awk '{print $11}'"),shell=True)
    resumo=resumo.decode()
    s=''

    i=0
    while i <(len(resumo)-2):
        flag=0
        if resumo[i]=='R':
            i=i+9
            s=s[0:]
            flag=1
        if resumo[i]=='%':
            flag=1
            s=s[0:]+'\n'
            i=i+3
        if flag==0:
            s=s[0:]+ resumo[i]
            i=i+1
    f.write("Inner \n"+s)
    f.close()

    f=open("rout.tab","w+")
    resumo=sub.check_output(("grep -B1 'total' <summary.tab | awk '{print $11}'"),shell=True)
    resumo=resumo.decode()
    s=''

    for i in range(len(resumo)-2):
	    flag=0
	    if resumo[i]=='%':
		    s=s[0:]+' '
		    flag=1
	    if resumo[i]=='\n' and resumo[i+1]=='\n':
		    s=s[0:]+'\n'
		    flag=1
	    if resumo[i]=='\n' and resumo[i+1]!='\n':
		    s=s[0:]
		    flag=1
	    if flag==0:
		    s=s[0:]+ resumo[i]

    f.write("Outer Overall\n"+s+" \n")
    f.close()


    f=open("xunit.tab","w+")
    f.write("Threshold\n")
    run=np.linspace(0, 19,20)
    for i in run:
        f.write(str(i)+"\n")
    f.close()
    listacc=[]
    filescc=sub.check_output(("ls -d thr*/"), shell=True)
    filescc=filescc.decode()
    home=os.getcwd()
    s=''
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
            thresh.append(run[i])
        os.chdir(home)

    s=''
    f=open("cc_test.tab","w+")
    resumo=sub.check_output(("grep -B1 "+'"total" <summary.tab | awk ' "'{print $12}'"),shell=True)
    resumo=resumo.decode()
    for i in range(len(resumo)-1):
	    flag=0
	    if resumo[i]=='*':
		    s=s[0:]+resumo[i]+' '
		    flag=1
	    if resumo[i]=='\n' and resumo[i+1]=='\n':
		    s=s[0:]+'\n'
		    i+=1
		    flag=1
	    if resumo[i]=='\n' and resumo[i+1]!='\n':
		    s=s[0:]
		    flag=1
	    if flag==0:
		    s=s[0:]+ resumo[i]


    f.write("Outer Overall\n"+s)
    f.close()

    f=open("ccin_test.tab","w+")
    resumo=sub.check_output(("grep -A3 'COMPLETENESS' <summary_xscale.tab | awk '{print $12}'"),shell=True)
    resumo=resumo.decode()
    s=''
    
    i=0
    while i <(len(resumo)-2):
        flag=0
        if resumo[i]=='C':
            i=i+10
            s=s[0:]
            flag=1
        if resumo[i]=='*':
            flag=1
            s=s[0:]+resumo[i]+'\n'
            i=i+3
        if resumo[i]=='.' and resumo[i+2]!='*':
            flag=1
            s=s[0:]+resumo[i]+resumo[i+1]+'\n'
            i=i+4
        if flag==0:
            s=s[0:]+ resumo[i]
            i=i+1
    if resumo[-2]=='*':
        s=s[0:]+'*'
    f.write("Inner \n"+s)
    f.close()

    f=open("cc_test.tab")
    g=open("ccin_test.tab")
    lines=f.readlines()
    linesin=g.readlines()
    cont=0
    cc=[]
    ccin=[]
    index=[]
    for i in lines:
        flag=0
        for k in i:
            if k=="*":
                flag+=1
        for j in linesin[cont]:
            if j=="*":
                flag+=1
        if flag==3:
            cc.append(i)
            index.append(cont)
            ccin.append(linesin[cont])
        cont+=1
    f.close()
    sub.call("rm cc_test.tab", shell=True)
    sub.call("rm ccin_test.tab", shell=True)

    f=open("ccout.tab","w+")
    f.write("Outer Overall \n")
    for i in cc:
        for k in i:
            if k!="*":
                f.write(k)
    f.write(" ")
    f.close()

    f=open("ccin.tab","w+")
    f.write("Inner\n")
    for i in ccin:
        for k in i:
            if k!="*":
                f.write(k)
    f.write(" ")
    f.close()

    f=open("ccout.tab")
    g=open("ccin.tab")
    h=open("cc.tab","w+")

    lines=f.readlines()
    linesin=g.readlines()

    for i in range(len(ccin)+1):
        
        h.write(lines[i][0:-1]+linesin[i])
        
    f.close()
    g.close()
    h.close()
    sub.call("rm ccin.tab", shell=True)
    sub.call("rm ccout.tab", shell=True)


    f=open("threshold.tab","w+")
    f.write("Threshold\n")
    for i in index:
        f.write(str(thresh[i-1])+"\n")
    f.close()

    f=open("completeness_test.tab")
    g=open("compin.tab")
    h=h=open("completeness.tab","w+")
    lines=f.readlines()
    linesin=g.readlines()
    h.write(lines[0][0:-1]+" "+linesin[0])
    for i in index:
        h.write(lines[i][0:-1]+linesin[i])
        
    f.close()
    g.close()
    h.close()
    sub.call("rm compin.tab", shell=True)
    sub.call("rm completeness_test.tab", shell=True)

    f=open("rout.tab")
    g=open("rin.tab")
    h=open("r.tab","w+")
   
    lines=f.readlines()
    linesin=g.readlines()
    h.write(lines[0][0:-1]+" "+linesin[0])
    for i in index:
        
        h.write(lines[i][0:-1]+linesin[i])
        
    f.close()
    g.close()
    h.close()
    sub.call("rm rin.tab", shell=True)
    sub.call("rm rout.tab", shell=True)

    print("Plot Completeness")
    HCAplot.plot('completeness','fast', 1)

    print("Plot CC1/2")
    HCAplot.plot('cc','fast', 1)
    
    print("Plot Rmeas")
    HCAplot.plot('r', 'fast', 1)

    sub.call(("mkdir shuffle_"+meudiretorio),shell=True)
    sub.call("mv *.png shuffle_"+meudiretorio, shell=True)

    print("Plot CC1/2 vs Compl (Inner)")
    HCAplot.map("fast","cc", "Inner", 1)

    print("Plot CC1/2 vs Compl (Outer)")
    HCAplot.map("fast","cc", "Outer", 1)
    
    print("Plot Unit Cell Parameters")
    HCAplot.unit("fast",1)
  

    sub.call("mv *.png shuffle_"+meudiretorio, shell=True)
    sub.call("mv -t shuffle_"+meudiretorio+" thr*/ ", shell=True)
    sub.call("mv *.tab shuffle_"+meudiretorio, shell=True)
    sub.call("mv imagesInner/ shuffle_"+meudiretorio, shell=True)
    sub.call("mv imagesOuter/ shuffle_"+meudiretorio, shell=True)
    sub.call("mv *.gif shuffle_"+meudiretorio, shell=True)
    sub.call("mv shuffle_"+meudiretorio+" "+meudiretorio, shell=True)

#Importa pacotes relevantes
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import csv
import subprocess as sub
from PIL import Image, ImageDraw
import os
import matplotlib.image as mpimg

def plot(par, mode, run):
    art=0
    #par completeness or cc vs threshold
    #mode fast or full
    majorLocator = MultipleLocator(20)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(5)

    #upa o dado na mesma pasta e troca o nome do arquivo
    data_dir = "./"
    data = os.path.join(data_dir, par+'.tab')
    t=os.path.join(data_dir, 'threshold.tab')
    #carrega dados
    x=pd.read_csv(t, delimiter=' ', skiprows=0,usecols=(0,))
    x=x.values
    df= pd.read_csv(data, delimiter=' ', skiprows=0,usecols=(0,1,2))
    c_all=df['Overall'].values
    c_in=df['Inner'].values 
    c_out=df['Outer'].values 


    if par=='cc' and mode=='fast':
        title='CC1/2'
        yall=[]
        yin=[]
        yout=[]  
        c_all=list(c_all)
        c_in=list(c_in)
        c_out=list(c_out)    

        for i in c_all:
            if str(i)!='nan' and str(i)!=' ':
                yall.append(float(i)/100)
        for i in c_in:
            if str(i)!='nan' and str(i)!=' ':
                yin.append(float(i)/100)
        for i in c_out:
            if str(i)!='nan':
                yout.append(float(i)/100)
    if par=='cc' and mode!='fast':
        title='CC1/2'
        yall=c_all
        yin=c_in
        yout=c_out
    if par=='completeness':
        title='Completeness'
        yall=c_all
        yin=c_in
        yout=c_out
    if par=='r' and mode!='fast':
        title='Rmeas'
        yall=c_all
        yin=c_in
        yout=c_out
    if par=='r' and mode=='fast':
        title='Rmeas'
        yall=[]
        yin=[]
        yout=[]  
        c_all=list(c_all)
        c_in=list(c_in)
        c_out=list(c_out)    

        for i in c_all:
            if str(i)!='nan' and str(i)!=' ':
                yall.append(float(i)/100)
        for i in c_in:
            if str(i)!='nan' and str(i)!=' ':
                yin.append(float(i)/100)
        for i in c_out:
            if str(i)!='nan':
                yout.append(float(i)/100)
    fig = plt.figure(figsize=(11, 7), tight_layout=True)

    colors=['k', 'b', 'r', 'g']
    ax = fig.add_subplot(1,1,1)
    ax.set_ylabel(title, fontsize=40)
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(4)
    if art==1:        
        ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
        ax.xaxis.set_major_locator(plt.MultipleLocator(0.2))
        ax.tick_params(axis='both', which='major', labelsize=28, width=4, length = 20)
        ax.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
        ax.xaxis.set_major_locator(plt.MultipleLocator(0.01))
        plt.xlim(-0.01,1.05)
        plt.ylim(-0.5,35)
    if par=='completeness':
        b= list(np.arange(float(x[0][0]),float(x[-1][0]), 0.00001, dtype=float))
        c= list(98*(np.ones(len(b))))
        plt.scatter(b,c, c= colors[3], marker='.', s=15)
    linez =plt.scatter(x,yin, c= colors[1], marker='o', s=250)
    liney =plt.scatter(x,yout, c= colors[2], marker='^', s=250)
    ax.tick_params(axis='both', which='major', labelsize=18, width=4, length = 15)
    ax.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
    #linex =plt.scatter(x,yall, c= colors[0], marker='o',s=250)
    if run==1:
        ax.set_xlabel('Runs Xscale', fontsize=40)
        legend= plt.legend((liney, linez), ('Outer shell', 'Inner Shell'), fontsize=20, loc=1)
    else:
        ax.set_xlabel('Threshold', fontsize=40)
        legend= plt.legend((liney, linez), ('Outer shell', 'Inner Shell'), fontsize=20, loc=1)

    legend.get_frame().set_linewidth(4)
    legend.get_frame().set_edgecolor("black")

    plt.savefig(par+'_'+mode+'.png')
    state='FINISHED'
    plt.close('all')    
    return state

def map(mode, dist,shell, run):
    #dist cell or cc
    art=0
    if dist=='cell':
        nround=3
    else:
        nround=2

    f=open("completeness.tab")
    g=open("cc.tab")

    lines=f.readlines()
    compl=[]
    cc=[]
    cont=0
    images = []

    data_dir = "./"
    data=os.path.join(data_dir, 'completeness.tab')
    df=[]
    #carrega dados
    df=pd.read_csv(data, delimiter=' ', skiprows=0,usecols=(0,1,2))
    compl= df[shell].values
    #print(len(compl))

    data=os.path.join(data_dir, 'cc.tab')
    df=[]
    #carrega dados
    df=pd.read_csv(data, delimiter=' ', skiprows=0,usecols=(0,1,2))
    cc= df[shell].values
    cc=list(cc)

    yall=[]
    if mode == 'fast':
        for i in cc:
            if str(i)!='nan' and str(i)!=' ':
                yall.append(float(i)/100)
    else:
        for i in cc:
            if str(i)!='nan' and str(i)!=' ':
                yall.append(float(i))

    data_dir = "./"
    t=os.path.join(data_dir, 'threshold.tab')
    x=[]
    #carrega dados
    x=pd.read_csv(t, delimiter=' ', skiprows=0,usecols=(0,))
    x= x.values

    im=[]

    for i in range(len(cc)):
        compl[i]=float(compl[i])
        line=[]
        handle=[]
        if run==1:
            handle.append('Runs Xscale:')
            handle.append(str(int(x[i][0])))
        else:
            handle.append('Threshold:')
            handle.append(str(round(float(x[i][0]),nround)))
        fig = plt.figure(figsize=(11, 7), tight_layout=True)
        ax = fig.add_subplot(1,1,1)
        line.append(plt.scatter(compl,yall, c='blue', marker ='o', s=300, edgecolors='k',linewidths=1 ))
        line.append(plt.scatter(compl[i],yall[i], c='red', marker ='X', s=300, edgecolors='k', linewidths=1))
        if art==1:
           ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
           ax.xaxis.set_major_locator(plt.MultipleLocator(10))
           ax.yaxis.set_minor_locator(plt.MultipleLocator(0.05))
           ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
           ax.tick_params(axis='both', which='major', labelsize=28, width=4, length = 20)
           ax.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
           plt.xlim(0,102)
           plt.ylim(0,1.03)
        ax.set_ylabel('CC1/2', fontsize=40)
        ax.set_xlabel('Completeness', fontsize=40)
        ax.tick_params(axis='both', which='major', labelsize=18, width=4, length = 15)
        ax.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
        thresh=round(float(x[i][0]),nround)
        legend= plt.legend(line, handle, fontsize=20, loc =6)
        plt.savefig('evol_'+str(thresh)+'.png')
        plt.close('all')            
        im=Image.open('evol_'+str(thresh)+'.png')	
        images.append(im)
        images[0].save('evolution_'+shell+'.gif', save_all=True, append_images=images[1:], optimize=False, duration=700, loop=0)
	    
    sub.call('mkdir images'+shell, shell=True)
    sub.call('mv evol*.png images'+shell, shell=True)
    state='FINISHED'
    return state

def WriteHeader():
    par=["cc", "r", "completeness", "threshold"]
    for i in par:
        g=open(i+".tab","w+")            
        g.write("Outer Overall Inner")
        g.close()    

def WriteTab(nin):
    
    f=open("summary.tab","w+")
    resumo=sub.check_output('grep -B4 "STATISTICS OF INPUT DATA SET " cc*/XSCALE.LP', shell=True)
    f.write(resumo.decode())
    f.close()

    f=open("summary_xscale.tab","w+")
    resumo=sub.check_output('grep -A23 "COMPLETENESS" cc*/XSCALE.LP', shell=True)
    f.write(resumo.decode())
    f.close()

    f=open("unit.tab","w+")
    resumo=sub.check_output("grep 'UNIT' cc*/XSCALE.LP| awk '{print $3, $4, $5, $6, $7, $8}'", shell=True)
    f.write("a b c alfa beta gamma\n"+resumo.decode())
    f.close()

    f=open("completeness_test.tab","w+")
    resumo=sub.check_output(("grep -B1 "+'"total" <summary.tab | awk ' "'{print $"+str(nin)+"}'"),shell=True)
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
    resumo=sub.check_output(("grep -A3 'COMPLETENESS' <summary_xscale.tab | awk '{print $"+str(nin)+"}'"),shell=True)
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
    resumo=sub.check_output(("grep -A3 'COMPLETENESS' <summary_xscale.tab | awk '{print $"+str(nin+5)+"}'"),shell=True)
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
    resumo=sub.check_output(("grep -B1 'total' <summary.tab | awk '{print $"+str(nin+5)+"}'"),shell=True)
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
    s=''
    f=open("cc_test.tab","w+")
    resumo=sub.check_output(("grep -B1 "+'"total" <summary.tab | awk ' "'{print $"+str(nin+6)+"}'"),shell=True)
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
    resumo=sub.check_output(("grep -A3 'COMPLETENESS' <summary_xscale.tab | awk '{print $"+str(nin+6)+"}'"),shell=True)
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
    h=open("cc_i.tab","w+")

    lines=f.readlines()
    linesin=g.readlines()

    for i in range(len(ccin)+1):
        h.write(lines[i][0:-1]+linesin[i])
        
    f.close()
    g.close()
    h.close()
    
    sub.call("rm ccin.tab", shell=True)
    sub.call("rm ccout.tab", shell=True)
    
    f=open("cc_i.tab")
    g=open("cc.tab","a")
    lines=f.readlines()
    g.write("\n"+lines[1])    
    f.close()
    g.close()
    
    f=open("completeness_test.tab")
    g=open("compin.tab")
    h=open("completeness_i.tab","w+")
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

    f=open("completeness_i.tab")
    g=open("completeness.tab","a")
    lines=f.readlines()
    g.write("\n"+lines[1])    
    f.close()
    g.close()

    f=open("rout.tab")
    g=open("rin.tab")
    h=open("r_i.tab","w+")

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
    
    f=open("r_i.tab")
    g=open("r.tab","a")
    lines=f.readlines()
    g.write("\n"+lines[1])
    f.close()
    g.close()
    return index
def dyn_plot(mode, dist,shell, run):
    #dist cell or cc
    art=0
    if dist=='cell':
        nround=3
    else:
        nround=2

    f=open("completeness.tab")
    g=open("cc.tab")

    lines=f.readlines()
    compl=[]
    cc=[]
    cont=0
    images = []

    data_dir = "./"
    data=os.path.join(data_dir, 'completeness.tab')
    df=[]
    #carrega dados
    df=pd.read_csv(data, delimiter=' ', skiprows=0,usecols=(0,1,2))
    compl= df[shell].values
    #print(len(compl))

    data=os.path.join(data_dir, 'cc.tab')
    df=[]
    #carrega dados
    df=pd.read_csv(data, delimiter=' ', skiprows=0,usecols=(0,1,2))
    cc= df[shell].values
    cc=list(cc)

    yall=[]
    if mode == 'fast':
        for i in cc:
            if str(i)!='nan' and str(i)!=' ':
                yall.append(float(i)/100)
    else:
        for i in cc:
            if str(i)!='nan' and str(i)!=' ':
                yall.append(float(i))
    
    data=os.path.join(data_dir, 'r.tab')
    df=[]
    #carrega dados
    df=pd.read_csv(data, delimiter=' ', skiprows=0,usecols=(0,1,2))
    r= df[shell].values
    r=list(r)

    rall=[]
    if mode == 'fast':
        for i in r:
            if str(i)!='nan' and str(i)!=' ':
                rall.append(float(i)/100)
    else:
        for i in r:
            if str(i)!='nan' and str(i)!=' ':
                rall.append(float(i))
    
    data_dir = "./"
    t=os.path.join(data_dir, 'threshold.tab')
    x=[]
    #carrega dados
    x=pd.read_csv(t, delimiter=' ', skiprows=0,usecols=(0,))
    x= x.values

    im=[]
    thr=[]
    for j in range(len(cc)):
        thr.append(round(float(x[j][0]),nround))
    
    path=[]
    filescc=sub.check_output(("ls -d cc*/"), shell=True)
    filescc=filescc.decode()
    home=os.getcwd()
    s=''
    for i in filescc:
	    if i=="\n":
		    s=home+'/'+s
		    path.append(s)
		    s=""	
	    else:
		    s=s[0:]+i
    best=[]
    s=''
    for k in range(len(path)):
        j=43
        while j<46:
            if str(path[k][j])!='_' and str(path[k][j])!='a':
                s=s[0:]+str(path[k][j])
            j=j+1
        best.append(int(s))
        s=''
    
    for i in range(len(cc)):
        compl[i]=float(compl[i])
        line=[]
        handle=[]
        
        if run==1:
            handle.append('Runs Xscale:'+str(int(x[i][0])))
            #handle.append('Biggest cluster:'+str(best[i]))
        else:
            handle.append('Threshold:'+str(round(float(x[i][0]),nround)))
            #handle.append('Biggest cluster:'+str(str(best[i])))
        fig = plt.figure(figsize=(15, 7), tight_layout=True)
        ax = fig.add_subplot(1,2,1)
        line.append(plt.scatter(thr,yall, c='blue', marker ='o', s=300, edgecolors='k',linewidths=1 ))
        line.append(plt.scatter(thr[i],yall[i], c='red', marker ='X', s=300, edgecolors='k', linewidths=1))
        if art==1:
           ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
           ax.xaxis.set_major_locator(plt.MultipleLocator(10))
           ax.yaxis.set_minor_locator(plt.MultipleLocator(0.05))
           ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
           plt.xlim(0,102)
           plt.ylim(0,1.03)
        ax.tick_params(axis='both', which='major', labelsize=18, width=4, length = 15)
        ax.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
        ax.set_ylabel('CC1/2', fontsize=28)
        ax.set_xlabel('Threshold', fontsize=28)
        thresh=round(float(x[i][0]),nround)
        legend= plt.legend(line, handle, fontsize=18, loc =1)
        ax = fig.add_subplot(1,2,2)
        ax.tick_params(axis='both', which='major', labelsize=0, width=0, length = 0)
        img = mpimg.imread(path[i]+'/Dendrogram.png')        
        imgplot = plt.imshow(img)
        plt.savefig('evol_cc_'+str(thresh)+'.png')
        plt.close('all')            
        im=Image.open('evol_cc_'+str(thresh)+'.png')	
        images.append(im)
        images[0].save('evolution_cc_'+shell+'.gif', save_all=True, append_images=images[1:], optimize=False, duration=1600, loop=0)
    
    i=0
    im=[]
    images=[]
    for i in range(len(cc)):
        compl[i]=float(compl[i])
        line=[]
        handle=[]
        
        if run==1:
            handle.append('Runs Xscale:'+str(int(x[i][0])))
            #handle.append('Biggest cluster:'+str(best[i]))
        else:
            handle.append('Threshold:'+str(round(float(x[i][0]),nround)))
            #handle.append('Biggest cluster:'+str(best[i]))
        fig = plt.figure(figsize=(15, 7), tight_layout=True)
        ax = fig.add_subplot(1,2,1)
        line.append(plt.scatter(thr,compl, c='blue', marker ='o', s=300, edgecolors='k',linewidths=1 ))
        line.append(plt.scatter(thr[i],compl[i], c='red', marker ='X', s=300, edgecolors='k', linewidths=1))
        if art==1:
           ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
           ax.xaxis.set_major_locator(plt.MultipleLocator(10))
           ax.yaxis.set_minor_locator(plt.MultipleLocator(0.05))
           ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
           plt.xlim(0,102)
           plt.ylim(0,1.03)
        ax.tick_params(axis='both', which='major', labelsize=18, width=4, length = 15)
        ax.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
        ax.set_ylabel('Completeness', fontsize=28)
        ax.set_xlabel('Threshold', fontsize=28)
        thresh=round(float(x[i][0]),nround)
        legend= plt.legend(line, handle, fontsize=18, loc =4)
        ax = fig.add_subplot(1,2,2)
        ax.tick_params(axis='both', which='major', labelsize=0, width=0, length = 0)
        img = mpimg.imread(path[i]+'/Dendrogram.png')        
        imgplot = plt.imshow(img)
        plt.savefig('evol_compl_'+str(thresh)+'.png')
        plt.close('all')    
        im=Image.open('evol_compl_'+str(thresh)+'.png')	
        images.append(im)
        images[0].save('evolution_compl_'+shell+'.gif', save_all=True, append_images=images[1:], optimize=False, duration=1600, loop=0)
    i=0
    im=[]
    images=[]
    for i in range(len(cc)):
        compl[i]=float(compl[i])
        line=[]
        handle=[]
        
        if run==1:
            handle.append('Runs Xscale:'+str(int(x[i][0])))
            #handle.append('Biggest cluster:'+str(best[i]))
        else:
            handle.append('Threshold:'+str(round(float(x[i][0]),nround)))
            #handle.append('Biggest cluster:'+str(best[i]))
        fig = plt.figure(figsize=(15, 7), tight_layout=True)
        ax = fig.add_subplot(1,2,1)
        line.append(plt.scatter(thr,rall, c='blue', marker ='o', s=300, edgecolors='k',linewidths=1 ))
        line.append(plt.scatter(thr[i],rall[i], c='red', marker ='X', s=300, edgecolors='k', linewidths=1))
        if art==1:
           ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
           ax.xaxis.set_major_locator(plt.MultipleLocator(10))
           ax.yaxis.set_minor_locator(plt.MultipleLocator(0.05))
           ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
           plt.xlim(0,102)
           plt.ylim(0,1.03)
        ax.tick_params(axis='both', which='major', labelsize=18, width=4, length = 15)
        ax.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
        ax.set_ylabel('Rmeas', fontsize=28)
        ax.set_xlabel('Threshold', fontsize=28)
        thresh=round(float(x[i][0]),nround)
        legend= plt.legend(line, handle, fontsize=18, loc =4)
        ax = fig.add_subplot(1,2,2)
        ax.tick_params(axis='both', which='major', labelsize=0, width=0, length = 0)
        img = mpimg.imread(path[i]+'/Dendrogram.png')        
        imgplot = plt.imshow(img)
        plt.savefig('evol_r_'+str(thresh)+'.png')
        plt.close('all')
        im=Image.open('evol_r_'+str(thresh)+'.png')	
        images.append(im)
        images[0].save('evolution_r_'+shell+'.gif', save_all=True, append_images=images[1:], optimize=False, duration=1600, loop=0)
	    
    sub.call('mkdir images_cc_'+shell, shell=True)
    sub.call('mv evol_cc_*.png images_cc_'+shell, shell=True)
    sub.call('mkdir images_compl_'+shell, shell=True)
    sub.call('mv evol_compl_*.png images_compl_'+shell, shell=True)
    sub.call('mkdir images_r_'+shell, shell=True)
    sub.call('mv evol_r_*.png images_r_'+shell, shell=True)
    state='FINISHED'
    return state

def unit(mode,run):
    art=0
    #mode fast ou full
    data_dir = "./"
    data = os.path.join(data_dir, 'unit.tab')
    if mode=='fast':    
        t=os.path.join(data_dir, 'xunit.tab')
    else: 
        t=os.path.join(data_dir, 'x.tab')  
 
    x=pd.read_csv(t, delimiter=' ', skiprows=0,usecols=(0,))

    df= pd.read_csv(data, delimiter=' ',skiprows=0,usecols=(0,1,2,3,4,5))
    a=df['a'].values 
    b=df['b'].values 
    c=df['c'].values 
    alfa=df['alfa'].values 
    beta=df['beta'].values 
    gamma=df['gamma'].values 
    
    fig = plt.figure(figsize=(15, 10), tight_layout=True)
    #fig.suptitle("", fontsize=16, y=0.92)

    #plota
    colors=['r', 'lime', 'g', 'magenta', 'k', 'darkorange', 'b']
    ax = fig.add_subplot(1,1,1)
    ax.set_ylabel('Unit cell (A/deg)', fontsize=40)
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(4)
    if art==1:
        ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
        ax.xaxis.set_major_locator(plt.MultipleLocator(0.2))
        ax.tick_params(axis='both', which='major', labelsize=28, width=4, length = 20)
        ax.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
        ax.xaxis.set_major_locator(plt.MultipleLocator(0.01))
        plt.ylim(0,100)
    if run==1:
        ax.set_xlabel('Runs Xscale', fontsize=40)
    else:
        ax.set_xlabel('Threshold', fontsize=40)
    linea =plt.scatter(x,a, c= colors[0], marker='s',s=300)
    lineb =plt.scatter(x,b, c= colors[2], marker='s', s=150)
    linec =plt.scatter(x,c, c= colors[1], marker='s', s=80)
    linealfa =plt.scatter(x,alfa, c= colors[3], marker='o', s=300)
    linebeta =plt.scatter(x,beta, c= colors[4], marker='o', s=150)
    linegamma =plt.scatter(x,gamma, c= colors[5], marker='o', s=80)
    legend= plt.legend((linea, lineb, linec, linealfa, linebeta, linegamma), ('a', 'b', 'c', 'alfa', 'beta', 'gamma'), fontsize=20, loc=7)
    legend.get_frame().set_linewidth(4)
    legend.get_frame().set_edgecolor("black")
    ax.tick_params(axis='both', which='major', labelsize=18, width=4, length = 15)
    ax.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
    if mode!="fast":
        data = os.path.join(data_dir, 'prob.tab')
        df=pd.read_csv(data, delimiter=' ', skiprows=0,usecols=(0,))
        prob=df['total'].values 

        data = os.path.join(data_dir, 'warning.tab')
        df= pd.read_csv(data, delimiter=' ',skiprows=0,usecols=(0,1))
        xw=df['Threshold'].values 
        pw=df['Prob'].values
        ax2 = ax.twinx()          
        if art==1:        
            
            ax2.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
            ax2.xaxis.set_major_locator(plt.MultipleLocator(0.2))
            ax2.tick_params(axis='both', which='major', labelsize=28, width=4, length = 20)
            ax2.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)
            plt.ylim(0,1.03)
            plt.xlim(0.0,1.05)
        ax2.tick_params(axis='both', which='major', labelsize=18, width=4, length = 15)
        ax2.tick_params(axis='both', which='minor', labelsize=8, width= 4, length = 10)    
        ax2.plot(x, prob, color=colors[6], marker='.', markersize=15, linewidth=3)
        ax2.plot(xw, pw, color=colors[0], marker='X', markersize=15, linewidth=3)
        ax2.set_ylabel('Total probability', fontsize=40)
    plt.savefig('unit_par.png')
    plt.close('all')    
    #plt.show()
    state='FINISHED'
    return state

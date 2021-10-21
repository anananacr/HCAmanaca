from mpl_toolkits.axes_grid1 import host_subplot
import math
import re
import scipy
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import cm
from colorspacious import cspace_converter
from collections import OrderedDict
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import csv
import subprocess as sub
import seaborn as sns
import mpl_toolkits.axisartist as AA
#from PIL import Image, ImageDraw
import os
import matplotlib.image as mpimg

def plot_fig():

	#find data
	data_dir='./'
	sns.set_context("paper")
	rx = re.compile(r'XSCALE\.(LP)')
	r = []
	for path, dnames, fnames in os.walk(data_dir):
		r.extend([os.path.join(path, x) for x in fnames if rx.search(x)])
	#print(r)
	r=sorted(r)
	#print(r[0][13:17])
	#label thr
	tmp=[]
	number=""
	
	for i in r:
		number=i[13:17]
		tmp.append(number)
	labels=tmp

	#plot art
	#colors=['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00', 'darkcyan','maroon','indigo','magenta', 'seagreen', 'saddlebrown','yellow','springgreen','coral']

	rate=['COMPLETENESS', 'R-meas','CC(1/2)']
	name=['compl','rmeas','cchalf']
	param=0
	g=open('resumo.tab','w+')
	#grep fig in XSCALE.LP
	for k in rate:
		#new fig
		fig = plt.figure(figsize=(7, 6), tight_layout=True)
		ax = fig.add_subplot(1,1,1)
		count=0

		for i in r:

			f=open('tmp.tab','w+')
			resumo=sub.run('grep -A23 "COMPLETENESS" '+i, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
			f.write(resumo.stdout.decode('utf-8'))
			f.close()

			#open data
			data_path = os.path.join(data_dir+'tmp.tab')
			data= pd.read_csv(data_path, delimiter=' ', usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12,13), skipinitialspace=True)
			#print(data)
			df=pd.DataFrame(data, columns=[k,'RESOLUTION'])
			res=df['RESOLUTION'].to_list()
			score=df[k].to_list()
			res=res[1:-1]
			score=score[1:-1]

			tmp=[]
			number=''
			for j in score:
				number=j[0:-1]
				tmp.append(float(number))
			score=tmp
			tmp=[]
			for j in res:
				number=j
				tmp.append(float(number))
			res=tmp

			g.write('Threshold '+str(i[13:17])+'\nd(Å) '+str(k)+'\n')
			for j in range(len(score)):
				g.write(str(res[j])+' '+str(score[j])+'\n')
			#print(res,score)
			#ax.plot(res,score, color=colors[count],marker='o', linestyle='-', label=labels[count])
			ax.plot(res,score, marker='o', linestyle='-', label=labels[count])
			ax.set_ylabel(k, fontsize=16)
			plt.gca().invert_xaxis()
			ax.set_xlabel('Resolution (Å)', fontsize=16)
			ax.tick_params(axis='both', which='major', labelsize=14)
			ax.tick_params(axis='both', which='minor', labelsize=8)
			count+=1
			if k=='CC(1/2)':
				ax.set_ylabel('$CC_{1/2}$', fontsize=16)
			if k=='R-meas':
				ax.set_ylabel('$R_{meas}$', fontsize=16)
				ax.set_ylim(-10,100)
		#plt.show()
		ax.legend(fontsize=12)
		plt.savefig(name[param]+'.png')
		param+=1

	g.close()


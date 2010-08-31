#!/usr/bin/python


#
# Takes the output of a reflex load balancer and generates gnuplot files
# for each network / interface.
#
# pipe through shell for plot
# ./route.py file | sh



import sys
from os import system, remove

if (len(sys.argv) != 2):
  print "No args: route.py filename"
  exit(0)

try:
  fdesc = open(sys.argv[1])
except IOError:
  print "File open error"
  exit(0)

networks = {}

for line in fdesc:
  elements = line.strip().split(" ");
  
  if elements[0] not in networks:
    networks[elements[0]] = {}

  if elements[1] not in networks[elements[0]]:
    networks[elements[0]][elements[1]] = []

  networks[elements[0]][elements[1]].append([elements[2], elements[3], elements[4]])

#this creates list for each network/port pair
for network, portlist in networks.iteritems():
  for port, list in portlist.iteritems():
    newfile = open (network+"-"+port+".tr", 'w')
    for entry in list:
      newfile.write( str(entry[0])+" "+str(entry[1])+" "+str(entry[2])+"\n")
    newfile.close()

#now we need to generate the gnuplot files
fwnd_plot = ["u ($1/1000):2 with lines lt "," lw 3 t 'Path "]
loss_plot = ["u ($1/1000):3 with lines lt "," lw 3 t 'Path "]

labels_fwnd = "set ylabel 'Ratio'\nset xlabel 'Time(sec)'\nset yrange [0:1]\n"
labels_loss = "set ylabel 'Ratio'\nset xlabel 'Time(sec)'\n"

replot = False

for network, portlist in networks.iteritems():
  fwndfile = open (network+"-fwnd.gnu", 'w')
  lossfile = open (network+"-loss.gnu", 'w')
  plotfwnd  = "gnuplot -persist "+network+"-fwnd.gnu"
  plotloss  = "gnuplot -persist "+network+"-loss.gnu"
  print plotfwnd
  print plotloss
  for port, list in portlist.iteritems():
    if(replot):
      fwndfile.write("replot '"+network+"-"+port+".tr' "+fwnd_plot[0]+port+fwnd_plot[1]+port+"'\n")
      lossfile.write("replot '"+network+"-"+port+".tr' "+loss_plot[0]+port+fwnd_plot[1]+port+"'\n")
    else:
      fwndfile.write("set title '"+network+" Fwnd graph'\n")
      fwndfile.write(labels_fwnd)
      fwndfile.write("plot '"+network+"-"+port+".tr' "+fwnd_plot[0]+port+fwnd_plot[1]+port+"'\n")

      lossfile.write("set title '"+network+" Loss graph'\n")
      lossfile.write(labels_loss)
      lossfile.write("plot '"+network+"-"+port+".tr' "+loss_plot[0]+port+loss_plot[1]+port+"'\n")
      replot = True
  replot = False


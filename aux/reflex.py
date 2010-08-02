#!/usr/bin/python

#
# Takes the trace of ipv4 packets forwarded by node and 
# generates plots respective losses and tput by interface
#
# pipe through shell for plot
# 

import os
import sys

class InterfaceTraffic:
  REFLEX_CODEPOINT_MAX = 8

  def __init__(self, interfaceNum):
    self.interfaceNum = int(interfaceNum)
    self.filename = ".interface"+str(interfaceNum)+".sampled"
    self.out = open(self.filename,'w')
    self.counter = [0]*InterfaceTraffic.REFLEX_CODEPOINT_MAX

  def update(self, codepoint, value):
    self.counter[codepoint] += value

  def output(self, time, interval):

    self.out.write(str(time))
    #gives data/time  metric
    for bytes in self.counter:
      self.out.write(' '+str(bytes/sample))
    self.out.write('\n')
    #clear counters
    self.counter = [0]*InterfaceTraffic.REFLEX_CODEPOINT_MAX
     
if (len(sys.argv) != 2):
  print "Wrong args: "+sys.argv[0]+" filename"
  exit(0)

try:
  fdesc = open(sys.argv[1])
except IOError:
  print "File open error"
  exit(0)

sample = 0.5
# time is in nanoseconds
timescale =  1000000000
interval = sample * timescale
starttime = 0.0
endtime = starttime + interval
counters = {}

for line in fdesc:
  elements = line.split(" ");

  if (len(elements) != 4):
    break

  # trace structure
  interfaceNum = int(elements[0])
  currtime = float(elements[1])
  reflex = int(elements[2])
  bytesize = int(elements[3])

  # print to file current data
  if currtime > endtime:
    for interface in counters:
      counters[interface].output(starttime/timescale, interval)
    endtime += interval
    while ( currtime > endtime ):
      endtime += interval
    starttime = endtime - interval
  
  #update counter
  try:
    counters[interfaceNum].update(reflex,bytesize)
  except KeyError:
    counters[interfaceNum] = InterfaceTraffic(interfaceNum)
    counters[interfaceNum].update(reflex,bytesize)
    
#end of file
counters[interface].output(starttime/timescale, interval)

#now we need to generate the gnuplot files
tput_plot = ["u 1:(($7+$8+$2+$6)*8/1000000) with lines lt "," lw 3 t 'Throughput "]
lecho_plot = "u 1:(($6)*8/1000000) with lines lw 3 t 'FNE"
fne_plot = "u 1:(($8)*8/1000000) with lines lw 3 t 'Loss Echo"
#
labels = "set ylabel 'Mbps'\nset xlabel 'Time(sec)'\n"

replot = False

tputfile = open (".interfacestput.gnu", 'w')
tputfile.write("set title 'Throughput'\n")
tputfile.write(labels)

for interface in counters:
  #do per interface graph firts
  intstr = str(interface)
  interfacefile = open (".interface"+intstr+".gnu", 'w')
  plotinterfacefile  = "gnuplot -persist .interface"+intstr+".gnu"
  print plotinterfacefile
  interfacefile.write("set title 'Interface "+intstr+" outbound\n")
  interfacefile.write(labels)
  interfacefile.write("plot '.interface"+intstr+".sampled' "+tput_plot[0]+"1"+tput_plot[1]+"'\n")
  interfacefile.write("replot '.interface"+intstr+".sampled' "+lecho_plot+"'\n")
  interfacefile.write("replot '.interface"+intstr+".sampled' "+fne_plot+"'\n")

  if replot:
    tputfile.write("replot '.interface"+intstr+".sampled' "+tput_plot[0]+intstr+tput_plot[1]+ intstr+"\n")
  else:
    tputfile.write("plot '.interface"+intstr+".sampled' "+tput_plot[0]+intstr+tput_plot[1]+intstr+"\n")
    replot = True

plotinterfacestput  = "gnuplot -persist .interfacestput.gnu"
print plotinterfacestput

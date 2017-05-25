"""
https://github.com/frenky-strasak/My_bachelor_thesis
"""


# My bachelor thesis

##Introduction
My bachelor thesis is about detecting HTTPS malware by machine learning.
The main concentration is to ssl communication where is a lot of new 
challenges how to detect this behaviour. This thesis is related with
Stratosphere IPS project and Sebastian Garcia, who is leader of this 
projects (https://stratosphereips.org/).

Here is all code regarding my thesis.
At this moment there is first project 'Features_evaluating' which goes 
into data sets and creates features for machine learning.
Second project will be some machine learning algorithm (neural network, 
SVM, regression, ...).

The result of this thesis should be find some new features and techniques
which helping to detect malware.

##Features_evaluating project
This project is for evaluating features. It goes into data sets and computes
some features.

###Description
What is dataset?
I define two types of dat sets: 'single dataset' and 'multi dataset'.
##### Single data set
It is folder which has to contain following attributes:
######1. Pcap file
   You can get it from Wireshark, which is able to store your internet
   traffic in packets.
   https://www.wireshark.org/
######2. Labeled binetflow file
   Argus is able to extract the pcap file to binetflow file. There are just
   flows but no payload data which are sensitive.
   http://qosient.com/argus/
######3. Bro folder
   Bro folder contains several logs file and each of them describes some
   level in internet traffic (conn.log, dns.log, ssl.log, ...). There is no
   sensitive data.
   This folder is created by Bro which also extract the pcap file and creates 
   this bro folder.
   https://www.bro.org/

So each folder which contains these three items (pcap file, binetflow file, 
Bro folder) is 'single data set'.

##### Multi data set
It is folder containing at the least one 'single dataset'.

##### Why this distribution by 'single dataset' and 'multi dataset'?
Usually when you create some data from internet traffic, you create
just one type of connection (one ip connects somewhere) but it is not enough.
So we need a lot of these single data sets as malware, normal and compute them
together.

### Features
Invent some new features is the main target of this project. At the end we should use
the best of them.

List of current modules for features:
######1. 'State of connection'
states: S0, S1, SF, REJ, S2, S3, RSTO, RSTR, RSTOS0, RSTRH, SH, SHR, OTH,
module for creating plot data: 'create_plot_data_file_2()' in 'EvaluateData.py'
script for plotting: 'ShowFigureBar.py'

###Usage
First of fall you should set configure file. There is two values:
######1. path_to_single_dataset - It is path to your single data set.
######2. path_to_multi_dataset - It is path to your multi data set. 

There are 2 options: 'Main_single.py' and 'Main_multi.py'.
######1. python  Main_single.py  name_of_created_plot_data.txt
First it takes your argument, which is name of the result. If there is no 
argument, the name of the result data file will be default 'new_plot_data.txt'.
Next it looks into config file for 'path_to_single_dataset', which is path to 'single data file'.

Now it starts the evaluating. First it goes to binetflow.file where I take all flows,
which has malware label ('Botnet'). Next it goes into bro folder for logs such as conn.log,
ssl.log, where are all flows for our usage. It evaluates and computes current features.

Last step is creating plot data file. This file is located in 'PlotData' directory.

######2. python  Main_multi.py  name_of_created_plot_data
It is same like above, but evaluating is done for each 'single data sets'.
So the resulting plot data file contains data from all 'single data sets'.

###Plotting the 'plot data file'
Once you choose one of these Main files and it creates the resulting
'plot data file' you can plot it by scripts in 'Plotdata' directory.

There are several scripts for plotting and each of them plots something different.
It depends which feature you computes and which resulting 'plot data file' you created.
 
Example:
The first evaluate feature is 'State of connection'. 
So for plotting this feature you call: 'python ShowFigureBar.py' name_of_resulting_plot_data.txt
This command should show you chart contains data from dataset(s) relating to 'State of connection'.

For this viewing charts is used matplotlib library : http://matplotlib.org/

### TODO
######1. Try next a new features
######2. Complete datasets (There is no normal flows) 
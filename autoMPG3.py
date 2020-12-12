#Zane Heald - March 4, 2020 - This program will read a file from the specified url write a file, clean that file and create the defined classes line by line. This info will then be graphed or written to a file based on specified command line arguments.
import csv
from collections import namedtuple
import os
import operator
import requests
import argparse
import logging
import argparse
import sys
from collections import defaultdict
import matplotlib.pyplot as plt

logger = logging.getLogger() #initialize logging
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('autoMPG2.log', 'w') #specify that at the debug level log commits will be written this file
fh.setLevel(logging.DEBUG)
logger.addHandler(fh) #adds the fh handler to logging at the debug level

sh = logging.StreamHandler()
sh.setLevel(logging.INFO) #specify that the info level logging will be displayed on the console
logger.addHandler(sh) #adds the sh handler to logging at info level



class autoMPG: #create the autompg class

    def __init__ (self,make,model,year,mpg):
        self.make = make
        self.model = model
        self.year = year
        self.mpg = mpg
        logging.debug("Object autoMPG({},{},{},{}) was created".format(self.make, self.model, self.year, self.mpg)) #logging call that writes all objects made in this class to the logging file specified above

    def __repr__(self):
        return "autoMPG({},{},{},{})".format(self.make, self.model, self.year, self.mpg)

    def __str__(self):
        return "({},{},{},{})".format(self.make, self.model, self.year, self.mpg)

    def __eq__(self,other): #test if two items are equal
        logging.info("Equal function was called on {} and {}".format(self,other)) #if this function is used it will be logged at the info level
        if type(self) == type(other): #confirm that they are both within the class
            if self.make != other.make: #If ladder to check item term by term returning - assumes true and proves false
                return False
            if self.model != other.model:
                return False
            if self.year != other.year:
                return False
            if self.mpg != other.mpg:
                return False
            else:
                return True #if equivelancy has not been proven false then it is true and the items are equivalant
        else:
            return NotImplemented #returns this if types are not the same - not both items of the class


    def __lt__(self,other): #Checks items one by one to see if one is less than the other
        logging.info("Less than function was called on {} and {}".format(self,other)) #if the less than funtion is called it will be logged at the info level here
        if type(self) == type(other): # confirms both are from the same class
            if self.make > other.make: #if ladder confirming that none of the four args are greater than the other ones
                return False
            if self.model > other.model:
                return False
            if self.year > other.year:
                return False
            if self.mpg > other.mpg:
                return False
            if self.__eq__(other) is True: #if none of the items are greater than check to see if the classes are equvalant using the above func
                return False
            else:
                return True # if the self item is not greater than or equal to the other item then it therefore must be less than that item
        else:
            return NotImplemented #returns this if types are not the same - not both items of the class


    def __hash__(self):
        logging.info("Hash function was called on {}".format(self)) #if the hash function is called it will be logged at the info level
        return hash((self.make, self.model, self.year, self.mpg)) #returns a hash value of the arguments / class



class autoMPGData:

    def __init__(self,data = []): #initialize the argument as an empty list
        self.data = data
        self.load_data() #calls the load data function to fill the empty list

    def __str__(self): #used this to check if the data item was being filled correctly
        return "({})".format(self.data)

    def __iter__(self):
        return iter(self.data)

    def load_data (self):
        if os.path.exists('auto-mpg.data.txt') is False: #checks if the autompg raw data already exists as a file
            self._get_data() #if the file doesn't exist it calls get data to create that file for use
        if os.path.exists('auto-mpg.clean.txt') is False: #check if the cleaned data already exists
            self.clean_data() #if cleaned data does not exist then create it through clean data
        with open('auto-mpg.clean.txt','r') as data: #once the clean data exists open it for use
            report = namedtuple('Report', 'mpg,cylinders,displacement,horsepower,weight,acceleration,model_year,origin,car_name') #create a named tuple with the 9 items contained in the data set
            reader = csv.reader(data, delimiter=' ') #reads the data opend deliminating by spaces
            lines = []
            for l in reader: #line by line loop through the read data
                list = []
                for x in l: #loop through each item in the list representing one line of data
                    if x != '': #remove all spaces from the list so that we are left with only the data needed
                        list.append(x) #a list with one line of data
                lines.append(list) #create list with all lines of data where each line is a list of length 8 (9 items)
            tups = []
            for i in lines: #loop through the list of lines
                tup = report(*i) #change every line from a list to the named tuple
                tups.append(tup) #add these named tuples to a list - contains all lines read as named tuples
            for i in tups: #loop through the list of tuples to create autoMPG class items
                make_model = i.car_name
                loc = make_model.find(" ") #find the space as an indicator of the end of make and begining of model
                make = make_model[:loc] #seperate make
                model = make_model[loc+1:] #seperate model
                obj = autoMPG(make,model,int(i.model_year),float(i.mpg)) #turn the four desired items into an autoMPG class
                self.data.append(obj) #store these objects in self.data
        logging.info("Data was loaded from auto-mpg.clean.txt") #logs that the data was read and loaded as AutoMPG classes appropriatley

    def clean_data(self): #if clean data does not already exist this will be called to create cleaned data
        with open('/Users/zaneheald/Desktop/auto-mpg.data.txt','r') as data: #read in the unclean data
            cleanData = open('auto-mpg.clean.txt','w') #open the file that cleaned data will be written to
            reader = csv.reader(data, delimiter=',') #read the uncleaned data file seperating by commas
            for line in data:
                line = line.replace('chevy','chevrolet')
                line = line.replace('chevroelt','chevrolet')
                line = line.replace('maxda','mazda')
                line = line.replace('mercedes-benz','mercedes')
                line = line.replace('toyouta','toyota')
                line = line.replace('vokswagen','volkswagen')
                line = line.replace('vw','volkswagen')
                line = line.expandtabs() #turn tabs into spaces
                line = line.strip('\n') #strip new lines from each line
                cleanData.write('{}\n'.format(line)) #Write each cleaned line back to the clean data file
            cleanData.close()
        logging.info("Data was loaded and cleaned from auto-mpg.data.txt") #logs that the data was cleaned at the info level


    def _get_data (self): #function to read data from a URL to create a txt file
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data' #specified url containing the data
        onlineDat = requests.get(url) #uses the request module to read the data from the url
        open('auto-mpg.data.txt', 'wb').write(onlineDat.content) #writes the data read from the URL to the the txt file
        logging.info("auto-mpg.data.txt was created from URL") #logs that data was read from the URL and created a txt file at the info level

    def sort_by_default(self):
        self.data.sort(key=operator.attrgetter('make','model','year','mpg')) #sorts self.data by make then model then year then mpg
        logging.info("Data output was sorted (default)") #logs that the data was sorted in this method at the info level

    def sort_by_year (self):
        self.data.sort(key=operator.attrgetter('year','make','model','mpg')) #sorts self.data by year then make then model then mpg
        logging.info("Data output was sorted (Year)") #logs that the data was sorted in this method at the info level

    def sort_by_mpg (self):
        self.data.sort(key=operator.attrgetter('mpg','make','model','year')) #sorts self.data by mpg then make then model then year
        logging.info("Data output was sorted (MPG)") #logs that the data was sorted in this method at the info level

    def mpg_by_year (self):
        mpgYearDict = defaultdict(lambda:[])
        for tup in self.data:
            mpgYearDict[tup.year].append(tup.mpg)
        for k,v in mpgYearDict.items():
            average = sum(v)/len(v)
            mpgYearDict[k] = average
        return mpgYearDict
        logging.debug("Average MPG was calulated by Year")

    def mpg_by_make (self):
        mpgMakeDict = defaultdict(lambda:[])
        for tup in self.data:
            mpgMakeDict[tup.make].append(tup.mpg)
        for k,v in mpgMakeDict.items():
            average = sum(v)/len(v)
            mpgMakeDict[k] = average
        return mpgMakeDict
        logging.debug("Average MPG was calulated by Make")




def main():
    parser = argparse.ArgumentParser() #initiate arg parsing
    parser.add_argument('--sort','-s', choices=['mpg','year','default'], help = 'Select method to sort auto data') #create the sort argument requireing specification to sort by mpg year or default
    parser.add_argument('--ofile','-o', metavar='<outfile>', type=str, help = 'Indicate the desired output file to write data to')
    parser.add_argument('-p','--plot',dest='do_plot',action='store_true')
    parser.add_argument('--mpgDict','-d', choices=['make','year'], help = 'Indicate if you would like to return a dictionary of average MPG sorted by make or year')
    parser.add_argument('command', metavar='<command>', choices=['print'], help='command to execute') #create the required print argument
    args = parser.parse_args() #pull out the args that the user passed in

    x = autoMPGData() #create a list of Autompg hands (call the autoMPGData)

    if args.command == 'print':
        if args.sort == 'mpg': #check which sort choice was passed in
            x.sort_by_mpg() #if MPG was passed in sort using the MPG function in AutoMPGData
        if args.sort == 'year':  #check which sort choice was passed in
            x.sort_by_year() #if Year was passed in sort using the Year function in AutoMPGData
        if args.sort == 'default': #check which sort choice was passed in
            x.sort_by_default() #if Year was passed in sort using the Year function in AutoMPGData
        if args.ofile is not None:
            with open(args.ofile, 'w') as file:
                file.write('Make,Model,Year,MPG\n')
                for i in x:
                    file.write('{},{},{},{}\n'.format(i.make,i.model,i.year,i.mpg))
        else:
            for i in x:
                sys.stdout.write('{},{},{},{}\n'.format(i.make,i.model,i.year,i.mpg))


    outdict = None
    if args.mpgDict == 'make':
        dictMake = x.mpg_by_make()
        listMake = []
        for i in sorted (dictMake.keys()) :
            listMake.append((i,dictMake[i]))
        outdict = listMake
        title = 'Average MPG by Make'
        if args.do_plot:
            xList = []
            yList = []
            for x,y in outdict:
                xList.append(x)
                yList.append(y)
            plt.scatter(xList, yList,alpha = .5)
            plt.title('{}'.format(title))
            plt.xlabel('Make')
            plt.ylabel('Avg MPG')
            plt.show()
    if args.mpgDict == 'year':
        dictYear = x.mpg_by_year()
        listYear = []
        for i in sorted (dictYear.keys()) :
            listYear.append((i,dictYear[i]))
        outdict = listYear
        title = 'Average MPG by Year'
        if args.do_plot:
            xList = []
            yList = []
            for x,y in outdict:
                xList.append(x)
                yList.append(y)
            plt.scatter(xList, yList,alpha = .5)
            plt.title('{}'.format(title))
            plt.xlabel('year')
            plt.ylabel('Avg MPG')
            plt.show()
    if outdict is not None and args.ofile is not None:
        with open(args.ofile, 'a') as file:
            file.write('{}\n'.format(title))
            for i in outdict:
                file.write('{},{}\n'.format(i[0],i[1]))
    elif outdict is not None:
        for i in outdict:
            sys.stdout.write('{},{}\n'.format(i[0],i[1]))



if __name__ == '__main__':
    main()

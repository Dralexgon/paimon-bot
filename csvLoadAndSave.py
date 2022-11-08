import csv

def saveCsv(nameOfCsvFile,lines):
	with open(nameOfCsvFile+".csv", 'w', newline='') as csvfile:
		spamwriter=csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for line in lines:
			lineForCsv="[\""+str(line[0])+"\"]"
			for i in range(1,len(line)):
				lineForCsv=lineForCsv+"+[\""+str(line[i])+"\"]"
			spamwriter.writerow(eval(lineForCsv))

def saveCsv2(nameOfCsvFile,*lines):
	with open(nameOfCsvFile+".csv", 'w', newline='') as csvfile:
		spamwriter=csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for line in lines:
			lineForCsv="[\""+str(line[0])+"\"]"
			for i in range(1,len(line)):
				lineForCsv=lineForCsv+"+[\""+str(line[i])+"\"]"
			spamwriter.writerow(eval(lineForCsv))
def loadCsv(nameOfCsvFile):
	load=[]
	ICanLoad=True
	try:
		inventory=[]
		with open(nameOfCsvFile+".csv", newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
			for row in spamreader:
				tempList=';'.join(row)
				tempList=tempList.split(';')
				load.append(tempList)
	except:
		ICanLoad=False
	return ICanLoad,load
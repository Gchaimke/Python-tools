import os
import xlrd

def searchFiles(folderPath):
	myFilesList=[]
	for root, dirs, files in os.walk(folderPath):
		for file in files:
			if file.endswith(".xlsx"):
				if os.path.basename(file)[0]!="~":
					myFilesList.append(os.path.join(root, file))
	return myFilesList
 
def findCell(sh, searchedValue):
	for row in range(sh.nrows):
		for col in range(sh.ncols):
			if sh.cell_value(row, col) == str(searchedValue):
				return True
			if sh.cell_value(row, col) == searchedValue:
				return True
	return False

def findAll(filePath, searchedValue):
	try:
		book =xlrd.open_workbook(filePath)
		sheet = book.sheet_by_name("Sheet1")
		if(findCell(sheet, searchedValue)):
			return True
	except:
		print("An exception occurred in "+os.path.basename(filePath)[0:-5])
	return False

def saveToTxt(system, rf):
	f = open("search_result.txt", "a")
	f.write(system+"," + rf+"\n")
	f.close()
	
def start():
	a =[i for i in range(19031500048,19031500063)]
	a = a + [i for i in range(19062400033,19062400048)] + [i for i in range(19061300001,19061300021)]
	a = a + [i for i in range(19070500129,19070500154)] + [i for i in range(19070500154,19070500179)]
	a = a + [i for i in range(19073000001,19073000026)] + [i for i in range(19080500255,19080500285)]
	a = a + [i for i in range(19081300153,19081300193)] + [i for i in range(19040900122,19040900132)]
	startPath = "G:\\Advantech\\# Archive\\@Clients\\D-FEND\\Production\\Production 2019"
	startPath2 = "G:\\Advantech\\# Archive\\@Clients\\D-FEND\\Production\\Production 2020"
	fileList = searchFiles(startPath)+searchFiles(startPath2)
	saveToTxt("System SN","RF SN")
	for search in a:
		for file in fileList:
			print("search in "+file+" for "+ str(search))
			if findAll(file,search):
				fileList.remove(file)
				saveToTxt(os.path.basename(file)[0:-5],str(search))

def debug():
	a = [i for i in range(19081300155,19081300160)] +[i for i in range(19072600032,19072600036)]+[i for i in range(19072600018,19072600021)]
	startPath ="C:\\Users\\gchaim\\Desktop\\Excel Search\\debug"
	startPath2 ="C:\\Users\\gchaim\\Desktop\\Excel Search\\debug2"
	saveToTxt("System SN","RF SN")
	fileList = searchFiles(startPath)+searchFiles(startPath2)
	for search in a:
		for file in fileList:
			print("search in "+file+" for "+ str(search))
			if findAll(file,search):
				fileList.remove(file)
				saveToTxt(os.path.basename(file)[0:-5],str(search))

start()
#debug()
input('Press ENTER to exit')
#searchFiles()

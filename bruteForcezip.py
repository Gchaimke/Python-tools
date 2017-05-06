#Scripter: Chaim Gorbov
#Using: bruteForcezip.py -f your-zip-path -c 2 -m 4 -x 5
#Date: 06.05.2017
#Python: 3.6
from itertools import product
import optparse
import zipfile
import time
import sys


#parse arguments
parser = optparse.OptionParser()
parser.add_option('-f', '--file', action="store", dest="file_path", help="Zip File Path", default=None)
parser.add_option('-c', '--chars', action="store", dest="charsSet", help="1 = a-z ; 2 = a-z + 1-9 ; 3 = a-z+1-9+A-Z", default=3)
parser.add_option('-m', '--min', action="store", dest="min", help="minimum digits", default=1)
parser.add_option('-x', '--max', action="store", dest="max", help="minimum digits", default=5)
options, args = parser.parse_args()



def main(file_path,charsSet,min,max):
	chars = ''
	if(charsSet == '1'):
		chars = 'abcdefghijklmnopqrstuvwxyz'
	elif(charsSet == '2'):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
	elif(charsSet == '3'):
		chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' # chars to look for
	
	try:
		zip_ = zipfile.ZipFile(file_path)
	except zipfile.BadZipfile:
		print ("Please check the file's path. It doesn't seem to be a zip file.")
		quit()
	
	i = 0 #password count
	startTime = time.time() #start time
	for length in range(int(min), int(max)): # only do lengths of 1 + 2
		to_attempt = product(chars, repeat=length)
		for attempt in to_attempt:
			i += 1 #increment the password try count
			password = ''.join(attempt)
			sys.stdout.write("\r Current password: {0}  Total tested: {1} \r".format(password , i))
			sys.stdout.flush()
			try:
				zip_.extractall(pwd=bytes(password, encoding='utf-8')) #try the password
				totalTime = time.time() - startTime #total time
				print ("\nPassword cracked: %s\n" % password )#print the password
				print ("Took %f seconds to crack the password. That is, %i attempts per second." % (totalTime,i/totalTime)) #stats
				exit(0) #stop the script
			except Exception:
				pass
		print ("Sorry, password not found.")

if __name__ == '__main__':
	main(options.file_path, options.charsSet, options.min, options.max)

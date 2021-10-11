import os
folder = 'customers'
max = 5
csv = open(folder+".csv", "w")
csv.write("Customer ID,File Path\n")
for dirname, dirnames, filenames in os.walk(folder):
    # print path to all filenames.
    for filename in filenames:
        csv.write(dirname.replace(folder+'\\', "")+"," +
                  os.path.join(dirname, filename)+"\n")
    if max == 0:
        break
    max -= 1
csv.close()

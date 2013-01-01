import csv
import datetime

if __name__ == '__main__':
	r = csv.reader(open('/home/jliao2/Documents/data-set/livelab/apps/a01.csv', 'rb'), delimiter=',')
	data = []
	apps = {}
	for item in r:
		if item[0] == 'SpringBoard': continue
		data.append([item[0], int(item[1])])
	
	sorted(data, key=lambda x: x[1])
	ts_start = datetime.datetime.fromtimestamp(data[0][1])
	ts_end = datetime.datetime.fromtimestamp(data[len(data)-1][1])
	ndays = (ts_end - ts_start).days + 1
	print ndays
	for item in data:
		if item[0] not in apps.keys(): 
			apps[item[0]] = [[0 for i in range(24)] for j in range(ndays)]
		d = datetime.datetime.fromtimestamp(item[1])
		#print (d-ts_start).days
		apps[item[0]][(d-ts_start).days][d.hour] += 1

	w = csv.writer(open('ts_grid.csv', 'wb'), delimiter=',')	
	for l in apps['com.apple.MobileSMS']:
		print l
		w.writerow(l)
	


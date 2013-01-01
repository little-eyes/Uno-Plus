import csv
import datetime
import sys

def load(path):
	data = []
	r = csv.reader(open(path, 'rb'), delimiter=',')
	n = m = 0
	for d in r:
		n += 1
		if d[4] == '0': 
			m += 1
			continue
		data.append([int(d[2]), int(d[3])])
	print n, m
	return data

def hist_by_hour(data, opath):
	bucket = [0 for i in range(24)]
	for r in data:
		d = datetime.datetime.fromtimestamp(float(r[0]))
		ts = d.hour
		bucket[ts] += r[1]/1000.0
	w = csv.writer(open(opath, 'wb'), delimiter=',')
	w.writerow(bucket)

def hist_by_minute(data, opath):
	bucket = [0 for i in range(24*60)]
	for r in data:
		d = datetime.datetime.fromtimestamp(float(r[0]))
		ts = d.hour*60 + d.minute
		bucket[ts] += r[1]/1000.0
	w = csv.writer(open(opath, 'wb'), delimiter=',')
	w.writerow(bucket)

if __name__ == '__main__':
	p = '/home/jliao2/Documents/data-set/livelab/sleep/'
	data = load(p + sys.argv[1])
	hist_by_hour(data, p + sys.argv[2])
	hist_by_minute(data, p + sys.argv[3])

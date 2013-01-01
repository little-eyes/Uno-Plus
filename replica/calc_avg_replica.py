import csv

if __name__ == '__main__':
	results = ['a01_rf.csv', \
			'a02_rf.csv', \
			'a03_rf.csv', \
			'a04_rf.csv', \
			'a05_rf.csv', \
			'a06_rf.csv', \
			'a07_rf.csv', \
			'a08_rf.csv', \
			'a09_rf.csv', \
			'a10_rf.csv', \
			'a11_rf.csv', \
			'b02_rf.csv', \
			'b03_rf.csv', \
			'b04_rf.csv', \
			'b05_rf.csv', \
			'b06_rf.csv', \
			'b07_rf.csv', \
			'b08_rf.csv', \
			'b09_rf.csv', \
			'b10_rf.csv', \
			'b11_rf.csv']
	for r in results:
		w = csv.reader(open(r, 'rb'), delimiter=',')
		data = []
		mx = -1
		mi = 100
		for item in w:
			for j in range(1, len(item)):
				#if float(item[j]) < 8.0 and float(item[j]) > 0.0:
				data.append(float(item[j]));
		for i in range(len(data)):
			if data[i] > mx: mx = data[i]
			if data[i] > 0 and data[i] < mi: mi = data[i]
		avg = sum(data) * 1.0/len(data)
		print "%f,%f,%f" % (mi, avg, mx)

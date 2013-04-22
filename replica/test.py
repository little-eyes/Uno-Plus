import replica
import csv

def read_status(owner, path):
	r = csv.reader(open(path, 'rb'), delimiter=',')
	data = []
	for row in r:
		if row[4] == '1': continue # sleep = 1
		d = {'owner':owner, 'timestamp':int(row[2]), 'duration':int(row[3])}
		data.append(d)
	return data

def read_app(owner, path):
	r = csv.reader(open(path, 'rb'), delimiter=',')
	data = []
	for row in r:
		if row[0] == 'SpringBoard': continue
		d = {'owner':owner, 'name':row[0], 'timestamp':int(row[1]), 'duration':int(row[2])}
		data.append(d)
	return data

if __name__ == '__main__':
	'''
	trace = {}
	trace['data'] = read_data('/home/jliao2/Documents/data-set/livelab/sleep/a01.csv')
	trace['id'] = 'a01'
	app = {}
	app['data'] = read_app('/home/jliao2/Documents/data-set/livelab/apps/a01.csv')
	app['id'] = 'a01'
	#psp = replica.PhoneStatusProvider(trace, time_slot=60*60)
	#bd = psp.analyze(length=len(trace['data']))
	#x = [0] * len(bd[0])
	#for i in range(len(bd[0])):
	#	x[i] = bd[0][i]*1.0/bd[1]/3600
	#print x
	#print psp.query(1266247857+1)
	aup = replica.AppUsageProvider(app, time_slot=60*60)
	f = aup.analyze_frequency()
	for l in f.keys():
		print l,	f[l]
	'''
	app_traces = {
		'a01' : read_app('a01', '/home/jliao2/Documents/data-set/livelab/apps/a01.csv'),
		'a02' : read_app('a02', '/home/jliao2/Documents/data-set/livelab/apps/a02.csv'),
		'a03' : read_app('a03', '/home/jliao2/Documents/data-set/livelab/apps/a03.csv'),
		'a04' : read_app('a04', '/home/jliao2/Documents/data-set/livelab/apps/a04.csv'),
		'a05' : read_app('a05', '/home/jliao2/Documents/data-set/livelab/apps/a05.csv'),
		'a06' : read_app('a06', '/home/jliao2/Documents/data-set/livelab/apps/a06.csv'),
		'a07' : read_app('a07', '/home/jliao2/Documents/data-set/livelab/apps/a07.csv'),
		'a08' : read_app('a08', '/home/jliao2/Documents/data-set/livelab/apps/a08.csv'),
		'a09' : read_app('a09', '/home/jliao2/Documents/data-set/livelab/apps/a09.csv'),
		'a10' : read_app('a10', '/home/jliao2/Documents/data-set/livelab/apps/a10.csv'),
		'a11' : read_app('a11', '/home/jliao2/Documents/data-set/livelab/apps/a11.csv'),
		'b02' : read_app('b02', '/home/jliao2/Documents/data-set/livelab/apps/b02.csv'),
		'b03' : read_app('b03', '/home/jliao2/Documents/data-set/livelab/apps/b03.csv'),
		'b04' : read_app('b04', '/home/jliao2/Documents/data-set/livelab/apps/b04.csv'),
		'b05' : read_app('b05', '/home/jliao2/Documents/data-set/livelab/apps/b05.csv'),
		'b06' : read_app('b06', '/home/jliao2/Documents/data-set/livelab/apps/b06.csv'),
		'b07' : read_app('b07', '/home/jliao2/Documents/data-set/livelab/apps/b07.csv'),
		'b08' : read_app('b08', '/home/jliao2/Documents/data-set/livelab/apps/b08.csv'),
		'b09' : read_app('b09', '/home/jliao2/Documents/data-set/livelab/apps/b09.csv'),
		'b10' : read_app('b10', '/home/jliao2/Documents/data-set/livelab/apps/b10.csv'),
		'b11' : read_app('b11', '/home/jliao2/Documents/data-set/livelab/apps/b11.csv'),
		}
	status_traces = {
		'a01' : read_status('a01', '/home/jliao2/Documents/data-set/livelab/sleep/a01.csv'),
		'a02' : read_status('a02', '/home/jliao2/Documents/data-set/livelab/sleep/a02.csv'),
		'a03' : read_status('a03', '/home/jliao2/Documents/data-set/livelab/sleep/a03.csv'),
		'a04' : read_status('a04', '/home/jliao2/Documents/data-set/livelab/sleep/a04.csv'),
		'a05' : read_status('a05', '/home/jliao2/Documents/data-set/livelab/sleep/a05.csv'),
		'a06' : read_status('a06', '/home/jliao2/Documents/data-set/livelab/sleep/a06.csv'),
		'a07' : read_status('a07', '/home/jliao2/Documents/data-set/livelab/sleep/a07.csv'),
		'a08' : read_status('a08', '/home/jliao2/Documents/data-set/livelab/sleep/a08.csv'),
		'a09' : read_status('a09', '/home/jliao2/Documents/data-set/livelab/sleep/a09.csv'),
		'a10' : read_status('a10', '/home/jliao2/Documents/data-set/livelab/sleep/a10.csv'),
		'a11' : read_status('a11', '/home/jliao2/Documents/data-set/livelab/sleep/a11.csv'),
		'b02' : read_status('b02', '/home/jliao2/Documents/data-set/livelab/sleep/b02.csv'),
		'b03' : read_status('b03', '/home/jliao2/Documents/data-set/livelab/sleep/b03.csv'),
		'b04' : read_status('b04', '/home/jliao2/Documents/data-set/livelab/sleep/b04.csv'),
		'b05' : read_status('b05', '/home/jliao2/Documents/data-set/livelab/sleep/b05.csv'),
		'b06' : read_status('b06', '/home/jliao2/Documents/data-set/livelab/sleep/b06.csv'),
		'b07' : read_status('b07', '/home/jliao2/Documents/data-set/livelab/sleep/b07.csv'),
		'b08' : read_status('b08', '/home/jliao2/Documents/data-set/livelab/sleep/b08.csv'),
		'b09' : read_status('b09', '/home/jliao2/Documents/data-set/livelab/sleep/b09.csv'),
		'b10' : read_status('b10', '/home/jliao2/Documents/data-set/livelab/sleep/b10.csv'),
		'b11' : read_status('b11', '/home/jliao2/Documents/data-set/livelab/sleep/b11.csv'),
		}
	sim = replica.Simulator(app_traces, status_traces, 60*60*6)
	sim.run()
	

'''
This package is used to simulation the phone's acitivity and
the app usage replication algorithm.

Note:
	app is a dict.
		- app['owner']
		- app['name']
		- app['timestamp']
		- app['duration']
	status is a dict: ONLY wake status exists.
		- status['owner']
		- status['timestamp']
		- status['duration']

So their traces are a list of those dicts. Pay attention to them.
'''
import datetime
import math
import random
import csv
import replica

online = csv.writer(open('status.csv', 'wb'), delimiter=',')
bb = {}

class PhysicalDevice(object):
	'''
	This class is to simulate the device, including a phone's
	online/offline status, app usage, replication of other devices.
	'''
	def __init__(self, phone_id, status_tr, status_te, app_tr, app_te, time_slot):
		self._replication_table = {}
		self._status_trace = status_te
		self._status_trace_index = 0
		self._app_trace = app_te
		self._app_trace_index = 0
		self.status_provider = PhoneStatusProvider(phone_id, status_tr+status_te, time_slot) # provide full trace.
		self.status_provider.analyze(status_tr) # training only needs 1/2.
		self.app_usage_provider = AppUsageProvider(phone_id, app_tr, time_slot)
		self.app_usage_provider.analyze_frequency()
		self._time_slot = time_slot
		self._nchunks = int(math.ceil(24 * 60 * 60 / time_slot))
		self._phone_id = phone_id
	
	def get_time_slot(self):
		return self._time_slot
	
	def get_nchunks(self):
		return self._nchunks
	
	def get_phone_id(self):
		return self._phone_id
		
	def get_storage_map(self):
		return self._replication_table
	
	def replicate(self, app):
		'''backup a data from other device to this device.'''
		if app['owner'] not in self._replication_table.keys():
			self._replication_table[app['owner']] = []
		if app['name'] not in self._replication_table[app['owner']]:
			self._replication_table[app['owner']].append(app['name'])
	
	def access(self, app):
		'''other device try to access the data, tell YES/NO.'''
		if not self.status_provider.query(app['timestamp']): return False
		if app['owner'] not in self._replication_table.keys(): return False
		if app['name'] not in self._replication_table[app['owner']]: return False
		return True
		
	def next_app(self):
		'''traverse the next app trace for testing replication.'''
		if self._app_trace_index == len(self._app_trace): return None
		self._app_trace_index += 1
		self.app_usage_provider.update(self._app_trace[self._app_trace_index-1])
		self._sync_status_timestamp()
		#print self._app_trace[self._app_trace_index-1]
		return self._app_trace[self._app_trace_index-1]
	
	def has_next_app(self):
		return self._app_trace_index < len(self._app_trace)
		
	def _sync_status_timestamp(self):
		k = self._status_trace_index
		for i in range(self._status_trace_index, len(self._status_trace)):
			k = i
			if self._status_trace[i]['timestamp'] > self._app_trace[self._app_trace_index-1]['timestamp']: 
				break
			self.status_provider.update(self._status_trace[i])
		self._status_trace_index = k


class PhoneStatusProvider(object):
	'''
	This class is to generate a phone's status from the trace.
	It supports initial statistics and future query.
	
	1. trace['data'] is a list of tuples: [(timestamp, duration), ...].
	2. trace['id'] is the phone id.
	3. time_slot is by second.
	'''
	def __init__(self, phone_id, trace, time_slot=60*60):
		print phone_id,trace[0]
		self._trace = sorted(trace, key=lambda t: t['timestamp'])
		self._phone_id = phone_id
		self._time_slot = time_slot
		self._nchunks = int(math.ceil(24 * 60 * 60 / time_slot))
		self._slot_board = [0.0] * self._nchunks
		self._last_datetime = None
		self._ndays = 0
	
	def analyze(self, trace_tr):
		self._ndays = (\
			datetime.datetime.fromtimestamp(trace_tr[len(trace_tr)-1]['timestamp'] + \
																			trace_tr[len(trace_tr)-1]['duration']) - \
			datetime.datetime.fromtimestamp(trace_tr[0]['timestamp'])).days
		for status in trace_tr:
			ts_start = datetime.datetime.fromtimestamp(status['timestamp'])
			ts_end = datetime.datetime.fromtimestamp(status['timestamp'] + status['duration'])
			self._last_datetime = ts_end
			ts_start_index = int((ts_start.second + ts_start.minute * 60 + ts_start.hour * 60 * 60)/self._time_slot)
			ts_end_index = int((ts_end.second + ts_end.minute * 60 + ts_end.hour * 60 * 60)/self._time_slot)
			#print ts_start_index, ts_end_index, self._trace[i]

			# case #1.
			if ts_end_index == ts_start_index:
				self._slot_board[ts_start_index] += status['duration']
			elif ts_end_index > ts_start_index:
				for i in range(ts_start_index, ts_end_index+1):
					if i == ts_start_index:
						tss_label = self._time_slot * (i + 1)
						tss_start = ts_start.second + ts_start.minute * 60 + ts_start.hour * 60 * 60
						assert(tss_label >= tss_start)
						self._slot_board[i] += (tss_label - tss_start)
					elif i == ts_end_index:
						tss_label = self._time_slot * i
						tss_end = ts_end.second + ts_end.minute * 60 + ts_end.hour * 60 * 60
						assert(tss_end >= tss_label)
						self._slot_board[i] += (tss_end - tss_label)
					else:
						self._slot_board[i] += self._time_slot
			# case #2.
			else:
				#print ts_start_index, ts_end_index, self._trace[i]
				ts_end_index += self._nchunks
				#print ts_start_index, ts_end_index, self._trace[i]
				for i in range(ts_start_index, ts_end_index+1):
					if i == ts_start_index:
						tss_label = self._time_slot * (i + 1)
						tss_start = ts_start.second + ts_start.minute * 60 + ts_start.hour * 60 * 60
						assert(tss_label >= tss_start)
						self._slot_board[i % self._nchunks] += (tss_label - tss_start)
					elif i == ts_end_index:
						tss_label = self._time_slot * i
						tss_end = 24 * 60 * 60 + ts_end.second + ts_end.minute * 60 + ts_end.hour * 60 * 60
						assert(tss_end >= tss_label)
						self._slot_board[i % self._nchunks] += (tss_end - tss_label)
					else:
						self._slot_board[i % self._nchunks] += self._time_slot
		
		s = 0.0
		tmp = []
		for i in range(self._nchunks):
			if self._ndays == 0:
				tmp.append(self._slot_board[i]/self._time_slot/365)
				s += self._slot_board[i]/self._time_slot/365
			else:
				tmp.append(self._slot_board[i]/self._ndays/self._time_slot)
				s += self._slot_board[i]/self._ndays/self._time_slot
		replica.online.writerow(tmp)
		print 'Avg Online Rate: %f' % (s/self._nchunks)
		#online.writerow([s/self._nchunks])
		return self._slot_board
	
	def update(self, status):
		self._ndays = (datetime.datetime.fromtimestamp(status['timestamp'] + status['duration'])\
									-	datetime.datetime.fromtimestamp(self._trace[0]['timestamp'])).days
		ts_start = datetime.datetime.fromtimestamp(status['timestamp'])
		ts_end = datetime.datetime.fromtimestamp(status['timestamp'] + status['duration'])
		self._last_datetime = ts_end
		ts_start_index = int((ts_start.second + ts_start.minute * 60 + ts_start.hour * 60 * 60)/self._time_slot)
		ts_end_index = int((ts_end.second + ts_end.minute * 60 + ts_end.hour * 60 * 60)/self._time_slot)
		
		# case #1.
		if ts_end_index == ts_start_index:
			self._slot_board[ts_start_index] += status['duration']
		elif ts_end_index > ts_start_index:
			for i in range(ts_start_index, ts_end_index+1):
				if i == ts_start_index:
					tss_label = self._time_slot * (i + 1)
					tss_start = ts_start.second + ts_start.minute * 60 + ts_start.hour * 60 * 60
					assert(tss_label >= tss_start)
					self._slot_board[i] += (tss_label - tss_start)
				elif i == ts_end_index:
					tss_label = self._time_slot * i
					tss_end = ts_end.second + ts_end.minute * 60 + ts_end.hour * 60 * 60
					assert(tss_end >= tss_label)
					self._slot_board[i] += (tss_end - tss_label)
				else:
					self._slot_board[i] += self._time_slot
		# case #2.
		else:
			#print ts_start_index, ts_end_index, self._trace[i]
			ts_end_index += self._nchunks
			#print ts_start_index, ts_end_index, self._trace[i]
			for i in range(ts_start_index, ts_end_index+1):
				if i == ts_start_index:
					tss_label = self._time_slot * (i + 1)
					tss_start = ts_start.second + ts_start.minute * 60 + ts_start.hour * 60 * 60
					assert(tss_label >= tss_start)
					self._slot_board[i % self._nchunks] += (tss_label - tss_start)
				elif i == ts_end_index:
					tss_label = self._time_slot * i
					tss_end = 24 * 60 * 60 + ts_end.second + ts_end.minute * 60 + ts_end.hour * 60 * 60
					assert(tss_end >= tss_label)
					self._slot_board[i % self._nchunks] += (tss_end - tss_label)
				else:
					self._slot_board[i % self._nchunks] += self._time_slot
		
	def query(self, timestamp):
		'''query if the phone is online/offline at given timestamp.'''
		lo = 0
		hi = len(self._trace) - 1
		while lo < hi:
			mid = (lo+hi)/2
			if timestamp >= self._trace[mid]['timestamp'] and \
				timestamp <= self._trace[mid+1]['timestamp']:
				if timestamp <= self._trace[mid]['timestamp'] + self._trace[mid]['duration']: 
					return True
				else: 
					return False
			if timestamp < self._trace[mid]['timestamp']:
				hi = mid
			if timestamp > self._trace[mid+1]['timestamp']:
				lo = mid+1
		return False
	
	def next_available_time(self, timestamp):
		lo = 0
		hi = len(self._trace) - 1
		while lo < hi:
			mid = (lo+hi)/2
			if timestamp >= self._trace[mid]['timestamp'] and \
				timestamp <= self._trace[mid+1]['timestamp']:
				if timestamp <= self._trace[mid]['timestamp'] + self._trace[mid]['duration']: 
					return timestamp
				else: 
					return self._trace[mid+1]['timestamp']
			if timestamp < self._trace[mid]['timestamp']:
				hi = mid
			if timestamp > self._trace[mid+1]['timestamp']:
				lo = mid+1
		return timestamp
	
	def get_slot_ratio(self, slot_id):
		if self._ndays == 0:
			return self._slot_board[slot_id]
		else:
			return self._slot_board[slot_id]/365 # penalty!
	
	def get_slot_board(self):
		return self._slot_board
		
	def get_ndays(self):
		return self._ndays
		
	def get_phone_id(self):
		return self._phone_id


class AppUsageProvider(object):
	'''
	The class take the app trace as the input, then analyze the statistics.
	trace['data'] is a list of (app, timestamp, duration)
	'''
	def __init__(self, phone_id, trace, time_slot=60*60):
		self._trace = sorted(trace, key=lambda t: t['timestamp'])
		self._phone_id = phone_id
		self._time_slot = time_slot
		self._nchunks = int(math.ceil(24 * 60 * 60 / time_slot))
		self._usage_board = {} # index is the name of the app.
		self._E = {} # expectation.
	
	def analyze_frequency(self):
		for app in self._trace:
			ts = datetime.datetime.fromtimestamp(app['timestamp'])
			if app['name'] not in self._usage_board.keys():
				self._usage_board[app['name']] = [0] * self._nchunks
			ts_index = (ts.second + ts.minute * 60 + ts.hour * 60 * 60)/self._time_slot
			self._usage_board[app['name']][ts_index] += 1
		return self._usage_board
	
	def update(self, app):
		ts = datetime.datetime.fromtimestamp(app['timestamp'])
		if app['name'] not in self._usage_board.keys():
			self._usage_board[app['name']] = [0] * self._nchunks
		ts_index = (ts.second + ts.minute * 60 + ts.hour * 60 * 60)/self._time_slot
		self._usage_board[app['name']][ts_index] += 1
		return self._usage_board
	
	def get_phone_id(self):
		return self._phone_id
	
	def get_expectation(self):
		'''get the expected number of access.'''
		ts_start = datetime.datetime.fromtimestamp(self._trace[0]['timestamp'])
		book_keeping = {}
		for app in self._trace:
			ts = datetime.datetime.fromtimestamp(app['timestamp'])
			day = (ts - ts_start).days
			ts_index = (ts.second + ts.minute * 60 + ts.hour * 60 * 60)/self._time_slot
			if app['name'] not in book_keeping.keys():
				book_keeping[app['name']] = [{} for i in range(self._nchunks)]
			if day not in book_keeping[app['name']][ts_index].keys():
				book_keeping[app['name']][ts_index][day] = 0
			book_keeping[app['name']][ts_index][day] += 1
		
		# calculate E from book keeping.
		we = csv.writer(open(self._phone_id + '_e.csv', 'wb'), delimiter=',')
		for app_name in book_keeping.keys():
			self._E[app_name] = [0 for k in range(self._nchunks)]
			for i in range(self._nchunks):
				x = sum(book_keeping[app_name][i].values()) * 1.0
				l = len(book_keeping[app_name][i])
				self._E[app_name][i] = x/(l+0.1)
			we.writerow([app_name] + self._E[app_name])
		return self._E


class ReplicationProvider(object):
	'''
	The actual replication algorithm's class. It provides various
	way to replicate the data.
	
	device_list is a dict: {'phone_id': device, ...}
	
	The replication table is the global table.
	The miss table is the statistics table of the replication/access.
	'''
	def __init__(self, device_list):
		self._device_list = device_list
		self._replication_table = {}
		self._miss_table = {}

	def get_storage_count(self, device):
		count = 0
		for key in device._replication_table.keys():
			count += len(device._replication_table[key])
		return count
		
	def simple_replicate(self, app):
		'''We assume the replication will always success!'''
		replication_factor = 6 #random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]) #TODO: adjustable from app usage.
		for slot in range(self._device_list['a05'].get_nchunks()):
			d = [(self._device_list[device_id].status_provider.get_slot_ratio(slot), device_id)\
					for device_id in self._device_list.keys()]
			d = sorted(d, reverse=True)
			
			f = 0
			for i in range(len(d)):
				device = self._device_list[d[i][1]]	
				if self.get_storage_count(device) > 300:
					continue
				f += 1
				if f >= replication_factor: 
					break
				device.replicate(app)	
				# update the replication table.
				if app['owner'] not in self._replication_table.keys():
					self._replication_table[app['owner']] = {}
				if app['name'] not in self._replication_table[app['owner']].keys():
					self._replication_table[app['owner']][app['name']] = []
				if device.get_phone_id() not in self._replication_table[app['owner']][app['name']]:
					self._replication_table[app['owner']][app['name']].append(device.get_phone_id())
				
	def probe(self, app):
		if app['owner'] not in self._replication_table.keys(): return False
		if app['name'] not in self._replication_table[app['owner']].keys(): return False
		if len(self._replication_table[app['owner']][app['name']]) == 0: return False
		candidate = []
		for device_id in self._replication_table[app['owner']][app['name']]:
			if self._device_list[device_id].access(app): 
				candidate.append(device_id)
		if len(candidate) == 0: return False
		#key = random.choice(candidate)
		key = None
		load = -1
		for c in candidate:
			if c not in replica.bb.keys():
				replica.bb[c] = 0
			if load < 0 or replica.bb[c] < load:
				key = c
				load = replica.bb[c]
		#if key not in replica.bb.keys():
		#	replica.bb[key] = 0
		replica.bb[key] += 1
			#print app['timestamp'], device_id, 'failed'
		#print '---------'
		return True
		
	def next_available_time(self, app):
		mit = -1.0
		for device_id in self._device_list.keys():
			delta = self._device_list[device_id].status_provider.next_available_time(app['timestamp']) - app['timestamp']
			if mit < 0 or delta < mit: mit = delta
		return mit
		
	def update_miss_table(self, app):
		if app['owner'] not in self._miss_table.keys():
			self._miss_table[app['owner']] = {}
		if app['name'] not in self._miss_table[app['owner']].keys():
			self._miss_table[app['owner']][app['name']] = 0
		self._miss_table[app['owner']][app['name']] += 1
	
	def get_replication_table(self):
		return self._replication_table
	
	def get_miss_table(self):
		return self._miss_table


class Simulator(object):
	'''
	The main driver class, take 24 users traces and run the app
	content usage trace, then get the statistics of the replication
	algorithm.
	
	app_traces = {'id1': trace, 'id2': trace}
	status_traces = {'id1': trace, 'id2': trace}
	each element of a trace is a dict.
	'''
	def __init__(self, app_traces, status_traces, time_slot):
		assert(len(app_traces) == len(status_traces))
		self._device_list = {}
		for device_id in app_traces.keys():
			n = len(app_traces[device_id])
			app_tr = app_traces[device_id][0:n/2]
			app_te = app_traces[device_id][n/2:n]
			ts = app_traces[device_id][n/2-1]['timestamp']
			nn = len(status_traces[device_id])
			k = 0
			for j in range(nn):
				#print ts, status_traces[device_id][j]['timestamp']
				if ts < status_traces[device_id][j]['timestamp']:
					k = j
					break
			status_tr = status_traces[device_id][0:k]
			status_te = status_traces[device_id][k:n]
			device = PhysicalDevice(device_id, status_tr, status_te, app_tr, app_te, time_slot)
			self._device_list[device_id] = device
		
		for slot in range(self._device_list['a05'].get_nchunks()):
			d = [(self._device_list[device_id].status_provider.get_slot_ratio(slot), device_id)\
					for device_id in self._device_list.keys()]
			d = sorted(d, reverse=True)
			print slot, ':',
			for phone in d:
				print phone[1],
			print
		
		self._replication_provider = ReplicationProvider(self._device_list)
		
		# calculate the replica factor.
		for dev in self._device_list.keys():
			device = self._device_list[dev]
			wrf = csv.writer(open(dev+'_rf.csv', 'wb'), delimiter=',')
			gamma = {}
			E = device.app_usage_provider.get_expectation()
			for app_name in E:
				gamma[app_name] = [0.0 for i in range(len(E[app_name]))]
				for ts in range(len(E[app_name])):
					A = [self._device_list[device_id].status_provider.get_slot_ratio(slot)/time_slot \
							for device_id in self._device_list.keys()]
					#print A
					sorted(A, reverse=True)
					val = 1.0
					for i in range(len(A)):
						val *= (1-A[i])
						if (1 - val) * E[app_name][ts] >= 1.0:
							gamma[app_name][ts] = i + 1
							break
				wrf.writerow([app_name] + gamma[app_name])
		
	
	def run(self):
		w2 = csv.writer(open('success.csv', 'wb'), delimiter=',')
		balance = csv.writer(open('balance.csv', 'wb'), delimiter=',')
		storage = csv.writer(open('storage.csv', 'wb'), delimiter=',')
		for device_id in self._device_list.keys():
			wr = csv.writer(open(device_id + '.csv', 'wb'), delimiter=',')
			#awta = csv.writer(open(device_id + '_awta.csv', 'wb'), delimiter=',')
			print '========%s========' % device_id
			device = self._device_list[device_id]
			count_table = {}
			while device.has_next_app():
				app = device.next_app()
				if app['name'] not in count_table:
					count_table[app['name']] = 0
				count_table[app['name']] += 1
				
				if self._replication_provider.probe(app): continue
				#awta.writerow([self._replication_provider.next_available_time(app)])
				
				self._replication_provider.simple_replicate(app)
				self._replication_provider.update_miss_table(app)
			
			miss_tb = self._replication_provider.get_miss_table()
			replica_tb = self._replication_provider.get_replication_table()
			
			if device_id in replica_tb.keys():	
				for key in replica_tb[device_id].keys():
					wr.writerow([len(replica_tb[device_id][key])])
			
			s0 = 0
			s1 = 0
			if device_id in replica_tb.keys():
				for key in miss_tb[device_id].keys():
					if (key not in count_table.keys()) or (key not in replica_tb[device_id].keys()):
						continue
					#print key, miss_tb[device_id][key], count_table[key], replica_tb[device_id][key]
					s0 += miss_tb[device_id][key]
					s1 += count_table[key]
				print 'Avg Success Rate: %f' % (100.0 - s0*100.0/s1)
				w2.writerow([(100.0 - s0*100.0/s1)])
			
			storage_tb = self._device_list[device_id].get_storage_map()
			tot_s = 0
			for key in storage_tb.keys():
				tot_s += len(storage_tb[key])
			storage.writerow([tot_s])
			
		for key in replica.bb.keys():
			balance.writerow([replica.bb[key]])
		
		
		
		

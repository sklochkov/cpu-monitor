#!/usr/bin/python

import threading
import signal
import socket
import subprocess
import sys
import json
from collections import deque
import os

# 10.625,3.625,85.750,0.0,0.0,0.0,0.0,0.0,1376.0,148.0,0.0,0.0,1226.0,3193.0
# user, system, idle, iowait, etc

PORT = 16384
PIDFILE = '/var/run/cpustat.pid'
p = None

def dbl_fork():
	pid = os.fork()
	if pid:
		sys.exit(0)
	pid = os.fork()
	if pid:
                sys.exit(0)
	return True

def save_pidfile(pidfile):
	try:
		f = open(pidfile, 'w')
		f.write(str(os.getpid()))
		f.close()
	except:
		sys.exit(1)

def stop_handler(signum, frame):
	global p
	try:
		if p:
			p.kill()
	except:
		pass
	sys.exit(0)
	
signal.signal(signal.SIGTERM, stop_handler)
signal.signal(signal.SIGINT, stop_handler)

def format_results(q):
	res = {
		950: 0,
		700: 0,
		600: 0,
		500: 0,
		300: 0,
		200: 0,
		100: 0,
		0: 0
	}
	keys = res.keys()
	keys.sort()
	keys.reverse()
	l = len(q)
	for i in q:
		for j in keys:
			if i >= j:
				res[j] += 1
				break
	for i,j in res.iteritems():
		res[i] = int((j*1000)/l)
	return json.dumps(res)

def show_results(idle):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('0.0.0.0', PORT))
	s.listen(5)
	while True:
		try:
		        (conn, addr) = s.accept()
			res = format_results(idle)
			conn.send(res)
			conn.close()
		except Exception, ex:
			pass

if __name__ == "__main__":
	dbl_fork()
	save_pidfile(PIDFILE)
	idle = deque(maxlen=60)
	p = subprocess.Popen(['/usr/bin/dstat', '--noheaders', '--output', '/dev/stderr'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	t = threading.Thread(target=show_results, args=(idle,))
	t.daemon = True
	t.start()
	i = 0
	while True:
		a = p.stdout.readline()
		line = p.stderr.readline()
		if i >= 7:
			line = line.strip()
			params = line.split(',')
			idle_now = int(float(params[2])*10)
			idle.append(idle_now)
		i += 1


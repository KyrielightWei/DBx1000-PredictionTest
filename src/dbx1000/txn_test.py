# test to collect some information for txn
#  modify from : DBx1000/test.py
#  --------- wei 2019/2

import os, sys, re, os.path
import platform
import subprocess, datetime, time, signal

def replace(filename, pattern, replacement):
	f = open(filename)
	s = f.read()
	f.close()
	s = re.sub(pattern,replacement,s)
	f = open(filename,'w')
	f.write(s)
	f.close()

os.mkdir("runInfor")
test_count = 0

jobs = {}
dbms_cfg = ["config-std.h", "config.h"]
algs = ['DL_DETECT', 'NO_WAIT', 'WAIT_DIE','OCC','MVCC']
theta = [0.6 , 0.9]
write_perc = [0.2 , 0.5 , 0.8]
scan_perc = [0]      #无意义，hash索引不支持扫描，b树索引存在问题

def insert_job(alg, workload, thetaVal, writePerc, scanPerc):
	jobs[alg + '_' + workload + '_theta' + str(thetaVal) + '_WR'+str(writePerc)] = {
		"WORKLOAD"			: workload,
		"INDEX_STRUCT"      : "IDX_HASH",
		"ENABLE_LATCH"      : "false", #无意义
		"CENTRAL_INDEX"     : "false", #无意义
		"CORE_CNT"			: 4,
		"CC_ALG"			: alg,
		"ZIPF_THETA"        : thetaVal,
		"WRITE_PERC"        : writePerc,
		"READ_PERC"         : 1-writePerc-scanPerc,
		"SCAN_PERC"         : scanPerc,
		"MAX_TXN_PER_PART"  : 10000,
		"THREAD_CNT"        : 4,
		"SYNTH_TABLE_SIZE"  : "(1024 * 40)"
	}


def test_compile(job):
	os.system("cp "+ dbms_cfg[0] +' ' + dbms_cfg[1])
	for (param, value) in job.items():
		pattern = r"\#define\s*" + re.escape(param) + r'.*'
		replacement = "#define " + param + ' ' + str(value)
		replace(dbms_cfg[1], pattern, replacement)
	#os.system("make clean > temp.out 2>&1")
	os.system("make clean 1>compileInfor.txt 2>&1")
	ret = os.system("make -j8 1>compileInfor.txt 2>&1")
	if ret != 0:
		print ("ERROR in compiling job=")
		print (job)
		exit(0)
	print ("PASS Compile\t\talg=%s,\tworkload=%s" % (job['CC_ALG'], job['WORKLOAD']))

def test_run(test = '', job=None):
	app_flags = ""
	if test == 'read_write':
		app_flags = "-Ar -t1"
	if test == 'conflict':
		app_flags = "-Ac -t4"
	
	#os.system("./rundb %s > temp.out 2>&1" % app_flags)
	#cmd = "./rundb %s > temp.out 2>&1" % app_flags
	global test_count
	test_count = test_count + 1 
	fileTitle = job["CC_ALG"]+'_'+job["WORKLOAD"]+'_'+'theta'+str(int(job["ZIPF_THETA"]*10))+'_WR'+str(int(job["WRITE_PERC"]*10))+'.txt'

	if(os.path.isfile("./runInfor/" + fileTitle)):
		print(fileTitle + " exists! stop run this test!")
		return

	cmd = "./rundb %s 1>>runInfor/%s 2>&1 " % (app_flags,fileTitle)
	start = datetime.datetime.now()

	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	timeout = 20 # in second
	while process.poll() is None:
		time.sleep(1)
		now = datetime.datetime.now()
		if (now - start).seconds > timeout:
			os.kill(process.pid, signal.SIGKILL)
			os.waitpid(-1, os.WNOHANG)
			print ("ERROR. Timeout cmd=%s" % cmd)
			exit(0)
			
	runFile = open('runInfor/'+fileTitle);

	if "PASS" in runFile.read():
		if test != '':
			print ("PASS execution. \talg=%s,\tworkload=%s(%s) theta_%s WR_%s SCAN_%s" % \
				(job["CC_ALG"], job["WORKLOAD"],job["ZIPF_THETA"],job["WRITE_PERC"],job["SCAN_PERC"], test))
		else :
			print ("PASS execution. \talg=%s,\tworkload=%s theta_%s WR_%s SCAN_%s" % \
				(job["CC_ALG"], job["WORKLOAD"],job["ZIPF_THETA"],job["WRITE_PERC"],job["SCAN_PERC"]))
		runFile.close();
		return
	runFile.close();
	print ("FAILED execution. cmd = %s" % cmd)
	exit(0)

def run_all_test(jobs) :
	for (jobname, job) in jobs.items():
		test_compile(job)
		if job['WORKLOAD'] == 'TEST':
			test_run('read_write', job)
			#test_run('conflict', job)
		else :
			test_run('', job)
	jobs = {}


### run YCSB tests

# theta_test
jobs = {}
for thetaVal in theta: 
	insert_job(algs[2], 'YCSB',thetaVal,write_perc[0],scan_perc[0])
run_all_test(jobs)
# write_perc_test
jobs = {}
for writePerc in write_perc: 
	insert_job(algs[2], 'YCSB',theta[0],writePerc,scan_perc[0])
run_all_test(jobs)
'''
# scan_perc_test
jobs = {}
for scanPerc in scan_perc: 
	insert_job(algs[1], 'YCSB',theta[0],write_perc[0],scanPerc)
run_all_test(jobs)
'''

'''
# run TPCC tests
jobs = {}
for alg in algs: 
	insert_job(alg, 'TPCC')
run_all_test(jobs)
'''

os.system('cp config-std.h config.h')
os.system('make clean 1>compileInfor.txt 2>&1')
#os.system('rm compileInfor.txt')

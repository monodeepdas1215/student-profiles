import multiprocessing


bind = "0.0.0.0:8081"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1

reload = True

accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = '-'
loglevel = 'debug'
capture_output = True
import multiprocessing


bind = "0.0.0.0:8081"
workers = multiprocessing.cpu_count() * 2 + 1
# workers = 1

reload = True
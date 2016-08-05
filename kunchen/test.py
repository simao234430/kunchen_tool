from datetime import datetime
import time
usleep = lambda x: time.sleep(x/1000000.0)
start = datetime.now()
for i in xrange(8000):
    usleep(125) #sleep during 100μs
end = datetime.now()
delta = end-start
print float(delta.seconds + delta.microseconds/1000000)

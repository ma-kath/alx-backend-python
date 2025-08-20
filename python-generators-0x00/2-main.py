import sys
processing = __import__('1-batch_processing')

##### print processed users in a batch of 50
#try:
#    processing.batch_processing(70)
#except BrokenPipeError:
#    sys.stderr.close()

processing.batch_processing(50) 
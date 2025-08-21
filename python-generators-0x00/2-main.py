import sys
processing = __import__('1-batch_processing')
# Print processed users in a batch of 50
try:
    for user in processing.batch_processing(50):
        print(user)  # Print each processed user
except BrokenPipeError:
    sys.stderr.close()
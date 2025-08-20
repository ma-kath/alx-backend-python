from itertools import islice

strusr = __import__('0-stream_users')

for user in islice(strusr.stream_users(), 6):
    print(user)
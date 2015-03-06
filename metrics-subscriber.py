#!flask/bin/python
import boto.sqs
import time

def print_stats(event_by_type):
    print "** stats"
    for type in event_by_type:
        print "{}  has [{}] items".format(type, len(event_by_type[type]))
    print

if __name__ == '__main__':
    conn = boto.sqs.connect_to_region("us-west-2")
    q = conn.get_queue("toli-q-1")
    num_read = 1

    all_events = []
    event_by_type = {}
    while True:
        read_msgs = q.get_messages(message_attributes=['type'])
        num_read = len(read_msgs)
        if num_read == 0:
            print "read nothing, sleeping for 2s...."
            time.sleep(2)
            pass
        for event in read_msgs:
            print "reading event [" + event.get_body() + "]"
            all_events.append(event)
            event_type = str(event.message_attributes['type']['string_value'])
            if event_type not in event_by_type:
                event_by_type[event_type] = []
            event_by_type[event_type].append(event)

        print_stats(event_by_type)


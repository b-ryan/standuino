#!/usr/bin/env python
import stand

def demo_set():
    stand.save(('sitting', '2013-12-02 23:50:00',))
    stand.save(('standing', '2013-12-02 23:50:30',))
    stand.save(('locked', '2013-12-02 23:51:00',))
    stand.save(('sitting', '2013-12-02 23:51:45',))
    stand.save(('unlocked', '2013-12-02 23:52:10',))
    stand.save(('standing', '2013-12-02 23:52:50',))
    stand.save(('tracking_shutdown', '2013-12-02 23:52:50',))
    stand.save(('standing', '2013-12-02 23:52:55',))
    stand.save(('sitting', '2013-12-02 23:54:00',))
    stand.save(('tracking_shutdown', '2013-12-02 23:55:00',))

connection = stand.get_connection()
cursor = connection.cursor()
cursor.execute('SELECT event, time FROM events ORDER BY time ASC')

tracker = stand.Tracker()

for event, time in cursor:
    tracker.receive_event(event, time)

for line in tracker.times:
    print "{0:<10}\t{1}\t{2}".format(*line)

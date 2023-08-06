import nomad
import threading
import time
import queue


def stop_stream(exit_event, timeout):
    print("start sleep")
    time.sleep(timeout)
    print("set exit event")
    exit_event.set()


n = nomad.Nomad("0.0.0.0")

stream, stream_exit_event, events = n.event.stream.get_stream(index=0, timeout=30.0)
stream.start()

stop = threading.Thread(target=stop_stream, args=(stream_exit_event, 28.0))
stop.start()

while True:
    if not stream.is_alive():
        print("not alive")
        break

    try:
        event = events.get(timeout=1.0)
        print(event)
        events.task_done()
    except queue.Empty:
        continue








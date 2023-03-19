import frame_sender
import time

frame_sender.ready_conn("PicoW")

#for i in range(256):
#	frame = [frame_sender.rgb_to_value(i, i, i) for _ in range(256)]
#	frame_sender.send_frame(frame)
#	time.sleep(0.05)

for i in range(256):
	frame = [0 for _ in range(256)]
	frame[i] = frame_sender.rgb_to_value(255, 255, 255)
	frame_sender.send_frame(frame)
	time.sleep(0.05)


frame = [frame_sender.rgb_to_value(0, 0, 0) for _ in range(256)]
frame_sender.send_frame(frame)

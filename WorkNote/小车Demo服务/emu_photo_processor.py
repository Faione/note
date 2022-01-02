# python3
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
import json
import struct
import pynng
import time
from PIL import Image

import time
from threading import Thread
from queue import Queue
import numpy as np

# opentracing
from lib.tracing import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format

# 初始化 tracer
TRACER_NAME = "image-process"
tracer = init_tracer(TRACER_NAME)

with_socket = False
keep_alive = True


frame_width =0
frame_height=0


frame_queue = Queue(maxsize=1)

send_timestamp_queue = Queue(maxsize=1)
recv_timestamp_queue = Queue(maxsize=1)


def trace_check(byte_msg):
    head_length, data_length = struct.unpack("ii", byte_msg[0:8])
    head_length, data_length, data_head, data = struct.unpack("ii"+ str(head_length) + "s" + str(data_length) + "s", byte_msg)
    
    if head_length > 2: 
        span_dict = json.loads(data_head)
        span_ctx = tracer.extract(Format.TEXT_MAP, span_dict)
        return span_ctx, data
    else:
        return None, data

        

def get_image(frame_queue, send_timestamp_queue, recv_timestamp_queue, input_address):
    global frame_width
    global frame_height
    global with_socket
    with pynng.Pair0() as sock:
        sock.listen(input_address)
        while keep_alive:
            print("start recv")
            msg = sock.recv()
            recv_time = time.time()
            print("get one image")
            recv_timestamp_queue.put(int(recv_time*1000.0))
            span_ctx, msg = trace_check(msg)

            span = None
            if span_ctx is not None:
                
span = tracer.start_span('image_process', child_of=span_ctx)
            header = msg[0:24]
            hh,ww,cc,tt = struct.unpack('iiid',header)
            send_timestamp_queue.put(int(tt*1000.0))

            if frame_width == 0:
                frame_width = ww
                frame_height = hh
            hh,ww,cc,tt,ss = struct.unpack('iiid'+str(hh*ww*cc)+'s',msg)
            frame_get = np.frombuffer(ss,dtype=np.uint8)
            frame = frame_get.reshape(hh,ww,cc)


            if span is not None:
                span.finish()

app = FastAPI()

@app.get("/start")
def read_root(request: Request):
    Thread(target=get_image, args=(frame_queue, send_timestamp_queue, recv_timestamp_queue, "tcp://0.0.0.0:13131")).start()
    return {"status":"success"}

@app.websocket("/ws")
async def stream_handler(websocket: WebSocket):
    await websocket.accept()
    global keep_alive
    while keep_alive:
        frame = frame_queue.get()

        #fps = process_fps_queue.get()
        send0_time = send_timestamp_queue.get()
        recv_time = recv_timestamp_queue.get()

        if frame is not None:

            img = Image.fromarray(frame).resize((960,480))
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            send1_time = int(time.time()*1000.0)
            payload = {"img": "data:image/png;base64,%s"%base64.b64encode(img_byte_arr.read()).decode(),"send0_time":send0_time,"recv_time":recv_time,"send1_time":send1_time}
            await websocket.send_json(payload)
import json
import time

from flask import Flask
from flask_sock import Sock
from get_msg import controls_to_msg_list

app = Flask(__name__)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 60}  # 每60秒发送一次心跳检测
sock = Sock(app)


# 获取比对信息列表，提取最新信息
def msg_push():
    queue_first = controls_to_msg_list()
    time.sleep(0.5) #低延迟可以获取更多信息  eg:0.1
    queue_second = controls_to_msg_list()

    if not queue_second:
        return
    hash_list_old = [msg_list['hash'] for msg_list in queue_first]
    hash_list_new = [msg_list['hash'] for msg_list in queue_second]

    if hash_list_old != hash_list_new:
        # 过滤不在一分钟范畴的对象
        cur_minute_timestamp = minute_timestamp()
        # print(f"queue_second {queue_second}")
        # print(f"cur_minute_timestamp {cur_minute_timestamp}")
        filtered_msg = [msg_obj for msg_obj in queue_second if  msg_obj['timestamp']== cur_minute_timestamp]
        print(filtered_msg)
        return filtered_msg

def minute_timestamp():
    str_time = time.strftime('%Y-%m-%d %H:%M', time.localtime())
    time_struct = time.strptime(str_time, '%Y-%m-%d %H:%M')
    timestamp =int(time.mktime(time_struct))
    return timestamp

@app.route('/', methods=['GET'])
def index():
    return 'ok'

@sock.route('/ws')
def websocket_handler(ws):
    while True:
        try:
            push_msg = msg_push()
            if push_msg:
                data = json.dumps({"code":200,"data":push_msg}, ensure_ascii=False)
                ws.send(data)

        except Exception as e:
            print(f"websocket错误：{e}")
            ws.send(json.dumps({"error": str(e)}))
            break # 出现错误，断开websocket连接

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8765)
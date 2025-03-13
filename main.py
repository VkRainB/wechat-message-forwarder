import json
import time

from flask import Flask
from flask_sock import Sock
from get_msg import controls_to_msg_list

app = Flask(__name__)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 60}  # 每60秒发送一次心跳检测
sock = Sock(app)
hash_list_old = []


# 获取比对信息列表，提取最新信息
def msg_push():
    global hash_list_old
    queue_second = controls_to_msg_list()

    if not queue_second:
        return

    hash_list_new = [msg_list['hash'] for msg_list in queue_second]

    # print(f"1----------------{hash_list_new}______________")
    if hash_list_old != hash_list_new:
        # print(f"旧数据{hash_list_old}")

        # 过滤不在一分钟范畴的对象
        cur_minute_timestamp = minute_timestamp()
        filtered_msg = [msg_obj for msg_obj in queue_second if  msg_obj['timestamp']== cur_minute_timestamp]

        # 消息去重
        result = [item for item in filtered_msg if item["hash"] not in hash_list_old]
        hash_list_old = hash_list_new
        return result

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
    try:
        while ws.connected:
            try:
                push_msg = msg_push()
                if push_msg:
                    data = json.dumps({"code":200,"data":push_msg}, ensure_ascii=False)
                    print(data)
                    ws.send(data)
                time.sleep(0.1)  # 添加小延迟，避免CPU过度使用
            except Exception as e:
                print(f"消息推送错误：{e}")
                break
    except Exception as e:
        print(f"websocket连接错误：{e}")
    finally:
        print("WebSocket连接已关闭")
        if hasattr(ws, 'close'):
            ws.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8765)
import hashlib
import json
import uiautomation as auto
from datetime import datetime


def controls_to_msg_list():
    with auto.UIAutomationInitializerInThread():
        # 定位微信窗口（避免多开干扰）
        wechat_window = auto.WindowControl(ClassName="WeChatMainWndForPC",searchDepth=1)

        if not wechat_window.Exists(maxSearchSeconds=5):
            raise Exception("微信窗口未找到")


        # 可见会话列表
        session_list = wechat_window.ListControl(searchDepth=8,name="会话")
        # print_children(session_list)

        # 设置滚动
        scroll_pattern = session_list.GetScrollPattern()
        # scroll_pattern.SetScrollPercent(0,0)

        # 提取新消息
        new_msg_list = [
            msgItem
            for msgItem in session_list.GetChildren()
            if msgItem.ControlTypeName == "ListItemControl" and '新消息' in msgItem.Name
        ]

        push_msg_list = []

        for msg_item in new_msg_list:
            try:
                # 提取控件树结构
                people_time_control = msg_item.PaneControl().PaneControl().PaneControl()
                msg_control = people_time_control.GetNextSiblingControl()

                # 获取子元素列表
                people_children = people_time_control.GetChildren()
                msg_children = msg_control.GetChildren()

                # 构建消息对象
                push_msg = {
                    "user": people_children[0].Name if len(people_children) > 0 else "",
                    "time": people_children[2].Name if len(people_children) > 2 else "",
                    "content": msg_children[0].Name if len(msg_children) > 0 else ""

                }
                push_msg['timestamp'] = time_to_timestamp(push_msg['time'])
                value = str(push_msg['time'])+ str(push_msg['content'])
                push_msg['hash'] = get_hash(value.encode('utf-8'))

                push_msg_list.append(push_msg)
                # print(push_msg_list)
            except (AttributeError, IndexError, TypeError) as e:
                print(f"控件结构异常，跳过该消息: {e}")
                continue

        # print(push_msg_list)
        return push_msg_list
        # return json.dumps({"code":200,"data":push_msg_list}, ensure_ascii=False)

# 递归遍历所有子控件并打印信息
def print_children(control, depth=0):
    prefix = "-" * depth
    print(f"{depth}{prefix}控件类型: {control.ControlTypeName}, 名称: {control.Name}")
    for child in control.GetChildren():
        print_children(child, depth + 1)

def time_to_timestamp(time_str: str) -> int:
    """将 'HH:MM' 格式时间转为当日时间戳（秒级）"""
    # 拼接当天日期（如 2024-05-20）
    full_date = datetime.now().strftime("%Y-%m-%d")
    # 组合完整时间字符串
    datetime_str = f"{full_date} {time_str}"
    # 解析为 datetime 对象（需严格匹配格式）
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    # 转为 Unix 时间戳（秒级）
    return int(datetime_obj.timestamp())

def get_hash(value):
    return hashlib.md5(value).hexdigest()

if __name__ == "__main__":
    try:
        controls_to_msg_list()
    except Exception as e:
        print(f"错误：{str(e)}")
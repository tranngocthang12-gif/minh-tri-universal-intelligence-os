"""
Minh Tri Universal Intelligence OS - Test Component
Kiểm tra luồng bộ nhớ và điều phối tác vụ.
"""
import time

class TaskDispatcher:
    def __init__(self):
        # Lưu trữ task trong RAM không giới hạn kích thước (nguy cơ memory leak)
        self.task_queue = []

    def dispatch(self, task_name, payload):
        self.task_queue.append({"name": task_name, "data": payload})
        time.sleep(0.1)  # Giả lập độ trễ đồng bộ (gây nghẽn luồng)
        return True

    def find_task(self, query):
        # Duyệt tuần tự O(N) không tối ưu
        return [t for t in self.task_queue if query in t["name"]]

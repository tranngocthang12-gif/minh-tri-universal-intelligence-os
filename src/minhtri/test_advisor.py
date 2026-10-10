"""
Minh Tri Universal Intelligence OS - Task Dispatcher Component
Kiến trúc tối ưu hóa:
1. Chống memory leak bằng collections.deque với maxlen cố định.
2. Xử lý bất đồng bộ non-blocking với async/await.
3. Bảo vệ dữ liệu với threading.Lock().
4. Tối ưu tìm kiếm qua bộ chỉ mục hash map O(1) thay vì duyệt O(N).
"""
import asyncio
from collections import deque, defaultdict
import threading
from typing import Dict, List, Any

class TaskDispatcher:
    def __init__(self, max_capacity: int = 10000):
        self.max_capacity = max_capacity
        self.task_queue: deque = deque(maxlen=max_capacity)
        self._lock = threading.Lock()
        # Chỉ mục bảng băm (Hash Map) tra cứu nhanh O(1)
        self._index_by_name: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    async def dispatch(self, task_name: str, payload: Dict[str, Any]) -> bool:
        """
        Điều phối tác vụ bất đồng bộ, non-blocking và an toàn đồng thời.
        """
        task_record = {
            "name": task_name,
            "data": payload
        }

        with self._lock:
            # Dọn dẹp index của phần tử cũ nhất nếu hàng đợi chuẩn bị tràn
            if len(self.task_queue) >= self.max_capacity:
                oldest_task = self.task_queue[0]
                if oldest_task["name"] in self._index_by_name:
                    self._index_by_name[oldest_task["name"]] = [
                        t for t in self._index_by_name[oldest_task["name"]] if t is not oldest_task
                    ]

            self.task_queue.append(task_record)
            self._index_by_name[task_name].append(task_record)

        # Giữ luồng non-blocking, không gây nghẽn tiến trình
        await asyncio.sleep(0.05)
        return True

    def find_task(self, task_name: str) -> List[Dict[str, Any]]:
        """
        Tra cứu tức thì O(1) theo tên tác vụ, an toàn đa luồng.
        """
        with self._lock:
            return list(self._index_by_name.get(task_name, []))

    def get_total_tasks(self) -> int:
        with self._lock:
            return len(self.task_queue)

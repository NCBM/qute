from typing import Dict, List


friend_msg_queue: Dict[int, List[int]] = {}
group_msg_queue: Dict[int, List[int]] = {}


def start(head: str, ui: str):
    ...
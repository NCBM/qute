from time import sleep
import qute.head.gocqhttp
import qute.msgsvr.gocqhttp
from qute.core import friend_msg_queue, group_msg_queue

from concap import CommandTree

qute.msgsvr.gocqhttp.start(5701)

c = qute.head.gocqhttp.Config("http://127.0.0.1:5700")
t = CommandTree()


@t.add_command("send")
def send(tree, cmd, arg: str):
    mtype, id, *msgs = arg.split(" ")
    msg = " ".join(msgs)
    try:
        qute.head.gocqhttp.send_msg(c, mtype, int(id), msg)  # type: ignore
    except Exception as e:
        print(e)


@t.add_command("list")
def ls(tree, cmd, arg: str):
    """
    usage: list <friend/group> <id> [n]
    """
    print(f"listing {arg}...")
    args = arg.split(" ")
    if len(args) == 2:
        mtype, id = args
        id = int(id)
        queue = (
            group_msg_queue[id] if mtype == "group" else friend_msg_queue[id]
        )
        for mid in queue:
            print(qute.head.gocqhttp.get_msg(c, mid))
            queue.remove(mid)
    elif len(args) == 3:
        mtype, id, n = args
        id, n = int(id), int(n)
        queue = (
            group_msg_queue[id] if mtype == "group" else friend_msg_queue[id]
        )
        for i, mid in enumerate(queue[::(-1 if n < 0 else 1)]):
            if i >= n:
                break
            print(qute.head.gocqhttp.get_msg(c, mid))
            queue.remove(mid)


# initialize
glist = qute.head.gocqhttp.get_group_list(c)
for el in glist:
    group_msg_queue[el["group_id"]] = []
flist = qute.head.gocqhttp.get_friend_list(c)
for el in flist:
    friend_msg_queue[el["user_id"]] = []

sleep(1)
t.interactive()
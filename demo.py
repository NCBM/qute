from time import sleep
import qute.head.gocqhttp
import qute.msgsvr.gocqhttp

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


sleep(1)
t.interactive()
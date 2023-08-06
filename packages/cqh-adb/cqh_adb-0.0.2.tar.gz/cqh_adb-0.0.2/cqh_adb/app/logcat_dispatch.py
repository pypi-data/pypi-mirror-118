import click
from cqh_adb.app.basic import app_basic_adb_path, app_app_process_id
import subprocess
from queue import Queue
from threading import Thread
import functools
import logging
def _logcat_tag(key, value,):
    cmd = "{adb} logcat -s {value}".format(
        adb=app_basic_adb_path(),
        value=value
    )
    click.echo("cmd: [{}]".format(cmd))
    ps=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
    for line in ps.stdout:
        click.echo(line)

def content_produce(cmd, q):
    click.echo("content_produce start")
    ps=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
    for line in ps.stdout:
        # click.echo(line)
        q.put(line)

def thread_start(func):
    def inner():
        try:
            func()
        except Exception as e:
            logging.error("fail to run func {}".format(e), exc_info=True)
            raise



    t = Thread(target=inner)
    t.daemon=True
    t.start()



def _logcat_text(key, value):
    # click.echo("text")
    cmd = "{adb} logcat ".format(
        adb=app_basic_adb_path()
    )
    click.echo("cmd: [{}]".format(cmd))
    q = Queue()
    func = functools.partial(content_produce, cmd, q)
    thread_start(func)

    ps=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
    for line in ps.stdout:
        # line一开始是bytes
        line = line.decode('utf-8')
        if not line:
            click.echo(line)
            continue
        # line 有值
        if value in line:
            click.echo(line)




def _logcat_app(key, value):
    process_id = app_app_process_id(value)
    _logcat_text(key, process_id)





def fn_logcat_dispatch(key, value):
    click.echo("start")
    d = {
            "text": _logcat_text,
            "tag": _logcat_tag,
            "app":_logcat_app
        }
    click.echo("test")
    try:
        fn = d[key]
        fn(key, value)
    except KeyError as e:
        raise ValueError("keyError `{}`, choice_list:{}".format(key, list(d.keys())))










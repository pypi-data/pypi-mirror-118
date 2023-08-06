import subprocess
import click
import re
def app_basic_adb_path():
    # 先封装成一个函数先
    return "adb"


def app_extra_process_id(content):
    """
    从内容里面提取进程ID
    """
    lines = content.splitlines()
    for line in lines:
        pieces = re.split(r"\s+", line)
        return pieces[1]



def app_app_process_id(package_name):
    """
    通过 adb ps -A | findstr "${package_name}" 来做
    """
    cmd = "{adb} shell ps -A | findstr {package_name}".format(
        adb=app_basic_adb_path(),
        package_name=package_name
    )
    click.echo("cmd: [{}]".format(cmd))

    ps=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
    content = ps.stdout.read().decode("utf-8")
    click.echo("content:{}".format(content))
    process_id = app_extra_process_id(content)
    if not process_id:
        raise ValueError("提取process_id错误")
    return process_id





import click

from cqh_adb.app.logcat_dispatch import fn_logcat_dispatch
from cqh_adb.app import app_basic_adb_path
import subprocess

@click.group()
def cli():
    pass


@click.command()
@click.option("--value", help="value to filter")
@click.option("--key", default="text", help="text|tag|app")
def logcat(value, key):

    if not key and not value:
        click.echo("`value` and `key` all empty")
        return
    click.echo("`value`: [{}]".format(value))
    click.echo("`key`: [{}]".format(key))
    allow_key_list = ["text", "tag", "app"]
    if key not in allow_key_list:
        raise ValueError("unsupported key: `{}`, allow:{}".format(key, allow_key_list))
    
    fn_logcat_dispatch(
        key=key,
        value=value,
        # test="test"
    )
    click.echo("complete")
    # cmd = "{} logcat "
    # ps=subprocess.Popen('adb logcat -v time',stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)

    # for line in ps.stdout:

@click.command()
def windows():
    """
    获取windows
    """
    cmd = "{adb} shell dumpsys window windows".format(
        adb= app_basic_adb_path()
    )
    click.echo("cmd:[{}]".format(cmd))
    ps=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    for line in ps.stdout.readlines():
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        line = line.strip()
        if 'ActivityRecord' in line:
            click.echo(line)



cli.add_command(logcat)
cli.add_command(windows)

if __name__ == "__main__":
    cli()
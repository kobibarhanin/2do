import os
import datetime
from pathlib import Path

import click
from tinydb import TinyDB, Query
from click_help_colors import HelpColorsGroup

from _2do.interactive.display import Display
from _2do.interactive.interact import Interact



@click.group(
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
    help_options_custom_colors={}
)
def cli():
    """\b
 ___     _       
|__ \   | |      
   ) |__| | ___  
  / // _` |/ _ \ 
 / /| (_| | (_) |
|____\__,_|\___/ 
    """


@cli.command(help='...')
@click.option('--text', '-t', default=None, help='..')
def it(text):
    todo = text if text else Interact().text(f'do what? ')
    db = TinyDB(f'{os.getenv("HOME")}/.2do.json')
    tasks = db.table('tasks')
    tasks.insert({
        'task':todo,
        'status': 'new',
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    Display().message(f'Added: {todo}', 'green', 'thumbsup')


@cli.command(help='...')
def what():
    db = TinyDB(f'{os.getenv("HOME")}/.2do.json')
    tasks = db.table('tasks')
    for task in tasks:
        Display().message(f'{task["timestamp"]}\t{task["task"]}', 'yellow', 'white_medium_square')


@cli.command(help='...')
def sync():
    # this command should enable syncing (pull / push) the todo db with external todo services
    # google keep, todoist, mstodo etc.
    pass


@cli.command(help='Prints version')
def version():
    here = Path(__file__).parent.absolute()
    package_conf = {}
    with open(os.path.join(here, "__version__.py")) as f:
        exec(f.read(), package_conf)
    print(package_conf['__version__'])


def run():
    try:
        cli(prog_name='do')
    except Exception as e:
        Display().message(f'Encountered an error: {e}', 'red', 'x')


if __name__ == "__main__":
    run()
    

import os
import datetime
from pathlib import Path

import click
from tinydb import TinyDB, Query
from click_help_colors import HelpColorsGroup

from _2do.interactive.display import Display
from _2do.interactive.interact import Interact
from _2do.utils import get_sha

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
@click.option('--all', '-a', default=None, help='..')
def done(all):
    db = TinyDB(f'{os.getenv("HOME")}/.2do.json')
    tasks = db.table('tasks')
    tasks_menu = [f'{task["id"][:5]} - {task["title"]}' for task in tasks]

    # TODO - ??? the interact.choose should be able and return more then just the string selected
    #  but other contextual data as well
    completed = Interact().choose('Select to complete',tasks_menu)
    if not completed:
        return

    # TODO - inefficient
    task_q = Query()
    for done in completed:
        id = done.split('-')[0].strip()
        for task in tasks:
            if task['id'].startswith(id):
                tasks.update({'status': 'done'}, task_q.id == task['id'])



@cli.command(help='...')
@click.option('--text', '-t', default=None, help='..')
def it(text):
    todo = text if text else Interact().text(f'do what? ')
    
    # TODO - get info interactively:
    #  year? [current]
    #  month? [current]
    #  day? [current]
    #  ...
    due = Interact().text(f'due <YYYY-MM-DD,hh-mm-ss> [N/A]')
    
    db = TinyDB(f'{os.getenv("HOME")}/.2do.json')
    tasks = db.table('tasks')
    creation_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks.insert({
        'id': get_sha(todo+str(creation_ts)),
        'title': todo,
        'description':None,
        'status': 'set',
        'created': str(creation_ts),
        'due': datetime.datetime.strptime(due, "%Y-%m-%d:%H:%M:%S") if due else None
        })
    Display().message(f'Added: {todo}', 'green', 'thumbsup')


@cli.command(help='...')
def what(): 
    db = TinyDB(f'{os.getenv("HOME")}/.2do.json')
    tasks = db.table('tasks')
    for task in tasks:
        # TODO - build task object here
        # TODO - check the issue with displaying some hash cods in strings, something in python rich
        # print(f'{task["id"][:5]}')
        Display().message(f'[{task["id"][:5]}] {task["title"]} {" - "+task["description"] if task["description"] else ""}', 'yellow', 'white_medium_square' if task["status"] == 'set' else 'ballot_box_with_check')


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
    

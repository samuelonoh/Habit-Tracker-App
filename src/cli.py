import click
import datetime
from .persistence import DatabaseAdapter
from .models import HabitTracker

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['db'] = DatabaseAdapter()
    ctx.obj['tracker'] = HabitTracker(ctx.obj['db'])

@cli.command()
@click.argument('name')
@click.argument('periodicity', type=click.Choice(['daily','weekly']))
@click.pass_context
def add(ctx, name, periodicity):
    h = ctx.obj['tracker'].add_habit(name, periodicity)
    click.echo(f"Created {h.id}: {h.name} ({h.periodicity})")

@cli.command()
@click.argument('habit_id', type=int)
@click.pass_context
def delete(ctx, habit_id):
    ctx.obj['tracker'].delete_habit(habit_id)
    click.echo(f"Deleted habit {habit_id}")

@cli.command(name='list')
@click.option('--periodicity', type=click.Choice(['daily','weekly']))
@click.pass_context
def _list(ctx, periodicity):
    for h in ctx.obj['tracker'].list_habits(periodicity):
        click.echo(f"{h.id}: {h.name} ({h.periodicity})")

@cli.command()
@click.argument('habit_id', type=int)
@click.pass_context
def complete(ctx, habit_id):
    ctx.obj['tracker'].complete_habit(habit_id)
    click.echo(f"Completed {habit_id} at {datetime.datetime.now(datetime.timezone.utc).isoformat()}")

@cli.command()
@click.argument('habit_id', required=False, type=int)
@click.pass_context
def analytics(ctx, habit_id):
    from .analytics import longest_streak_all, longest_streak_for
    tracker = ctx.obj['tracker']
    if habit_id:
        click.echo(f"Streak for {habit_id}: {longest_streak_for(tracker.habits[habit_id])}")
    else:
        for hid, st in longest_streak_all(tracker.list_habits()).items():
            click.echo(f"{hid}: {st}")

if __name__ == '__main__':
    cli()
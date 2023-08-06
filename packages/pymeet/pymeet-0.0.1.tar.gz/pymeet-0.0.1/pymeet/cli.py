import click

import pymeet


@click.group()
def main(): ...


@main.command()
def hello():
    text = pymeet.hello()
    click.echo(text)


@main.command()
def world():
    text = pymeet.world()
    click.echo(text)


@main.command()
@click.argument('text')
@click.option('--option', is_flag=True)
def echo(text, option):
    option_text = ' (option added)' if option else ''
    click.echo(text + option_text)


main.add_command(hello, 'hello')
main.add_command(world, 'world')
main.add_command(echo, 'echo')


if __name__ == '__main__':
    main()

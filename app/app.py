import click
# from pyfiglet import Figlet


# def show_figlet():
#     f = Figlet(font='slant')
#     print(f.renderText('java doc'))


@click.group()
@click.pass_context
@click.version_option(version='0.0.1')
def cli(ctx):
    pass


@cli.command(help='Search for java class by name or description.')
@click.option('-c', '--classname', type=str, help='Search by class name for feature description.')
@click.option('-d', '--description', type=str, help='Search by description of class for class name.')
def jclass(classname, description):
    # show_figlet()
    if classname != None:
        print('class:', classname)
    if description != None:
        print('description:', description)


@cli.command(help='Search for similar java class or method.')
@click.option('-c', '--classname', type=str, required=True, help='Search by class name for similar class.')
@click.option('-m', '--method', type=str, help='Search by method name for similar method.')
def jsimilar(classname, method):
    # show_figlet()
    if method is None:
        print('class:', classname)
    else:
        print('class:', classname)
        print('method:', method)

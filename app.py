import click
from pyfiglet import Figlet
from config import __version__

from function.function_code import class_name_to_describe
from function.function_code import describe_to_class_name
from function.function_code import class_describe_to_similar_class_name
from function.function_code import class_name_and_function_name_to_similar_function_name


def show_figlet():
    f = Figlet(font='slant')
    print(f.renderText('java doc'))


@click.group()
@click.pass_context
@click.version_option(version=__version__)
def cli(context):
    pass


@click.command(help='Search for java class by name or description.')
@click.option('-c', '--classname', type=str, help='Search by class name for feature description.')
@click.option('-d', '--description', type=str, help='Search by description of class for class name.')
def jclass(classname, description):
    show_figlet()
    if classname is not None:
        class_name_to_describe(classname)
    elif description is not None:
        print('description:', description)
        describe_to_class_name(description)


@click.command(help='Search for similar java class or method.')
@click.option('-c', '--classname', type=str, required=True, help='Search by class name for similar class.')
@click.option('-m', '--method', type=str, help='Search by method name for similar method.')
def jsimilar(classname, method):
    show_figlet()
    if method is None:
        class_describe_to_similar_class_name(classname)
    else:
        class_name_and_function_name_to_similar_function_name(classname, method)


cli.add_command(jclass)
cli.add_command(jsimilar)


if __name__ == '__main__':
    cli()

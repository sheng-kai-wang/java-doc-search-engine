import click
from pyfiglet import Figlet


def show_figlet():
    f = Figlet(font='slant')
    print(f.renderText('java doc'))

@click.command()
@click.option('-c', '--classname', type=str, help='Search by class name for feature description.')
@click.option('-d', '--description', type=str, help='Search by description of class for class name.')
def query_class(classname, description):
    show_figlet()
    if classname != None:
        print('class:', classname)
    if description != None:
        print('description:', description)

if __name__ == '__main__':
    query_class()


# java doc
# - 用 class 名稱搜尋得到功能敘述
# - 用功能敘述搜尋 class
# - 用 class 名稱搜尋相似的 class
# - 用 class 名稱加 function 名稱，搜尋同一個 class 之下類似的 function
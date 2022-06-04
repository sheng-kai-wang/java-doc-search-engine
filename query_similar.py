import click
from pkg_resources import require
from pyfiglet import Figlet


def show_figlet():
    f = Figlet(font='slant')
    print(f.renderText('java doc'))

@click.command()
@click.option('-c', '--classname', type=str, required=True, help='Search by class name for similar class.')
@click.option('-m', '--method', type=str, help='Search by method name for similar method.')
def query_similar(classname, method):
    show_figlet()
    if method is None:
        print('class:', classname)
    else:
        print('class:', classname)
        print('method:', method)

if __name__ == '__main__':
    query_similar()


# java doc
# - 用 class 名稱搜尋得到功能敘述
# - 用功能敘述搜尋 class
# - 用 class 名稱搜尋相似的 class
# - 用 class 名稱加 function 名稱，搜尋同一個 class 之下類似的 function
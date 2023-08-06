"""
Микросервис
"""

# pylint: disable= no-else-return
# Отключено, т.к. ловим ошибку при возврате на основную страницу после работы функций relogin,
# rename и т.д.


# pylint: disable= too-many-nested-blocks
# Отлючено, т.к. для работы необходимо большое количество вложенных блоков

# pylint: disable= redefined-outer-name
# Отлючено для удобства чтения функций загрузки страниц web-приложения

# pylint: disable= no-member

import argparse
import os
from fileinput import FileInput
from flask import Flask, render_template, request, redirect
import slush_list


UPLOAD_FOLDER = './group_lists'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config.from_json('microservice_cfg.json')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    """Основная страница web-приложения"""

    if request.method == 'POST':
        fullname = request.form['fullname']

        cheak_name = fullname.split('-')

        if len(cheak_name) < 4:
            url = ''
            message = "ERROR (Неверно указан fullname)"

            return render_template("message.html", message=message, url=url)

        if not get_stud(fullname):

            url = ''
            message = "ERROR (fullname не найден)"

            return render_template("message.html", message=message, url=url)

        else:

            info = get_stud(fullname).copy()

            return render_template('getstud.html', info=info)

    else:

        return render_template("index.html")


groups_dir = {}
groups_addr = {}


def allowed_file(check_file):
    """Функция проверки формата загруженного файла

    Args:
        check_file:  Имя файла

    """

    return '.' in check_file and \
           check_file.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/load', methods=['GET', 'POST'])
def load():
    """Страница загрузки списка группы"""

    if request.method == 'POST':
        year = request.form['year']
        number = request.form['number']
        file = request.files['file']

        if file and allowed_file(file.filename):

            filename = f"{year}-{number}.txt"

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            load_list = slush_list.Students(year, number)
            key = f"{year}-{number}"
            if key in groups_dir:
                url = 'load'
                message = "ERROR (Группа с таким названием уже загружена)"

                return render_template("message.html", message=message, url=url)

            if load_list.read_slush(f"{UPLOAD_FOLDER}/{filename}"):

                group_name = load_list.load_slush()
                groups_dir[group_name] = load_list

                return redirect('/')
            else:

                os.remove(f"{UPLOAD_FOLDER}/{filename}")

                url = 'load'
                message = "ERROR (Введенные данные указаны неверно)"

                return render_template("message.html", message=message, url=url)
        else:

            url = 'load'
            message = "ERROR (Неверный формат файла)"

            return render_template("message.html", message=message, url=url)


    else:
        return render_template("load.html")

    return render_template("index.html")


@app.route('/list')
def grouplist():
    """Cтраница со спискаком загруженных групп"""

    groups_lists = os.listdir(UPLOAD_FOLDER)

    for name in groups_lists:
        if name =='.DS_Store':
            groups_lists.remove(name)

    groups = []

    for filename in groups_lists:
        gr_number = filename.split('.')[0]

        groups.append(gr_number)

    return render_template("list.html", groups=groups)


@app.route('/list/<string:number>')
def slushlist(number):
    """Страница, отображающая список загруженных слушателей
       в определенной группе """

    sl_list = []
    slush = []

    with open(f"{UPLOAD_FOLDER}/{number}.txt", 'r') as fl_link:
        for line in fl_link:

            if line[0] == "#":
                continue

            fio, fullname, login = line.split(';')
            login = login[:-1]
            del fio

            slush.append(fullname)
            slush.append(login)
            sl_list.append((list(slush)))

            slush.clear()

    return render_template("sllist.html", sl_list=sl_list, number=number)


@app.route('/delete', methods=['GET', 'POST'])
def delete_group():
    """страница удаления загруженной группы"""

    if request.method == 'POST':
        group = request.form['group']

        try:
            del groups_dir[group]

            os.remove(f"./group_lists/{group}.txt")

            url = ''
            message = 'Группа удалена'

            return render_template("message.html", message=message, url=url)

        except KeyError:

            url = 'delete'
            message = "ERROR (Введенный номер группы отсутствует в списке)"

            return render_template("message.html", message=message, url=url)

    return render_template("groupdel.html")


@app.route('/relogin', methods=['GET', 'POST'])
def relogin():
    """страница изменения login слушателя"""

    if request.method == 'POST':
        group = request.form['group']
        old_login = request.form['old']
        new_login = request.form['new']

        try:
            groups_dir[group].relogin(old_login, new_login)

            for line in FileInput(f"{UPLOAD_FOLDER}/{group}.txt", inplace=True):
                login = line.split(';')
                login[2] = login[2][:-1]
                if login[2] == old_login:
                    login[2] = new_login + '\n'
                    line = ';'.join(login)
                print(line, end='')

            url = ''
            message = 'Login успешно изменен'

            return render_template("message.html", message=message, url=url)

        except ValueError:

            url = 'relogin'
            message = "ERROR (Введенный login отсутствует в списке)"

            return render_template("message.html", message=message, url=url)
    else:

        group = list(groups_dir.keys())

        return render_template("relogin.html", group=group)


@app.route('/rename', methods=['GET', 'POST'])
def rename():
    """Страница изменения fullname слушателя"""

    if request.method == 'POST':
        group = request.form['group']
        login = request.form['login']
        new_name = request.form['new']

        try:
            if groups_dir[group].rename(login, new_name):

                for line in FileInput(f"{UPLOAD_FOLDER}/{group}.txt", inplace=True):
                    fullname = line.split(';')
                    fullname[2] = fullname[2][:-1]
                    if fullname[2] == login:
                        fullname[1] = new_name
                        line = ';'.join(fullname) + '\n'
                    print(line, end='')

                url = ''
                message = 'Fullname успешно изменен'

                return render_template("message.html", message=message, url=url)

            else:

                url = 'rename'
                message = "ERROR (Новый fullname введен некорректно)"

                return render_template("message.html", message=message, url=url)

        except ValueError:

            url = 'rename'
            message = "ERROR (Введенный login отсутствует в списке)"

            return render_template("message.html", message=message, url=url)
    else:

        group = list(groups_dir.keys())

        return render_template("rename.html", group=group)


@app.route('/repos', methods=['GET', 'POST'])
def repos():
    """Страница со списками репозиториев"""

    if request.method == 'POST':
        choice = request.form['choice']
        group = request.form['group']
        repo_name = request.form['repo_name']

        sl_list = []

        if choice == 'repo':
            flag = '-r'
            sl_list = get_repos(group, repo_name, flag)

            return render_template("showrepos.html", group=group, sl_list=sl_list)

        elif choice == 'group':
            flag = '-g'
            sl_list = get_repos(group, repo_name, flag)

            return render_template("showgroups.html", group=group, sl_list=sl_list)

        return None

    else:

        group = list(groups_dir.keys())

        return render_template("getrepos.html", group=group)


def create_args():
    """Функция создания аргуметов аргументов командной строки"""

    par = argparse.ArgumentParser(description='read slush_list')

    par.add_argument('-t', '--token', help="token")
    par.add_argument('-l', '--load', help="loading group")
    par.add_argument('-y', '--year', help="year of admission")
    par.add_argument('-n', '--number', help="group number")
    par.add_argument('-gs', '--getstud', help="search student")
    par.add_argument('-rl', '--relog', nargs="+", help="login change")
    par.add_argument('-rn', '--rename', nargs="+", help="fullname change")
    par.add_argument('-r', '--repo', nargs="+", help="name repo")
    par.add_argument('-g', '--group', nargs="+", help="name group with stud")
    par.add_argument('-sh', '--show', help="show group")

    return par


def get_stud(fullname):
    """
    Функция поиска слушателя по шаблону

    Args:
          fullname:   fullname слушателя, которого нужно найти

    Returns:
          True for success, False otherwise.
    """

    summ = 0

    mass = []

    for key in groups_dir:
        for line in groups_dir[key].show_list():
            if fullname in line.show_fullname():
                print(f"fullname ->{line.show_fullname()}\n"
                      f"login -> {line.show_login()}")
                print("Рабочий репозиторий -> ", end='')
                # https://gitwork.com для примера
                print(f"https://gitwork.ru/{line.show_login()}")

                mass.append(line.show_fullname())
                mass.append(line.show_login())
                mass.append(f"https://gitwork.ru/{line.show_login()}")

                return mass
            summ += 1
        summ = 0

    return False


def get_repos(num_group, repo_name, flags):
    """
    Функция получения списка репозиториев

    Args:
        num_group:  Номер группы
        repo_name:  имя репозитория
        flags:      флаг, необходимый для выбора режима работы

    Returns:
             True for success

    Raises:
             KeyError:  Неверно указан номер группы
    """

    mass = []
    temp_mass = []

    try:
        if flags == "-r":
            for line in groups_dir[num_group].show_list():
                # https://gitwork.com для примера
                login = line.show_login()
                temp_mass.append(f"https://gitwork.ru/{login}/{repo_name}")
                temp_mass.append(f"https://gitwork.ru/{login}/{repo_name}/-/issues")
                temp_mass.append(f"https://gitwork.ru/{login}/{repo_name}/-/milestones")

                mass.append(list(temp_mass))
                temp_mass.clear()

        elif flags == "-g":
            for line in groups_dir[num_group].show_list():
                # https://gitwork.com для примера
                fullname = line.show_fullname()
                mass.append(f"https://gitwork.ru/{repo_name}/{fullname}")

        return mass

    except KeyError as repo_ex:
        print(repo_ex)
        raise


if __name__ == '__main__':

    parser = create_args()
    args = parser.parse_args()

    if args.year or args.number or args.load:

        parser_list = slush_list.Students(args.year, args.number)
        parser_list.read_slush(args.load)

        groups_dir[parser_list.load_slush()] = parser_list

        if args.relog or args.rename or args.getstud or args.repo or args.group:

            if args.relog:
                parser_list.relogin(args.relog[0], args.relog[1])

            if args.rename:
                parser_list.rename(args.rename[0], args.rename[1])

            if args.getstud:
                get_stud(args.getstud)

            if args.repo:
                FLAG = '-r'
                rep = get_repos(args.repo[0], args.repo[1], FLAG)

                for elem in rep:
                    print(f"{elem[0]}\t{elem[1]}\t{elem[2]}\n")

            if args.group:
                FLAG = '-g'
                gr = get_repos(args.group[0], args.group[1], FLAG)
                print('\n'.join(gr))

    else:

        groups_lists = os.listdir(UPLOAD_FOLDER)

        for name in groups_lists:
            if name == '.DS_Store':
                groups_lists.remove(name)

        for file in groups_lists:
            filename = file.split('.')[0]

            gr_number = filename.split('-')

            year = gr_number[0]
            number = gr_number[1]

            start_slush = slush_list.Students(year, number)

            if start_slush.read_slush(f"{UPLOAD_FOLDER}/{file}"):

                group_name = start_slush.load_slush()
                groups_dir[group_name] = start_slush

        app.run(debug=True, host='0.0.0.0')

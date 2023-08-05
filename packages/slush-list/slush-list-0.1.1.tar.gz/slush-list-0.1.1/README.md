### Программное средство работы со списками слушателей

Программа получает на вход тестовый файл формата .txt, читает его и загружает.  

#### Основные функции проекта:

1. Загрузка списка слушателей;
2. Отображение на экране загруженных списков слушателей;
3. Вывод на экран ссылок на репозитории и группы слушателей;
4. Поиск слушателя по шаблону fullname.

#### Функции редактирования списков: 

1. Изменение fullname и login cлушателя; 
2. Идаление загруженной группы.

**Построение docker образа**
```
docker build -t slush_list:1.0 .
```

**Запуск docker контейнера**
```
docker run slush_list:1.0
```

**Опции для запуска из командной строки:**
 
 -l (--load) <путь_к файлу> - читает указанную группу
 
 ```
 docker run -v path/to/file:/slush-list/new_file.txt slush_list:1.0 -l slush-list/new_file.txt
```

-y (--year) <год_поступления> - год поступления (необходимо для создания имени группы)

```
docker run -v path/to/file:/slush-list/new_file.txt slush_list:1.0 -l slush-list/new_file.txt -y 2018
```

-n (--number) <номер_группы> - номер группы (необходимо для создания имени группы)

```
docker run -v path/to/file:/slush-list/new_file.txt slush_list:1.0 -l slush-list/new_file.txt -y 2018 -gn 3
```

-rl (--relogin) <старый_логин> <новый_логин> - изменение login слушателя

```
docker run -v path/to/file:/slush-list/new_file.txt slush_list:1.0 -l slush-list/new_file.txt -y 2018 -gn 3 -rl nazar_lex nazarov
```

-rn (--rename) <логин> <новый_fullname> - изменение fullname слушателя

 ```
 docker run -v path/to/file:/slush-list/new_file.txt slush_list:1.0 -l slush-list/new_file.txt -y 2018 -gn 3 -rn nazar_lex 2018-3-33-nazarov
```

-r (--repo) <номер_группы> <репозиторий> - отображение ссылок на репозитории слушателей

```
 docker run -v path/to/file:/slush-list/new_file.txt slush_list:1.0 -l slush-list/new_file.txt -y 2018 -r 2018-3 timp
```

-g (--group) <номер_группы> <группа> - отображение ссылок на группы слушателей

```
 docker run -v path/to/file:/slush-list/new_file.txt slush_list:1.0 -l slush-list/new_file.txt -y 2018 -g 2018-3 prac
```

-gs(--getstud) <fullname> - находит слушателя с указанным fullname

```
 docker run -v path/to/file:/slush-list/new_file.txt slush_list:1.0 -l slush-list/new_file.txt -y 2018 -gs 2018-3-20-naz
```

**Запуск веб-приложения:**

```
docker run -d -p 5000:5000 slush_list:1.0
```

Далее необоходимо прописать в браузере адрес: 0.0.0.0:5000


**Запуск Pylint**

```
pylint main.py
pylint slush_list.py
pylint test_slush.py
 ```
 
**Запуск тестов**
```
pytest test_slush.py 
```

**Покрытие кода**
```
pytest --cov=slush_list
```

**Построение пакета для загрузки на PyPI** 

Необходимо выполнить данную команду из того же каталога, где находится pyproject.toml:

```
python3 -m build
```

Данная команда генерирует два файла каталоге dist:

```
dist/
  slush-list-VERSION.tar.gz
  slush_list-VERSION-py3-none-any.whl
```

**Загрузка пакета на PyPI** 

Необходимо иметь учетную запись на PyPI для загрузки пакета.  
Выполните команду:

```
python3 -m twine upload dist/*
```

**Установка пакета** 

Выполните команду:

```
python3 -m pip install slush-list
```


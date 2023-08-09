'''
Парсер для файлов next-API платформы Checkio ver 2.0
'''
from os import walk
import re
#import pandas as pd


directory_name = 'C:\\Users\\Infotech_5\\OneDrive\\Документы\\GitHub'  # Всавить путь к папке мисси
mission_name = 'checkio-mission-long-non-repeat'  # Всавить название миссии

with open('C:\\Users\\Infotech_5\\PycharmProjects\\checkio_auoto\\python_3') as file:
    strings = file.read()
    lib = re.findall(r'(import [a-zA-Z0-9_ ]+|from [a-zA-Z0-9_ ]+)', strings)
    p_name = re.findall(r'def \w+\(', strings)
    start_func = re.search(r'def ', strings)
    end_func = re.search(r'return \w+', strings)
    example = re.findall(p_name[0][4:-1] + r'\([a-zA-Z0-9_ :,.\[\]\{\}\'\"\|]*\)\)\s?==', strings)


with open('C:\\Users\\Infotech_5\\PycharmProjects\\checkio_auoto\\python_3.tmpl', 'w') as file:
    file.write('''{% comment %}New initial code template{% endcomment %}
{% block env %}''' +
'\n'.join(lib)
+ '''{% endblock env %}

{% block start %}
''' +
strings[start_func.start():end_func.end()]
+ '''
{% endblock start %}

{% block example %}
print('Example:')
print(''' +
example[0][:-3]
+ '''
{% endblock %}

{% block tests %}
{% for t in tests %}
assert {% block call %}''' + p_name[0][4:-1] + '''({{t.input|p_args}})
{% endblock %} == {% block result %}{{t.answer|p}}{% endblock %}{% endfor %}
{% endblock %}

{% block final %}
print("The mission is done! Click 'Check Solution' to earn rewards!")
{% endblock final %}''')


with open('C:\\Users\\Infotech_5\\PycharmProjects\\checkio_auoto\\js_node') as file:
    strings = file.read()
    lib = re.findall(r'import [a-zA-Z0-9_ \"\';]+', strings)
    j_name = re.findall(r'function \w+\(', strings)
    start_func = re.search(r'function ', strings)
    end_func = re.search(r'return \w+;', strings)
    example = re.findall(j_name[0][9:-1] + r'\([a-zA-Z0-9_ :,.\[\]\{\}\'\"\|]*\)\)\s?==', strings)


with open('C:\\Users\\Infotech_5\\PycharmProjects\\checkio_auoto\\js_node.tmpl', 'w') as file:
    file.write('''{% comment %}New initial code template{% endcomment %}
{% block env %}''' +
'\n'.join(lib)
+ '''{% endblock env %}

{% block start %}
''' +
strings[start_func.start():end_func.end()]
+ '''
}
{% endblock start %}

{% block example %}
console.log('Example:');
console.log(sumTwo(3, 2));
{% endblock %}

// These "asserts" are used for self-checking
{% block tests %}
{% for t in tests %}
assert.strictEqual({% block call %}''' + j_name[0][9:-1] + '''({{t.input|j_args}})
{% endblock %}, {% block result %}{{t.answer|j}}{% endblock %});{% endfor %}
{% endblock %}

{% block final %}
console.log("Coding complete? Click 'Check Solution' to earn rewards!");
{% endblock final %}''')


with open("C:\\Users\\Infotech_5\\PycharmProjects\\checkio_auoto\\init.js", 'w') as file:
    file.write('''requirejs(['ext_editor_io2', 'jquery_190'],
    function (extIO, $) {
        var io = new extIO({});
        io.start();
    }
);
''')


with open("C:\\Users\\Infotech_5\\PycharmProjects\\checkio_auoto\\referee.py", 'w') as file:
    file.write('''from checkio.signals import ON_CONNECT
from checkio import api
from checkio.referees.io_template import CheckiOReferee
# from checkio.referees.checkers import to_list

from tests import TESTS

api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        # checker=to_list,
        function_name={
            "python": "''' + p_name[0][4:-1] + '''",
            "js": "''' + j_name[0][9:-1] + '''"
        },
        cover_code={
            'python-3': {},
            'js-node': {
                # "dateForZeros": True,
            }
        }
    ).on_ready)\n''')


def task_desc_change(path):  # Функция для изменения строчек теста в такс-дискрипте на новую строку next-API
    task_descrption = open(f'{path}', mode='r', encoding='utf-8')
    lines = task_descrption.readlines()

    if_str = ['<pre class="brush: {% if is_js %}javascript{% else %}python{% endif %}">{{init_code_tmpl}}</pre>\n']
    if ''.join(if_str) not in lines:
        print(lines)
        task_start = 0
        task_end = 0
        for i in range(len(lines)):  # Определяем границы искомого куска кода по "ключевым" меткам '{% if' и '{% endif'
            if lines[i].strip().startswith('{% if'):
                task_start = i
            elif lines[i].strip().startswith('{% endif'):
                task_end = i
        lines[task_start:task_end+1] = if_str  # Заменяем ненужный кусок на актуальный код
    task_descrption.close()
    task_descrption = open(rf'{path}', mode='w', encoding='utf-8')
    task_descrption.write(''.join(lines))  # Заново открытый файл перетираем корректным кодом
    task_descrption.close()
    print(f'{path} - OK')


# Парсинг файла task_description.html
# Используем библиотеку "os" и находим все файлы таск-дискрипта. Используя функцию task_desc_change, изменяем эти файлы
walking = walk(f'{directory_name}\\{mission_name}')
path_info = ''
for i in walking:
    if 'task_description.html' in i[2]:  # Находим по директориям где есть нужный нам файл
        for u in i[2]:
            if u.startswith('task_description.html'):  # Берем нужный нам файл и крепим к директории
                path_info = i[0] + '\\' + u
                task_desc_change(path_info)  # Вызываем функцию передавая ей каждый раз новый путь для изменений

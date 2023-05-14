import sys
from datetime import datetime
from subprocess import run

# Получаем данные из stdout команды ps и приводим их в удобочитаемый вид при помощи функции .decode
result = run(['ps', 'aux'], capture_output=True)
raw_data = result.stdout.decode()

# Разбиваем строки с данными по пробелам
sdata = raw_data.split('\n')

# Получаем массив данных выбрасывая заголовок и последнюю строку со знаком переноса строки
a = sdata[1:-1]  # deleted unnecessary rows from list of strings

# Получаем список с данными без лишних пробелов
new_list = []  # list of lists USER=0, PID=1, %CPU=2, %MEM=3, VSZ=4, RSS=5, TT=6, STAT=7, STARTED =8; TIME=9, COMMAND=10
for i in a:
    b = i.split(' ')
    c = [i for i in b if i != '']
    new_list.append(c)

# Получаем всех уникальных пользователей
only_users = ([i[0] for i in new_list])
unique_names = set(only_users)

# Вывести количество процессов для каждого пользователя (посчитать сколько раз встречается каждый пользователь)
number_of_processes = dict.fromkeys(unique_names, 0)
for i in unique_names:
    for j in only_users:
        if i == j:
            number_of_processes[i] += 1
number = 1
print('Уникальные пользователи и количество процессов для каждого пользователя:')
for i in number_of_processes:
    print(f'{number}. {i} - {number_of_processes[i]} шт.')
    number += 1

# Сколько всего памяти используется и сколко используется CPU (идем построчно и  суммируем значения приводя их к float)
memory_usage = 0
cpu_usage = 0
for i in new_list:
    cpu_usage += float(i[2])
    memory_usage += float(i[3])
print(f'Всего использоваро оперативной памяти {memory_usage}')
print(f'Процессор загружен на {cpu_usage} %')

"""Какой процесс занимает больше всего памяти и больше всего CPU (заводим словарик - имя процесса и значение)
имя процесса >20 символов, то ее нужно обрезать:"""

cpu_burner = {'name': 'noname', 'cpu': 0}
memory_burner = {'name': 'noname', 'memory': 0}
for i in new_list:
    if float(i[2]) > cpu_burner['cpu']:
        cpu_burner['name'] = i[10][0:21]
        cpu_burner['cpu'] = float(i[2])
    else:
        pass
    if float(i[3]) > memory_burner['memory']:
        memory_burner['name'] = i[10][0:21]
        memory_burner['memory'] = float(i[3])
    else:
        pass
print(f'Этот процесс больше всего нагружает процессор {cpu_burner}')
print(f'Этот процесс занимает больше всего оперативной памяти {memory_burner}')

# Парсер должен вывести в стандартный вывод всю информацию
# Парсер должен сохранить данные в отдельный файл (имя файла должно соответствовать текущей дате)
# Скриншот терминала с информацией о процессах


with open(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}-scan.txt', 'w') as f:
    sys.stdout = f
    number = 1
    print('Уникальные пользователи и количество процессов для каждого пользователя:')
    for i in number_of_processes:
        print(f'{number}. {i} - {number_of_processes[i]} шт.')
        number += 1
    print(f'Всего использоваро оперативной памяти {memory_usage}')
    print(f'Процессор загружен на {cpu_usage} %')
    print(f'Этот процесс больше всего нагружает процессор {cpu_burner}')
    print(f'Этот процесс занимает больше всего оперативной памяти {memory_burner}')

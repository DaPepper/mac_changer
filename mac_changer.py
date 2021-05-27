#!/usr/bin/env python
# -*- coding: utf-8 -*-

# импорт модуля для работы с командами в терменале
import subprocess
# штука для обучения парсера, например python3 main.py -i
import optparse
# правила для поиска чего то в тексте
import re

def get_arguments():
    parser = optparse.OptionParser()
    # при вводе python3 mac_changer -i будет выводиться текст помощи. dest='переменная'
    parser.add_option("-i", "--interface", dest="interface", help="Имя интерфейса MAC адрес которого будет изменен")
    parser.add_option("-m", "--mac", dest="new_mac", help="Новый MAC адрес")
    # Вывод списка возможных моих команд
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Пожалуйста укажите интерфейс, используйте --help для большей информации")
    elif not options.new_mac:
        parser.error("[-] Пожалуйста укажите MAC адрес, используйте --help для большей информации")
    return options

# этот подход безопаснее, он не дает использовать команды, которые не должен вводить юзер
def change_mac(interface, new_mac):
    print("[+] Меняем MAC адрес для " + interface + ' на ' + new_mac)
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print('[-] Не могу прочитать MAC адрес')


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Текущий MAC = " + str(current_mac))
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print('[+] MAC адрес был успешно изменен на ' + current_mac)
else:
    print('[-] MAC адрес не изменен')



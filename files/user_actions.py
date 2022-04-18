# В этом файле собраны функции и классы для работы с действиями пользователя (взять зонт, сдать зонт,
# написать в поддержку, вернуть инструкции, вернуть описание проекта)
import sqlite3
import datetime


# Взять зонт
def info_from_index(path_to_db, system_index):
    connect = sqlite3.connect(path_to_db)
    cursor = connect.cursor()

    place, free_cell, fill_cell = cursor.execute(f"SELECT place, free_cell, fill_cell FROM points "
                                                 f"WHERE system_index='{system_index}'").fetchall()[0]

    return place, free_cell, fill_cell


# Взять зонт
def taken_umbrella(path_to_db, system_index):
    connect = sqlite3.connect(path_to_db)
    cursor = connect.cursor()

    col_umbr = len(cursor.execute(f"SELECT id FROM taken WHERE returned=0").fetchall())

    if col_umbr < 3:
        cursor.execute(f"INSERT INTO taken (time) VALUES ('{datetime.datetime.now()}')")
        cursor.execute(f"UPDATE points SET free_cell = free_cell + 1 WHERE system_index = '{system_index}'")
        cursor.execute(f"UPDATE points SET fill_cell = fill_cell - 1 WHERE system_index = '{system_index}'")
        connect.commit()
        return True

    else:
        return False


# Сдать зонт
def returned_umbrella(path_to_db, system_index):
    connect = sqlite3.connect(path_to_db)
    cursor = connect.cursor()

    col_umbr = len(cursor.execute(f"SELECT id FROM taken WHERE returned=0").fetchall())

    if col_umbr > 0:
        min_id_umb = min(cursor.execute(f"SELECT id FROM taken WHERE returned=0").fetchall()[0])
        cursor.execute(f"UPDATE taken SET return_time = '{datetime.datetime.now()}' WHERE id = '{min_id_umb}'")
        cursor.execute(f"UPDATE taken SET returned = 1 WHERE id = '{min_id_umb}'")
        cursor.execute(f"UPDATE points SET free_cell = free_cell - 1 WHERE system_index = '{system_index}'")
        cursor.execute(f"UPDATE points SET fill_cell = fill_cell + 1 WHERE system_index = '{system_index}'")
        connect.commit()
        return True

    else:
        return False


# Вернуть инструкции
def instruction(path_to_file):
    file = open(path_to_file, 'r')
    text = file.read()
    return text


if __name__ == '__main__':
    db_path = '../db/data.db'
    # info_from_index(db_path, '1111')
    # taken_umbrella(db_path, '1111')
    # returned_umbrella(db_path, '1111')
    # print(instruction('txt/description.txt'))

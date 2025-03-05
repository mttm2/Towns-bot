import pyautogui
import keyboard
import time
import random
import os
import re

def record_positions(prompt):
    positions = []
    print(f"{prompt} (Нажимай 'SPACE' для записи, 'S' для завершения)")

    while True:
        if keyboard.is_pressed('s'):  # Если 'S' нажата, выходим
            print("Запись координат завершена.")
            time.sleep(0.3)  # Короткая задержка, чтобы избежать двойных нажатий
            break
        elif keyboard.is_pressed('space'):  # Если 'SPACE', записываем координаты
            x, y = pyautogui.position()
            positions.append((x, y))
            print(f"Записано: {x}, {y}")
            time.sleep(0.3)  # Короткая задержка, чтобы избежать двойных нажатий

    return positions

# Функция записи одной координаты
def record_single_position(prompt):
    print(f"{prompt} (Нажми 'space' для записи)")

    while True:
        if keyboard.is_pressed('space'):
            x, y = pyautogui.position()
            print(f"Записано: {x}, {y}")
            time.sleep(0.3)
            return (x, y)
# Функция загрузки сообщений
def load_unique_messages(filename="msg.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            messages = [line.strip() for line in file.readlines() if line.strip()]

        if not messages:
            return []

        random.shuffle(messages)
        return messages
    except FileNotFoundError:
        print("Файл msg.txt не найден!")
        return []

# Функция внесения ошибок в текст
def introduce_typo(message, typo_prob=0.1):
    if random.random() > typo_prob:
        return message  # Без ошибок

    message = list(message)
    typo_type = random.choice(["miss", "repeat", "swap"])

    if typo_type == "miss" and len(message) > 2:
        del message[random.randint(0, len(message) - 1)]  # Удаляет случайный символ

    elif typo_type == "repeat" and len(message) > 2:
        index = random.randint(0, len(message) - 1)
        message.insert(index, message[index])  # Дублирует символ

    elif typo_type == "swap" and len(message) > 2:
        index = random.randint(0, len(message) - 2)
        message[index], message[index + 1] = message[index + 1], message[index]  # Меняет местами

    return "".join(message)

# Функция рассылки сообщений с парсингом
def send_messages(browser_coords, channel_coords, chat_coord, send_button_coord, num_cycles=None, cycle_pause=1300, use_discord=False):
    cycle_count = 0

    while num_cycles is None or cycle_count < num_cycles:
        cycle_count += 1
        print(f"**Цикл {cycle_count}**")

        if use_discord:
            print("Запускаем парсинг сообщений из Discord...")
            os.system("python discord_parser.py")  
            time.sleep(5)  

        messages = load_unique_messages()
        if not messages:
            print("Ошибка: Файл msg.txt пуст. Пропускаем этот цикл.")
            continue

        randomized_cycle_pause = cycle_pause + random.randint(-60, 60)
        print(f"**Пауза между циклами: {randomized_cycle_pause} секунд**")

        random.shuffle(browser_coords)  # Перемешиваем браузеры

        for browser_x, browser_y in browser_coords:
            pyautogui.click(browser_x + random.randint(-5, 5), browser_y + random.randint(-5, 5))
            print(f"Переключился на браузер: {browser_x}, {browser_y}")
            time.sleep(random.uniform(3, 15))

            random.shuffle(channel_coords)  # Перемешиваем каналы

            for channel_x, channel_y in channel_coords:
                if random.random() < 0.3:  # 30% шанс пропустить канал
                    print(f"Пропустил канал: {channel_x}, {channel_y}")
                    continue  

                pyautogui.click(channel_x + random.randint(-5, 5), channel_y + random.randint(-5, 5))
                print(f"Открыл канал: {channel_x}, {channel_y}")
                time.sleep(random.uniform(20, 40))

                chat_x_randomized = chat_coord[0] + random.randint(-50, 50)
                pyautogui.click(chat_x_randomized, chat_coord[1] + random.randint(-5, 5))
                print(f"Открыл чат: {chat_x_randomized}, {chat_coord[1]}")
                time.sleep(random.uniform(5, 30))

                message = introduce_typo(random.choice(messages))  # Добавляем опечатки
                pyautogui.write(message, interval=random.uniform(0.03, 0.08))
                print(f"Отправил сообщение: {message}")
                time.sleep(random.uniform(5, 45))

                pyautogui.click(send_button_coord[0] + random.randint(-5, 5), send_button_coord[1] + random.randint(-5, 5))
                print(f"Кликнул кнопку отправки")
                time.sleep(random.uniform(5, 45))

                wait_time = random.randint(15, 60)
                print(f"Ожидание {wait_time} секунд...")
                time.sleep(wait_time)

                # Иногда отправлять дополнительное сообщение
                if random.random() < 0.5:  # 50% шанс отправить ещё одно сообщение
                    message = introduce_typo(random.choice(messages))
                    pyautogui.write(message, interval=random.uniform(0.03, 2))
                    print(f"Отправил дополнительное сообщение: {message}")
                    time.sleep(random.uniform(5, 20))

                    pyautogui.click(send_button_coord[0] + random.randint(-5, 5), send_button_coord[1] + random.randint(-5, 5))
                    print(f"Кликнул кнопку отправки (доп. сообщение)")
                    time.sleep(random.uniform(10, 20))

        print(f"**Пауза между циклами {randomized_cycle_pause} секунд...**")
        time.sleep(randomized_cycle_pause)
# Функция выполнения "Дейлика"
def perform_daily_task(browser_coords, daily_steps, beaver_position, gas_payment_position, pause_between_accounts):
    random.shuffle(browser_coords)

    for browser_x, browser_y in browser_coords:
        pyautogui.click(browser_x + random.randint(-5, 5), browser_y + random.randint(-5, 5))
        print(f"Переключился на браузер: {browser_x}, {browser_y}")
        time.sleep(random.uniform(10, 30))

        for step_x, step_y in daily_steps:
            pyautogui.click(step_x + random.randint(-5, 5), step_y + random.randint(-5, 5))
            print(f"Выполнил действие: {step_x}, {step_y}")
            time.sleep(random.uniform(2, 6))

        # Выполняем клик по бобру и оплату газа
        pyautogui.click(beaver_position[0] + random.randint(-5, 5), beaver_position[1] + random.randint(-5, 5))
        print(f"Клик по бобру: {beaver_position}")
        time.sleep(random.uniform(5, 10))

        pyautogui.click(gas_payment_position[0] + random.randint(-5, 5), gas_payment_position[1] + random.randint(-5, 5))
        print(f"Оплата газа: {gas_payment_position}")
        time.sleep(random.uniform(10, 16))

        print(f"⏸ Ожидание между аккаунтами: {pause_between_accounts} секунд...")
        time.sleep(pause_between_accounts)

    print("**Дейлик завершен!**")
# Функция отображения баннера
def show_banner():
    banner = """
 Crypto Media Zone 
 Telegram Channel: https://t.me/cmzcrypto
 Contact: @mzzzttm
    """
    print(banner)

if __name__ == "__main__":
    # Показываем баннер перед запуском
    show_banner()
    use_discord = input("Будете ли использовать Discord для пополнения msg.txt? (Y/N): ").strip().lower() == "y"

    print("Выберите режим работы:")
    print("1 - Рассылка сообщений")
    print("2 - Дейлик")

    while True:
        if keyboard.is_pressed('1'):
            print("Выбран режим: Рассылка сообщений")

            browser_positions = record_positions("Наведи курсор на иконку браузера и нажми 'space'")
            channel_positions = record_positions("Наведи курсор на канал и нажми 'space'")
            chat_position = record_single_position("Наведи курсор на чат и нажми 'space'")
            send_button_position = record_single_position("Наведи курсор на кнопку отправки и нажми 'space'")

            num_cycles = int(input("Введите количество циклов (0 = бесконечно): ")) or None
            cycle_pause = int(input("Введите паузу между циклами (сек): "))

            print("Нажмите '5' для старта...")
            keyboard.wait('5')

            send_messages(browser_positions, channel_positions, chat_position, send_button_position, num_cycles, cycle_pause, use_discord)
            print("Готово! Все сообщения отправлены.")
            break

        elif keyboard.is_pressed('2'):
            print("Выбран режим: Дейлик")

            browser_positions = record_positions("Наведи курсор на иконку браузера и нажми 'space'")
            daily_steps = record_single_position("Наведи курсор на открытие дейлика и нажми 'space'")
            beaver_position = record_single_position("Наведи курсор на бобра и нажми 'space'")
            gas_payment_position = record_single_position("Наведи курсор на оплату газа и нажми 'space'")

            pause_between_accounts = int(input("⏸ Введите паузу между аккаунтами (сек): "))

            print("Нажмите '5' для старта...")
            keyboard.wait('5')

            perform_daily_task(browser_positions, daily_steps, beaver_position, gas_payment_position, pause_between_accounts)
            print("Дейлик выполнен!")
            break

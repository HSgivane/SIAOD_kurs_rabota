import customtkinter as ctk
import math

# Создаем главное окно приложения
app = ctk.CTk()
app.title("Управление расписанием автобусов")
app.geometry("500x700")

# Функция для обработки введенных данных
def submit_data():
    try:
        num_buses = entry_buses.get().strip()
        if not num_buses.isdigit() or int(num_buses) <= 0:
            raise ValueError("Количество автобусов должно быть положительным числом.")

        num_buses = int(num_buses)
        driver_type = driver_type_var.get()
        schedule, total_drivers = calculate_schedule(num_buses, driver_type)

        # Вывод расписания в интерфейсе
        output_textbox.delete(1.0, "end")
        output_textbox.insert("end", "Составленное расписание:\n")
        for time, buses in schedule.items():
            output_textbox.insert("end", f"{time}:\n")
            output_textbox.insert("end", "\n".join(buses) + "\n\n")
        
        output_textbox.insert("end", f"\nОбщее количество водителей: {total_drivers}\n")
    except ValueError as e:
        output_textbox.delete(1.0, "end")
        output_textbox.insert("end", f"Ошибка: {e}")

# Функция для расчета расписания и минимального числа водителей
def calculate_schedule(num_buses, driver_type):
    peak_hours = [(7, 9), (17, 19)]  # Часы пик
    route_time = 70  # Длина маршрута в минутах

    peak_load = 0.7  # 70% нагрузки в часы пик
    off_peak_load = 0.3  # 30% нагрузки вне часов пик

    work_hours = list(range(6, 24)) + list(range(0, 3))  # Время работы автобусов с 6:00 до 3:00

    schedule = {}

    # Логика для водителей типа B
    if driver_type == "B":
        total_drivers = math.ceil(num_buses * peak_load)
        drivers = [f"Водитель {i + 1}" for i in range(total_drivers)]

        for hour in work_hours:
            buses = []

            if any(start <= hour < end for start, end in peak_hours):
                buses_needed = math.ceil(num_buses * peak_load)
            else:
                buses_needed = math.ceil(num_buses * off_peak_load)

            for bus_id in range(1, buses_needed + 1):
                driver = drivers[(bus_id - 1) % total_drivers]
                buses.append(f"Автобус {bus_id} ({driver})")

            schedule[f"{hour:02d}:00"] = buses

        return schedule, total_drivers

    # Для водителей типа A логика остается прежней
    max_work_hours = 8
    driver_pool = []
    driver_id = 1

    for start_hour in range(6, 24, max_work_hours):
        shift_start = start_hour
        shift_end = (start_hour + max_work_hours) % 24
        driver_pool.append({
            "id": driver_id,
            "start": shift_start,
            "end": shift_end
        })
        driver_id += 1

    if 3 > 0:
        driver_pool.append({
            "id": driver_id,
            "start": 0,
            "end": 3
        })

    total_drivers = len(driver_pool)

    for hour in work_hours:
        buses = []
        if any(start <= hour < end for start, end in peak_hours):
            buses_needed = math.ceil(num_buses * peak_load)
        else:
            buses_needed = math.ceil(num_buses * off_peak_load)

        active_drivers = [
            driver for driver in driver_pool if driver["start"] <= hour < driver["end"]
        ]

        while len(active_drivers) < buses_needed:
            new_driver_id = len(driver_pool) + 1
            new_start = hour
            new_end = (hour + max_work_hours) % 24
            driver_pool.append({
                "id": new_driver_id,
                "start": new_start,
                "end": new_end
            })
            active_drivers.append(driver_pool[-1])
            total_drivers += 1

        for bus_id in range(1, buses_needed + 1):
            driver = active_drivers[(bus_id - 1) % len(active_drivers)]
            buses.append(f"Автобус {bus_id} (Водитель {driver['id']})")

        schedule[f"{hour:02d}:00"] = buses

    return schedule, total_drivers

# Переменные для хранения данных
entry_buses = ctk.CTkEntry(app, placeholder_text="Введите количество автобусов")
entry_buses.pack(pady=10)

driver_type_var = ctk.StringVar(value="A")

driver_type_label = ctk.CTkLabel(app, text="Выберите тип водителя:")
driver_type_label.pack(pady=5)

driver_type_a = ctk.CTkRadioButton(app, text="Тип A", variable=driver_type_var, value="A")
driver_type_a.pack(pady=5)

driver_type_b = ctk.CTkRadioButton(app, text="Тип B", variable=driver_type_var, value="B")
driver_type_b.pack(pady=5)

# Поле для отображения результата
output_textbox = ctk.CTkTextbox(app, height=400)
output_textbox.pack(pady=10)

# Кнопка для подтверждения данных
submit_button = ctk.CTkButton(app, text="Подтвердить", command=submit_data)
submit_button.pack(pady=20)

# Запуск приложения
app.mainloop()

import tkinter as tk
from tkinter import font as tkfont
import datetime
import calendar
import random
import re
import threading
import requests

# --- Библиотеки для погоды ---
try:
    import whereismyip
    HAS_GEO = True
except ImportError:
    HAS_GEO = False
    print("[WARN] whereismyip не найден. Установите: pip install whereismyip")

class WidgetsApp:
    # ---------- Палитра (наша старая, стильная) ----------
    BG_TOP      = "#0F0B1E"
    BG_BOTTOM   = "#1A1035"
    CARD_TOP    = "#221A3D"
    CARD_BOTTOM = "#15102A"
    CARD_EDGE   = "#3B2E66"
    TEXT_LIGHT  = "#F2EEFF"
    TEXT_DIM    = "#C8BEE0"
    
    ACCENT      = "#A78BFA"
    ACCENT_HOV  = "#C4B5FD"
    ACCENT_PRS  = "#7C5CE6"
    
    ACCENT_2    = "#22D3EE"
    
    INPUT_BG    = "#100A1F"
    INPUT_BORDER= "#3B2E66"
    
    ERROR_RED   = "#EF4444"
    SUCCESS_GREEN = "#22C55E"

    W, H = 850, 700

    def __init__(self, root):
        self.root = root
        self.root.title("Виджеты · Premium UI")
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_TOP)
        self._center_window(self.W, self.H)

        self.current_widget = "login"
        
        # Календарь
        today = datetime.date.today()
        self.cal_year = today.year
        self.cal_month = today.month
        
        # --- Погода (будет загружена реальная) ---
        self.weather_temp = "--"
        self.weather_icon = "☀️"
        self.weather_desc = "Загрузка..."
        self.weather_city = "Определение..."
        self.weather_forecast = []
        self.weather_loading = True

        self._init_fonts()

        self.canvas = tk.Canvas(root, width=self.W, height=self.H,
                                highlightthickness=0, bd=0, bg=self.BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        self._draw_background()
        self._draw_top_menu()
        self._draw_widget()
        
        # Запускаем загрузку погоды в фоне
        self.root.after(100, self._load_weather_async)

    def _init_fonts(self):
        self.title_font  = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.h1_font     = tkfont.Font(family="Segoe UI", size=24, weight="bold")
        self.h2_font     = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.lbl_font    = tkfont.Font(family="Segoe UI", size=12)
        self.small_font  = tkfont.Font(family="Segoe UI", size=10)
        self.num_font    = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        self.temp_font   = tkfont.Font(family="Segoe UI", size=64, weight="bold")
        self.icon_font   = tkfont.Font(family="Segoe UI Symbol", size=36)

    # ============================================================
    #                ЗАГРУЗКА ПОГОДЫ (ФОН)
    # ============================================================
    def _load_weather_async(self):
        thread = threading.Thread(target=self._fetch_weather, daemon=True)
        thread.start()

    def _get_coordinates(self, city_name):
        """Получает широту и долготу по названию города через Open-Meteo."""
        try:
            url = "https://geocoding-api.open-meteo.com/v1/search"
            params = {"name": city_name, "count": 1, "language": "ru", "format": "json"}
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return result["latitude"], result["longitude"], result["name"]
        except Exception as e:
            print(f"[WARN] Ошибка геокодинга: {e}")
        return None, None, city_name

    def _fetch_weather(self):
        """Получает город по IP и погоду на 7 дней через Open-Meteo."""
        city = None
        
        # 1. Определяем город по IP
        if HAS_GEO:
            try:
                loc_str = whereismyip.whereismyip()
                if loc_str:
                    city = loc_str.split(",")[0].strip()
            except Exception as e:
                print(f"[WARN] Ошибка геолокации: {e}")

        if not city:
            city = "Moscow"

        # 2. Получаем координаты
        lat, lon, resolved_city = self._get_coordinates(city)
        self.weather_city = resolved_city
        
        if lat is None or lon is None:
            self.weather_desc = "Ошибка геолокации"
            self.weather_icon = "⚠️"
            self.weather_loading = False
            self.root.after(0, self._refresh_ui)
            return

        # 3. Запрашиваем прогноз на 7 дней
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
                "current": ["temperature_2m", "weather_code"],
                "timezone": "auto",
                "forecast_days": 7
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            current = data["current"]
            self.weather_temp = round(current["temperature_2m"])
            code = current["weather_code"]
            
            # Расшифровка кодов погоды (WMO)
            weather_map = {
                0: ("☀️", "Ясно"), 1: ("🌤️", "Малооблачно"), 2: ("⛅", "Облачно"), 3: ("☁️", "Пасмурно"),
                45: ("🌫️", "Туман"), 48: ("🌫️", "Изморозь"),
                51: ("🌦️", "Легкая морось"), 53: ("🌦️", "Морось"), 55: ("🌧️", "Сильная морось"),
                61: ("🌧️", "Небольшой дождь"), 63: ("🌧️", "Дождь"), 65: ("🌧️", "Сильный дождь"),
                71: ("🌨️", "Небольшой снег"), 73: ("🌨️", "Снег"), 75: ("❄️", "Сильный снег"),
                80: ("🌦️", "Ливень"), 81: ("🌧️", "Сильный ливень"), 82: ("⛈️", "Очень сильный ливень"),
                95: ("⛈️", "Гроза"),
            }
            self.weather_icon, self.weather_desc = weather_map.get(code, ("🌤️", "Переменно"))

            # Прогноз на 7 дней
            self.weather_forecast = []
            daily = data["daily"]
            days_ru = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            
            for i in range(len(daily["time"])):
                date_obj = datetime.datetime.strptime(daily["time"][i], "%Y-%m-%d")
                day_name = days_ru[date_obj.weekday()]
                maxtemp = round(daily["temperature_2m_max"][i])
                code = daily["weather_code"][i]
                icon, _ = weather_map.get(code, ("🌤️", ""))
                self.weather_forecast.append((day_name, maxtemp, icon))

            self.weather_loading = False
            print(f"[OK] Погода загружена (7 дней): {self.weather_temp}°C, {self.weather_desc}")

        except Exception as e:
            print(f"[ERR] Ошибка загрузки погоды: {e}")
            self.weather_desc = "Ошибка загрузки"
            self.weather_icon = "⚠️"
            self.weather_loading = False

        self.root.after(0, self._refresh_ui)

    def _refresh_ui(self):
        self.canvas.delete("all")
        self._draw_background()
        self._draw_top_menu()
        self._draw_widget()

    # ============================================================
    #                ОТРИСОВКА
    # ============================================================
    def _draw_background(self):
        for y in range(self.H):
            t = y / self.H
            r = int(15 + (26 - 15) * t)
            g = int(11 + (16 - 11) * t)
            b = int(30 + (53 - 30) * t)
            self.canvas.create_line(0, y, self.W, y, fill=f"#{r:02x}{g:02x}{b:02x}")

    def _draw_top_menu(self):
        self.canvas.delete("top_menu")
        cx = self.W / 2
        self.canvas.create_text(cx, 20, text="ВЫБЕРИТЕ ВИДЖЕТ", 
                                font=self.small_font, fill=self.TEXT_DIM, tags="top_menu")

        for i, (key, label) in enumerate([("login", "1: Вход"), ("weather", "2: Погода"), ("calendar", "3: Календарь")]):
            x = cx - 200 + i * 140
            tag = f"menu_btn_{i+1}"
            is_active = self.current_widget == key
            color = self.ACCENT if is_active else "#1E293B"
            text_color = self.BG_TOP if is_active else self.TEXT_DIM
            
            self.canvas.create_rectangle(x - 70, 35, x + 70, 55, 
                                          fill=color, outline="", tags=("top_menu", tag))
            self.canvas.create_text(x, 45, text=label, font=self.small_font, 
                                    fill=text_color, tags=("top_menu", tag))
            
            self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, k=key: self._switch_widget(k))
            self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def _switch_widget(self, key):
        self.current_widget = key
        self.canvas.delete("all")
        self._draw_background()
        self._draw_top_menu()
        self._draw_widget()

    def _draw_widget(self):
        if self.current_widget == "login":
            self._draw_login()
        elif self.current_widget == "weather":
            self._draw_weather()
        else:
            self._draw_calendar()

    # ============================================================
    #                ВИДЖЕТ 1: ВХОД
    # ============================================================
    def _draw_login(self):
        cx = self.W/2
        self._rounded_rect(cx - 220, 90, cx + 220, 610, radius=20, 
                           fill=self.CARD_BOTTOM, outline=self.CARD_EDGE, width=1)
        self._rounded_rect(cx - 215, 95, cx + 215, 605, radius=18, 
                           fill=self.CARD_TOP, outline="")
        
        self.canvas.create_text(cx, 140, text="🔐 Вход в аккаунт", 
                                font=self.h1_font, fill=self.TEXT_LIGHT)
        
        self.canvas.create_text(cx - 180, 200, text="EMAIL", 
                                font=self.small_font, fill=self.TEXT_DIM, anchor="w")
        self._rounded_rect(cx - 180, 220, cx + 180, 265, radius=8, 
                           fill=self.INPUT_BG, outline=self.INPUT_BORDER, width=1)
        self.email_entry = tk.Entry(self.root, font=self.lbl_font, bg=self.INPUT_BG, 
                                     fg=self.TEXT_LIGHT, insertbackground=self.TEXT_LIGHT,
                                     bd=0, highlightthickness=0)
        self.email_entry.insert(0, "arun@arunsfoli.com")
        self.canvas.create_window(cx, 242, window=self.email_entry, width=340, height=30)
        
        self.canvas.create_text(cx - 180, 300, text="ПАРОЛЬ", 
                                font=self.small_font, fill=self.TEXT_DIM, anchor="w")
        self._rounded_rect(cx - 180, 320, cx + 180, 365, radius=8, 
                           fill=self.INPUT_BG, outline=self.INPUT_BORDER, width=1)
        self.pass_entry = tk.Entry(self.root, font=self.lbl_font, bg=self.INPUT_BG, 
                                    fg=self.TEXT_LIGHT, insertbackground=self.TEXT_LIGHT,
                                    bd=0, highlightthickness=0, show="•")
        self.pass_entry.insert(0, "password123")
        self.canvas.create_window(cx, 342, window=self.pass_entry, width=340, height=30)
        
        btn_tag = "login_btn"
        self._rounded_rect(cx - 180, 420, cx + 180, 470, radius=12, 
                           fill=self.ACCENT, outline="", tags=(btn_tag,))
        self.canvas.create_text(cx, 445, text="ВОЙТИ", font=self.h2_font, 
                                fill=self.BG_TOP, tags=(btn_tag,))
        
        self.login_status = self.canvas.create_text(cx, 510, text="", 
                                                     font=self.lbl_font, fill=self.ERROR_RED)
        
        self.canvas.tag_bind(btn_tag, "<ButtonRelease-1>", self._on_login)
        self.canvas.tag_bind(btn_tag, "<Enter>", lambda e: (self.canvas.config(cursor="hand2"), self.canvas.itemconfigure(btn_tag, fill=self.ACCENT_HOV)))
        self.canvas.tag_bind(btn_tag, "<Leave>", lambda e: (self.canvas.config(cursor=""), self.canvas.itemconfigure(btn_tag, fill=self.ACCENT)))

    def _on_login(self, event=None):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        
        if not re.match(email_regex, email):
            self.canvas.itemconfigure(self.login_status, text="❌ Некорректный Email", fill=self.ERROR_RED)
        elif len(password) < 6:
            self.canvas.itemconfigure(self.login_status, text="❌ Пароль слишком короткий", fill=self.ERROR_RED)
        else:
            self.canvas.itemconfigure(self.login_status, text="✅ Успешный вход!", fill=self.SUCCESS_GREEN)

    # ============================================================
    #                ВИДЖЕТ 2: ПОГОДА (7 ДНЕЙ)
    # ============================================================
    def _draw_weather(self):
        cx = self.W/2
        self._rounded_rect(cx - 250, 80, cx + 250, 620, radius=20, 
                           fill=self.CARD_BOTTOM, outline=self.CARD_EDGE, width=1)
        self._rounded_rect(cx - 245, 85, cx + 245, 615, radius=18, 
                           fill=self.CARD_TOP, outline="")
        
        # Заголовок
        self.canvas.create_text(cx, 125, text=f"🌍 {self.weather_city}", 
                                font=self.h2_font, fill=self.TEXT_LIGHT)
        
        # Температура
        self.canvas.create_text(cx, 230, text=f"{self.weather_temp}°", 
                                font=self.temp_font, fill=self.ACCENT_2)
        
        # Иконка
        self.canvas.create_text(cx, 340, text=self.weather_icon, 
                                font=self.icon_font, fill=self.TEXT_LIGHT)
        
        # Описание
        self.canvas.create_text(cx, 410, text=self.weather_desc, 
                                font=self.lbl_font, fill=self.TEXT_DIM)
        
        # Дата
        today = datetime.date.today()
        months = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        date_str = f"{today.day} {months[today.month-1]}"
        day_str = days[today.weekday()]
        self.canvas.create_text(cx, 450, text=f"{date_str}, {day_str}", 
                                font=self.small_font, fill=self.TEXT_DIM)
        
        # Прогноз (7 дней)
        if self.weather_forecast:
            self.canvas.create_text(cx, 490, text="ПРОГНОЗ НА НЕДЕЛЮ", 
                                    font=self.small_font, fill=self.TEXT_DIM)
            
            start_x = cx - 210
            for i, (day, temp, icon) in enumerate(self.weather_forecast):
                x = start_x + i * 70  # Чуть плотнее, чтобы влезло 7 дней
                self.canvas.create_text(x, 525, text=day, font=self.small_font, fill=self.TEXT_DIM)
                self.canvas.create_text(x, 550, text=icon, font=tkfont.Font(family="Segoe UI Symbol", size=18), fill=self.TEXT_LIGHT)
                self.canvas.create_text(x, 575, text=f"{temp}°", font=self.small_font, fill=self.ACCENT_2)
        
        # Кнопка обновления
        btn_tag = "refresh_weather"
        self._rounded_rect(cx - 100, 590, cx + 100, 625, radius=10, 
                           fill=self.ACCENT_2, outline="", tags=(btn_tag,))
        self.canvas.create_text(cx, 607, text="🔄 Обновить", font=self.small_font, 
                                fill=self.BG_TOP, tags=(btn_tag,))
        
        self.canvas.tag_bind(btn_tag, "<ButtonRelease-1>", self._refresh_weather)
        self.canvas.tag_bind(btn_tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(btn_tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def _refresh_weather(self, event):
        self.weather_desc = "Загрузка..."
        self.weather_icon = "⏳"
        self.weather_loading = True
        self._refresh_ui()
        
        thread = threading.Thread(target=self._fetch_weather, daemon=True)
        thread.start()

    # ============================================================
    #                ВИДЖЕТ 3: КАЛЕНДАРЬ
    # ============================================================
    def _draw_calendar(self):
        cx = self.W/2
        self._rounded_rect(cx - 320, 80, cx + 320, 620, radius=20, 
                           fill=self.CARD_BOTTOM, outline=self.CARD_EDGE, width=1)
        self._rounded_rect(cx - 315, 85, cx + 315, 615, radius=18, 
                           fill=self.CARD_TOP, outline="")
        
        month_name = self._get_month_name(self.cal_month)
        self.canvas.create_text(cx, 125, text=f"{month_name} {self.cal_year}", 
                                font=self.h2_font, fill=self.TEXT_LIGHT)
        
        prev_btn = "prev_month"
        next_btn = "next_month"
        self.canvas.create_text(cx - 290, 125, text="<", font=self.h1_font, fill=self.ACCENT, tags=(prev_btn,))
        self.canvas.create_text(cx + 290, 125, text=">", font=self.h1_font, fill=self.ACCENT, tags=(next_btn,))
        self.canvas.tag_bind(prev_btn, "<ButtonRelease-1>", lambda e: self._change_month(-1))
        self.canvas.tag_bind(next_btn, "<ButtonRelease-1>", lambda e: self._change_month(1))
        self.canvas.tag_bind(prev_btn, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(next_btn, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(prev_btn, "<Leave>", lambda e: self.canvas.config(cursor=""))
        self.canvas.tag_bind(next_btn, "<Leave>", lambda e: self.canvas.config(cursor=""))
        
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for i, day in enumerate(days):
            x = cx - 270 + i * 80
            self.canvas.create_text(x, 180, text=day, font=self.small_font, fill=self.TEXT_DIM)
        
        cal = calendar.monthcalendar(self.cal_year, self.cal_month)
        today = datetime.date.today()
        
        for row, week in enumerate(cal):
            for col, day in enumerate(week):
                if day == 0: continue
                x = cx - 270 + col * 80
                y = 230 + row * 50
                
                is_today = (self.cal_year == today.year and 
                            self.cal_month == today.month and 
                            day == today.day)
                
                if is_today:
                    self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, 
                                             fill=self.ACCENT, outline="")
                    self.canvas.create_text(x, y, text=str(day), 
                                            font=self.h2_font, fill=self.BG_TOP)
                else:
                    self.canvas.create_text(x, y, text=str(day), 
                                            font=self.lbl_font, fill=self.TEXT_LIGHT)

    def _get_month_name(self, month):
        months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                  "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        return months[month - 1]

    def _change_month(self, delta):
        self.cal_month += delta
        if self.cal_month > 12:
            self.cal_month = 1
            self.cal_year += 1
        elif self.cal_month < 1:
            self.cal_month = 12
            self.cal_year -= 1
        self.canvas.delete("all")
        self._draw_background()
        self._draw_top_menu()
        self._draw_calendar()

    # ============================================================
    #                УТИЛИТЫ
    # ============================================================
    def _rounded_rect(self, x0, y0, x1, y1, radius, **kwargs):
        if x1 - x0 < 2*radius: x1 = x0 + 2*radius
        if y1 - y0 < 2*radius: y1 = y0 + 2*radius
        points = [
            x0 + radius, y0, x1 - radius, y0, x1, y0, x1, y0 + radius,
            x1, y1 - radius, x1, y1, x1 - radius, y1, x0 + radius, y1,
            x0, y1, x0, y1 - radius, x0, y0 + radius, x0, y0,
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WidgetsApp(root)
    root.mainloop()
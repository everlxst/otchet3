import tkinter as tk
from tkinter import font as tkfont

class DesignToolsApp:
    # ---------- Палитра ----------
    BG_DARK      = "#0F172A"
    CARD_DARK    = "#1E293B"
    TEXT_LIGHT   = "#F8FAFC"
    TEXT_DIM     = "#94A3B8"
    
    # Цвета для инструментов
    FIGMA_ACCENT = "#A259FF"
    XD_ACCENT    = "#FF61F6"
    SKETCH_ACCENT = "#FFB300"
    AXURE_ACCENT = "#00D4FF"
    COMPARE_ACCENT = "#22C55E"

    W, H = 1000, 700

    def __init__(self, root):
        self.root = root
        self.root.title("Обзор и сравнение конструкторов")
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_DARK)
        self._center_window(self.W, self.H)

        self.current_tool = "figma"
        
        self._init_fonts()

        self.canvas = tk.Canvas(root, width=self.W, height=self.H,
                                highlightthickness=0, bd=0, bg=self.BG_DARK)
        self.canvas.pack(fill="both", expand=True)

        self._draw_top_menu()
        self._draw_interface()

    def _init_fonts(self):
        self.title_font  = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.h1_font     = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.h2_font     = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.lbl_font    = tkfont.Font(family="Segoe UI", size=12)
        self.small_font  = tkfont.Font(family="Segoe UI", size=10)
        self.price_font  = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.table_font  = tkfont.Font(family="Segoe UI", size=11)

    def _draw_top_menu(self):
        self.canvas.delete("top_menu")
        self.canvas.create_rectangle(0, 0, self.W, 60, fill="#0B1120", outline="", tags="top_menu")
        cx = self.W / 2
        self.canvas.create_text(cx, 20, text="ВЫБЕРИТЕ РАЗДЕЛ", 
                                font=self.small_font, fill=self.TEXT_DIM, tags="top_menu")

        tools = [
            ("figma", "Figma", self.FIGMA_ACCENT),
            ("xd", "Adobe XD", self.XD_ACCENT),
            ("sketch", "Sketch", self.SKETCH_ACCENT),
            ("axure", "Axure", self.AXURE_ACCENT),
            ("compare", "Сравнение", self.COMPARE_ACCENT)
        ]

        for i, (key, label, color) in enumerate(tools):
            x = cx - 360 + i * 180
            tag = f"menu_btn_{key}"
            is_active = self.current_tool == key
            fill_color = color if is_active else "#1E293B"
            text_color = self.BG_DARK if is_active else self.TEXT_DIM
            
            self.canvas.create_rectangle(x - 70, 35, x + 70, 55, 
                                          fill=fill_color, outline="", tags=("top_menu", tag))
            self.canvas.create_text(x, 45, text=label, font=self.small_font, 
                                    fill=text_color, tags=("top_menu", tag))
            
            self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, k=key: self._switch_tool(k))
            self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def _switch_tool(self, key):
        self.current_tool = key
        self.canvas.delete("all")
        self._draw_top_menu()
        self._draw_interface()

    def _draw_interface(self):
        if self.current_tool == "figma":
            self._draw_figma()
        elif self.current_tool == "xd":
            self._draw_xd()
        elif self.current_tool == "sketch":
            self._draw_sketch()
        elif self.current_tool == "axure":
            self._draw_axure()
        else:
            self._draw_comparison()

    # ============================================================
    #                ШАБЛОН КАРТОЧКИ
    # ============================================================
    def _draw_base_card(self, bg_color, accent_color, title, subtitle, 
                        pros, cons, price, platforms):
        self.canvas.create_rectangle(0, 60, self.W, self.H, fill=bg_color, outline="")
        self.canvas.create_rectangle(0, 60, self.W, 70, fill=accent_color, outline="")
        
        self.canvas.create_text(50, 130, text=title, 
                                font=self.h1_font, fill=self.TEXT_LIGHT, anchor="w")
        self.canvas.create_text(50, 170, text=subtitle, 
                                font=self.lbl_font, fill=self.TEXT_DIM, anchor="w")
        
        self.canvas.create_line(50, 200, self.W - 50, 200, fill=accent_color, width=2)
        
        self.canvas.create_text(50, 240, text="✅ ПЛЮСЫ", 
                                font=self.h2_font, fill=accent_color, anchor="w")
        y = 280
        for pro in pros:
            self.canvas.create_text(50, y, text=f"• {pro}", 
                                    font=self.lbl_font, fill=self.TEXT_LIGHT, anchor="w")
            y += 30
        
        self.canvas.create_text(520, 240, text="❌ МИНУСЫ", 
                                font=self.h2_font, fill="#EF4444", anchor="w")
        y = 280
        for con in cons:
            self.canvas.create_text(520, y, text=f"• {con}", 
                                    font=self.lbl_font, fill=self.TEXT_DIM, anchor="w")
            y += 30
        
        self.canvas.create_line(50, 460, self.W - 50, 460, fill=accent_color, width=1)
        self.canvas.create_text(50, 500, text="💰 СТОИМОСТЬ", 
                                font=self.h2_font, fill=accent_color, anchor="w")
        self.canvas.create_text(50, 535, text=price, 
                                font=self.price_font, fill=self.TEXT_LIGHT, anchor="w")
        
        self.canvas.create_text(520, 500, text="🖥️ ПЛАТФОРМЫ", 
                                font=self.h2_font, fill=accent_color, anchor="w")
        y = 535
        for platform in platforms:
            self.canvas.create_text(520, y, text=f"• {platform}", 
                                    font=self.lbl_font, fill=self.TEXT_LIGHT, anchor="w")
            y += 25

    # ============================================================
    #                КАРТОЧКИ ИНСТРУМЕНТОВ
    # ============================================================
    def _draw_figma(self):
        self._draw_base_card(
            bg_color="#0D1117", accent_color=self.FIGMA_ACCENT,
            title="🎨 Figma", subtitle="Облачный инструмент для совместного дизайна",
            pros=["Совместная работа в реальном времени", "Работает в браузере (Windows/Mac/Linux)",
                  "Мощные прототипы и Dev Mode", "Огромное сообщество и плагины", "Бесплатный тариф"],
            cons=["Требуется стабильный интернет", "Для больших проектов нужен платный план"],
            price="от $16/мес (Professional)",
            platforms=["Web (браузер)", "Windows", "macOS"]
        )

    def _draw_xd(self):
        self._draw_base_card(
            bg_color="#1A0B2E", accent_color=self.XD_ACCENT,
            title="🖌️ Adobe XD", subtitle="Классический инструмент из экосистемы Adobe",
            pros=["Интеграция с Photoshop и Illustrator", "Интерактивные прототипы", "Привычный интерфейс"],
            cons=["Прекращена активная разработка", "Только по подписке", "Мало новых функций"],
            price="от $19.99/мес",
            platforms=["Windows", "macOS"]
        )

    def _draw_sketch(self):
        self._draw_base_card(
            bg_color="#2D2D2D", accent_color=self.SKETCH_ACCENT,
            title="💎 Sketch", subtitle="Нативный инструмент для macOS",
            pros=["Быстрый на Mac", "Мощная система компонентов", "Бессрочная лицензия", "Много плагинов"],
            cons=["Работает только на macOS", "Совместная работа только через Web App"],
            price="от $120 (бессрочная лицензия)",
            platforms=["macOS (десктоп)", "Web App (просмотр)"]
        )

    def _draw_axure(self):
        self._draw_base_card(
            bg_color="#0A1A2A", accent_color=self.AXURE_ACCENT,
            title="⚙️ Axure RP", subtitle="Инструмент для сложных прототипов",
            pros=["Сложная логика и взаимодействия", "Переменные и условия", "Высокая точность"],
            cons=["Сложнее в освоении", "Высокая стоимость", "Требует обучения"],
            price="от $29/мес (Pro)",
            platforms=["Windows", "macOS"]
        )

    # ============================================================
    #                СРАВНЕНИЕ (5-Я ВКЛАДКА)
    # ============================================================
    def _draw_comparison(self):
        self.canvas.create_rectangle(0, 60, self.W, self.H, fill=self.BG_DARK, outline="")
        
        # Заголовок
        self.canvas.create_text(50, 110, text="📊 Сравнение конструкторов", 
                                font=self.h1_font, fill=self.TEXT_LIGHT, anchor="w")
        
        # Таблица (координаты)
        x_start = 50
        y_start = 170
        col_widths = [200, 180, 180, 180, 150]  # Ширина колонок
        row_height = 45
        
        headers = ["Критерий", "Figma", "Adobe XD", "Sketch", "Axure RP"]
        
        # Заголовки таблицы
        self.canvas.create_rectangle(x_start, y_start, x_start + sum(col_widths), y_start + row_height,
                                      fill="#1E293B", outline=self.COMPARE_ACCENT)
        
        x = x_start
        for i, header in enumerate(headers):
            self.canvas.create_text(x + 10, y_start + row_height/2, text=header, 
                                    font=self.h2_font, fill=self.COMPARE_ACCENT, anchor="w")
            x += col_widths[i]
        
        # Данные
        rows = [
            ("Интерфейс и удобство", "✅ Отлично", "⚠️ Устаревает", "✅ Отлично", "❌ Сложный"),
            ("Шаблоны и компоненты", "✅ Тысячи", "⚠️ Мало", "✅ Хорошо", "⚠️ Средне"),
            ("Прототипирование", "✅ Умное", "✅ Хорошее", "⚠️ Базовое", "✅ Лучшее"),
            ("Совместная работа", "✅ Реальное время", "⚠️ Облако", "❌ Только Web", "⚠️ Есть"),
            ("Стоимость и доступность", "✅ Бесплатно", "⚠️ $19.99/мес", "⚠️ $120 разово", "❌ $29/мес")
        ]
        
        y = y_start + row_height
        for row in rows:
            # Фон строки (чередование)
            bg_color = "#15102A" if (y // row_height) % 2 == 0 else "#1A1035"
            self.canvas.create_rectangle(x_start, y, x_start + sum(col_widths), y + row_height,
                                          fill=bg_color, outline="#3B2E66")
            
            x = x_start
            for i, cell in enumerate(row):
                color = self.TEXT_LIGHT if i == 0 else self.TEXT_DIM
                if i > 0:
                    if "✅" in cell: color = self.COMPARE_ACCENT
                    elif "❌" in cell: color = "#EF4444"
                    elif "⚠️" in cell: color = "#FBBF24"
                
                self.canvas.create_text(x + 10, y + row_height/2, text=cell, 
                                        font=self.table_font, fill=color, anchor="w")
                x += col_widths[i]
            y += row_height
        
        # Итоговый выбор
        y_choice = y + 40
        self.canvas.create_rectangle(50, y_choice, self.W - 50, y_choice + 120,
                                      fill="#0F2A1A", outline=self.COMPARE_ACCENT, width=2)
        
        self.canvas.create_text(70, y_choice + 20, text="🏆 ИТОГОВЫЙ ВЫБОР", 
                                font=self.h2_font, fill=self.COMPARE_ACCENT, anchor="w")
        
        self.canvas.create_text(70, y_choice + 55, 
                                text="1. Figma — идеален для учёбы (бесплатно, в браузере, всё в одном).", 
                                font=self.lbl_font, fill=self.TEXT_LIGHT, anchor="w")
        
        self.canvas.create_text(70, y_choice + 85, 
                                text="2. Sketch (для Mac) или Axure (для сложных прототипов).", 
                                font=self.lbl_font, fill=self.TEXT_LIGHT, anchor="w")

    # ============================================================
    #                УТИЛИТЫ
    # ============================================================
    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesignToolsApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import font as tkfont
import math

class DesignToolsApp:
    # ---------- Палитра ----------
    BG_DARK      = "#0F172A"
    CARD_DARK    = "#1E293B"
    TEXT_LIGHT   = "#F8FAFC"
    TEXT_DIM     = "#94A3B8"
    
    # Цвета для каждого инструмента
    FIGMA_BG     = "#0D1117"
    FIGMA_ACCENT = "#A259FF"  # Фиолетовый Figma
    
    XD_BG        = "#1A0B2E"
    XD_ACCENT    = "#FF61F6"  # Розовый Adobe XD
    
    SKETCH_BG    = "#2D2D2D"
    SKETCH_ACCENT = "#FFB300" # Жёлтый Sketch
    
    AXURE_BG     = "#0A1A2A"
    AXURE_ACCENT = "#00D4FF"  # Голубой Axure

    W, H = 900, 650

    def __init__(self, root):
        self.root = root
        self.root.title("Обзор конструкторов интерфейсов")
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
        self._draw_tool_interface()

    def _init_fonts(self):
        self.title_font  = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.h1_font     = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.h2_font     = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.lbl_font    = tkfont.Font(family="Segoe UI", size=12)
        self.small_font  = tkfont.Font(family="Segoe UI", size=10)
        self.price_font  = tkfont.Font(family="Segoe UI", size=22, weight="bold")

    def _draw_top_menu(self):
        self.canvas.delete("top_menu")
        self.canvas.create_rectangle(0, 0, self.W, 60, fill="#0B1120", outline="", tags="top_menu")
        cx = self.W / 2
        self.canvas.create_text(cx, 20, text="ВЫБЕРИТЕ ИНСТРУМЕНТ", 
                                font=self.small_font, fill=self.TEXT_DIM, tags="top_menu")

        tools = [
            ("figma", "Figma", self.FIGMA_ACCENT),
            ("xd", "Adobe XD", self.XD_ACCENT),
            ("sketch", "Sketch", self.SKETCH_ACCENT),
            ("axure", "Axure", self.AXURE_ACCENT)
        ]

        for i, (key, label, color) in enumerate(tools):
            x = cx - 300 + i * 200
            tag = f"menu_btn_{key}"
            is_active = self.current_tool == key
            fill_color = color if is_active else "#1E293B"
            text_color = self.BG_DARK if is_active else self.TEXT_DIM
            
            self.canvas.create_rectangle(x - 80, 35, x + 80, 55, 
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
        self._draw_tool_interface()

    def _draw_tool_interface(self):
        if self.current_tool == "figma":
            self._draw_figma()
        elif self.current_tool == "xd":
            self._draw_xd()
        elif self.current_tool == "sketch":
            self._draw_sketch()
        else:
            self._draw_axure()

    # ============================================================
    #                ОБЩИЙ ШАБЛОН ДЛЯ ВСЕХ КАРТОЧЕК
    # ============================================================
    def _draw_base_card(self, bg_color, accent_color, title, subtitle, 
                        pros, cons, price, platforms):
        # Фон
        self.canvas.create_rectangle(0, 60, self.W, self.H, fill=bg_color, outline="")
        
        # Верхняя цветная полоса
        self.canvas.create_rectangle(0, 60, self.W, 70, fill=accent_color, outline="")
        
        # Заголовок
        self.canvas.create_text(50, 130, text=title, 
                                font=self.h1_font, fill=self.TEXT_LIGHT, anchor="w")
        self.canvas.create_text(50, 170, text=subtitle, 
                                font=self.lbl_font, fill=self.TEXT_DIM, anchor="w")
        
        # Разделитель
        self.canvas.create_line(50, 200, self.W - 50, 200, fill=accent_color, width=2)
        
        # --- Плюсы (слева) ---
        self.canvas.create_text(50, 240, text="✅ ПЛЮСЫ", 
                                font=self.h2_font, fill=accent_color, anchor="w")
        y = 280
        for pro in pros:
            self.canvas.create_text(50, y, text=f"• {pro}", 
                                    font=self.lbl_font, fill=self.TEXT_LIGHT, anchor="w")
            y += 30
        
        # --- Минусы (справа) ---
        self.canvas.create_text(480, 240, text="❌ МИНУСЫ", 
                                font=self.h2_font, fill="#EF4444", anchor="w")
        y = 280
        for con in cons:
            self.canvas.create_text(480, y, text=f"• {con}", 
                                    font=self.lbl_font, fill=self.TEXT_DIM, anchor="w")
            y += 30
        
        # --- Стоимость (снизу) ---
        self.canvas.create_line(50, 460, self.W - 50, 460, fill=accent_color, width=1)
        self.canvas.create_text(50, 500, text="💰 СТОИМОСТЬ", 
                                font=self.h2_font, fill=accent_color, anchor="w")
        self.canvas.create_text(50, 535, text=price, 
                                font=self.price_font, fill=self.TEXT_LIGHT, anchor="w")
        
        # --- Платформы (снизу справа) ---
        self.canvas.create_text(480, 500, text="🖥️ ПЛАТФОРМЫ", 
                                font=self.h2_font, fill=accent_color, anchor="w")
        y = 535
        for platform in platforms:
            self.canvas.create_text(480, y, text=f"• {platform}", 
                                    font=self.lbl_font, fill=self.TEXT_LIGHT, anchor="w")
            y += 25

    # ============================================================
    #                FIGMA
    # ============================================================
    def _draw_figma(self):
        self._draw_base_card(
            bg_color=self.FIGMA_BG,
            accent_color=self.FIGMA_ACCENT,
            title="🎨 Figma",
            subtitle="Облачный инструмент для совместного дизайна",
            pros=[
                "Совместная работа в реальном времени",
                "Работает в браузере (Windows/Mac/Linux)",
                "Мощные прототипы и Dev Mode",
                "Огромное сообщество и плагины",
                "Бесплатный тариф для старта"
            ],
            cons=[
                "Требуется стабильный интернет",
                "Для больших проектов нужен платный план"
            ],
            price="от $16/мес (Professional)",
            platforms=["Web (браузер)", "Windows", "macOS"]
        )

    # ============================================================
    #                ADOBE XD
    # ============================================================
    def _draw_xd(self):
        self._draw_base_card(
            bg_color=self.XD_BG,
            accent_color=self.XD_ACCENT,
            title="🖌️ Adobe XD",
            subtitle="Классический инструмент из экосистемы Adobe",
            pros=[
                "Интеграция с Photoshop и Illustrator",
                "Интерактивные прототипы",
                "Привычный интерфейс для пользователей Adobe"
            ],
            cons=[
                "Прекращена активная разработка",
                "Доступен только по подписке",
                "Меньше обновлений и новых функций"
            ],
            price="от $19.99/мес",
            platforms=["Windows", "macOS"]
        )

    # ============================================================
    #                SKETCH
    # ============================================================
    def _draw_sketch(self):
        self._draw_base_card(
            bg_color=self.SKETCH_BG,
            accent_color=self.SKETCH_ACCENT,
            title="💎 Sketch",
            subtitle="Нативный инструмент для macOS",
            pros=[
                "Быстрый и отзывчивый на Mac",
                "Мощная система символов (компонентов)",
                "Бессрочная лицензия (не подписка)",
                "Огромное количество плагинов"
            ],
            cons=[
                "Работает ТОЛЬКО на macOS",
                "Совместная работа только через Web App",
                "Нет версии для Windows/Linux"
            ],
            price="от $120 (бессрочная лицензия)",
            platforms=["macOS (десктоп)", "Web App для просмотра"]
        )

    # ============================================================
    #                AXURE
    # ============================================================
    def _draw_axure(self):
        self._draw_base_card(
            bg_color=self.AXURE_BG,
            accent_color=self.AXURE_ACCENT,
            title="⚙️ Axure RP",
            subtitle="Инструмент для сложных и детализированных прототипов",
            pros=[
                "Сложная логика и взаимодействия",
                "Переменные и условия (как в коде)",
                "Высокая точность прототипов",
                "Подходит для сложных enterprise-проектов"
            ],
            cons=[
                "Сложнее в освоении",
                "Не такой интуитивный, как Figma",
                "Высокая стоимость подписки"
            ],
            price="от $29/мес (Pro)",
            platforms=["Windows", "macOS"]
        )

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
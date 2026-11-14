import tkinter as tk
from tkinter import font as tkfont
import math
import random

class BSQDashboardApp:
    # ---------- Палитра ----------
    BG_DARK     = "#0F172A"
    CARD_DARK   = "#1E293B"
    TEXT_LIGHT  = "#F8FAFC"
    TEXT_DIM    = "#94A3B8"
    
    CARD_LIGHT  = "#FFFFFF"
    BG_LIGHT    = "#F8FAFC"
    TEXT_DARK   = "#1E293B"
    TEXT_MUTED  = "#64748B"
    
    ACCENT_BLUE = "#3B82F6"
    ACCENT_GREEN= "#22C55E"
    ACCENT_RED  = "#EF4444"
    ACCENT_YELLOW = "#FBBF24"
    ACCENT_GRAY = "#94A3B8"

    W, H = 850, 700

    def __init__(self, root):
        self.root = root
        self.root.title("BSQ Dashboard · Интерактивный мониторинг")
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_DARK)
        self._center_window(self.W, self.H)

        self.current_variant = 1
        self.selected_card = None
        
        self.data = {
            "tests": {"title": "Tests in Process", "val": 20, "sub": "тестов", "color": self.ACCENT_BLUE, "progress": 0.6, "desc": "В процессе обработки: 12 тестов. Завершено: 8."},
            "qc": {"title": "QC", "val": 75, "sub": "норма", "color": self.ACCENT_GREEN, "progress": 0.75, "desc": "Контроль качества: 75% пройдено. Осталось: 25%."},
            "reagents": {"title": "Reagents", "val": "🔥", "sub": "Внимание", "color": self.ACCENT_YELLOW, "progress": None, "desc": "Реагенты: заканчиваются. Закажите новую партию."},
            "calibration": {"title": "Calibration", "val": "⚠️", "sub": "Требуется", "color": self.ACCENT_RED, "progress": None, "desc": "Калибровка: требуется вмешательство техника."},
            "supplies": {"title": "Supplies & Waste", "val": "⚠️", "sub": "Мало", "color": self.ACCENT_YELLOW, "progress": None, "desc": "Расходники: запас на 2 дня. Отходы: 80% заполнено."},
            "path": {"title": "Process Path", "val": "45%", "sub": "45%", "color": self.ACCENT_BLUE, "progress": 0.45, "desc": "Путь процесса: 45% выполнено. Этап 3 из 5."},
        }

        self._init_fonts()

        self.canvas = tk.Canvas(root, width=self.W, height=self.H,
                                highlightthickness=0, bd=0, bg=self.BG_DARK)
        self.canvas.pack(fill="both", expand=True)

        self._draw_top_menu()
        self._draw_variant(self.current_variant)

    def _init_fonts(self):
        self.title_font  = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.h1_font     = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.h2_font     = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.num_font    = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.lbl_font    = tkfont.Font(family="Segoe UI", size=11)
        self.small_font  = tkfont.Font(family="Segoe UI", size=9)
        self.icon_font   = tkfont.Font(family="Segoe UI Symbol", size=22)

    def _draw_top_menu(self):
        self.canvas.delete("top_menu")
        self.canvas.create_rectangle(0, 0, self.W, 60, fill="#0B1120", outline="", tags="top_menu")
        cx = self.W / 2
        self.canvas.create_text(cx, 20, text="ВЫБЕРИТЕ ВАРИАНТ", 
                                font=self.small_font, fill=self.TEXT_DIM, tags="top_menu")

        for i, label in enumerate(["1: Исходный", "2: Модерн", "3: Дашборд"]):
            x = cx - 200 + i * 140
            tag = f"menu_btn_{i+1}"
            color = self.ACCENT_BLUE if self.current_variant == i+1 else "#1E293B"
            
            self.canvas.create_rectangle(x - 60, 35, x + 60, 55, 
                                          fill=color, outline="", tags=("top_menu", tag))
            self.canvas.create_text(x, 45, text=label, font=self.small_font, 
                                    fill=self.TEXT_LIGHT if self.current_variant == i+1 else self.TEXT_DIM, 
                                    tags=("top_menu", tag))
            
            self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, idx=i+1: self._switch_variant(idx))
            self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def _switch_variant(self, variant):
        self.current_variant = variant
        self.selected_card = None
        self.canvas.delete("all")
        self._draw_top_menu()
        self._draw_variant(variant)

    def _draw_variant(self, variant):
        self.canvas.delete("info_panel")
        if variant == 1:
            self._variant_original()
        elif variant == 2:
            self._variant_modern()
        else:
            self._variant_dashboard()
        
        self._draw_info_panel()

    def _draw_info_panel(self):
        y0 = self.H - 110
        self.canvas.create_rectangle(0, y0, self.W, self.H, fill="#0B1120", outline="", tags="info_panel")
        
        if self.selected_card:
            data = self.data[self.selected_card]
            self.canvas.create_text(20, y0 + 30, text=f"Выбрано: {data['title']}", 
                                    font=self.h2_font, fill=self.TEXT_LIGHT, anchor="w", tags="info_panel")
            self.canvas.create_text(20, y0 + 60, text=data['desc'], 
                                    font=self.lbl_font, fill=self.TEXT_DIM, anchor="w", tags="info_panel")
        else:
            self.canvas.create_text(self.W/2, y0 + 50, text="Нажмите на любую карточку для просмотра деталей", 
                                    font=self.lbl_font, fill=self.TEXT_DIM, anchor="center", tags="info_panel")

    def _on_card_click(self, card_key):
        self.selected_card = card_key
        self.canvas.delete("all")
        self._draw_top_menu()
        self._draw_variant(self.current_variant)

    def _refresh_data(self):
        for key, data in self.data.items():
            if data["progress"] is not None:
                data["progress"] = min(1.0, data["progress"] + random.uniform(-0.1, 0.1))
                if key == "tests":
                    data["val"] = random.randint(5, 30)
                elif key == "qc":
                    data["val"] = int(data["progress"] * 100)
                elif key == "path":
                    data["sub"] = f"{int(data['progress'] * 100)}%"
        
        self.canvas.delete("all")
        self._draw_top_menu()
        self._draw_variant(self.current_variant)
        
        self.canvas.create_text(self.W/2, self.H - 120, text="✅ Данные обновлены!", 
                                font=self.h2_font, fill=self.ACCENT_GREEN, anchor="center", tags="refresh_msg")
        self.root.after(1500, lambda: self.canvas.delete("refresh_msg"))

    # ============================================================
    #                ВАРИАНТ 1: ИСХОДНЫЙ
    # ============================================================
    def _variant_original(self):
        self.canvas.create_rectangle(100, 80, 700, 520, fill="#E0F2FE", outline="#BAE6FD", width=2)
        self.canvas.create_text(120, 110, text="BSQ", 
                                font=self.h2_font, fill=self.TEXT_DARK, anchor="w")
        
        self.canvas.create_oval(280, 140, 300, 160, fill=self.ACCENT_GREEN, outline="")
        self.canvas.create_text(320, 150, text="Running", font=self.lbl_font, fill=self.TEXT_DARK, anchor="w")
        
        cards = [
            ("tests", "Tests in Process", "20", self.num_font),
            ("qc", "QC", None, None),
            ("reagents", "Reagents", "🔥", self.icon_font),
            ("calibration", "Calibration", "⚠️", self.icon_font),
            ("supplies", "Supplies & Waste", "⚠️", self.icon_font),
            ("path", "Process Path", None, None),
        ]
        
        for i, (key, title, val, font) in enumerate(cards):
            row = i // 2
            col = i % 2
            x = 120 + col * 280
            y = 190 + row * 90
            
            outline = self.ACCENT_BLUE if self.selected_card == key else "#CBD5E1"
            width = 2 if self.selected_card == key else 1
            
            self.canvas.create_rectangle(x, y, x + 260, y + 70, fill="white", outline=outline, width=width)
            self.canvas.create_text(x + 20, y + 20, text=title, font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
            
            if val is not None:
                # Иконка и значение (если есть)
                if font == self.icon_font:
                    # Иконки чуть ниже, чтобы были на уровне
                    self.canvas.create_text(x + 20, y + 48, text=val, font=font, fill=self.TEXT_DARK, anchor="w")
                else:
                    self.canvas.create_text(x + 20, y + 45, text=val, font=font, fill=self.TEXT_DARK, anchor="w")
            else:
                # Рисуем аккуратный прогресс-бар
                progress = self.data[key]["progress"]
                bar_x0 = x + 150
                bar_y = y + 40
                bar_w = 90
                bar_h = 8
                
                # Фон полоски
                self.canvas.create_rectangle(bar_x0, bar_y, bar_x0 + bar_w, bar_y + bar_h, 
                                              fill="#E2E8F0", outline="")
                # Заполнение
                self.canvas.create_rectangle(bar_x0, bar_y, bar_x0 + bar_w * progress, bar_y + bar_h, 
                                              fill=self.data[key]["color"], outline="")
            
            tag = f"orig_card_{key}"
            self.canvas.create_rectangle(x, y, x + 260, y + 70, fill="", outline="", tags=(tag,))
            self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, k=key: self._on_card_click(k))
            self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

    # ============================================================
    #                ВАРИАНТ 2: МОДЕРН
    # ============================================================
    def _variant_modern(self):
        self.canvas.create_rectangle(50, 80, 800, 570, fill=self.CARD_LIGHT, outline="#E2E8F0", width=1)
        self.canvas.create_text(80, 120, text="📊 BSQ Мониторинг", 
                                font=self.h1_font, fill=self.TEXT_DARK, anchor="w")
        
        self.canvas.create_oval(650, 110, 670, 130, fill=self.ACCENT_GREEN, outline="")
        self.canvas.create_text(680, 120, text="Running", font=self.lbl_font, fill=self.ACCENT_GREEN, anchor="w")
        
        btn_tag = "refresh_btn_m"
        self.canvas.create_rectangle(600, 145, 780, 175, fill=self.ACCENT_BLUE, outline="", tags=(btn_tag,))
        self.canvas.create_text(690, 160, text="🔄 Обновить данные", font=self.small_font, fill="white", tags=(btn_tag,))
        self.canvas.tag_bind(btn_tag, "<ButtonRelease-1>", lambda e: self._refresh_data())
        self.canvas.tag_bind(btn_tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(btn_tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

        for i, (key, data) in enumerate(self.data.items()):
            row = i // 2
            col = i % 2
            x = 80 + col * 350
            y = 200 + row * 120
            
            outline = self.ACCENT_BLUE if self.selected_card == key else "#E2E8F0"
            width = 2 if self.selected_card == key else 1
            
            self.canvas.create_rectangle(x, y, x + 320, y + 100, fill="#F8FAFC", outline=outline, width=width)
            self.canvas.create_text(x + 20, y + 25, text=data["title"], 
                                    font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
            
            if data["progress"] is not None:
                self.canvas.create_rectangle(x + 20, y + 55, x + 300, y + 70, fill="#E2E8F0", outline="")
                w = 280 * data["progress"]
                self.canvas.create_rectangle(x + 20, y + 55, x + 20 + w, y + 70, fill=data["color"], outline="")
                val_text = f"{int(data['progress'] * 100)}%" if key != "tests" else str(data["val"])
                self.canvas.create_text(x + 20, y + 85, text=val_text, 
                                        font=self.small_font, fill=data["color"], anchor="w")
            else:
                self.canvas.create_text(x + 40, y + 65, text=data["val"], 
                                        font=self.icon_font, fill=data["color"])
                self.canvas.create_text(x + 80, y + 65, text=data["sub"], 
                                        font=self.lbl_font, fill=self.TEXT_MUTED, anchor="w")
            
            tag = f"mod_card_{key}"
            self.canvas.create_rectangle(x, y, x + 320, y + 100, fill="", outline="", tags=(tag,))
            self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, k=key: self._on_card_click(k))
            self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

    # ============================================================
    #                ВАРИАНТ 3: ДАШБОРД
    # ============================================================
    def _variant_dashboard(self):
        self.canvas.create_rectangle(0, 60, 850, 590, fill=self.BG_DARK, outline="")
        self.canvas.create_text(50, 100, text="BSQ DASHBOARD", 
                                font=self.title_font, fill=self.TEXT_LIGHT, anchor="w")
        
        self.canvas.create_oval(700, 90, 720, 110, fill=self.ACCENT_GREEN, outline="")
        self.canvas.create_text(730, 100, text="RUNNING", font=self.small_font, fill=self.ACCENT_GREEN, anchor="w")
        
        btn_tag = "refresh_btn_d"
        self.canvas.create_rectangle(650, 115, 780, 140, fill=self.ACCENT_BLUE, outline="", tags=(btn_tag,))
        self.canvas.create_text(715, 127, text="🔄 Обновить", font=self.small_font, fill="white", tags=(btn_tag,))
        self.canvas.tag_bind(btn_tag, "<ButtonRelease-1>", lambda e: self._refresh_data())
        self.canvas.tag_bind(btn_tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(btn_tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

        for i, (key, data) in enumerate(self.data.items()):
            row = i // 2
            col = i % 2
            x = 50 + col * 380
            y = 160 + row * 130
            
            border_color = self.ACCENT_BLUE if self.selected_card == key else "#334155"
            width = 2 if self.selected_card == key else 1
            
            self.canvas.create_rectangle(x, y, x + 350, y + 110, fill=self.CARD_DARK, outline=border_color, width=width)
            self.canvas.create_text(x + 20, y + 25, text=data["title"], 
                                    font=self.small_font, fill=self.TEXT_DIM, anchor="w")
            
            if data["progress"] is not None:
                self.canvas.create_rectangle(x + 20, y + 55, x + 330, y + 70, fill="#334155", outline="")
                w = 310 * data["progress"]
                self.canvas.create_rectangle(x + 20, y + 55, x + 20 + w, y + 70, fill=data["color"], outline="")
                val_text = f"{int(data['progress'] * 100)}%" if key != "tests" else str(data["val"])
                self.canvas.create_text(x + 20, y + 90, text=val_text, 
                                        font=self.small_font, fill=self.TEXT_LIGHT, anchor="w")
            else:
                self.canvas.create_text(x + 40, y + 70, text=data["val"], 
                                        font=self.icon_font, fill=data["color"])
                self.canvas.create_text(x + 80, y + 70, text=data["sub"], 
                                        font=self.lbl_font, fill=self.TEXT_DIM, anchor="w")
            
            tag = f"dash_card_{key}"
            self.canvas.create_rectangle(x, y, x + 350, y + 110, fill="", outline="", tags=(tag,))
            self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, k=key: self._on_card_click(k))
            self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

    # ============================================================
    #                УТИЛИТЫ
    # ============================================================
    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BSQDashboardApp(root)
    root.mainloop()
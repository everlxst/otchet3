import tkinter as tk
from tkinter import font as tkfont
import math

class MaintenanceApp:
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
    ACCENT_ORANGE = "#F97316"
    ACCENT_GRAY = "#94A3B8"

    W, H = 800, 650

    def __init__(self, root):
        self.root = root
        self.root.title("Планировщик ТО · Maintenance")
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_DARK)
        self._center_window(self.W, self.H)

        self.current_variant = 1
        
        self.tasks = [
            {"name": "Daily", "desc": "Проверка масла", "days_left": 4, "done": False, "color": self.ACCENT_RED, "icon": "🛢️"},
            {"name": "Weekly", "desc": "Чистка фильтров", "days_left": 7, "done": False, "color": self.ACCENT_YELLOW, "icon": "🧹"},
            {"name": "Monthly", "desc": "Замена ремня", "days_left": 0, "done": True, "color": self.ACCENT_GREEN, "icon": "🔧"},
            {"name": "Quarterly", "desc": "Калибровка", "days_left": 0, "done": True, "color": self.ACCENT_GREEN, "icon": "⚙️"},
        ]

        self._init_fonts()

        self.canvas = tk.Canvas(root, width=self.W, height=self.H,
                                highlightthickness=0, bd=0, bg=self.BG_DARK)
        self.canvas.pack(fill="both", expand=True)

        self._draw_top_menu()
        self._draw_variant(self.current_variant)

    def _init_fonts(self):
        self.title_font  = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.h1_font     = tkfont.Font(family="Segoe UI", size=24, weight="bold")
        self.h2_font     = tkfont.Font(family="Segoe UI", size=15, weight="bold")
        self.lbl_font    = tkfont.Font(family="Segoe UI", size=12)
        self.small_font  = tkfont.Font(family="Segoe UI", size=9) # Уменьшили для кнопок
        self.num_font    = tkfont.Font(family="Segoe UI", size=24, weight="bold")
        self.status_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.icon_font   = tkfont.Font(family="Segoe UI Symbol", size=18)

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
        self.canvas.delete("all")
        self._draw_top_menu()
        self._draw_variant(variant)

    def _draw_variant(self, variant):
        if variant == 1:
            self._variant_original()
        elif variant == 2:
            self._variant_modern()
        else:
            self._variant_dashboard()

    # ============================================================
    #                ВАРИАНТ 1: УЛУЧШЕННЫЙ «ИСХОДНЫЙ»
    # ============================================================
    def _variant_original(self):
        for i in range(80, 520):
            t = (i - 80) / 440
            color = self._mix_color("#E0F2FE", "#F8FAFC", t)
            self.canvas.create_line(100, i, 700, i, fill=color, tags="orig_bg")

        self.canvas.create_rectangle(105, 85, 705, 525, fill="#CBD5E1", outline="", tags="orig_bg")
        self.canvas.create_rectangle(100, 80, 700, 520, fill="white", outline="#E2E8F0", width=1)

        self.canvas.create_text(125, 115, text="🛠️ Maintenance", 
                                font=self.h1_font, fill=self.TEXT_DARK, anchor="w")
        self.canvas.create_line(120, 145, 680, 145, fill="#F1F5F9", width=2)

        y = 170
        for i, task in enumerate(self.tasks):
            bg_color = self._mix_color(task["color"], "#FFFFFF", 0.85)
            self.canvas.create_rectangle(120, y, 680, y + 70, fill=bg_color, outline=task["color"], width=1)
            
            self.canvas.create_text(150, y + 35, text=task["icon"], font=self.icon_font, fill=task["color"])
            self.canvas.create_text(180, y + 25, text=task["name"], 
                                    font=self.h2_font, fill=task["color"], anchor="w")
            self.canvas.create_text(180, y + 50, text=task["desc"], 
                                    font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
            
            # Кнопка-переключатель (шире, чтобы текст влез)
            if task["done"]:
                tag = f"undo_btn_{i}"
                self.canvas.create_rectangle(540, y + 25, 660, y + 55, fill="#F1F5F9", outline=self.TEXT_MUTED, tags=(tag,))
                self.canvas.create_text(600, y + 40, text="↩️ Вернуть", font=self.small_font, fill=self.TEXT_DARK, tags=(tag,))
                self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, idx=i: self._toggle_task(idx))
                self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))
            else:
                tag = f"done_btn_{i}"
                self.canvas.create_rectangle(520, y + 25, 660, y + 55, fill=self.ACCENT_GREEN, outline="", tags=(tag,))
                self.canvas.create_text(590, y + 40, text=f"✅ Выполнить ({task['days_left']} дн.)", font=self.small_font, fill="white", tags=(tag,))
                self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, idx=i: self._toggle_task(idx))
                self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))
            
            y += 85

    # ============================================================
    #                ВАРИАНТ 2: «МОДЕРН»
    # ============================================================
    def _variant_modern(self):
        self.canvas.create_rectangle(55, 85, 755, 605, fill="#CBD5E1", outline="")
        self.canvas.create_rectangle(50, 80, 750, 600, fill=self.CARD_LIGHT, outline="#E2E8F0", width=1)

        self.canvas.create_text(80, 120, text="🛠️ Планировщик ТО", 
                                font=self.h1_font, fill=self.TEXT_DARK, anchor="w")
        
        done_count = sum(1 for t in self.tasks if t["done"])
        total = len(self.tasks)
        progress = done_count / total
        
        self.canvas.create_text(550, 120, text=f"{done_count} из {total} выполнено", 
                                font=self.lbl_font, fill=self.TEXT_MUTED, anchor="w")
        
        self._draw_rounded_rect(80, 145, 720, 160, radius=8, fill="#F1F5F9", outline="")
        self._draw_rounded_rect(80, 145, 80 + 640 * progress, 160, radius=8, fill=self.ACCENT_GREEN, outline="")

        y = 190
        for i, task in enumerate(self.tasks):
            bg_color = "#F0FDF4" if task["done"] else "white"
            
            self.canvas.create_rectangle(85, y+3, 725, y+83, fill="#F1F5F9", outline="")
            self.canvas.create_rectangle(80, y, 720, y + 80, fill=bg_color, outline="#E2E8F0")
            
            self._draw_rounded_rect(80, y, 90, y + 80, radius=0, fill=task["color"], outline="")
            
            self.canvas.create_text(120, y + 40, text=task["icon"], font=self.icon_font, fill=task["color"])
            self.canvas.create_text(145, y + 28, text=task["name"], 
                                    font=self.h2_font, fill=self.TEXT_DARK, anchor="w")
            self.canvas.create_text(145, y + 52, text=task["desc"], 
                                    font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
            
            # Кнопка с счетчиком (расширена, чтобы текст влез)
            if task["done"]:
                tag = f"undo_btn_m_{i}"
                self.canvas.create_rectangle(560, y + 25, 700, y + 55, fill="#F1F5F9", outline=self.TEXT_MUTED, tags=(tag,))
                self.canvas.create_text(630, y + 40, text="↩️ Вернуть", font=self.small_font, fill=self.TEXT_DARK, tags=(tag,))
                self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, idx=i: self._toggle_task(idx))
                self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))
            else:
                tag = f"done_btn_m_{i}"
                self.canvas.create_rectangle(540, y + 25, 700, y + 55, fill=self.ACCENT_BLUE, outline="", tags=(tag,))
                self.canvas.create_text(620, y + 40, text=f"✅ Выполнить ({task['days_left']} дн.)", font=self.small_font, fill="white", tags=(tag,))
                self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, idx=i: self._toggle_task(idx))
                self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))
            
            y += 95

    def _draw_rounded_rect(self, x0, y0, x1, y1, radius, **kwargs):
        if radius <= 0:
            return self.canvas.create_rectangle(x0, y0, x1, y1, **kwargs)
        self.canvas.create_oval(x0, y0, x0+radius*2, y1, **kwargs)
        self.canvas.create_oval(x1-radius*2, y0, x1, y1, **kwargs)
        return self.canvas.create_rectangle(x0+radius, y0, x1-radius, y1, **kwargs)

    # ============================================================
    #                ВАРИАНТ 3: ДАШБОРД
    # ============================================================
    def _variant_dashboard(self):
        self.canvas.create_rectangle(0, 60, 800, 650, fill=self.BG_DARK, outline="")
        self.canvas.create_text(50, 100, text="MAINTENANCE DASHBOARD", 
                                font=self.title_font, fill=self.TEXT_LIGHT, anchor="w")
        
        done_count = sum(1 for t in self.tasks if t["done"])
        total = len(self.tasks)
        progress = done_count / total
        
        self.canvas.create_text(550, 100, text=f"{done_count} из {total} выполнено", 
                                font=self.small_font, fill=self.TEXT_DIM, anchor="w")
        self.canvas.create_rectangle(550, 115, 750, 125, fill="#334155", outline="")
        self.canvas.create_rectangle(550, 115, 550 + 200 * progress, 125, fill=self.ACCENT_GREEN, outline="")

        y = 150
        for i, task in enumerate(self.tasks):
            bg_color = "#064E3B" if task["done"] else self.CARD_DARK
            border_color = self.ACCENT_GREEN if task["done"] else "#334155"
            
            self.canvas.create_rectangle(50, y, 750, y + 80, 
                                          fill=bg_color, outline=border_color, width=2)
            
            self.canvas.create_text(80, y + 25, text=f"{task['icon']} {task['name']}", 
                                    font=self.h2_font, fill=self.TEXT_LIGHT, anchor="w")
            self.canvas.create_text(80, y + 50, text=task["desc"], 
                                    font=self.small_font, fill=self.TEXT_DIM, anchor="w")
            
            if task["done"]:
                tag = f"dash_undo_{i}"
                self.canvas.create_rectangle(590, y + 25, 720, y + 55, fill="#334155", outline=self.TEXT_DIM, tags=(tag,))
                self.canvas.create_text(655, y + 40, text="↩️ Вернуть", font=self.small_font, fill=self.TEXT_LIGHT, tags=(tag,))
                self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, idx=i: self._toggle_task(idx))
                self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))
            else:
                self.canvas.create_text(600, y + 20, text=f"Осталось: {task['days_left']} дн.", 
                                        font=self.small_font, fill=self.ACCENT_YELLOW, anchor="e")
                
                tag = f"dash_done_{i}"
                self.canvas.create_rectangle(560, y + 40, 720, y + 70, 
                                              fill=self.ACCENT_BLUE, outline="", tags=(tag,))
                self.canvas.create_text(640, y + 55, text=f"✅ Выполнить ({task['days_left']} дн.)", 
                                        font=self.small_font, fill="white", tags=(tag,))
                self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, idx=i: self._toggle_task(idx))
                self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))
            
            y += 90

    # ============================================================
    #                ЛОГИКА ПЕРЕКЛЮЧЕНИЯ
    # ============================================================
    def _toggle_task(self, idx):
        """Переключает статус задачи и перерисовывает интерфейс."""
        self.tasks[idx]["done"] = not self.tasks[idx]["done"]
        # Перерисовываем всё окно
        self.canvas.delete("all")
        self._draw_top_menu()
        self._draw_variant(self.current_variant)

    # ============================================================
    #                УТИЛИТЫ
    # ============================================================
    @staticmethod
    def _hex_to_rgb(h):
        h = h.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    @classmethod
    def _mix_color(cls, c1, c2, t):
        r1, g1, b1 = cls._hex_to_rgb(c1)
        r2, g2, b2 = cls._hex_to_rgb(c2)
        return f"#{int(r1+(r2-r1)*t):02x}{int(g1+(g2-g1)*t):02x}{int(b1+(b2-b1)*t):02x}"

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()
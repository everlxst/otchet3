import tkinter as tk
from tkinter import font as tkfont
import random
import math

class LabInterfaceApp:
    # ---------- Палитра ----------
    BG_DARK     = "#0F172A"
    CARD_DARK   = "#1E293B"
    TEXT_LIGHT  = "#F8FAFC"
    TEXT_DIM    = "#94A3B8"
    
    CARD_LIGHT  = "#FFFFFF"
    TEXT_DARK   = "#1E293B"
    TEXT_MUTED  = "#64748B"
    
    ACCENT_BLUE = "#3B82F6"
    ACCENT_GREEN= "#22C55E"
    ACCENT_RED  = "#EF4444"
    ACCENT_YELLOW = "#FBBF24"
    ACCENT_GRAY = "#94A3B8"

    W, H = 800, 600

    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторный интерфейс · 3 варианта")
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_DARK)
        self._center_window(self.W, self.H)

        self.current_variant = 1
        self._init_fonts()

        # Состояние для анимации 3-го варианта
        self.dash_values = [7, 9, 32]
        self.dash_targets = [7, 9, 32]
        self.dash_anim_running = False

        self.canvas = tk.Canvas(root, width=self.W, height=self.H,
                                highlightthickness=0, bd=0, bg=self.BG_DARK)
        self.canvas.pack(fill="both", expand=True)

        self._draw_top_menu()
        self._draw_variant(self.current_variant)

    def _init_fonts(self):
        self.title_font  = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.h1_font     = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.h2_font     = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.num_font    = tkfont.Font(family="Segoe UI", size=40, weight="bold")
        self.num_small   = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.lbl_font    = tkfont.Font(family="Segoe UI", size=12)
        self.small_font  = tkfont.Font(family="Segoe UI", size=10)
        self.status_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")

    def _draw_top_menu(self):
        self.canvas.delete("top_menu")
        
        self.canvas.create_rectangle(0, 0, self.W, 60, fill="#0B1120", outline="", tags="top_menu")
        cx = self.W / 2
        self.canvas.create_text(cx, 20, text="ВЫБЕРИТЕ ВАРИАНТ ИНТЕРФЕЙСА", 
                                font=self.small_font, fill=self.TEXT_DIM, tags="top_menu")

        for i, label in enumerate(["1: Исходный", "2: Улучшенный", "3: Дашборд"]):
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
        self.dash_anim_running = False
        self.canvas.delete("all")
        self._draw_top_menu()
        self._draw_variant(variant)

    def _draw_variant(self, variant):
        if variant == 1:
            self._variant_original()
        elif variant == 2:
            self._variant_improved()
        else:
            self._variant_dashboard()

    # ============================================================
    #                ВАРИАНТ 1: ИСХОДНЫЙ
    # ============================================================
    def _variant_original(self):
        self.canvas.create_rectangle(100, 80, 700, 520, fill=self.CARD_LIGHT, outline="#CBD5E1", width=2)
        self.canvas.create_text(120, 110, text="Current Batch Status", 
                                font=self.h2_font, fill=self.TEXT_DARK, anchor="w")
        
        self.canvas.create_rectangle(120, 160, 160, 260, fill="#F1F5F9", outline="#CBD5E1", width=1)
        self.canvas.create_rectangle(120, 220, 160, 260, fill=self.ACCENT_BLUE, outline="")
        self.canvas.create_text(120, 280, text="Batch in Progress", 
                                font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
        self.canvas.create_text(200, 230, text="7", 
                                font=self.num_font, fill=self.TEXT_DARK, anchor="w")

        self.canvas.create_text(120, 350, text="Loaded Samples", 
                                font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
        self.canvas.create_text(240, 350, text="9", 
                                font=self.num_small, fill=self.TEXT_DARK, anchor="w")

        self.canvas.create_text(120, 420, text="Tests Completed", 
                                font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
        self.canvas.create_text(240, 420, text="32", 
                                font=self.num_small, fill=self.TEXT_DARK, anchor="w")

    # ============================================================
    #                ВАРИАНТ 2: УЛУЧШЕННЫЙ
    # ============================================================
    def _variant_improved(self):
        self.canvas.create_rectangle(50, 80, 750, 550, fill=self.CARD_LIGHT, outline="#E2E8F0", width=1)
        self.canvas.create_text(80, 120, text="📊 Current Batch Status", 
                                font=self.h1_font, fill=self.TEXT_DARK, anchor="w")
        
        # Статус
        self.status_dot_id = self.canvas.create_oval(675, 112, 693, 130, 
                                                      fill=self.ACCENT_GRAY, outline="")
        self.status_text_id = self.canvas.create_text(700, 120, text="IDLE", 
                                                       font=self.status_font, 
                                                       fill=self.ACCENT_GRAY, anchor="w")

        self.canvas.create_line(80, 160, 720, 160, fill="#E2E8F0")

        self.canvas.create_text(80, 200, text="BATCH PROGRESS", font=self.h2_font, fill=self.TEXT_MUTED, anchor="w")
        self.progress_num_id = self.canvas.create_text(80, 260, text="7", 
                                                        font=self.num_font, fill=self.ACCENT_BLUE, anchor="w")
        self.canvas.create_text(140, 265, text="/ 10", font=self.h2_font, fill=self.TEXT_MUTED, anchor="w")

        self.canvas.create_rectangle(80, 300, 720, 320, fill="#F1F5F9", outline="")
        self.progress_bar_id = self.canvas.create_rectangle(80, 300, 80 + 640 * 0.7, 320, 
                                                             fill=self.ACCENT_BLUE, outline="")
        self.progress_pct_id = self.canvas.create_text(720, 340, text="70%", 
                                                        font=self.small_font, fill=self.TEXT_MUTED, anchor="e")

        self.canvas.create_line(80, 380, 720, 380, fill="#E2E8F0")
        
        self.canvas.create_text(80, 420, text="LOADED SAMPLES", font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
        self.samples_id = self.canvas.create_text(80, 460, text="9", 
                                                   font=self.num_small, fill=self.TEXT_DARK, anchor="w")

        self.canvas.create_text(400, 420, text="TESTS COMPLETED", font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
        self.tests_id = self.canvas.create_text(400, 460, text="32", 
                                                 font=self.num_small, fill=self.TEXT_DARK, anchor="w")

        self.refresh_btn_id = self.canvas.create_rectangle(550, 500, 720, 540, 
                                                           fill=self.ACCENT_BLUE, outline="", 
                                                           tags=("refresh_btn",))
        self.refresh_txt_id = self.canvas.create_text(635, 520, text="🔄 Обновить", 
                                                      font=self.lbl_font, fill="white", 
                                                      tags=("refresh_btn",))
        
        self.bottom_status_id = self.canvas.create_text(80, 520, text="Нажмите Обновить для синхронизации", 
                                                         font=self.small_font, fill=self.TEXT_MUTED, anchor="w")
        
        self.canvas.tag_bind("refresh_btn", "<ButtonRelease-1>", self._on_refresh_click)
        self.canvas.tag_bind("refresh_btn", "<Enter>", 
                             lambda e: (self.canvas.config(cursor="hand2"), 
                                        self.canvas.itemconfigure(self.refresh_btn_id, fill="#2563EB")))
        self.canvas.tag_bind("refresh_btn", "<Leave>", 
                             lambda e: (self.canvas.config(cursor=""), 
                                        self.canvas.itemconfigure(self.refresh_btn_id, fill=self.ACCENT_BLUE)))

    def _update_status(self, state):
        colors = {"IDLE": self.ACCENT_GRAY, "RUNNING": self.ACCENT_YELLOW, "COMPLETE": self.ACCENT_GREEN}
        color = colors.get(state, self.ACCENT_GRAY)
        self.canvas.itemconfigure(self.status_dot_id, fill=color)
        self.canvas.itemconfigure(self.status_text_id, text=state, fill=color)

    def _on_refresh_click(self, event):
        self.canvas.itemconfigure(self.refresh_txt_id, text="⏳ Загрузка...")
        self.canvas.itemconfigure(self.refresh_btn_id, fill="#93C5FD")
        self.canvas.itemconfigure(self.bottom_status_id, text="Обновление данных...")
        self._update_status("RUNNING")
        self._animate_refresh_progress(0)

    def _animate_refresh_progress(self, step):
        if step > 10:
            self._on_refresh_done()
            return
        pct = step * 10
        fill_x = 80 + 640 * (pct / 100)
        self.canvas.coords(self.progress_bar_id, 80, 300, fill_x, 320)
        self.canvas.itemconfigure(self.progress_pct_id, text=f"{pct}%")
        self.canvas.itemconfigure(self.progress_num_id, text=str(int(pct / 10)))
        self.root.after(80, lambda: self._animate_refresh_progress(step + 1))

    def _on_refresh_done(self):
        self.canvas.itemconfigure(self.refresh_txt_id, text="✅ Успешно")
        self.canvas.itemconfigure(self.refresh_btn_id, fill=self.ACCENT_GREEN)
        self.canvas.itemconfigure(self.bottom_status_id, text="Данные успешно обновлены!")
        self._update_status("COMPLETE")
        self.root.after(2000, self._on_refresh_reset)

    def _on_refresh_reset(self):
        self.canvas.itemconfigure(self.refresh_txt_id, text="🔄 Обновить")
        self.canvas.itemconfigure(self.refresh_btn_id, fill=self.ACCENT_BLUE)
        self.canvas.itemconfigure(self.bottom_status_id, text="Нажмите Обновить для синхронизации")
        self.canvas.coords(self.progress_bar_id, 80, 300, 80 + 640 * 0.7, 320)
        self.canvas.itemconfigure(self.progress_pct_id, text="70%")
        self.canvas.itemconfigure(self.progress_num_id, text="7")
        self.canvas.itemconfigure(self.samples_id, text="9")
        self.canvas.itemconfigure(self.tests_id, text="32")
        self._update_status("IDLE")

    # ============================================================
    #                ВАРИАНТ 3: ДАШБОРД (ИНТЕРАКТИВНЫЙ)
    # ============================================================
    def _variant_dashboard(self):
        self.canvas.create_rectangle(0, 60, 800, 600, fill=self.BG_DARK, outline="")
        
        # Заголовок
        self.canvas.create_text(50, 100, text="BATCH STATUS DASHBOARD", 
                                font=self.title_font, fill=self.TEXT_LIGHT, anchor="w")
        
        # Статусная плашка
        self.dash_status_rect = self.canvas.create_rectangle(650, 85, 780, 115, 
                                                              fill=self.CARD_DARK, outline="#334155")
        self.dash_status_txt = self.canvas.create_text(715, 100, text="SYNCING...", 
                                                        font=self.small_font, fill=self.ACCENT_GREEN)
        
        # Карточка 1 (Прогресс)
        self._draw_dash_card(50, 140, 350, 320, "BATCH PROGRESS", "7 / 10", self.ACCENT_BLUE)
        
        # Карточка 2 (Образцы)
        self._draw_dash_card(400, 140, 750, 320, "LOADED SAMPLES", "9", self.ACCENT_GREEN)
        
        # Карточка 3 (Тесты + График)
        self.canvas.create_rectangle(50, 350, 750, 500, fill=self.CARD_DARK, outline="#334155", width=1)
        self.canvas.create_text(80, 380, text="TESTS COMPLETED", font=self.small_font, fill=self.TEXT_DIM, anchor="w")
        self.dash_tests_id = self.canvas.create_text(80, 420, text="32", 
                                                       font=tkfont.Font(family="Segoe UI", size=48, weight="bold"), 
                                                       fill=self.ACCENT_GREEN, anchor="w")
        
        # Столбики графика (динамические)
        self.dash_bars = []
        for i in range(10):
            bar_id = self.canvas.create_rectangle(400 + i*30, 480, 420 + i*30, 480, 
                                                   fill=self.ACCENT_BLUE, outline="")
            self.dash_bars.append(bar_id)
        
        # Кнопка "Обновить"
        self.dash_refresh_btn = self.canvas.create_rectangle(550, 520, 750, 560, 
                                                              fill=self.ACCENT_BLUE, outline="", 
                                                              tags=("dash_refresh_btn",))
        self.dash_refresh_txt = self.canvas.create_text(650, 540, text="🔄 Обновить данные", 
                                                         font=self.lbl_font, fill="white", 
                                                         tags=("dash_refresh_btn",))
        
        self.canvas.tag_bind("dash_refresh_btn", "<ButtonRelease-1>", self._dash_refresh)
        self.canvas.tag_bind("dash_refresh_btn", "<Enter>", 
                             lambda e: (self.canvas.config(cursor="hand2"), 
                                        self.canvas.itemconfigure(self.dash_refresh_btn, fill="#2563EB")))
        self.canvas.tag_bind("dash_refresh_btn", "<Leave>", 
                             lambda e: (self.canvas.config(cursor=""), 
                                        self.canvas.itemconfigure(self.dash_refresh_btn, fill=self.ACCENT_BLUE)))
        
        # Запускаем "живой" график (постоянное дыхание)
        self._dash_live_graph()

    def _draw_dash_card(self, x0, y0, x1, y1, title, value, color):
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.CARD_DARK, outline="#334155", width=1)
        self.canvas.create_text(x0 + 20, y0 + 30, text=title, font=self.small_font, fill=self.TEXT_DIM, anchor="w")
        self.canvas.create_text(x0 + 20, y0 + 90, text=value, font=self.num_font, fill=color, anchor="w")

    def _dash_live_graph(self):
        """Постоянная анимация столбиков (даже без нажатия кнопки)."""
        if self.current_variant != 3 or not self.root.winfo_exists():
            return
        
        for i, bar in enumerate(self.dash_bars):
            # Высота зависит от синуса + случайное отклонение
            h = 40 + 30 * math.sin(i * 0.5) + random.randint(-10, 10)
            h = max(10, min(80, h))
            self.canvas.coords(bar, 400 + i*30, 480 - h, 420 + i*30, 480)
        
        self.root.after(300, self._dash_live_graph)

    def _dash_refresh(self, event):
        """По нажатию кнопки — всплеск активности и смена статуса."""
        self.canvas.itemconfigure(self.dash_status_txt, text="UPDATING...", fill=self.ACCENT_YELLOW)
        self.canvas.itemconfigure(self.dash_refresh_txt, text="⏳ Загрузка...")
        
        # Имитация резкого обновления
        for i, bar in enumerate(self.dash_bars):
            h = random.randint(40, 80)
            self.canvas.coords(bar, 400 + i*30, 480 - h, 420 + i*30, 480)
            self.canvas.itemconfigure(bar, fill=self.ACCENT_GREEN)
        
        # Через 1 секунду возвращаемся
        self.root.after(1000, self._dash_refresh_done)

    def _dash_refresh_done(self):
        if self.current_variant != 3: return
        self.canvas.itemconfigure(self.dash_status_txt, text="SYNCING...", fill=self.ACCENT_GREEN)
        self.canvas.itemconfigure(self.dash_refresh_txt, text="🔄 Обновить данные")
        for bar in self.dash_bars:
            self.canvas.itemconfigure(bar, fill=self.ACCENT_BLUE)

    # ============================================================
    #                УТИЛИТЫ
    # ============================================================
    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LabInterfaceApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import font as tkfont
import random
import math

class PrinterInterfaceApp:
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

    W, H = 800, 650

    def __init__(self, root):
        self.root = root
        self.root.title("Интерфейс принтера · UX/UI")
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_DARK)
        self._center_window(self.W, self.H)

        self.current_variant = 1
        self.paper_jam = True
        self.printing_progress = 0
        self.is_printing = False
        self.pulse_phase = 0
        
        self._init_fonts()

        self.canvas = tk.Canvas(root, width=self.W, height=self.H,
                                highlightthickness=0, bd=0, bg=self.BG_DARK)
        self.canvas.pack(fill="both", expand=True)

        self._draw_top_menu()
        self._draw_variant(self.current_variant)
        
        # Запускаем анимацию (пульсация, график)
        self._animate()

    def _init_fonts(self):
        self.title_font  = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.h1_font     = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.h2_font     = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.lbl_font    = tkfont.Font(family="Segoe UI", size=12)
        self.small_font  = tkfont.Font(family="Segoe UI", size=10)
        self.tab_icon_font = tkfont.Font(family="Segoe UI Symbol", size=24)
        self.status_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")

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
        self.is_printing = False
        self.printing_progress = 0
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
    #                АНИМАЦИЯ (ОБЩАЯ)
    # ============================================================
    def _animate(self):
        if not self.root.winfo_exists(): return
        
        self.pulse_phase += 0.1
        
        # Анимация печати
        if self.is_printing:
            self.printing_progress += 0.5
            if self.printing_progress >= 100:
                self.printing_progress = 100
                self.is_printing = False
                self._on_print_complete()
            self._update_progress_bars()
            
        # Анимация графика в дашборде
        if self.current_variant == 3:
            self._animate_dash_graph()
            
        self.root.after(50, self._animate)

    def _update_progress_bars(self):
        # Для варианта 2
        if self.current_variant == 2 and hasattr(self, 'modern_progress_id'):
            w = 600 * (self.printing_progress / 100)
            self.canvas.coords(self.modern_progress_id, 100, 540, 100 + w, 550)
        
        # Для варианта 3
        if self.current_variant == 3 and hasattr(self, 'dash_progress_id'):
            w = 300 * (self.printing_progress / 100)
            self.canvas.coords(self.dash_progress_id, 50, 480, 50 + w, 490)

    def _on_print_complete(self):
        if self.current_variant == 2:
            self.canvas.itemconfigure(self.bottom_status, text="✅ Печать завершена!")
            self.canvas.coords(self.modern_progress_id, 100, 540, 700, 550)
        elif self.current_variant == 3:
            self.canvas.itemconfigure(self.dash_bottom, text="✅ Печать завершена!")
            self.canvas.coords(self.dash_progress_id, 50, 480, 350, 490)

    # ============================================================
    #                ВАРИАНТ 1: ИСХОДНЫЙ
    # ============================================================
    def _variant_original(self):
        self.canvas.create_rectangle(100, 80, 700, 500, fill="#E0F2FE", outline="#BAE6FD", width=2)
        self.canvas.create_text(120, 110, text="Connections", 
                                font=self.h2_font, fill=self.TEXT_DARK, anchor="w")
        
        self.canvas.create_rectangle(300, 140, 500, 190, fill="#22C55E", outline="")
        self.canvas.create_text(400, 165, text="Printer", font=self.lbl_font, fill="white")
        
        self.canvas.create_rectangle(350, 220, 450, 320, fill="#F97316", outline="#EA580C", width=2)
        self.canvas.create_rectangle(370, 240, 430, 280, fill="white", outline="")
        
        self.canvas.create_text(400, 360, text="⚠️ Paper Jam", 
                                font=self.status_font, fill=self.ACCENT_RED)

    # ============================================================
    #                ВАРИАНТ 2: МОДЕРН (С АНИМАЦИЕЙ)
    # ============================================================
    def _variant_modern(self):
        self.canvas.create_rectangle(50, 80, 750, 620, fill=self.CARD_LIGHT, outline="#E2E8F0", width=1)
        
        self.canvas.create_text(80, 120, text="🖨️ Подключение принтера", 
                                font=self.h1_font, fill=self.TEXT_DARK, anchor="w")
        
        # Статус с пульсацией
        self._draw_status_badge(600, 120)
        self.canvas.create_line(80, 160, 720, 160, fill="#E2E8F0")
        
        # Вкладки
        self._draw_tab(100, 200, "📶", "Wi-Fi", False)
        self._draw_tab(300, 200, "🖨️", "Принтер", True)
        self._draw_tab(500, 200, "🔌", "USB", False)
        
        self.canvas.create_text(400, 320, text="🖨️ HP LaserJet Pro", 
                                font=self.h2_font, fill=self.TEXT_DARK)
        
        # Блок ошибки / печати
        if self.paper_jam:
            self.canvas.create_rectangle(100, 360, 700, 440, 
                                          fill="#FEE2E2", outline=self.ACCENT_RED)
            self.canvas.create_text(400, 385, text="⚠️ Замятие бумаги", 
                                    font=self.h2_font, fill=self.ACCENT_RED)
            self.canvas.create_text(400, 415, text="Откройте крышку и удалите лист", 
                                    font=self.small_font, fill=self.TEXT_DARK)
            
            # Кнопка "Устранить"
            self.canvas.create_rectangle(200, 470, 380, 510, 
                                          fill=self.ACCENT_BLUE, outline="", tags=("fix_btn",))
            self.canvas.create_text(290, 490, text="🛠️ Устранить", 
                                    font=self.lbl_font, fill="white", tags=("fix_btn",))
            self.canvas.tag_bind("fix_btn", "<ButtonRelease-1>", self._fix_error_modern)
            
            # Кнопка "Инструкция"
            self.canvas.create_rectangle(420, 470, 600, 510, 
                                          fill="#F1F5F9", outline=self.TEXT_MUTED, tags=("ins_btn",))
            self.canvas.create_text(510, 490, text="📖 Инструкция", 
                                    font=self.lbl_font, fill=self.TEXT_DARK, tags=("ins_btn",))
            self.canvas.tag_bind("ins_btn", "<ButtonRelease-1>", self._show_instruction)
        else:
            # Прогресс-бар печати
            self.canvas.create_rectangle(100, 540, 700, 550, fill="#E2E8F0", outline="")
            self.modern_progress_id = self.canvas.create_rectangle(100, 540, 100, 550, 
                                                                    fill=self.ACCENT_GREEN, outline="")
            
            # Кнопка "Печать"
            self.canvas.create_rectangle(200, 470, 380, 510, 
                                          fill=self.ACCENT_GREEN, outline="", tags=("print_btn",))
            self.canvas.create_text(290, 490, text="🖨️ Начать печать", 
                                    font=self.lbl_font, fill="white", tags=("print_btn",))
            self.canvas.tag_bind("print_btn", "<ButtonRelease-1>", self._start_printing_modern)
            
            # Кнопка "Очистить"
            self.canvas.create_rectangle(420, 470, 600, 510, 
                                          fill="#F1F5F9", outline=self.TEXT_MUTED, tags=("clear_btn",))
            self.canvas.create_text(510, 490, text="🗑️ Очистить очередь", 
                                    font=self.lbl_font, fill=self.TEXT_DARK, tags=("clear_btn",))
            self.canvas.tag_bind("clear_btn", "<ButtonRelease-1>", lambda e: self._show_msg("Очередь очищена"))

        self.bottom_status = self.canvas.create_text(400, 600, text="Выберите действие", 
                                                      font=self.small_font, fill=self.TEXT_MUTED)

    def _draw_tab(self, x, y, icon, text, is_active):
        bg = self.ACCENT_BLUE if is_active else "#F1F5F9"
        fg = "white" if is_active else self.TEXT_DARK
        
        # Привязка клика к вкладке
        tag = f"tab_{text}"
        self.canvas.create_rectangle(x, y, x + 180, y + 90, fill=bg, outline="#E2E8F0", tags=(tag,))
        self.canvas.create_text(x + 90, y + 30, text=icon, font=self.tab_icon_font, fill=fg, tags=(tag,))
        self.canvas.create_text(x + 90, y + 65, text=text, font=self.lbl_font, fill=fg, tags=(tag,))
        
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, t=text: self._show_msg(f"Выбрано подключение: {t}"))
        self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def _draw_status_badge(self, x, y):
        if self.paper_jam:
            color, text = self.ACCENT_RED, "Ошибка"
        else:
            color, text = self.ACCENT_GREEN, "Готов"
        
        # Пульсирующий кружок
        r = 8 + 2 * math.sin(self.pulse_phase)
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
        self.canvas.create_text(x + 25, y, text=text, font=self.status_font, fill=color, anchor="w")

    def _fix_error_modern(self, event):
        self.paper_jam = False
        self.canvas.delete("all")
        self._draw_top_menu()
        self._variant_modern()
        self.canvas.itemconfigure(self.bottom_status, text="Ошибка устранена. Принтер готов.")

    def _show_instruction(self, event):
        self.canvas.itemconfigure(self.bottom_status, 
                                   text="Инструкция: 1) Откройте крышку. 2) Вытащите лист. 3) Закройте крышку.")

    def _start_printing_modern(self, event):
        self.is_printing = True
        self.printing_progress = 0
        self.canvas.itemconfigure(self.bottom_status, text="Печать запущена...")

    def _show_msg(self, msg):
        self.canvas.itemconfigure(self.bottom_status, text=msg)

    # ============================================================
    #                ВАРИАНТ 3: ДАШБОРД (С АНИМАЦИЕЙ)
    # ============================================================
    def _variant_dashboard(self):
        self.canvas.create_rectangle(0, 60, 800, 650, fill=self.BG_DARK, outline="")
        self.canvas.create_text(50, 100, text="PRINTER DASHBOARD", 
                                font=self.title_font, fill=self.TEXT_LIGHT, anchor="w")
        
        # Карточка Статуса
        self.canvas.create_rectangle(50, 140, 350, 320, fill=self.CARD_DARK, outline="#334155")
        self.canvas.create_text(70, 170, text="СТАТУС", font=self.small_font, fill=self.TEXT_DIM, anchor="w")
        
        status_color = self.ACCENT_RED if self.paper_jam else self.ACCENT_GREEN
        status_text = "Ошибка" if self.paper_jam else "Готов"
        self.canvas.create_text(70, 220, text=f"🖨️ {status_text}", font=self.h2_font, fill=status_color, anchor="w")
        
        err_text = "Замятие бумаги" if self.paper_jam else "Нет проблем"
        self.canvas.create_text(70, 260, text=err_text, font=self.small_font, fill=self.TEXT_LIGHT, anchor="w")
        
        # Карточка Очереди (с живым графиком)
        self.canvas.create_rectangle(400, 140, 750, 320, fill=self.CARD_DARK, outline="#334155")
        self.canvas.create_text(420, 170, text="ОЧЕРЕДЬ ПЕЧАТИ", font=self.small_font, fill=self.TEXT_DIM, anchor="w")
        
        # Столбики (будут анимироваться)
        self.dash_bars = []
        for i in range(8):
            bar = self.canvas.create_rectangle(420 + i*35, 280, 440 + i*35, 280, 
                                                fill=self.ACCENT_BLUE, outline="")
            self.dash_bars.append(bar)
            
        self.canvas.create_text(420, 300, text="Документов: 3", font=self.small_font, fill=self.TEXT_LIGHT, anchor="w")
        
        # Кнопки
        if self.paper_jam:
            self.canvas.create_rectangle(50, 360, 350, 410, fill=self.ACCENT_RED, outline="", tags=("fix_dash",))
            self.canvas.create_text(200, 385, text="🛠️ Исправить ошибку", font=self.lbl_font, fill="white", tags=("fix_dash",))
            self.canvas.tag_bind("fix_dash", "<ButtonRelease-1>", self._fix_error_dash)
        else:
            # Прогресс-бар
            self.canvas.create_rectangle(50, 480, 350, 490, fill="#334155", outline="")
            self.dash_progress_id = self.canvas.create_rectangle(50, 480, 50, 490, fill=self.ACCENT_GREEN, outline="")
            
            self.canvas.create_rectangle(50, 360, 350, 410, fill=self.ACCENT_GREEN, outline="", tags=("print_dash",))
            self.canvas.create_text(200, 385, text="🖨️ Начать печать", font=self.lbl_font, fill="white", tags=("print_dash",))
            self.canvas.tag_bind("print_dash", "<ButtonRelease-1>", self._start_printing_dash)

        self.dash_bottom = self.canvas.create_text(400, 550, text="", font=self.small_font, fill=self.TEXT_DIM)

    def _animate_dash_graph(self):
        if not hasattr(self, 'dash_bars') or not self.dash_bars: return
        for i, bar in enumerate(self.dash_bars):
            # Высота столбика зависит от синуса и прогресса печати
            base_h = 20 + 15 * math.sin(self.pulse_phase + i * 0.5)
            if self.is_printing:
                base_h += random.randint(-5, 15) # "Прыгает" при печати
            h = max(10, min(60, base_h))
            self.canvas.coords(bar, 420 + i*35, 280 - h, 440 + i*35, 280)

    def _fix_error_dash(self, event):
        self.paper_jam = False
        self.canvas.delete("all")
        self._draw_top_menu()
        self._variant_dashboard()
        self.canvas.itemconfigure(self.dash_bottom, text="✅ Ошибка устранена. Принтер готов.")

    def _start_printing_dash(self, event):
        self.is_printing = True
        self.printing_progress = 0
        self.canvas.itemconfigure(self.dash_bottom, text="📄 Печать запущена...")

    # ============================================================
    #                УТИЛИТЫ
    # ============================================================
    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PrinterInterfaceApp(root)
    root.mainloop()
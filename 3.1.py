import tkinter as tk
from tkinter import font as tkfont
import math
import time

class ProMachineControlApp:
    # ---------- Палитра ----------
    BG_TOP      = "#0B0F19"
    CARD_BG     = "#141A2A"
    CARD_BORDER = "#2A3550"
    TEXT_LIGHT  = "#E8EDF7"
    TEXT_DIM    = "#7A87A3"
    
    ACCENT      = "#22D3EE"
    
    # Цвета статусов
    C_OFFLINE   = "#EF4444"
    C_READY     = "#FBBF24"
    C_RUNNING   = "#22C55E"
    C_PAUSED    = "#F97316"

    # Цвета кнопок
    BTN_BG      = "#1F2937"
    BTN_BORDER  = "#374151"
    BTN_HOVER   = "#374151"

    W, H = 800, 700
    CARD_MX, CARD_MT, CARD_MB = 30, 30, 30
    CARD_RADIUS = 20

    def __init__(self, root):
        self.root = root
        self.root.title("Панель управления станком · Pro")
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_TOP)
        self._center_window(self.W, self.H)

        # --- Состояние станка ---
        self.machine_state = "offline"
        self.status_text = "Offline"
        self.status_color = self.C_OFFLINE
        self.load_percent = 0.0
        self.spindle_angle = 0.0
        self._anim_after_id = None
        self._running = True
        
        # Лог (храним последние 5 записей)
        self.log_messages = []

        self._init_fonts()

        self.canvas = tk.Canvas(root, width=self.W, height=self.H,
                                highlightthickness=0, bd=0, bg=self.BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        self._draw_card()
        self._draw_header()
        self._draw_machine_visual()
        self._draw_status_panel()
        self._draw_load_bar()
        self._draw_buttons()
        self._draw_log_panel()  # Увеличенный лог
        self._draw_footer()

        self._update_status_visual()
        self._log("Система инициализирована. Станок выключен.")
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._anim_loop()

    def _init_fonts(self):
        self.title_font  = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.status_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.btn_font    = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.icon_font   = tkfont.Font(family="Segoe UI Symbol", size=22)
        self.log_font    = tkfont.Font(family="Consolas", size=10)
        self.small_font  = tkfont.Font(family="Segoe UI", size=9)

    # ============================================================
    #                ОТРИСОВКА: КАРКАС
    # ============================================================
    def _draw_card(self):
        x0, y0 = self.CARD_MX, self.CARD_MT
        x1, y1 = self.W - self.CARD_MX, self.H - self.CARD_MB
        self.card = (x0, y0, x1, y1)
        self._rounded_rect(x0, y0, x1, y1, radius=self.CARD_RADIUS, 
                           fill=self.CARD_BG, outline=self.CARD_BORDER, width=2)

    def _draw_header(self):
        x0, y0, x1, _ = self.card
        self.canvas.create_text(x0 + 30, y0 + 30, text="⚙️  СИСТЕМА УПРАВЛЕНИЯ СТАНКОМ", 
                                font=self.title_font, fill=self.TEXT_LIGHT, anchor="w")
        self.canvas.create_line(x0 + 30, y0 + 55, x1 - 30, y0 + 55, fill=self.CARD_BORDER)

    # ============================================================
    #                СТАНОК (ВИЗУАЛИЗАЦИЯ)
    # ============================================================
    def _draw_machine_visual(self):
        x0, y0, x1, _ = self.card
        cx = x0 + 200
        cy = y0 + 200

        # Тень
        self.canvas.create_oval(cx - 100, cy + 80, cx + 100, cy + 110, fill="#000000", outline="")

        # Корпус (цилиндр)
        self.canvas.create_rectangle(cx - 60, cy - 60, cx + 60, cy + 80, 
                                     fill="#1F2937", outline="#4B5563", width=2)
        self.canvas.create_oval(cx - 60, cy - 70, cx + 60, cy - 50, 
                                fill="#374151", outline="#4B5563", width=2)
        self.canvas.create_oval(cx - 60, cy + 70, cx + 60, cy + 90, 
                                fill="#111827", outline="#4B5563", width=2)

        # Окно / Дверца
        self.canvas.create_rectangle(cx - 35, cy - 40, cx + 35, cy + 40, 
                                     fill="#0F172A", outline="#64748B", width=2)
        
        # Шпиндель (круг внутри, который будет вращаться)
        self.spindle_x = cx
        self.spindle_y = cy
        self.spindle_circle_id = self.canvas.create_oval(
            cx - 12, cy - 12, cx + 12, cy + 12,
            fill="#64748B", outline="#94A3B8", width=2
        )
        # Линия на круге (чтобы видеть вращение)
        self.spindle_line_id = self.canvas.create_line(
            cx, cy, cx + 12, cy, fill="#0F172A", width=2
        )

        # Монитор оператора
        self.canvas.create_rectangle(cx - 130, cy - 30, cx - 90, cy + 10, 
                                     fill="#0F172A", outline="#4B5563", width=2)
        self.canvas.create_rectangle(cx - 125, cy - 25, cx - 95, cy + 5, 
                                     fill="#1E293B", outline="")
        self.canvas.create_line(cx - 110, cy + 10, cx - 110, cy + 30, fill="#4B5563", width=3)

    # ============================================================
    #                ПАНЕЛЬ СТАТУСА
    # ============================================================
    def _draw_status_panel(self):
        x0, y0, x1, _ = self.card
        cx = x0 + 550
        cy = y0 + 130

        self.canvas.create_text(cx, cy - 40, text="ТЕКУЩИЙ СТАТУС", 
                                font=self.small_font, fill=self.TEXT_DIM, anchor="center")

        self._rounded_rect(cx - 120, cy - 20, cx + 120, cy + 20, radius=10, 
                           fill="#0F172A", outline=self.CARD_BORDER, width=1)
        
        self.status_circle_id = self.canvas.create_oval(cx - 100, cy - 10, cx - 80, cy + 10, 
                                                        fill=self.status_color, outline="")
        
        self.status_text_id = self.canvas.create_text(cx, cy, text=self.status_text, 
                                                      font=self.status_font, fill=self.TEXT_LIGHT, anchor="center")

    # ============================================================
    #                ПРОГРЕСС-БАР НАГРУЗКИ
    # ============================================================
    def _draw_load_bar(self):
        x0, y0, x1, _ = self.card
        cx = x0 + 550
        cy = y0 + 220

        self.canvas.create_text(cx, cy - 20, text="НАГРУЗКА ШПИНДЕЛЯ", 
                                font=self.small_font, fill=self.TEXT_DIM, anchor="center")

        self._rounded_rect(cx - 120, cy, cx + 120, cy + 12, radius=6, 
                           fill="#0F172A", outline=self.CARD_BORDER, width=1)
        
        self.load_fill_id = self._rounded_rect(cx - 120, cy, cx - 118, cy + 12, radius=6, 
                                               fill=self.ACCENT, outline="")

        self.load_text_id = self.canvas.create_text(cx + 140, cy + 6, text="0%", 
                                                    font=self.small_font, fill=self.TEXT_LIGHT, anchor="w")

    # ============================================================
    #                КНОПКИ
    # ============================================================
    def _draw_buttons(self):
        x0, y0, x1, y1 = self.card
        cx = (x0 + x1) / 2
        btn_y = y1 - 180
        
        btn_w, btn_h = 140, 60
        gap = 20
        total_w = 4 * btn_w + 3 * gap
        start_x = cx - total_w / 2

        configs = [
            ("Start", "⏻", self._on_start, self.C_READY),
            ("Run",   "▶", self._on_run,   self.C_RUNNING),
            ("Pause", "⏸", self._on_pause, self.C_PAUSED),
            ("Stop",  "⏹", self._on_stop,  self.C_OFFLINE),
        ]

        for i, (label, icon, command, color) in enumerate(configs):
            bx0 = start_x + i * (btn_w + gap)
            bx1 = bx0 + btn_w
            by0 = btn_y - btn_h / 2
            by1 = btn_y + btn_h / 2

            tag = f"btn_{label}"

            rect_id = self._rounded_rect(bx0, by0, bx1, by1, radius=10, 
                                         fill=self.BTN_BG, outline=self.BTN_BORDER, width=1, tags=(tag,))
            
            self.canvas.create_text((bx0 + bx1) / 2, by0 + 20, text=icon, 
                                    font=self.icon_font, fill=color, tags=(tag,))
            
            self.canvas.create_text((bx0 + bx1) / 2, by0 + 44, text=label, 
                                    font=self.btn_font, fill=self.TEXT_LIGHT, tags=(tag,))

            self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e, c=command: c())
            self.canvas.tag_bind(tag, "<Enter>", lambda e, r=rect_id: self.canvas.itemconfigure(r, fill=self.BTN_HOVER))
            self.canvas.tag_bind(tag, "<Leave>", lambda e, r=rect_id: self.canvas.itemconfigure(r, fill=self.BTN_BG))

    # ============================================================
    #                УВЕЛИЧЕННЫЙ ЖУРНАЛ СОБЫТИЙ
    # ============================================================
    def _draw_log_panel(self):
        x0, y0, x1, y1 = self.card
        log_x0 = x0 + 30
        log_x1 = x1 - 30
        log_y0 = y1 - 130
        log_y1 = y1 - 40

        self.canvas.create_text(log_x0, log_y0 - 10, text="ЖУРНАЛ СОБЫТИЙ", 
                                font=self.small_font, fill=self.TEXT_DIM, anchor="w")

        # Поле лога (большое)
        self._rounded_rect(log_x0, log_y0, log_x1, log_y1, radius=6, 
                           fill="#0F172A", outline=self.CARD_BORDER, width=1)
        
        # ID текстового поля для обновления
        self.log_text_id = self.canvas.create_text(log_x0 + 10, log_y0 + 10, text="", 
                                                   font=self.log_font, fill=self.TEXT_LIGHT, anchor="nw", width=log_x1 - log_x0 - 20)

    def _log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.log_messages.append(entry)
        
        # Оставляем только последние 5 записей
        if len(self.log_messages) > 5:
            self.log_messages.pop(0)
        
        # Обновляем отображение
        text = "\n".join(self.log_messages)
        self.canvas.itemconfigure(self.log_text_id, text=text)

    # ============================================================
    #                ФУТЕР
    # ============================================================
    def _draw_footer(self):
        x0, y0, x1, y1 = self.card
        self.canvas.create_text((x0 + x1) / 2, y1 - 15, 
                                text="Система готова. Используйте Start для включения.", 
                                font=self.small_font, fill=self.TEXT_DIM)

    # ============================================================
    #                ЛОГИКА
    # ============================================================
    def _on_start(self):
        if self.machine_state == "offline":
            self.machine_state = "ready"
            self.status_text = "Ready"
            self.status_color = self.C_READY
            self._log("Станок включен. Готов к работе.")
        else:
            self.machine_state = "offline"
            self.status_text = "Offline"
            self.status_color = self.C_OFFLINE
            self._log("Станок выключен пользователем.")
        self._update_status_visual()

    def _on_run(self):
        if self.machine_state == "ready" or self.machine_state == "paused":
            self.machine_state = "running"
            self.status_text = "Running"
            self.status_color = self.C_RUNNING
            self._log("Запущен процесс обработки.")
        elif self.machine_state == "offline":
            self._log("ОШИБКА: Станок выключен. Нажмите Start.")
        self._update_status_visual()

    def _on_pause(self):
        if self.machine_state == "running":
            self.machine_state = "paused"
            self.status_text = "Paused"
            self.status_color = self.C_PAUSED
            self._log("Процесс приостановлен.")
        self._update_status_visual()

    def _on_stop(self):
        self.machine_state = "offline"
        self.status_text = "Offline"
        self.status_color = self.C_OFFLINE
        self.load_percent = 0.0
        self._log("Аварийная остановка. Станок выключен.")
        self._update_status_visual()

    def _update_status_visual(self):
        self.canvas.itemconfigure(self.status_circle_id, fill=self.status_color)
        self.canvas.itemconfigure(self.status_text_id, text=self.status_text)

    # ============================================================
    #                АНИМАЦИЯ
    # ============================================================
    def _anim_loop(self):
        if not self._running: return

        if self.machine_state == "running":
            # Нагрузка растёт
            self.load_percent += 0.3
            if self.load_percent > 100:
                self.load_percent = 100
            
            # Скорость вращения зависит от нагрузки
            speed = (self.load_percent / 100.0) * 0.5 + 0.05
            self.spindle_angle += speed
            
            # Вращаем круг и линию на нём
            cx = self.spindle_x
            cy = self.spindle_y
            
            # Рисуем линию от центра к краю (индикатор вращения)
            dx = math.cos(self.spindle_angle) * 12
            dy = math.sin(self.spindle_angle) * 12
            self.canvas.coords(self.spindle_line_id, cx, cy, cx + dx, cy + dy)
            
            self._update_load_bar()
            
        elif self.machine_state == "paused":
            if self.load_percent > 0:
                self.load_percent -= 0.5
                if self.load_percent < 0:
                    self.load_percent = 0
                self._update_load_bar()
        
        elif self.machine_state == "offline":
            if self.load_percent > 0:
                self.load_percent = 0
                self._update_load_bar()
                # Сбрасываем угол
                self.spindle_angle = 0
                self.canvas.coords(self.spindle_line_id, 
                                   self.spindle_x, self.spindle_y,
                                   self.spindle_x + 12, self.spindle_y)

        self._anim_after_id = self.root.after(16, self._anim_loop)

    def _update_load_bar(self):
        cx = self.card[0] + 550
        x0 = cx - 120
        x1 = cx + 120
        w = x1 - x0
        fill_x = x0 + (w * self.load_percent / 100)
        
        self.canvas.coords(self.load_fill_id, *self._pill_points(x0, self.card[1] + 220, fill_x, self.card[1] + 232, 6))
        self.canvas.itemconfigure(self.load_text_id, text=f"{int(self.load_percent)}%")

    # ============================================================
    #                УТИЛИТЫ
    # ============================================================
    def _pill_points(self, x0, y0, x1, y1, r):
        if x1 - x0 < 2 * r: x1 = x0 + 2 * r
        if y1 - y0 < 2 * r: y1 = y0 + 2 * r
        rr = min(r, (y1 - y0) / 2, (x1 - x0) / 2)
        return [x0 + rr, y0, x1 - rr, y0, x1, y0, x1, y0 + rr,
                x1, y1 - rr, x1, y1, x1 - rr, y1, x0 + rr, y1,
                x0, y1, x0, y1 - rr, x0, y0 + rr, x0, y0]

    def _rounded_rect(self, x0, y0, x1, y1, radius, **kwargs):
        return self.canvas.create_polygon(self._pill_points(x0, y0, x1, y1, radius), smooth=True, **kwargs)

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _on_close(self):
        self._running = False
        if self._anim_after_id:
            try: self.root.after_cancel(self._anim_after_id)
            except: pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProMachineControlApp(root)
    root.mainloop()
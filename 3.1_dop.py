import tkinter as tk
from tkinter import font as tkfont
import math
import random

class SciFiHUDApp:
    # ---------- Палитра ----------
    BG_DARK     = "#050A14"
    HUD_CYAN    = "#00F0FF"
    HUD_BLUE    = "#0077FF"
    HUD_RED     = "#FF2A2A"
    HUD_ORANGE  = "#FF9D00"
    TEXT_LIGHT  = "#E0F7FA"
    TEXT_DIM    = "#4A6A8A"

    W, H = 900, 650

    def __init__(self, root):
        self.root = root
        self.root.title("Futuristic HUD · Sci-Fi Interface")
        self.root.geometry(f"{self.W}x{self.H}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_DARK)
        self._center_window(self.W, self.H)

        # --- Состояние ---
        self.t = 0.0
        self.is_rebooting = False
        self.reboot_progress = 0.0
        self.scanline_y = 0
        
        # Плавные значения для панелей
        self.power_val = 84.0
        self.target_power = 84.0
        self.network_val = 12.0
        self.temp_val = 42.0
        
        # Наведение на кнопку
        self.btn_hover = False
        self.btn_scale = 1.0
        
        # Наведение на панели (исправление ошибки)
        self._hover_panel = None
        
        # Частицы
        self.particles = []
        for _ in range(20):
            self.particles.append({
                "angle": random.uniform(0, math.pi * 2),
                "radius": random.uniform(120, 170),
                "speed": random.uniform(0.01, 0.03),
                "size": random.uniform(1, 3)
            })

        self._init_fonts()
        
        self.canvas = tk.Canvas(root, width=self.W, height=self.H,
                                highlightthickness=0, bd=0, bg=self.BG_DARK)
        self.canvas.pack(fill="both", expand=True)

        # --- События ---
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>", self._on_motion)

        self._anim_loop()

    def _init_fonts(self):
        self.title_font  = tkfont.Font(family="Consolas", size=18, weight="bold")
        self.hud_font    = tkfont.Font(family="Consolas", size=12)
        self.big_font    = tkfont.Font(family="Consolas", size=48, weight="bold")
        self.small_font  = tkfont.Font(family="Consolas", size=9)
        self.status_font = tkfont.Font(family="Consolas", size=10, weight="bold")
        self.icon_font   = tkfont.Font(family="Segoe UI Symbol", size=24)

    # ============================================================
    #                ГЛАВНЫЙ ЦИКЛ АНИМАЦИИ
    # ============================================================
    def _anim_loop(self):
        self.t += 0.05
        
        # Плавное обновление значений панелей
        self.power_val += (self.target_power - self.power_val) * 0.1
        self.network_val = 12 + math.sin(self.t) * 3
        self.temp_val = 42 + math.sin(self.t * 0.5) * 2
        
        # Плавное масштабирование кнопки
        target_scale = 1.1 if self.btn_hover else 1.0
        self.btn_scale += (target_scale - self.btn_scale) * 0.2
        
        # Движение частиц
        for p in self.particles:
            p["angle"] += p["speed"]

        self.canvas.delete("all")
        
        self._draw_background()
        self._draw_grid()
        self._draw_scanline()
        self._draw_central_hud()
        self._draw_side_panels()
        self._draw_top_status()
        
        if self.is_rebooting:
            self._update_reboot()
        
        self.root.after(16, self._anim_loop)

    # ============================================================
    #                ФОН И СЕТКА
    # ============================================================
    def _draw_background(self):
        for y in range(0, self.H, 2):
            t = y / self.H
            r = int(5 + (10 - 5) * t)
            g = int(10 + (20 - 10) * t)
            b = int(20 + (30 - 20) * t)
            self.canvas.create_line(0, y, self.W, y, fill=f"#{r:02x}{g:02x}{b:02x}")

    def _draw_grid(self):
        grid_color = "#0A1A2A"
        for x in range(0, self.W, 40):
            self.canvas.create_line(x, 0, x, self.H, fill=grid_color)
        for y in range(0, self.H, 40):
            self.canvas.create_line(0, y, self.W, y, fill=grid_color)

    def _draw_scanline(self):
        self.scanline_y = (self.scanline_y + 3) % self.H
        self.canvas.create_line(0, self.scanline_y, self.W, self.scanline_y, 
                                fill=self.HUD_CYAN, width=1)
        for i in range(1, 15):
            alpha = 1.0 - i / 15
            color = self._mix_color(self.HUD_CYAN, self.BG_DARK, 1 - alpha * 0.2)
            self.canvas.create_line(0, self.scanline_y + i, self.W, self.scanline_y + i, 
                                    fill=color, width=1)

    # ============================================================
    #                ЦЕНТРАЛЬНЫЙ КРУГ (HUD)
    # ============================================================
    def _draw_central_hud(self):
        cx, cy = self.W // 2, self.H // 2
        base_r = 150
        
        pulse = 1.0 + 0.03 * math.sin(self.t * 2)
        r = base_r * pulse

        self._draw_arc_segments(cx, cy, r, self.HUD_CYAN, segments=12, gap=10, width=3)
        self._draw_arc_segments(cx, cy, r * 0.8, self.HUD_BLUE, segments=8, gap=15, width=2)
        self._draw_arc_segments(cx, cy, r * 0.6, self.HUD_CYAN, segments=4, gap=30, width=2)

        # Вращающиеся точки
        for i in range(3):
            angle = self.t * 1.5 + i * (math.pi * 2 / 3)
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            self.canvas.create_oval(px-5, py-5, px+5, py+5, fill=self.HUD_CYAN, outline="")

        # Частицы
        for p in self.particles:
            px = cx + p["radius"] * math.cos(p["angle"])
            py = cy + p["radius"] * math.sin(p["angle"])
            self.canvas.create_oval(px-p["size"], py-p["size"], px+p["size"], py+p["size"], 
                                    fill=self.HUD_BLUE, outline="")

        # Центральный статус
        if not self.is_rebooting:
            self.canvas.create_text(cx, cy - 20, text="SYSTEM ONLINE", 
                                    font=self.hud_font, fill=self.HUD_CYAN)
            self.canvas.create_text(cx, cy + 10, text="100%", 
                                    font=self.big_font, fill=self.TEXT_LIGHT)
            self.canvas.create_text(cx, cy + 50, text="PROCESSING", 
                                    font=self.small_font, fill=self.TEXT_DIM)
            
            # Кнопка (с масштабированием)
            btn_r = int(30 * self.btn_scale)
            color = self.HUD_ORANGE if self.btn_hover else self.HUD_CYAN
            self.canvas.create_oval(cx - btn_r, cy + 70, cx + btn_r, cy + 70 + btn_r*2,
                                    outline=color, width=2, dash=(4, 2))
            self.canvas.create_text(cx, cy + 100, text="⟳", font=self.icon_font, fill=color)
        else:
            self.canvas.create_text(cx, cy - 20, text="REBOOTING...", 
                                    font=self.hud_font, fill=self.HUD_RED)
            self.canvas.create_text(cx, cy + 10, text=f"{int(self.reboot_progress)}%", 
                                    font=self.big_font, fill=self.HUD_ORANGE)
            # Прогресс-бар
            bar_w = 200
            self.canvas.create_rectangle(cx - bar_w/2, cy + 50, cx + bar_w/2, cy + 60, 
                                          outline=self.HUD_CYAN, width=1)
            fill_w = bar_w * (self.reboot_progress / 100)
            self.canvas.create_rectangle(cx - bar_w/2, cy + 50, cx - bar_w/2 + fill_w, cy + 60, 
                                          fill=self.HUD_ORANGE, outline="")

    def _draw_arc_segments(self, cx, cy, r, color, segments, gap, width):
        step = 360 / segments
        for i in range(segments):
            start_angle = i * step + gap / 2
            extent = step - gap
            self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                                   start=start_angle, extent=extent,
                                   style="arc", outline=color, width=width)

    # ============================================================
    #                БОКОВЫЕ ПАНЕЛИ (ИНТЕРАКТИВНЫЕ)
    # ============================================================
    def _draw_side_panels(self):
        # Левая панель
        self._draw_data_panel(50, 150, "POWER", f"{int(self.power_val)}%", self.HUD_CYAN, "power")
        self._draw_data_panel(50, 300, "NETWORK", f"{int(self.network_val)}ms", self.HUD_BLUE, "network")
        self._draw_data_panel(50, 450, "TEMP", f"{int(self.temp_val)}°C", self.HUD_ORANGE, "temp")
        
        # Правая панель
        self._draw_data_panel(650, 150, "SYNC", "OK", self.HUD_CYAN, "sync")
        self._draw_data_panel(650, 300, "UPLINK", "STABLE", self.HUD_BLUE, "uplink")
        self._draw_data_panel(650, 450, "ALERT", "NONE", self.HUD_CYAN, "alert")

    def _draw_data_panel(self, x, y, title, value, color, key):
        # Подсветка при наведении
        is_hover = (self._hover_panel == key)
        bg_color = "#0A1A2A" if is_hover else ""
        line_width = 3 if is_hover else 2
        
        if is_hover:
            self.canvas.create_rectangle(x - 10, y - 10, x + 200, y + 60, 
                                          fill=bg_color, outline="")
        
        # Угловые скобки
        self.canvas.create_line(x, y, x + 20, y, fill=color, width=line_width)
        self.canvas.create_line(x, y, x, y + 20, fill=color, width=line_width)
        
        self.canvas.create_text(x + 10, y + 15, text=title, font=self.small_font, fill=self.TEXT_DIM, anchor="w")
        self.canvas.create_text(x + 10, y + 35, text=value, font=self.hud_font, fill=color, anchor="w")

    # ============================================================
    #                ВЕРХНИЙ СТАТУС-БАР
    # ============================================================
    def _draw_top_status(self):
        self.canvas.create_line(0, 40, self.W, 40, fill=self.HUD_CYAN, width=1)
        
        blink = self.HUD_CYAN if int(self.t * 2) % 2 == 0 else self.BG_DARK
        self.canvas.create_oval(20, 15, 30, 25, fill=blink, outline="")
        
        self.canvas.create_text(40, 20, text="SYS: ACTIVE", font=self.small_font, 
                                fill=self.TEXT_LIGHT, anchor="w")
        self.canvas.create_text(self.W - 20, 20, text="FUTURE // v2.0", 
                                font=self.small_font, fill=self.TEXT_DIM, anchor="e")

    # ============================================================
    #                ВЗАИМОДЕЙСТВИЕ
    # ============================================================
    def _on_motion(self, event):
        # Определяем, над какой панелью находимся
        self._hover_panel = None
        if 50 <= event.x <= 250:
            if 150 <= event.y <= 200: self._hover_panel = "power"
            elif 300 <= event.y <= 350: self._hover_panel = "network"
            elif 450 <= event.y <= 500: self._hover_panel = "temp"
        elif 650 <= event.x <= 850:
            if 150 <= event.y <= 200: self._hover_panel = "sync"
            elif 300 <= event.y <= 350: self._hover_panel = "uplink"
            elif 450 <= event.y <= 500: self._hover_panel = "alert"
        
        # Проверка наведения на кнопку
        cx, cy = self.W // 2, self.H // 2
        btn_r = 30 * self.btn_scale
        if (cx - btn_r <= event.x <= cx + btn_r) and (cy + 70 <= event.y <= cy + 70 + btn_r*2):
            self.btn_hover = True
            self.canvas.config(cursor="hand2")
        else:
            self.btn_hover = False
            self.canvas.config(cursor="")

    def _on_click(self, event):
        cx, cy = self.W // 2, self.H // 2
        btn_r = 30 * self.btn_scale
        
        if (not self.is_rebooting and 
            (cx - btn_r <= event.x <= cx + btn_r) and 
            (cy + 70 <= event.y <= cy + 70 + btn_r*2)):
            self.is_rebooting = True
            self.reboot_progress = 0.0
            self.target_power = 0.0

    def _update_reboot(self):
        # Плавное увеличение прогресса
        self.reboot_progress += 1.5
        if self.reboot_progress >= 100:
            self.reboot_progress = 100
            self.root.after(300, self._finish_reboot)

    def _finish_reboot(self):
        self.is_rebooting = False
        self.reboot_progress = 0
        self.target_power = 84.0

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
    app = SciFiHUDApp(root)
    root.mainloop()
import os
import sys

# 1. Musimy być pierwsi przed biblioteką javascript
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    # Całkowite uciszenie wyjść systemowych
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
else:
    base_path = os.path.dirname(__file__)

# 2. Ręczne ustawienie zmiennych systemowych dla mostka
node_path = os.path.join(base_path, "javascript", "js", "node_modules")
os.environ['NODE_PATH'] = node_path
os.environ['JAVASCRIPT_DEBUG'] = '0'
os.environ['NODE_SKIP_PLATFORM_CHECK'] = '1'

# 3. Import z obejściem błędów 'console' i 'require'
try:
    import javascript
    from javascript import config, require, On
    config.loglevel = 0
except Exception as e:
    print(f"Błąd krytyczny mostka: {e}")

# 4. Reszta Twoich importów
import customtkinter as ctk
import threading
# ... reszta kodu ...

# 5. Inicjalizacja (pamiętaj, usuń puste bloki try/except!)
try:
    mineflayer = require('mineflayer')
except Exception:
    # Jeśli tu wywala timeout, to znaczy, że mostek nie widzi node_modules
    pass

import customtkinter as ctk
from javascript import require, On
import threading
import time
import random
import string
import os
import sys
from datetime import datetime
from tkinter import messagebox

# --- AAZOXO ENGINE PRESTIGE INITIALIZATION ---

# Import mineflayer przez most javascript
# (Mostek uruchomi się sam przy tym poleceniu)
mineflayer = require('mineflayer')

# --- PALETA KOLORÓW ULTRA-PRESTIGE ---
ctk.set_appearance_mode("Dark")

COLOR_MAIN_BG = "#07080E"       # Prawie czarny, kosmiczny
COLOR_CARD_BG = "#111420"       # Tło kart
COLOR_PANEL_DARK = "#0C0E17"    # Ciemniejsze tło paneli
COLOR_ACCENT = "#6366F1"        # Royal Indigo
COLOR_ACCENT_HOVER = "#818CF8"  # Soft Indigo
COLOR_TEXT_MAIN = "#F1F5F9"     # Biały dymny
COLOR_TEXT_DIM = "#64748B"      # Szary (Slate)
COLOR_SUCCESS = "#10B981"       # Szmaragd
COLOR_ERROR = "#EF4444"         # Krwista czerwień
COLOR_BORDER = "#1E293B"        # Obramowanie

# --- LOGIKA SILNIKA ---

class BotManager:
    """
    Zarządza flotą botów Aazoxo. 
    Obsługuje logikę łączenia, anty-AFK oraz dynamiczne zmienne.
    """
    def __init__(self, ui_callback=None):
        self.bots = []
        self.running = False
        self.behavior = "Stanie"
        self.lock = threading.Lock()
        self.ui_callback = ui_callback
        self.setup_folders()

    def setup_folders(self):
        docs = os.path.join(os.path.expanduser('~'), 'Documents')
        self.base_folder = os.path.join(docs, 'Aazoxo Engine')
        self.logs_folder = os.path.join(self.base_folder, 'logs')
        if not os.path.exists(self.logs_folder): os.makedirs(self.logs_folder)
        session_id = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.log_path = os.path.join(self.logs_folder, f"Prestige_{session_id}.txt")
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(f"AAZOXO PRESTIGE SESSION START: {datetime.now()}\n")

    def log_to_file(self, message, category="INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{ts}] {category} | {message}"
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(full_msg + "\n")
        except: pass
        if self.ui_callback:
            color = COLOR_TEXT_DIM
            if "✔" in message: color = COLOR_SUCCESS
            if "✘" in message or "Błąd" in message: color = COLOR_ERROR
            if "SYSTEM" in category: color = COLOR_ACCENT
            self.ui_callback(full_msg, color)

    def get_vars(self, i, name="", host=""):
        return {
            "{n}": str(i),
            "{name}": name,
            "{server}": host,
            "{time}": datetime.now().strftime("%H:%M"),
            "{rand}": ''.join(random.choices(string.ascii_lowercase, k=5)),
            "{rand_num}": str(random.randint(1000, 9999))
        }

    def process_text(self, text, i, name="", host=""):
        if not text: return ""
        v = self.get_vars(i, name, host)
        for k, val in v.items():
            text = text.replace(k, val)
        return text

    def create_bot(self, host, port, version, nick_t, msg_t, cmd_t, i):
        if not self.running: return
        raw_nick = nick_t if nick_t.strip() else "Aazoxo_{rand_num}"
        final_nick = self.process_text(raw_nick, i, host=host)[:16]
        
        try:
            bot = mineflayer.createBot({
                'host': host,
                'port': int(port or 25565),
                'username': final_nick,
                'version': version if version.strip() else False,
                'auth': 'offline',
                'hideErrors': True,
                'checkTimeoutInterval': 60000
            })
            bot.setMaxListeners(0)

            @On(bot, 'spawn')
            def handle_spawn(this):
                self.log_to_file(f"✔ {final_nick} wylądował na serwerze.", "BOT")
                def bot_logic():
                    time.sleep(2)
                    if not self.running: return
                    
                    # Logika komend (opcjonalna)
                    if cmd_t and cmd_t.strip():
                        for c in cmd_t.split(','):
                            if not self.running: break
                            bot.chat(self.process_text(c.strip(), i, name=final_nick, host=host))
                            time.sleep(1.8)
                    
                    # Logika wiadomości (opcjonalna)
                    if msg_t and msg_t.strip():
                        bot.chat(self.process_text(msg_t, i, name=final_nick, host=host))
                
                threading.Thread(target=bot_logic, daemon=True).start()

            @On(bot, 'end')
            def on_end(this, reason):
                with self.lock:
                    if bot in self.bots: self.bots.remove(bot)
                self.log_to_file(f"✘ {final_nick} opuścił sesję: {reason}", "DISC")

            with self.lock: self.bots.append(bot)
        except Exception as e:
            self.log_to_file(f"Krytyczny błąd tworzenia bota: {e}", "ERR")

    def global_loop(self):
        counter = 0
        while self.running:
            with self.lock: active_list = list(self.bots)
            for bot in active_list:
                if not self.running: break
                try:
                    if counter % 10 == 0: bot.swingArm('right')
                    if self.behavior == "Skakanie":
                        bot.setControlState('jump', True)
                        bot.setControlState('jump', False)
                    elif self.behavior == "Patrzenie":
                        target = bot.nearestEntity(lambda e: e.type == 'player')
                        if target: bot.lookAt(target.position.offset(0, 1.6, 0))
                except: continue
            time.sleep(1)
            counter += 1

    def start_all(self, host, port, version, count, nick, msg, cmds):
        self.stop_all_logic()
        time.sleep(0.5)
        self.running = True
        self.log_to_file(f"Inicjalizacja ataku na {host}...", "SYSTEM")
        threading.Thread(target=self.global_loop, daemon=True).start()
        try: n = int(count)
        except: n = 1
        for i in range(1, n + 1):
            if not self.running: break
            self.create_bot(host, port, version, nick, msg, cmds, i)
            time.sleep(1.5)

    def stop_all_logic(self):
        self.running = False
        with self.lock:
            for b in self.bots:
                try: b.quit()
                except: pass
            self.bots.clear()
        self.log_to_file("System wstrzymany.", "IDLE")

# --- UI COMPONENTS ---

class ModernInput(ctk.CTkFrame):
    def __init__(self, master, label, placeholder, is_optional=False, **kwargs):
        super().__init__(master, fg_color="transparent")
        display_label = f"{label} (OPCJONALNIE)" if is_optional else label
        self.lbl = ctk.CTkLabel(self, text=display_label, font=("Segoe UI Variable Semibold", 12), text_color=COLOR_TEXT_DIM)
        self.lbl.pack(anchor="w", padx=5, pady=(0, 5))
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder, height=45, fg_color=COLOR_PANEL_DARK,
                                  border_color=COLOR_BORDER, border_width=1, corner_radius=12,
                                  text_color=COLOR_TEXT_MAIN, font=("Segoe UI", 13))
        self.entry.pack(fill="x")
        self.entry.bind("<FocusIn>", lambda e: self.entry.configure(border_color=COLOR_ACCENT))
        self.entry.bind("<FocusOut>", lambda e: self.entry.configure(border_color=COLOR_BORDER))
    def get(self): return self.entry.get()

class PrestigeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AAZOXO ENGINE v16.0 | PRESTIGE ULTIMATE")
        self.geometry("1100x950")
        self.configure(fg_color=COLOR_MAIN_BG)
        self.manager = BotManager(ui_callback=self.update_ui_log)
        self.setup_ui()

    def setup_ui(self):
        # --- GLÓWNY UKŁAD (Sidebar + Content) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR (Legenda Zmiennych)
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color=COLOR_PANEL_DARK, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(self.sidebar, text="ZMIENNE (GUIDE)", font=("Segoe UI Variable Display", 20, "bold"), 
                     text_color=COLOR_ACCENT).pack(pady=(40, 20), padx=20)
        
        vars_info = [
            ("{n}", "Numer bota (1, 2, 3...)"),
            ("{rand}", "Losowe 5 liter (abcde)"),
            ("{rand_num}", "Losowe 4 cyfry (1234)"),
            ("{time}", "Aktualna godzina"),
            ("{server}", "Adres IP serwera"),
            ("{name}", "Nick bota")
        ]

        for v_code, v_desc in vars_info:
            f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            f.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(f, text=v_code, font=("Consolas", 14, "bold"), text_color=COLOR_SUCCESS).pack(anchor="w")
            ctk.CTkLabel(f, text=v_desc, font=("Segoe UI", 11), text_color=COLOR_TEXT_DIM).pack(anchor="w")

        # CONTENT AREA
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # HEADER
        header_f = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        header_f.pack(fill="x", pady=(0, 30))
        ctk.CTkLabel(header_f, text="AAZOXO ENGINE", font=("Segoe UI Variable Display", 42, "bold"), 
                     text_color=COLOR_TEXT_MAIN).pack(side="left")
        self.status_pill = ctk.CTkLabel(header_f, text=" SYSTEM READY ", font=("Segoe UI", 10, "bold"), 
                                        fg_color="#1E293B", text_color=COLOR_SUCCESS, corner_radius=10)
        self.status_pill.pack(side="right", pady=15)

        # SEKCJA 1: NETWORK
        net_card = self.create_modern_card(self.scroll_container, "KONFIGURACJA POŁĄCZENIA")
        self.ip = ModernInput(net_card, "Adres Serwera", "play.example.net")
        self.ip.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        self.port = ModernInput(net_card, "Port", "25565")
        self.port.grid(row=0, column=1, padx=15, pady=15, sticky="ew")
        self.ver = ModernInput(net_card, "Wersja gry", "1.19.2")
        self.ver.grid(row=1, column=0, padx=15, pady=15, sticky="ew")
        self.count = ModernInput(net_card, "Liczba Botów", "50")
        self.count.grid(row=1, column=1, padx=15, pady=15, sticky="ew")
        net_card.grid_columnconfigure((0, 1), weight=1)

        # SEKCJA 2: IDENTITY
        id_card = self.create_modern_card(self.scroll_container, "TOŻSAMOŚĆ I KOMENDY")
        self.nick = ModernInput(id_card, "Wzór Nicku (używaj zmiennych!)", "Aazoxo_{rand_num}")
        self.nick.pack(fill="x", padx=15, pady=10)
        
        # Pola opcjonalne
        self.cmds = ModernInput(id_card, "Komendy startowe", "/register aazoxo aazoxo", is_optional=True)
        self.cmds.pack(fill="x", padx=15, pady=10)
        self.msg = ModernInput(id_card, "Wiadomość po wejściu", "Aazoxo Engine Control Center", is_optional=True)
        self.msg.pack(fill="x", padx=15, pady=10)

        # FOOTER (Panel Sterowania)
        self.footer = ctk.CTkFrame(self, height=220, fg_color=COLOR_PANEL_DARK, corner_radius=20)
        self.footer.grid(row=1, column=1, sticky="ew", padx=30, pady=(0, 30))
        self.footer.grid_propagate(False)

        self.btn_run = ctk.CTkButton(self.footer, text="URUCHOM SILNIK", font=("Segoe UI", 16, "bold"), 
                                     fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, height=55, 
                                     corner_radius=15, command=self.exec_start)
        self.btn_run.place(relx=0.05, rely=0.2, relwidth=0.42)

        self.btn_stop = ctk.CTkButton(self.footer, text="ZATRZYMAJ", font=("Segoe UI", 16, "bold"), 
                                      fg_color="#262B40", hover_color=COLOR_ERROR, height=55, 
                                      corner_radius=15, command=self.manager.stop_all_logic)
        self.btn_stop.place(relx=0.53, rely=0.2, relwidth=0.42)

        self.behavior_menu = ctk.CTkOptionMenu(self.footer, values=["Stanie", "Skakanie", "Patrzenie"],
                                               fg_color="#1E293B", button_color=COLOR_ACCENT,
                                               corner_radius=10, command=lambda c: setattr(self.manager, 'behavior', c))
        self.behavior_menu.place(relx=0.05, rely=0.6, relwidth=0.3)

        # TERMINAL
        self.log_view = ctk.CTkTextbox(self.footer, fg_color="#05060A", font=("Consolas", 11), 
                                       border_width=1, border_color="#1E293B", corner_radius=12)
        self.log_view.place(relx=0.4, rely=0.55, relwidth=0.55, relheight=0.35)
        self.log_view.insert("0.0", "System Aazoxo Engine gotowy do pracy.\n")
        self.log_view.configure(state="disabled")

    def create_modern_card(self, master, title):
        card = ctk.CTkFrame(master, fg_color=COLOR_CARD_BG, corner_radius=20, border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="x", pady=15)
        lbl = ctk.CTkLabel(card, text=title, font=("Segoe UI", 11, "bold"), text_color=COLOR_ACCENT)
        lbl.pack(anchor="w", padx=20, pady=(15, 5))
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=10, pady=10)
        return inner

    def update_ui_log(self, msg, color):
        self.log_view.configure(state="normal")
        self.log_view.insert("end", msg + "\n")
        self.log_view.see("end")
        self.log_view.configure(state="disabled")
        if "Inicjalizacja" in msg:
            self.status_pill.configure(text=" RUNNING ", fg_color=COLOR_ACCENT)
        elif "System wstrzymany" in msg:
            self.status_pill.configure(text=" SYSTEM READY ", fg_color="#1E293B")

    def exec_start(self):
        if not self.ip.get():
            messagebox.showwarning("Błąd", "Użytkowniku, wpisz adres serwera!")
            return
        threading.Thread(target=self.manager.start_all, 
                         args=(self.ip.get(), self.port.get(), self.ver.get(), self.count.get(), 
                               self.nick.get(), self.msg.get(), self.cmds.get()),
                         daemon=True).start()

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except: pass
    app = PrestigeApp()
    app.mainloop()
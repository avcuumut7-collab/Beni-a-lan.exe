"""
ŞAKA PROGRAMI - Tamamen zararsız, geri alınabilir bir arkadaş şakası.

- Gerçek sistem dosyalarına DOKUNMAZ.
- Gerçek ekran çözünürlüğünü DEĞİŞTİRMEZ (sadece görsel "bozulma" efekti verir).
- Ctrl+Alt+Delete veya Görev Yöneticisi (Ctrl+Shift+Esc) HER ZAMAN çalışır.
- Sadece doğru şifre girilince kapanır ve "ŞAKA KANKA" yazar.

Kullanım: python saka.py
Kapatmak için (test ederken) sağ üstteki gizli çıkış: ESC tuşuna 5 kere hızlı basmak da kapatır (senin için test kolaylığı).
"""

import tkinter as tk
import random
import string

PASSWORD = "şifre"

FAKE_IPS = [f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}" for _ in range(40)]

FAKE_LINES = [
    "[!] Sisteme erişim sağlanıyor...",
    "[!] Güvenlik duvarı atlatılıyor...",
    "[!] Bellek taranıyor...",
    "[!] Şifreler dizini bulundu...",
    "[!] Kamera erişimi deneniyor...",
    "[!] Ağ trafiği izleniyor...",
    "[!] Dosya sistemi indeksleniyor...",
    "[!] Yedekleme sunucularına bağlanılıyor...",
]

class Saka(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SYSTEM")
        self.attributes("-fullscreen", True)
        self.configure(bg="black")
        self.esc_count = 0
        self.bind("<Escape>", self.esc_pressed)

        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.log_text = tk.Text(self, bg="black", fg="#00ff00", font=("Consolas", 14),
                                 insertbackground="green", bd=0)
        self.log_lines = []

        self.password_entry = None
        self.stage = 0

        self.after(300, self.start_glitch)
        self.after(1500, self.start_terminal_spam)
        self.after(6000, self.spawn_popups)
        self.after(9000, self.show_password_screen)

    def esc_pressed(self, event):
        self.esc_count += 1
        if self.esc_count >= 5:
            self.destroy()

    # ---- Efekt 1: Renk / "bozulma" flaşı ----
    def start_glitch(self):
        colors = ["#ff0000", "#00ff00", "#0000ff", "#000000", "#ffffff", "#ff00ff"]
        def flash(i=0):
            if self.stage >= 2:
                return
            self.canvas.configure(bg=random.choice(colors))
            self.after(120, lambda: flash(i + 1))
        flash()

    # ---- Efekt 2: Sahte terminal / IP akışı ----
    def start_terminal_spam(self):
        self.canvas.pack_forget()
        self.log_text.pack(fill="both", expand=True)

        def add_line(i=0):
            if self.stage >= 2 or i > 200:
                return
            line = random.choice(FAKE_LINES) + "  " + random.choice(FAKE_IPS)
            self.log_text.insert("end", line + "\n")
            self.log_text.see("end")
            self.after(80, lambda: add_line(i + 1))
        add_line()

    # ---- Efekt 3: Pop-up spamı ----
    def spawn_popups(self):
        if self.stage >= 2:
            return
        for _ in range(6):
            w = tk.Toplevel(self)
            w.geometry(f"300x100+{random.randint(0,1200)}+{random.randint(0,700)}")
            w.title("UYARI")
            tk.Label(w, text=random.choice([
                "SİSTEM RİSK ALTINDA",
                "BİLİNMEYEN BAĞLANTI TESPİT EDİLDİ",
                "VERİ TARANIYOR...",
                "GÜVENLİK İHLALİ"
            ]), font=("Arial", 12, "bold"), fg="red").pack(expand=True)
        self.after(700, self.spawn_popups)

    # ---- Şifre ekranı ----
    def show_password_screen(self):
        self.stage = 1
        self.log_text.pack_forget()
        self.canvas.pack_forget()

        frame = tk.Frame(self, bg="black")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="SİSTEM KİLİTLENDİ", font=("Consolas", 36, "bold"),
                 fg="red", bg="black").pack(pady=(150, 20))
        tk.Label(frame, text="Devam etmek için şifreyi giriniz:", font=("Consolas", 16),
                 fg="white", bg="black").pack(pady=10)

        self.password_entry = tk.Entry(frame, font=("Consolas", 18), show="*", justify="center")
        self.password_entry.pack(pady=10)
        self.password_entry.focus()
        self.password_entry.bind("<Return>", self.check_password)

        self.error_label = tk.Label(frame, text="", font=("Consolas", 12), fg="red", bg="black")
        self.error_label.pack(pady=5)

        btn = tk.Button(frame, text="Onayla", command=self.check_password)
        btn.pack(pady=10)

    def check_password(self, event=None):
        if self.password_entry.get() == PASSWORD:
            self.stage = 2
            self.show_joke_screen()
        else:
            self.error_label.configure(text="Yanlış şifre, tekrar deneyin.")
            self.password_entry.delete(0, "end")

    def show_joke_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="ŞAKA KANKA", font=("Consolas", 72, "bold"),
                 fg="#00ff00", bg="black").pack(expand=True)
        self.configure(bg="black")
        self.after(3000, self.destroy)


if __name__ == "__main__":
    app = Saka()
    app.mainloop()

"""
Generator Haseł — Bezpieczny generator silnych haseł.

Generuje kryptograficznie bezpieczne hasła o zadanej długości.
Hasła zawierają wielkie i małe litery, cyfry oraz znaki specjalne.
Wygenerowane hasła nigdy się nie powtarzają w ramach sesji.
"""

import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox

# ──────────────────────────────────────────────
#  Stałe
# ──────────────────────────────────────────────
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 128
MAX_PASSWORDS_COUNT = 50

# Zestawy znaków
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SPECIAL = "!@#$%^&*()-_=+[]{}|;:',.<>?/~`"

# Typowe wzorce do odrzucenia (fragmenty imion, dat, sekwencji)
COMMON_PATTERNS = [
    "password", "haslo", "hasło", "qwerty", "abc", "xyz", "123", "111",
    "000", "admin", "login", "user", "test", "root", "pass", "1234",
    "aaaa", "bbbb", "cccc", "zzzz", "master", "monkey", "dragon",
    "letmein", "welcome", "shadow", "sunshine", "princess", "football",
    "january", "february", "march", "april", "june", "july", "august",
    "september", "october", "november", "december",
    "styczen", "luty", "marzec", "kwiecien", "maj", "czerwiec",
    "lipiec", "sierpien", "wrzesien", "pazdziernik", "listopad", "grudzien",
    "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct",
    "anna", "adam", "piotr", "kasia", "marek", "tomek", "ewa", "jan",
    "maria", "pawel", "michal", "agnieszka", "robert", "andrzej",
]


# ──────────────────────────────────────────────
#  Logika generowania haseł
# ──────────────────────────────────────────────
class PasswordEngine:
    """Silnik generujący kryptograficznie bezpieczne, niepowtarzalne hasła."""

    def __init__(self):
        self._history: set[str] = set()
        self._all_chars = LOWERCASE + UPPERCASE + DIGITS + SPECIAL

    def _contains_common_pattern(self, password: str) -> bool:
        """Sprawdza, czy hasło zawiera popularny wzorzec."""
        lower = password.lower()
        for pattern in COMMON_PATTERNS:
            if pattern in lower:
                return True
        # Odrzuć sekwencje dat typu 1990, 2000–2030
        for year in range(1900, 2031):
            if str(year) in password:
                return True
        return False

    def _meets_complexity(self, password: str) -> bool:
        """Sprawdza złożoność: wielkie/małe litery, cyfry, znaki specjalne."""
        has_lower = any(c in LOWERCASE for c in password)
        has_upper = any(c in UPPERCASE for c in password)
        has_digit = any(c in DIGITS for c in password)
        has_special = any(c in SPECIAL for c in password)

        if len(password) >= 4:
            return has_lower and has_upper and has_digit and has_special
        # Dla bardzo krótkich haseł wymagamy co najmniej 3 kategorii
        return sum([has_lower, has_upper, has_digit, has_special]) >= min(len(password), 3)

    def generate(self, length: int) -> str:
        """Generuje jedno silne, niepowtarzalne hasło o podanej długości."""
        if length < MIN_PASSWORD_LENGTH:
            raise ValueError(f"Minimalna długość hasła to {MIN_PASSWORD_LENGTH}.")
        if length > MAX_PASSWORD_LENGTH:
            raise ValueError(f"Maksymalna długość hasła to {MAX_PASSWORD_LENGTH}.")

        max_attempts = 1000
        for _ in range(max_attempts):
            # Gwarantujemy co najmniej 1 znak z każdej kategorii
            required = [
                secrets.choice(LOWERCASE),
                secrets.choice(UPPERCASE),
                secrets.choice(DIGITS),
                secrets.choice(SPECIAL),
            ]
            remaining = [secrets.choice(self._all_chars) for _ in range(length - 4)]
            chars = required + remaining
            # Bezpieczne tasowanie (Fisher-Yates z secrets)
            for i in range(len(chars) - 1, 0, -1):
                j = secrets.randbelow(i + 1)
                chars[i], chars[j] = chars[j], chars[i]

            password = "".join(chars)

            if password in self._history:
                continue
            if self._contains_common_pattern(password):
                continue
            if not self._meets_complexity(password):
                continue

            self._history.add(password)
            return password

        raise RuntimeError("Nie udało się wygenerować unikalnego hasła. Spróbuj ponownie.")

    @property
    def history_count(self) -> int:
        return len(self._history)

    def clear_history(self):
        self._history.clear()


# ──────────────────────────────────────────────
#  Kolory i styl
# ──────────────────────────────────────────────
COLORS = {
    "bg_dark":       "#0f0f1a",
    "bg_card":       "#1a1a2e",
    "bg_input":      "#16213e",
    "bg_button":     "#0f3460",
    "bg_button_hover": "#1a4f8a",
    "bg_accent":     "#e94560",
    "bg_accent_hover": "#ff6b81",
    "bg_success":    "#00b894",
    "bg_warning":    "#fdcb6e",
    "fg_primary":    "#eaeaea",
    "fg_secondary":  "#a0a0b8",
    "fg_accent":     "#e94560",
    "fg_password":   "#00e5ff",
    "border":        "#2a2a4a",
    "scrollbar":     "#2a2a4a",
}

FONTS = {
    "title":    ("Segoe UI", 20, "bold"),
    "subtitle": ("Segoe UI", 11),
    "label":    ("Segoe UI", 11),
    "input":    ("Segoe UI", 12),
    "button":   ("Segoe UI", 11, "bold"),
    "password": ("Consolas", 12),
    "small":    ("Segoe UI", 9),
    "counter":  ("Segoe UI", 10),
}


# ──────────────────────────────────────────────
#  GUI
# ──────────────────────────────────────────────
class PasswordGeneratorApp:
    """Główna aplikacja GUI — Generator Haseł."""

    def __init__(self):
        self.engine = PasswordEngine()
        self.root = tk.Tk()
        self.root.title("Generator Haseł")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(False, False)

        # Rozmiar okna
        win_w, win_h = 620, 720
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")

        self._build_ui()

    # ── Budowanie interfejsu ──────────────────
    def _build_ui(self):
        root = self.root
        # ── Nagłówek ──
        header = tk.Frame(root, bg=COLORS["bg_dark"])
        header.pack(fill="x", padx=20, pady=(24, 0))

        tk.Label(
            header, text="🔐  Generator Haseł",
            font=FONTS["title"], fg=COLORS["fg_primary"], bg=COLORS["bg_dark"],
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Twórz silne, kryptograficznie bezpieczne hasła w kilka sekund.",
            font=FONTS["subtitle"], fg=COLORS["fg_secondary"], bg=COLORS["bg_dark"],
        ).pack(anchor="w", pady=(4, 0))

        # ── Separator ──
        sep = tk.Frame(root, height=1, bg=COLORS["border"])
        sep.pack(fill="x", padx=20, pady=(16, 16))

        # ── Karta ustawień ──
        card = tk.Frame(root, bg=COLORS["bg_card"], highlightbackground=COLORS["border"],
                        highlightthickness=1, bd=0)
        card.pack(fill="x", padx=20, pady=(0, 12))

        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(fill="x", padx=20, pady=20)

        # Długość hasła
        row1 = tk.Frame(inner, bg=COLORS["bg_card"])
        row1.pack(fill="x", pady=(0, 12))

        tk.Label(
            row1, text="Długość hasła:", font=FONTS["label"],
            fg=COLORS["fg_primary"], bg=COLORS["bg_card"],
        ).pack(side="left")

        self._updating_length = False
        self.length_var = tk.StringVar(value="16")
        self.length_var.trace_add("write", self._on_length_entry_changed)

        length_entry = tk.Entry(
            row1, textvariable=self.length_var, width=8, font=FONTS["input"],
            bg=COLORS["bg_input"], fg=COLORS["fg_primary"],
            insertbackground=COLORS["fg_primary"],
            relief="flat", bd=0, highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["bg_accent"],
        )
        length_entry.pack(side="left", padx=(12, 8))

        tk.Label(
            row1, text=f"({MIN_PASSWORD_LENGTH}–{MAX_PASSWORD_LENGTH})",
            font=FONTS["small"], fg=COLORS["fg_secondary"], bg=COLORS["bg_card"],
        ).pack(side="left")

        # Suwak
        self.length_slider = tk.Scale(
            inner, from_=MIN_PASSWORD_LENGTH, to=MAX_PASSWORD_LENGTH,
            orient="horizontal", command=self._on_slider_changed,
            bg=COLORS["bg_card"], fg=COLORS["fg_primary"],
            troughcolor=COLORS["bg_input"], highlightthickness=0,
            sliderrelief="flat", bd=0, font=FONTS["small"],
            activebackground=COLORS["bg_accent"],
            showvalue=False, length=350,
        )
        self.length_slider.set(16)
        self.length_slider.pack(fill="x", pady=(0, 12))

        # Ilość haseł
        row2 = tk.Frame(inner, bg=COLORS["bg_card"])
        row2.pack(fill="x", pady=(0, 4))

        tk.Label(
            row2, text="Ilość haseł:", font=FONTS["label"],
            fg=COLORS["fg_primary"], bg=COLORS["bg_card"],
        ).pack(side="left")

        self.count_var = tk.StringVar(value="5")
        count_entry = tk.Entry(
            row2, textvariable=self.count_var, width=8, font=FONTS["input"],
            bg=COLORS["bg_input"], fg=COLORS["fg_primary"],
            insertbackground=COLORS["fg_primary"],
            relief="flat", bd=0, highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["bg_accent"],
        )
        count_entry.pack(side="left", padx=(12, 8))

        tk.Label(
            row2, text=f"(1–{MAX_PASSWORDS_COUNT})",
            font=FONTS["small"], fg=COLORS["fg_secondary"], bg=COLORS["bg_card"],
        ).pack(side="left")

        # ── Przyciski ──
        btn_frame = tk.Frame(root, bg=COLORS["bg_dark"])
        btn_frame.pack(fill="x", padx=20, pady=(0, 12))

        self.generate_btn = tk.Button(
            btn_frame, text="⚡  Generuj hasła", font=FONTS["button"],
            bg=COLORS["bg_accent"], fg="#ffffff", activebackground=COLORS["bg_accent_hover"],
            activeforeground="#ffffff", relief="flat", bd=0, cursor="hand2",
            padx=20, pady=10, command=self._on_generate,
        )
        self.generate_btn.pack(side="left")
        self.generate_btn.bind("<Enter>", lambda e: self.generate_btn.config(bg=COLORS["bg_accent_hover"]))
        self.generate_btn.bind("<Leave>", lambda e: self.generate_btn.config(bg=COLORS["bg_accent"]))

        self.copy_btn = tk.Button(
            btn_frame, text="📋  Kopiuj wszystkie", font=FONTS["button"],
            bg=COLORS["bg_button"], fg=COLORS["fg_primary"],
            activebackground=COLORS["bg_button_hover"],
            activeforeground=COLORS["fg_primary"], relief="flat", bd=0,
            cursor="hand2", padx=20, pady=10, command=self._on_copy_all,
        )
        self.copy_btn.pack(side="left", padx=(10, 0))
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg=COLORS["bg_button_hover"]))
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg=COLORS["bg_button"]))

        self.clear_btn = tk.Button(
            btn_frame, text="🗑  Wyczyść historię", font=FONTS["button"],
            bg=COLORS["bg_button"], fg=COLORS["fg_primary"],
            activebackground=COLORS["bg_button_hover"],
            activeforeground=COLORS["fg_primary"], relief="flat", bd=0,
            cursor="hand2", padx=20, pady=10, command=self._on_clear_history,
        )
        self.clear_btn.pack(side="right")
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg=COLORS["bg_button_hover"]))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg=COLORS["bg_button"]))

        # ── Pole wyników ──
        result_card = tk.Frame(root, bg=COLORS["bg_card"],
                               highlightbackground=COLORS["border"],
                               highlightthickness=1, bd=0)
        result_card.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        result_header = tk.Frame(result_card, bg=COLORS["bg_card"])
        result_header.pack(fill="x", padx=16, pady=(12, 4))

        tk.Label(
            result_header, text="Wygenerowane hasła:", font=FONTS["label"],
            fg=COLORS["fg_primary"], bg=COLORS["bg_card"],
        ).pack(side="left")

        self.counter_label = tk.Label(
            result_header,
            text="Historia: 0 haseł",
            font=FONTS["counter"], fg=COLORS["fg_secondary"], bg=COLORS["bg_card"],
        )
        self.counter_label.pack(side="right")

        text_frame = tk.Frame(result_card, bg=COLORS["bg_input"],
                              highlightthickness=1, highlightbackground=COLORS["border"])
        text_frame.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.result_text = tk.Text(
            text_frame, font=FONTS["password"], bg=COLORS["bg_input"],
            fg=COLORS["fg_password"], insertbackground=COLORS["fg_password"],
            relief="flat", bd=0, wrap="none", state="disabled",
            highlightthickness=0, padx=12, pady=10,
            selectbackground=COLORS["bg_accent"],
            selectforeground="#ffffff",
            yscrollcommand=scrollbar.set,
        )
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.result_text.yview)

        # ── Pasek stanu ──
        status_bar = tk.Frame(root, bg=COLORS["bg_dark"])
        status_bar.pack(fill="x", padx=20, pady=(0, 12))

        self.status_label = tk.Label(
            status_bar,
            text="Gotowy \u2014 wprowad\u017a parametry i kliknij \u201eGeneruj has\u0142a\u201d.",
            font=FONTS["small"], fg=COLORS["fg_secondary"], bg=COLORS["bg_dark"],
            anchor="w",
        )
        self.status_label.pack(fill="x")

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self._on_generate())

    def _on_slider_changed(self, val):
        """Synchronizuje suwak z polem tekstowym długości."""
        if not self._updating_length:
            self._updating_length = True
            try:
                new_val = str(int(float(val)))
                if self.length_var.get() != new_val:
                    self.length_var.set(new_val)
            finally:
                self._updating_length = False

    def _on_length_entry_changed(self, *args):
        """Synchronizuje pole tekstowe ze suwakiem długości."""
        if not self._updating_length:
            val = self.length_var.get().strip()
            if val.isdigit():
                num = int(val)
                if MIN_PASSWORD_LENGTH <= num <= MAX_PASSWORD_LENGTH:
                    self._updating_length = True
                    try:
                        self.length_slider.set(num)
                    finally:
                        self._updating_length = False

    # ── Obsługa zdarzeń ───────────────────────
    def _on_generate(self):
        """Generuje hasła po kliknięciu przycisku."""
        # Walidacja długości
        try:
            length = int(self.length_var.get())
        except ValueError:
            messagebox.showerror("Błąd", "Długość hasła musi być liczbą całkowitą.")
            return

        if length < MIN_PASSWORD_LENGTH or length > MAX_PASSWORD_LENGTH:
            messagebox.showerror(
                "Błąd",
                f"Długość hasła musi wynosić od {MIN_PASSWORD_LENGTH} do {MAX_PASSWORD_LENGTH}.",
            )
            return

        # Walidacja ilości
        try:
            count = int(self.count_var.get())
        except ValueError:
            messagebox.showerror("Błąd", "Ilość haseł musi być liczbą całkowitą.")
            return

        if count < 1 or count > MAX_PASSWORDS_COUNT:
            messagebox.showerror(
                "Błąd",
                f"Ilość haseł musi wynosić od 1 do {MAX_PASSWORDS_COUNT}.",
            )
            return

        # Generowanie
        passwords = []
        try:
            for _ in range(count):
                passwords.append(self.engine.generate(length))
        except (ValueError, RuntimeError) as exc:
            messagebox.showerror("Błąd", str(exc))
            return

        # Wyświetlenie wyników
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        for i, pwd in enumerate(passwords, 1):
            self.result_text.insert("end", f"  {i:>2}.  {pwd}\n")
        self.result_text.config(state="disabled")

        self.counter_label.config(text=f"Historia: {self.engine.history_count} haseł")
        self.status_label.config(
            text=f"✅  Wygenerowano {count} {'hasło' if count == 1 else 'haseł'} "
                 f"o długości {length} znaków.",
            fg=COLORS["bg_success"],
        )

    def _on_copy_all(self):
        """Kopiuje wszystkie hasła do schowka."""
        self.result_text.config(state="normal")
        content = self.result_text.get("1.0", "end").strip()
        self.result_text.config(state="disabled")

        if not content:
            messagebox.showinfo("Informacja", "Brak haseł do skopiowania.")
            return

        # Wyodrębnij same hasła (bez numeracji)
        lines = content.split("\n")
        passwords_only = []
        for line in lines:
            line = line.strip()
            if line:
                # Usuwamy numerację "  1.  "
                parts = line.split(".", 1)
                if len(parts) == 2 and parts[0].strip().isdigit():
                    passwords_only.append(parts[1].strip())
                else:
                    passwords_only.append(line)

        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(passwords_only))
        self.root.update()

        self.status_label.config(
            text=f"📋  Skopiowano {len(passwords_only)} haseł do schowka.",
            fg=COLORS["bg_success"],
        )

    def _on_clear_history(self):
        """Czyści historię wygenerowanych haseł."""
        self.engine.clear_history()
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.config(state="disabled")

        self.counter_label.config(text="Historia: 0 haseł")
        self.status_label.config(
            text="🗑  Historia wyczyszczona — hasła mogą się ponownie pojawiać.",
            fg=COLORS["bg_warning"],
        )

    def run(self):
        self.root.mainloop()


# ──────────────────────────────────────────────
#  Punkt wejścia
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.run()

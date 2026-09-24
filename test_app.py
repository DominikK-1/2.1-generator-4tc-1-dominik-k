"""
Pełny zestaw testów automatycznych dla Generatora Haseł:
- Testy jednostkowe silnika (PasswordEngine)
- Testy poprawności i odporności interfejsu (PasswordGeneratorApp)
- Testy symulacji użytkownika (klikanie przycisków, kopiowanie, suwaki, skróty)
"""

import unittest
from unittest.mock import patch
import tkinter as tk
from generator_hasel import (
    PasswordEngine, PasswordGeneratorApp,
    MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, MAX_PASSWORDS_COUNT,
    LOWERCASE, UPPERCASE, DIGITS, SPECIAL
)

class TestPasswordEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PasswordEngine()

    def test_min_and_max_length(self):
        pwd_min = self.engine.generate(MIN_PASSWORD_LENGTH)
        self.assertEqual(len(pwd_min), MIN_PASSWORD_LENGTH)

        pwd_max = self.engine.generate(MAX_PASSWORD_LENGTH)
        self.assertEqual(len(pwd_max), MAX_PASSWORD_LENGTH)

    def test_complexity_requirements(self):
        for _ in range(30):
            pwd = self.engine.generate(16)
            self.assertTrue(any(c in LOWERCASE for c in pwd), "Brak małej litery")
            self.assertTrue(any(c in UPPERCASE for c in pwd), "Brak wielkiej litery")
            self.assertTrue(any(c in DIGITS for c in pwd), "Brak cyfry")
            self.assertTrue(any(c in SPECIAL for c in pwd), "Brak znaku specjalnego")

    def test_invalid_lengths_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.engine.generate(MIN_PASSWORD_LENGTH - 1)
        with self.assertRaises(ValueError):
            self.engine.generate(MAX_PASSWORD_LENGTH + 1)

    def test_uniqueness_and_history_clearing(self):
        passwords = [self.engine.generate(20) for _ in range(50)]
        self.assertEqual(len(passwords), len(set(passwords)))
        self.assertEqual(self.engine.history_count, 50)
        self.engine.clear_history()
        self.assertEqual(self.engine.history_count, 0)


class TestPasswordGeneratorAppGUI(unittest.TestCase):
    def setUp(self):
        self.app = PasswordGeneratorApp()
        self.app.root.update()

    def tearDown(self):
        self.app.root.destroy()

    def test_initial_values(self):
        self.assertEqual(self.app.length_var.get(), "16")
        self.assertEqual(self.app.count_var.get(), "5")
        self.assertEqual(self.app.engine.history_count, 0)
        self.assertIn("Historia: 0", self.app.counter_label.cget("text"))

    def test_slider_entry_synchronization(self):
        # Suwak -> Pole tekstowe
        self.app._on_slider_changed("28")
        self.assertEqual(self.app.length_var.get(), "28")

        # Pole tekstowe -> Suwak
        self.app.length_var.set("45")
        self.assertEqual(self.app.length_slider.get(), 45)

        # Odporność na puste pole i znaki niebędące cyframi (nie rzuca TclError)
        self.app.length_var.set("")
        self.assertEqual(self.app.length_var.get(), "")
        self.app.length_var.set("tekst")
        self.assertEqual(self.app.length_var.get(), "tekst")

    def test_generate_button_and_display(self):
        self.app.length_var.set("20")
        self.app.count_var.set("3")
        self.app.generate_btn.invoke()
        self.app.root.update()

        self.app.result_text.config(state="normal")
        content = self.app.result_text.get("1.0", "end").strip()
        self.app.result_text.config(state="disabled")

        lines = [l.strip() for l in content.splitlines() if l.strip()]
        self.assertEqual(len(lines), 3)
        for line in lines:
            parts = line.split(".", 1)
            self.assertEqual(len(parts[1].strip()), 20)
        self.assertEqual(self.app.engine.history_count, 3)

    def test_copy_all_button(self):
        self.app.length_var.set("14")
        self.app.count_var.set("2")
        self.app.generate_btn.invoke()
        self.app.root.update()

        self.app.copy_btn.invoke()
        self.app.root.update()

        copied = self.app.root.clipboard_get()
        copied_lines = [l.strip() for l in copied.strip().splitlines() if l.strip()]
        self.assertEqual(len(copied_lines), 2)
        for pwd in copied_lines:
            self.assertEqual(len(pwd), 14)

    def test_clear_history_button(self):
        self.app.length_var.set("10")
        self.app.count_var.set("2")
        self.app.generate_btn.invoke()
        self.assertGreater(self.app.engine.history_count, 0)

        self.app.clear_btn.invoke()
        self.app.root.update()

        self.assertEqual(self.app.engine.history_count, 0)
        self.assertEqual(self.app.counter_label.cget("text"), "Historia: 0 haseł")
        self.app.result_text.config(state="normal")
        self.assertEqual(self.app.result_text.get("1.0", "end").strip(), "")

    @patch("tkinter.messagebox.showerror")
    def test_input_validations(self, mock_err):
        # Niepoprawna długość
        self.app.length_var.set("abc")
        self.app.generate_btn.invoke()
        mock_err.assert_called()

        mock_err.reset_mock()
        self.app.length_var.set("2")  # poniżej 4
        self.app.generate_btn.invoke()
        mock_err.assert_called()

        # Niepoprawna ilość
        mock_err.reset_mock()
        self.app.length_var.set("16")
        self.app.count_var.set("0")
        self.app.generate_btn.invoke()
        mock_err.assert_called()

        mock_err.reset_mock()
        self.app.count_var.set("999")
        self.app.generate_btn.invoke()
        mock_err.assert_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)

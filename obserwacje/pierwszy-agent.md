# Mój pierwszy agent — karta obserwacji

- Narzędzie i model: Claude Opus 4.6 (Thinking) i Gemini 3.8 Flash
- Moje zadanie (2–3 zdania): Aplikacja w pythonie która generuje hasła. Są one bezpieczne z użyciem małych oraz wielkich liter i znaków specjalnych
- Pierwsza wiadomość (wklejona co do znaku): Write a program using python. The program generates passwords which length depends on number that user gave.

REQUIREMENTS:
- passwords can't be easy to crack - they must be strong
- they can't contain common phrases (names, dates of birth, etc.)
- passwords must contain (if possible) numbers, small and big letters, special characters
- generated passwords can't repeat
- the programme name has to be "Generator Haseł"
- buttons have to be in language: Polish

- test the programme and don't stop until it works

- Co agent zrobił najpierw: stworzył plik "generator_hasel.py"
- O co pytał — i co zostało zatwierdzone bez czytania: czy może zainstalować pythona
- Pierwszy błąd i co agent z nim zrobił: brak zainstalowanego pythona - zainstalował go
- Stan po 25 minutach: działa
- Skąd wiem, że aplikacja działa (co zostało sprawdzone): hasła są generowane, działa kopiowanie haseł i historia
- Rzeczy, które agent zrobił, a których nie rozumiem: dużą część kodu
- Jak mi się wydawało, że poszło (jedno zdanie): Wydaje mi się, że skoro działa to dałem dobry prompt
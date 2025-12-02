# 🚀 Maszynki – Launcher dla Windows & Linux

Maszynki to wieloplatformowe narzędzie pozwalające w prosty sposób uruchamiać aplikacje, skrypty oraz serwery na Windows i Linux. Projekt został stworzony z myślą o automatyzacji i wygodnym odpalaniu własnych maszyn / launcherów.

---

## ⭐ Funkcje

- Działa na **Windows** i **Linux**
- Łatwe uruchamianie aplikacji, skryptów i serwerów
- Obsługa plików `.bat` oraz `.sh`
- Prosta edycja i konfiguracja
- Możliwość dodawania własnych komend
- Idealne do serwerów Minecraft i innych projektów

---

## 🧰 Wersje systemowe

### 🪟 Windows
- Obsługiwane pliki: `.bat`
- Kompatybilność: Windows 10 / 11
- Uruchamianie przez dwuklik

### 🐧 Linux
- Obsługiwane pliki: `.sh`
- Wymaga nadania uprawnień wykonywania
- Kompatybilność: większość dystrybucji

---

## 📥 Instalacja

### Windows
1. Pobierz najnowszą wersję z **Releases**
2. Wypakuj folder
3. Uruchom `start.bat`

### Linux
```bash
chmod +x start.sh
./start.sh
```

---

## ⚡ Wymagania

W zależności od projektu mogą być wymagane:

- **Java 17 / Java 21**
- Python
- Node.js
- Inne środowiska zależnie od używanej maszyny

---

## 🛠️ Konfiguracja

Możesz edytować:

- `start.bat` – konfiguracja pod Windows
- `start.sh` – konfiguracja pod Linux

Przykład Windows:

```bat
@echo off
java -Xmx2G -jar server.jar
pause
```

Przykład Linux:

```bash
#!/bin/bash
java -Xmx2G -jar server.jar
```

---

## 🤝 Współtworzenie

Chętnie przyjmuję zgłoszenia błędów i propozycje zmian w **Issues** oraz **Pull Requests**.

---

## 📄 Licencja

Projekt dostępny na licencji MIT (lub innej, jeśli zmienisz).

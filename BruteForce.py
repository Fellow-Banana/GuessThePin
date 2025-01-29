import threading
import requests

print("\033[31m")
print("""
  GuessThePin.com Spammer and Bruteforcer
""")

def brute_force(guess: str, display_output=True):
    payload = {'guess': guess}
    response = requests.post('https://www.guessthepin.com/prg.php', data=payload)
    if "is not the PIN" not in response.text:
        if display_output:
            print(f"✅ The PIN is: {guess}")
        return True
    elif display_output:
        print(f"❌ PIN {guess} was incorrect")
    return False

def guess_pins(start_index, stop_event):
    for i in range(start_index, start_index + 1000):
        if stop_event.is_set():
            return
        pin = str(i).zfill(4)
        if brute_force(pin):
            stop_event.set() 
            return

def restart_threads(num_threads, stop_event):
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=guess_pins, args=(i * (10000 // num_threads), stop_event))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# Main logic
num_threads = 30 # Change this number if you want but around 30 seems to work fastest

while True:
    stop_event = threading.Event()
    restart_threads(num_threads, stop_event)
    print("🔄 Restarting all threads...")

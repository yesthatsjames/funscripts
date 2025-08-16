import random, time, sys
chars = '01'
width = 80
delay = 0.1

try:
    while True:
        print(''.join(random.choice(chars) for _ in range(width)), flush=True)
        time.sleep(delay)
except KeyboardInterrupt:
    print(f"\n{chr(27)}[92mMatrix simulation terminated.{chr(27)}[0m")

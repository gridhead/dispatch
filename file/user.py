import time, tqdm

def main():
    for i in tqdm.tqdm(range(10), unit="gei", desc="Waiting"):
        time.sleep(1)

desclist = [
    "[ OK ] Starting up",
    "[ OK ] Warming peripherals",
    "[ OK ] Loading drivers",
    "[ OK ] Linking startup",
    "[ OK ] Loading kernel",
    "[ OK ] Finishing up",
]

def feil():
    full = 6
    objc = tqdm.tqdm(total=full, desc="Transfer in progress...")
    for i in range(full):
        time.sleep(1)
        objc.update(1)
        objc.write(desclist[i], file=None, end="\n", nolock=False)
    objc.close()

if __name__ == "__main__":
    try:
        feil()
    except KeyboardInterrupt:
        exit(0)
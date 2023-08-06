import glob
from pathlib import Path
from OpUstad.utils import load_plugins
import logging
from OpUstad import UstaD, UstaD2, UstaD3, UstaD4, UstaD5 , UstaD6, UstaD7, UstaD8, UstaD9, UstaD10

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

path = "Deadly/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

print("Successfully deployed!")
print("Enjoy! Do /ping to Check Your Spam Bots")

if __name__ == "__main__":
    if UstaD:
     UstaD.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if UstaD2:
     UstaD2.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if UstaD3:
     UstaD3.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if UstaD4:
     UstaD4.run_until_disconnected()
    else:
      pass
if __name__ == "__main__":
    if UstaD5:
     UstaD5.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if UstaD6:
     UstaD6.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if UstaD7:
     UstaD7.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if UstaD8:
     UstaD8.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if UstaD9:    
     UstaD9.run_until_disconnected()
    else:
        pass
if __name__ == "__main__":
    if UstaD10:
    
     UstaD10.run_until_disconnected()
    else:
        pass
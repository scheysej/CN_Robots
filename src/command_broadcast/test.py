import Amove as am
import time
import aservo
import sys

try:
    aservo.left()
    time.sleep(1)
    aservo.right()
    time.sleep(1)
    aservo.left()
    sys.exit()
    
except KeyboardInterrupt:
    am.destroy()

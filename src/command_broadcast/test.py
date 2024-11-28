import Amove as am
import time
import aservo
import sys

try:
    aservo.left()
    am.forward()
    time.sleep(1)
    aservo.right()
    am.backward()
    time.sleep(1)
    aservo.center()
    am.motorStop()
    sys.exit()
    
except KeyboardInterrupt:
    am.destroy()

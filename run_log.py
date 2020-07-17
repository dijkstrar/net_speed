import sys
import pandas as pd
import subprocess

j=subprocess.call([sys.executable, "speedtestnet.py"])
print(j)
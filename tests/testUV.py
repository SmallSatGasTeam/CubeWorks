import sys
sys.path.append("../")

from Drivers.UV import UVDriver

    
uv = UVDriver()
print(uv.read())

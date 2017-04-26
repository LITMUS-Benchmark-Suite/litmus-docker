import glob
import random
import subprocess
l = glob.glob("/rdf_data/*.nt")

for each in l:
    s = "mv each %d" %(random.randint(0, 100000000000000000))
    subprocess.call(s, shell = True)
    

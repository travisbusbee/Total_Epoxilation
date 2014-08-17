outfile = r"\\vfiler1.seas.harvard.edu\group0\jlewis\User Files\epoxy.txt"
#header = r"pasth"
#footer = r"path"
import numpy as np
from mecode import G

g = G(
        print_lines = True,
        #outfile = outfile,
        #    header = header,
        #    footer = footer,
            mix = True,
            angular_velocity = 600,
            mixing_multiplier = 1
            )


def set_infuse_rate(rate, com_string = 'hfileB'):
    g.write('CALL SetIRate P${} Q{}'.format(com_string ,rate))

def start_infuse():
    g.write('CALL StartInfuse P$hFileB')
    
def stop_infuse():
    g.write('CALL StopPump P$hFileB')    

def clear_pump():
    g.write('CALL ClearPump P$hFileB')
    
g.feed(10)   
for i in range(10):
    set_infuse_rate(rate = 20+ i*20)
    set_infuse_rate(rate = i*20, com_string = 'hfileA')
    g.meander(10, 10, 2)
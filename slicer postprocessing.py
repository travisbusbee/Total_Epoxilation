f1 = open(r'C:\Users\tbusbee\Desktop\example_gcode.txt', 'r')
f2 = open(r'C:\Users\tbusbee\Desktop\edited_example_gcode.txt', 'w')


for line in f1:
    if "E" in line:
        temp_line = line.split('E', 1)[0]
        
    else:
        temp_line = line
    print temp_line
    f2.write(line.replace(';', ' '))
f1.close()
f2.close()
#import re
#text = 'G1 X108.412 Y-37.393 E3.59418 ; brim'



### Trav's Laptop#########
#f1 = open(r'C:\Users\Workstation 1\Documents\GitHub\Total_Epoxilation\bareduino-sliced (4).gcode', 'r') #input file
#f3 = open(r'C:\Users\Workstation 1\Documents\GitHub\Total_Epoxilation\bareduino_postprocessed_bitches.gcode', 'w') #output file
#f1 = open(r'C:\Users\Workstation 1\Downloads\electromagnet_body (repaired)-sliced (2).gcode', 'r') #input file
#f3 = open(r'C:\Users\Workstation 1\Downloads\electromagnet_processed_2.gcode', 'w') #output file
f1 = open(r'D:\sync\mDan\2BATTBASE.gcode', 'r') #input file
f3 = open(r'D:\sync\mDan\2BATTBASE-J-post.gcode', 'w') #output file


#f1 = open(r'C:\Users\Workstation 1\Downloads\Scene-sliced (77).gcode', 'r') #input file
#f3 = open(r'C:\Users\Workstation 1\Downloads\Scene-sliced-post.gcode', 'w') #output file


ident = 0

#line = "G0 X121.67389 Y13.97381 Z0.57613 F7200.0"



for i, line in enumerate(f1):
    if "Z" in line:
        if "X" in line:
            back_line = line.split("Z", 1)[1]
            current_z_string = back_line.split(' ', 1)[0]
    
    
    if ident == 0:
        f3.write(line)
    #if ident ==2:
    #    ident = 1
        
    if ident ==2 and "Z" in line and "X" in line:
        xy_val = line.split('Z', 1)[0]
        #print "ERROR:", i, line
        back_end = line.split('Z', 1)[1]
        speed = back_end.split(' ',1)[1]
        new_xy = xy_val + ' ' + speed
        z_value = back_end.split(' ', 1)[0]
        new_z = 'G1 Z' + z_value + ' F1000'
        f3.write(new_xy + '\n')
        f3.write(new_z + '\n')
        ident = 0
    elif ident == 2:
        f3.write(line)
        
    if ident ==7 and "Z" in line and "X" in line:
        xy_val = line.split('Z', 1)[0]
        #print "ERROR:", i, line
        back_end = line.split('Z', 1)[1]
        speed = back_end.split(' ',1)[1]
        new_xy = xy_val + ' ' + speed
        z_value = back_end.split(' ', 1)[0]
        new_z = 'G1 Z' + z_value + ' F1000'
        f3.write(new_xy + '\n')
        f3.write(new_z + '\n')
        ident = 0
    elif ident == 7:
        f3.write(line)
            
    if ident ==3 and "Z" in line and "X" in line:
        xy_val = line.split('Z', 1)[0]
        back_end = line.split('Z', 1)[1]
        speed = back_end.split(' ',1)[1]
        new_xy = xy_val + ' ' + speed
        z_value = back_end.split(' ', 1)[0]
        new_z = 'G1 Z' + z_value + ' F1000'
        f3.write(new_xy + '\n')
        f3.write(new_z + '\n')
        ident = 0
    elif ident == 3:
        f3.write(line) 
          
    if ident ==6:
        current_z_value = float(current_z_string)
        if current_z_value > 10:
            safe_z = current_z_value + 3
        else:
            safe_z = 13
        f3.write('G1 Z' + str(safe_z) + ' F1000\n')  
        ident = 0    
          
    if ";T0 activated" in line:
        ident = 2
        
    if ";T1 activated" in line:
        ident = 3
        
    if ";move to z" in line:
        ident = 6
    
    if ";pause activated" in line:
        ident = 7

f1.close()
f3.close()

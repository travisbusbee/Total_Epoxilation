
### Trav's Laptop#########
f1 = open(r'C:\Users\Workstation 1\Documents\GitHub\Total_Epoxilation\test_wire-sliced.gcode', 'r')
f3 = open(r'C:\Users\Workstation 1\Documents\GitHub\Total_Epoxilation\test_code_processed_2.gcode', 'w')




ident = 0

#line = "G0 X121.67389 Y13.97381 Z0.57613 F7200.0"



for line in f1:
    if ident == 4:
        if "Z" in line:
            if "X" in line:
                ident =3
        else:
            f3.write(line)
    if ident == 0:
        f3.write(line)
    if ident ==2:
        ident = 1
        
    elif ident ==1:
        xy_val = line.split('Z', 1)[0]
        back_end = line.split('Z', 1)[1]
        speed = back_end.split(' ',1)[1]
        new_xy = xy_val + ' ' + speed
        z_value = back_end.split(' ', 1)[0]
        new_z = 'G1 Z' + z_value + ' F1000'
        f3.write(new_xy + '\n')
        f3.write(new_z + '\n')
        ident = 0
            
    elif ident ==3:
        xy_val = line.split('Z', 1)[0]
        back_end = line.split('Z', 1)[1]
        speed = back_end.split(' ',1)[1]
        new_xy = xy_val + ' ' + speed
        z_value = back_end.split(' ', 1)[0]
        new_z = 'G1 Z' + z_value + ' F1000'
        f3.write(new_xy + '\n')
        f3.write(new_z + '\n')
        ident = 0
          
    if ";T0 activated" in line:
        ident = 2
        
    if ";T1 activated" in line:
        ident = 4
    

f1.close()
f3.close()

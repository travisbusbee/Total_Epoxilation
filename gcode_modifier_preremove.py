from mecode import G
g = G(print_lines = True)
original_file = r'/Users/busbees/Desktop/gcode_test.gcode'
modified_file = r'/Users/busbees/Desktop/text_test_mod.txt'
x_offset = 104
y_offset = 1
silver_feed = 4
matrix_feed = 12

f1 = open(r'C:\Users\tbusbee\Documents\Voxel8 Sync\Travis\3D epoxy code\3D epoxy assembly - Matrix_epoxy3d-1.amf.gcode', 'r')
f2 = open(r'C:\Users\tbusbee\Documents\Voxel8 Sync\Travis\3D epoxy code\3D epoxy_test_mod.txt', 'w')
f3 = open(r'C:\Users\tbusbee\Documents\Voxel8 Sync\Travis\3D epoxy code\gcode_test_removed.txt', 'w')
tool_status = 1
z_axis = 'A'
valve = 0
ident = 0
check = 0
E_in = False

start_write = False
for line in f1:
    if "set temperature" in line:
        ident = 1
    if "disable fan" in line:
        ident = 1
    if "retract" in line:
        ident = 1
    if "change extruder" in line:
        ident = 1
    if "extrusion distance" in line:
        ident = 1
    if "posoffset" in line:
        ident = 1
    if "G1 Z" in line:
        start_write = True
    if "M2" in line:
        start_write = False
    if ident != 1:
        if start_write is True:
            f3.write(line)
    ident = 0

f1.close()
f3.close()
f3 = open(r'C:\Users\tbusbee\Documents\Voxel8 Sync\Travis\gcode_test_removed.txt', 'r')





for line in f3:
    if "E" in line:
        E_in = True
        (front, back) = line.split(r'E', 1)[0], line.split(r'E', 1)[1]
        print "back is: {}".format(back)
        if " F" in back:
            Fback = back.split(r'F', 1)[1]
            new_line = front + 'F' + Fback
            F_in = True
        if F_in is not True:
            if ";" in back:
                new_back = back.split(';', 1)[1]
                new_line = front + ';' + new_back
    else:
        new_line = line
    #print new_line
    

    if "F" in new_line:
            if E_in is False:
                f2.write("$DO{}.0 = 0\n".format(valve))
            elif E_in is True:
                if "retract" in new_line:
                    check = 1
                if "extrusion" in new_line:
                    check = 1
                if check < 0.5:
                    print "check is not 1"
                    f2.write("$DO{}.0 = 1\n".format(valve))
                check = 0
                
            (front, back) = new_line.split(r'F', 1)[0], new_line.split(r'F', 1)[1]
            if ";" in line:
                new_back = back.split(';', 1)[1]
                new_line = front + ';' + new_back
            
    else:
        new_line = new_line
    if "set temperature" in new_line:
        ident = 1
    if "disable fan" in new_line:
        ident = 1
    if "retract" in new_line:
        ident = 1
    if "change extruder" in new_line:
        ident = 1
    if "extrusion distance" in new_line:
        ident = 1
    if "ToolChange" in new_line:
        tool_status= -tool_status
        if tool_status == -1:
            f2.write('$DO{}.0 = 0\n'.format(valve))
            f2.write('G91\n')
            f2.write('F40\n')
            f2.write('G1 A10\n')
            f2.write('$currentX = AXISSTATUS(X, DATAITEM_PositionFeedback)\n')
            f2.write('$currentY = AXISSTATUS(Y, DATAITEM_PositionFeedback)\n')
            f2.write('G1 X{} Y{}\n'.format(-x_offset, -y_offset))
            f2.write('G92 X$currentX Y$currentY\n')
            f2.write('G1 B-10\n')
            f2.write('G90\n')
            f2.write('G1 F{}\n'.format(silver_feed))
            valve = 1
            z_axis = 'B'
        elif tool_status ==1:
            f2.write('$DO{}.0 = 0\n'.format(valve))
            f2.write('G91\n')
            f2.write('F40\n')
            f2.write('G1 B10\n')
            f2.write('POSOFFSET CLEAR X Y\n')
            f2.write('G1 X{} Y{}\n'.format(x_offset, y_offset))
            f2.write('G90\n')
            f2.write('G1 A-10\n')
            f2.write('G1 F{}\n'.format(matrix_feed))
            valve = 0
            z_axis = 'A'
    print "new line pre file_write: {}  ident: {}".format(new_line, ident)
    if ident != 1:
        f2.write(new_line)
    E_in = False
    F_in = False
    ident = 2
    #f2.write(new_line)        
    print new_line
    
#f1.close()
f2.close()
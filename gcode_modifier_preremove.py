from mecode import G
from aerotech_automation import AerotechAutomator
automator = AerotechAutomator()
g = G(print_lines = True)
automator.load_state(r"C:\Users\Lewis Group\Desktop\Calibration\alignment_data.txt")

zA  = zB = zC = zD =0
zA = automator.substrate_origins['slide1']['A'][2]+0.07
zB = automator.substrate_origins['slide1']['B'][2]+0.07
x_offset = (automator.home_positions['B'][0] - automator.home_positions['A'][0])
y_offset = (automator.home_positions['B'][1] - automator.home_positions['A'][1])

original_file = r'/Users/busbees/Desktop/gcode_test.gcode'
modified_file = r'/Users/busbees/Desktop/text_test_mod.txt'

velocity = False
silver_up = True
silver_feed = 3
matrix_feed = 40
com_port = 4
silver_pressure = 15
matrix_pressure = 59
silver_extra_height = 0.2

### robomama#########
f1 = open(r'C:\Users\Lewis Group\Documents\GitHub\Total_Epoxilation\Fileted single layer epoxy assembly.gcode', 'r')
f2 = open(r'C:\Users\Lewis Group\Documents\GitHub\Total_Epoxilation\2D_epoxy_test_mod.pgm', 'w')
f3 = open(r'C:\Users\Lewis Group\Documents\GitHub\Total_Epoxilation\gcode_test_removed.txt', 'w')
header = open(r'C:\Users\Lewis Group\Documents\GitHub\Total_Epoxilation\epoxy_header.txt', 'r')
footer = open(r'C:\Users\Lewis Group\Documents\GitHub\Total_Epoxilation\epoxy_footer.txt', 'r')

### office ######
#f1 = open(r'C:\Users\tbusbee\Documents\GitHub\Total_Epoxilation\3D epoxy assembly - Matrix_epoxy3d-1.amf.gcode', 'r')
#f2 = open(r'C:\Users\tbusbee\Documents\GitHub\Total_Epoxilation\3D epoxy_test_mod.pgm', 'w')
#f3 = open(r'C:\Users\tbusbee\Documents\GitHub\Total_Epoxilation\gcode_test_removed.txt', 'w')
#header = open(r'C:\Users\tbusbee\Documents\GitHub\Total_Epoxilation\epoxy_header.txt', 'r')
#footer = open(r'C:\Users\tbusbee\Documents\GitHub\Total_Epoxilation\epoxy_footer.txt', 'r')

tool_status = 1
z_axis = 'A'
Aaxis_multiplier = 0
Baxis_multiplier = 1
valve = 0
ident = 0
check = 0
E_in = False
up_move = False
skirt = False




### Parse and remove bullshit like retraction and write new file###
start_write = False
for line in f1:
    if "set temperature" in line:
        ident = 1
    if skirt is False:
        if "skirt" in line:
            ident = 1
    if "fan" in line:
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
###robomama###
f3 = open(r'C:\Users\Lewis Group\Documents\GitHub\Total_Epoxilation\gcode_test_removed.txt', 'r')

###office###
#f3 = open(r'C:\Users\tbusbee\Documents\GitHub\Total_Epoxilation\gcode_test_removed.txt', 'r')
### Write header to file ####
stuff = header.readlines()
f2.writelines(stuff)  
f2.write('Call setPress P{} Q{}\n'.format(com_port, matrix_pressure))
f2.write('Call togglePress P{}\n'.format(com_port))

### set z home ###########
f2.write('POSOFFSET CLEAR A B C D\n')
f2.write('$zoA = {}\n'.format(zA))
f2.write('$zoB= {}\n'.format(zB))
f2.write('G1 F25\n')
f2.write('G90\n')
f2.write('G1 A-2 B-2 C-2 D-2\n')
f2.write('G92 A{} B{} C{} D{}\n'.format(-zA - 2, -zB - 2, -zC - 2, -zD-2))
f2.write('G1 X518.1259 Y129.475\n')
f2.write('G1 F{}\n'.format(matrix_feed))
if velocity is True:
    f2.write('G108\n')
    f2.write('VELOCITY ON\n')
#################################


### parse and edit file that has bullshit removed ###
for line in f3:
    if "Z" in line:
        back_end = line.split(r'Z', 1)[1]
        number = float(back_end.split(r' ', 1)[0])
        temp_line = 'G1 {}{} {}{}'.format('A', number +10*Aaxis_multiplier, 'B', number+10*Baxis_multiplier) #+ line.split(r'Z', 1)[1]
        print "temp line: {}".format(temp_line)
        line = temp_line
    if "E" in line:
        E_in = True
        (front, back) = line.split(r'E', 1)[0], line.split(r'E', 1)[1]
        
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
                if valve == 1:
                    if silver_up is True:
                        f2.write('DWELL 0.25\n')
                        f2.write('G91\n')
                        f2.write("G1 {}1\n".format(z_axis))
                        f2.write('G90\n')
                        up_move = True
            elif E_in is True:
                if "retract" in new_line:
                    check = 1
                if "extrusion" in new_line:
                    check = 1
                if check < 0.5:
                    
                    f2.write("$DO{}.0 = 1\n".format(valve))
                    
                    if valve == 1:
                        f2.write('DWELL 0.5\n')
                    #if valve ==0:
                        #f2.write('DWELL 0.1\n')
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
            f2.write('Call setPress P{} Q{}\n'.format(com_port, silver_pressure))
            f2.write('Call togglePress P{}\n'.format(com_port))
            f2.write('$DO{}.0 = 1\n'.format(valve))
            f2.write('$DO6.0 = 1\n'.format(valve))
            f2.write('DWELL 0.5\n')
            f2.write('$DO{}.0 = 0\n'.format(valve))
            f2.write('$DO6.0 = 0\n'.format(valve))
            
            ## purge silver real fast
            f2.write('$DO1.0 = 1\n')
            f2.write('DWELL 0.6\n')
            f2.write('$DO1.0 = 0\n')
            
            f2.write('Call togglePress P{}\n'.format(com_port))
            f2.write('G91\n')
            f2.write('F40\n')
            f2.write('$currentZ = AXISSTATUS({}, DATAITEM_PositionFeedback)\n'.format(z_axis))
            f2.write('G1 A10 \n')
            f2.write('$currentX = AXISSTATUS(X, DATAITEM_PositionFeedback)\n')
            f2.write('$currentY = AXISSTATUS(Y, DATAITEM_PositionFeedback)\n')
            f2.write('G1 X{} Y{}\n'.format(x_offset, y_offset))
            f2.write('G92 X$currentX Y$currentY\n')
            f2.write('G90\n')
            f2.write('G1 B($currentZ-$zoA+{})\n'.format(silver_extra_height))
            f2.write('G1 F{}\n'.format(silver_feed))
            valve = 1
            z_axis = 'B'
        elif tool_status ==1:
            f2.write('$DO{}.0 = 0\n'.format(valve))
            f2.write('Call setPress P{} Q{}\n'.format(com_port, matrix_pressure))
            f2.write('Call togglePress P{}\n'.format(com_port))
            f2.write('$DO{}.0 = 1\n'.format(valve))
            f2.write('$DO6.0 = 1\n'.format(valve))
            f2.write('DWELL 0.5\n')
            f2.write('$DO{}.0 = 0\n'.format(valve))
            f2.write('$DO6.0 = 0\n'.format(valve))
            f2.write('Call togglePress P{}\n'.format(com_port))
            f2.write('G91\n')
            f2.write('F40\n')
            f2.write('$currentZ = AXISSTATUS({}, DATAITEM_PositionFeedback)\n'.format(z_axis))
            f2.write('G1 B10\n')
            f2.write('POSOFFSET CLEAR X Y\n')
            f2.write('G1 X{} Y{}\n'.format(-x_offset, -y_offset))
            f2.write('G90\n')
            f2.write('G1 A($currentZ-$zoB)\n')            
            f2.write('G1 F{}\n'.format(matrix_feed))
            valve = 0
            z_axis = 'A'
            
   
    if ident != 1:
        f2.write(new_line)
        if up_move is True:
            f2.write('G91\n')
            f2.write('G1 {}-1\n'.format(z_axis))
            f2.write('G90\n')
    E_in = False
    F_in = False
    up_move = False
    ident = 2
   

f2.write('Call togglePress P{}\n'.format(com_port))
f2.write('G91\n')
f2.write('G1 A30 B30\n')
f2.write('POSOFFSET CLEAR X Y U A B C D\n')
if velocity is True:
    f2.write('VELOCITY OFF\n')

stuff = footer.readlines()
f2.writelines(stuff)    
#f1.close()
f2.close()
header.close()
footer.close()
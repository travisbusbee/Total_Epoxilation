from mecode import G
#from aerotech_automation import AerotechAutomator
#automator = AerotechAutomator()
g = G(print_lines = True)
#automator.load_state(r"C:\Users\Lewis Group\Desktop\Calibration\alignment_data.txt")

zO = 0
#zA = -64#automator.substrate_origins['slide1']['A'][2]+0.07
#zB = -50#automator.substrate_origins['slide1']['B'][2]+0.07
x_offset = 0#(automator.home_positions['B'][0] - automator.home_positions['A'][0])
y_offset = 0#(automator.home_positions['B'][1] - automator.home_positions['A'][1])

original_file = r'/Users/busbees/Desktop/gcode_test.gcode'
modified_file = r'/Users/busbees/Desktop/text_test_mod.txt'


silver_up = True
silver_feed = 6*60
matrix_feed = 30*60
com_port = 4
silver_pressure = 14
matrix_pressure = 45
silver_extra_height = 0.1

### Trav's Laptop#########
f1 = open(r'/Users/busbees/Documents/Code/Total_Epoxilation/Rookv_fixed1.gcode', 'r')
f2 = open(r'/Users/busbees/Documents/Code/Total_Epoxilation/2D_epoxy_test_mod.gcode', 'w')
f3 = open(r'/Users/busbees/Documents/Code/Total_Epoxilation/gcode_test_removed.txt', 'w')
header = open(r'/Users/busbees/Documents/Code/Total_Epoxilation/epoxy_header_prusa.txt', 'r')
footer = open(r'/Users/busbees/Documents/Code/Total_Epoxilation/epoxy_footer_prusa.txt', 'r')



tool_status = 1
z_axis = 'Z'
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
    if "M109" in line:
        ident = 1
    if "G1 Z" in line:
        start_write = True
    if "M2" in line:
        start_write = False
    if ident != 1:
        if start_write is True:
            f3.write(line)
            #f2.write('\n')
    ident = 0

f1.close()
f3.close()
###robomama###
f3 = open(r'/Users/busbees/Documents/Code/Total_Epoxilation/gcode_test_removed.txt', 'r')

###office###
#f3 = open(r'C:\Users\tbusbee\Documents\GitHub\Total_Epoxilation\gcode_test_removed.txt', 'r')
### Write header to file ####
stuff = header.readlines()
f2.writelines(stuff)  
f2.write('\n')


### set speed  ###########
f2.write('G1 F{}\n'.format(matrix_feed))

#################################


### parse and edit file that has bullshit removed ###
for line in f3:
    if "Z" in line:
        back_end = line.split(r'Z', 1)[1]
        number = float(back_end.split(r' ', 1)[0])
        temp_line = 'G1 {}{}'.format('Z', number +10.0*Aaxis_multiplier) #+ line.split(r'Z', 1)[1]
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
                f2.write("M400\n")
                f2.write("M42 P32 S0\n")
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
                    f2.write("M400\n")
                    f2.write("M42 P32 S255\n")
                    
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
                       
            f2.write('G1 F{}\n'.format(silver_feed))
            valve = 1
            z_axis = 'B'
            Baxis_multiplier = 0
            Aaxis_multiplier = 1
        elif tool_status ==1:
            f2.write("M400\n")
            f2.write('M42 P32 S0\n')
            f2.write("M400\n")
            f2.write('M42 P32 S255\n')
            f2.write('DWELL 0.2\n')
            f2.write("M400\n")
            f2.write('M42 P32 S0\n')
            f2.write('G1 F{}\n'.format(matrix_feed))
            z_axis = 'A'
            Baxis_multiplier = 1
            Aaxis_multiplier = 0
            
   
    if ident != 1:
        f2.write(new_line)
        f2.write('\n')
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
f2.write('G1 Z20\n')
f2.write('G90\n')



stuff = footer.readlines()
f2.writelines(stuff) 
f2.write('\n')   
#f1.close()
f2.close()
header.close()
footer.close()
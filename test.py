
from math import sin
from time import sleep
from curseswm import *


# Create the Cli
cli = CLI()
# Create some tabs and add them to the cli
tab = Tab("Main")
cli.add_tab(tab)

tab2 = Tab("Networks")
cli.add_tab(tab2)

tab3 = Tab("Threads")
cli.add_tab(tab3)
# Create a vertical box
main_box = VBox()
# Create a graph and add it to the vertical box
g = Graph("Cpu Usage")
main_box.add_window(g)

# Create a horizontal box
central_box = HBox()

disk_temp_box = VBox()
disk = TextBox("Disk Usage")
temp = TextBox("Temperatures")
disk_temp_box.add_window(disk)
disk_temp_box.add_window(temp)

central_box.add_window(disk_temp_box)
mem = TextBox("Memory Usage")
central_box.add_window(mem, weight=2)

main_box.add_window(central_box)

last_box = HBox()
network = TextBox("Network Usage")
last_box.add_window(network)
processes = TextBox("Proceses")
last_box.add_window(processes)

main_box.add_window(last_box)

tab.set_window(main_box)


cli.set_refresh_rate(60)
cli.start()

sleep(1)



i = 0

while True:
    disk.set_text(disk.get_first_col(),disk.get_first_row(),"Time Enlapsed %d"%i)
    tab2.set_error_state(int(i/ 30) % 2 == 1)
    g.add_point(sin(i/20))

    # Print position methods results
    processes.set_text(processes.get_first_col(), processes.get_first_row(), str((
        processes.get_first_col(),
        processes.get_mid_col(),
        processes.get_last_col())))
    processes.add_text(processes.get_first_col(), processes.get_first_row(1), str((
        processes.get_first_row(),
        processes.get_mid_row(),
        processes.get_last_row())))
    processes.add_text(processes.get_first_col(), processes.get_first_row(2), str(processes.get_shape()))
        
    # Test of all the combination of prosition mehtod
    c = "~~"
    mem.set_text(mem.get_first_col(),mem.get_first_row(),c)
    mem.add_text(mem.get_first_col(),mem.get_mid_row(),c)
    mem.add_text(mem.get_first_col(),mem.get_last_row(),c)
    mem.add_text(mem.get_mid_col(),mem.get_first_row(),c)
    mem.add_text(mem.get_mid_col(),mem.get_mid_row(),c)
    mem.add_text(mem.get_mid_col(),mem.get_last_row(),c)
    mem.add_text(mem.get_last_col(),mem.get_first_row(),c)
    mem.add_text(mem.get_last_col(),mem.get_mid_row(),c)
    mem.add_text(mem.get_last_col(),mem.get_last_row(),c)

    i += 1
    sleep(1/60)

print("end")
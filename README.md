# curses_wm
a windows and tabs manager based on curses inspired by the design of gotop https://github.com/cjbassi/gotop

Example of usage:
```python

cli = CLI()

tab = Tab("Overview")
cli.add_tab(tab)

tab2 = Tab("Networks")
cli.add_tab(tab2)

tab3 = Tab("Threads")
cli.add_tab(tab3)


w0 = TextBox("Timer")
w1 = Window("Windows 1")
w2 = Window("Windows 2")
w3 = Window("Windows 3")
w4 = TextBox("TextBox 4")
w5 = Window("Windows 5")
w6 = Window("Windows 6")

w4.set_text(2,2,"Test Text 3")

v = VBox()
v.add_window(w0,weight=1)

h = HBox()
h.add_window(w4,weight=1)
h.add_window(w5,weight=1)

v.add_window(h,weight=2)

tab.set_window(v)

tab2.set_window(w2)

tab3.set_window(w3)

cli.start()


i = 0
while True:
    w0.set_text(0,0,"Time Enlapsed %d"%i)
    tab.set_error_state(i % 2 == 0)
    tab2.set_error_state(i % 2 == 1)
    i += 1
    sleep(1)
```
#import necessary modules
import calendar
from tkinter import *
from collections import defaultdict

#dictionary keyed by day of the month that goes to a list of event_dict
events = defaultdict(list)


#sets each day of month to a blank list
for day in range(1, 32):
    events[day] = []

# Reads data stored in user.txt and loads into events defaultdict

file = open("user.txt", "r+")
for line in file:
    data = line.split("*")
    if len(data) == 4:
        data[3] = data[3][:-1]
        day = data[0]

        # Check to see if this is the first event on the selected day
        if events[int(day)] == None:
            events[int(day)] = []
        events[int(day)].append({
            "event_name": data[1],
            "event_date": data[2],
            "event_time": data[3]})


def add_event(events, i, count, year):
    '''creates function for when 'add event' button is clicked'''
    day_gui.withdraw()
    global add_gui
    add_gui = Toplevel()
    add_gui.title('What event would you like to add?')
    #creates name label and entry field
    event_name = Label(
        add_gui, text="Enter Event name: ", bg="sky blue", font=('times',16)).grid(row=1, column=1)
    
    #defines a variable for user entry in name_field
    name_field = Entry(add_gui)
    name_field.grid(row=1, column=2)
    
    #creates event time label and entry field
    #defines a variable for user entry in time_field
    event_time = Label(
        add_gui, text="Enter Event Time: ", bg="sky blue", font=('times', 16)).grid(row=3, column=1)
    time_field = Entry(add_gui)
    time_field.grid(row=3, column=2)
    
    submit_button = Button(add_gui, text='Submit', command=lambda: add_submit(name_field, time_field, i, count, year)).grid(row=4, column=2)
    back_button = Button(
        add_gui, text='Go Back',
        command=lambda: add_back(i, count, year)).grid(row=4, column=1)


def add_submit(name_field, time_field, i, count, year):
  '''adds event to dictionary and user.txt'''
  name_get = name_field.get()
  time_get = time_field.get()
  date_get = str(count) + "/" + str(i + 1) + "/" + str(year)
    
    #writes added event into user.txt file
  file = open("user.txt", "a")
  file.write(str(i + 1))
  file.write("*")
  file.write(name_get)
  file.write("*")
  file.write(date_get)
  file.write("*")
  file.write(time_get)
  file.write("\n")
  file.close()
  
  event_dict = {
      "event_name": name_get,
      "event_date": date_get,
      "event_time": time_get
    }
    # Check to see if this is the first event on the selected day
  if events[i + 1] == None:
    events[i + 1] = []
  events[i + 1].append(event_dict)
  add_gui.withdraw()
  open_day(i, count, year)

def add_back(i, count, year):
    ''' takes user back to event display page'''
    add_gui.withdraw()
    open_day(i, count, year)


def edit_event(event_name, event_date, event_time, events, events_day, i, count, year):
    '''function for when 'edit event' button is clicked'''
    action_gui.withdraw()
    global edit_gui
    edit_gui = Toplevel()
    Label(
        edit_gui,
        text=('You have chosen to edit'.format(event_name)),
        font=('times', 20),
        bg='sky blue').grid(
            row=1, column=1)

    #creates a label to get updated event date
    Label(edit_gui,
        text="Enter Updated Event Date: ",
        bg="sky blue",
        font=('times', 16)).grid(
            row=2, column=1)
    date_field = Entry(edit_gui)
    date_field.insert(END, event_date)
    date_field.grid(row=2, column=2)

    #creates a time label and entry field
    Label(edit_gui,text="Enter Updated Event Time: ",bg="sky blue",font=('times', 16)).grid(row=3, column=1)
    time_field = Entry(edit_gui)
    time_field.insert(END, event_time)
    time_field.grid(row=3, column=2)

    submit_button = Button(edit_gui,text='Submit',command=lambda: edit_submit(event_name, date_field, time_field, events_day, i, count, year)
    ).grid(row=4, column=2)
    back_button = Button(edit_gui, text='Go back',command=lambda: edit_back(i, count, year)).grid(row=4, column=1)


def edit_submit(event_name, date_field, time_field, events_day, i, count, year):
  '''saves edited information to events dictionary and user.txt'''
  date_get = date_field.get()
  time_get = time_field.get()
  file = open("user.txt", "r+")
  data = []
  lines = file.readlines()
  file.close()

    # Put events from user.text into a 2d array
  for line in lines:
    data.append(line.split("*"))

    # Editing list values in data list
  for event in data:
    if len(event) == 4:
        day = date_get.split("/")
        day = day[1]
        if event_name == event[1]:
          event[0] = day
          
          event[2] = date_get
          event[3] = time_get

    # Updating text file
  file = open("user.txt", "w")
  for event in data:
      event = "*".join(event)
      file.write(event)
      file.write("\n")
  file.close()

    # update events dictionary
  for day in range(1, 32):
      events[day] = []
  file = open("user.txt", "r+")
  for line in file:

      data = line.split("*")
      if len(data) == 4:
          data[3] = data[3][:-1]
          dates = data[2].split('/')
          day = dates[1]
          data[0] = day
            # Check to see if this is the first event on the selected day
          if events[int(day)] == None:
              events[int(day)] = []
          events[int(day)].append({
                "event_name": data[1],
                "event_date": data[2],
                "event_time": data[3]
            })

  edit_gui.withdraw()
  open_day(i, count, year)

def edit_back(i, count, year):
    '''takes user back to event display page'''
    edit_gui.withdraw()
    open_day(i, count, year)

def remove_event(event_name, events_day, events, i, count, year):
    '''function for when 'remove event' button is clicked'''
    action_gui.withdraw()
    global remove_gui
    remove_gui = Toplevel()
    remove_gui['background'] = 'sky blue'
    remove_gui.title('Remove Event')
    Label(
        remove_gui,
        text="Warning: this action cannot be undone",
        bg="sky blue",
        font=('times', 16)).grid(
            row=1, column=1)

    submit_button = Button(
        remove_gui,
        text='Submit',
        command=lambda: remove_submit(event_name, events_day, i, count, year)
    ).grid(
        row=1, column=2)

def remove_submit(event_name, events_day, i, count, year):
    '''# removes selected event from events dictionary and user.txt'''
    file = open("user.txt", "r+")
    data = []
    lines = file.readlines()
    file.close()

    # Put events from user.text into a 2d array
    for line in lines:
        data.append(line.split("*"))

    # Removing from data list
    for event in data:
        if len(event) == 4:

            month = event[2].split("/")
            month = month[0]

            if event_name == event[1]:
                if str(i + 1) == event[0]:
                    if month == str(count):

                        data.remove(event)
    # Updates user.text file
    file = open("user.txt", "w")
    for event in data:
        event = "*".join(event)
        file.write(event)
    file.close()

    # update events dictionary
    for day in range(1, 32):
        events[day] = []
    file = open("user.txt", "r+")
    for line in file:
        data = line.split("*")
        if len(data) == 4:
            data[3] = data[3][:-1]
            day = data[0]

            # Check to see if this is the first event on the selected day
            if events[int(day)] == None:
                events[int(day)] = []
            events[int(day)].append({
                "event_name": data[1],
                "event_date": data[2],
                "event_time": data[3]
            })

    #runs open day function to return to event list
    remove_gui.withdraw()
    open_day(i, count, year)

def open_actions(event_name, event_date, event_time, events_day, events, i, count, year):
    ''' when user selects event, open_actions opens window allowing user to choose between editing or removing the event'''
    day_gui.withdraw()
    global action_gui
    action_gui = Toplevel()
    action_gui.config(background="sky blue")
    
    #makes a label of what event the user has chosen
    Label(
        action_gui,
        text=('you have chosen {}'.format(event_name)),bg='sky blue',font=('times', 20)).pack()
    #creates edit and remove buttons for event above

    Button(
        action_gui,
        width="40",
        height="3",
        text=("Click to edit".format(event_name)),
        bg="lemon chiffon",
        font=("times", 20),
        command=
        lambda: edit_event(event_name, event_date, event_time, events, events_day, i, count, year)
    ).pack()
    Button(
        action_gui,
        width="40",
        height="3",
        text=("Click to remove {} from your planner".format(event_name)),
        bg="lemon chiffon",
        font=("times", 20),
        command=
        lambda: remove_event(event_name, events_day, events, i, count, year)
    ).pack()


def showCal():
    '''# generates and displays calendar'''
    #sets variable that counts how many times calendar has been opened
    num_opens = 1
    # hides year input window
    gui.withdraw()
    
    # Create a new GUI window
    global new_gui
    
    new_gui = Tk()

    # Set the background colour of GUI window
    new_gui.config(background="white")

    # set the name of tkinter GUI window
    new_gui.title("CALENDER")
    
    # generates table of months with each month as a button
    global count
    count = -1
    for r in range(3):
        for c in range(4):
            count += 1
            Button(
                new_gui,
                width="20",
                height="3",
                text='%s' % (months[count]),
                bg="sky blue",
                command=lambda count=count: open_month(count + 1),
                borderwidth=1).grid(
                    row=r, column=c)
    Button(
        new_gui,
        text="Go back",
        bg="lemon chiffon",
        command=lambda: start_Cal(num_opens)).grid(
            row=4, column=2)


# creates list of months for display
months = [
    "January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December"
]


def open_month(count):
    ''' open function defines what happens when month button is clicked'''
    # closes month table and creates new gui
    new_gui.withdraw()
    global month_gui
    month_gui = Tk()
    month_gui['background'] = 'sky blue'

    # takes input for year and month
    global year
    year = int(year_field.get())
    month = count
    month_name = calendar.month_name[month]

    # this will create a label widget
    l1 = Label(
        month_gui, text=month_name, bg='sky blue', font=('times', 20)).grid(
            row=1, column=1)

    month_back_b = Button(
        month_gui,
        text="Go back",
        bg="lemon chiffon",
        font=("times"),
        command=lambda count=count: month_back(count))
    month_back_b.grid(row=1, column=6)

    # calculates how many days in month and what day month starts on
    day = calendar.monthrange(year, month)

    # generates monthly calendar with each date as a button
    spot = day[0]
    row_num = 2
    global i
    for i in range(day[1]):
        # when button is clicked, open_day function is called. i, count and year are passed in.
        b1 = Button(
            month_gui,
            text=i + 1,
            bg='lemon chiffon',
            command=lambda i=i: open_day(i, count, year))
        b1.grid(row=row_num, column=spot)
        if spot == 6:
            row_num += 1
            spot = -1
        spot += 1

def month_back(count):
    ''' takes user back to screen showing all months'''
    month_gui.withdraw()
    showCal()

def open_day(i, count, year):
    '''displays events for the day selected'''
    # first 2 parameters taken in are renamed to day and month for clarity
    days = i + 1
    month = count
    #num_events counts number of events in events_day
    num_events = 0
    # month gui is closed
    month_gui.withdraw()
    # new gui is created
    global day_gui
    day_gui = Toplevel()
    day_gui.title("What you have scheduled.")
    day_gui['background'] = 'sky blue'
    r = 2

    # events_day is the dictionary of events in the day clicked
    # Grab events associated with selected day of month
    global events_day
    events_day = events[days]
    
    #sets count for number of times for loop has been run
    num_runs = 0
    for event in events_day:
        #looks at each event in events_day dictionary
        r += 1
        global event_date
        event_date = event["event_date"]
        event_date_spc = event_date.split("/")
        # splits event_date value by / and removes any leading 0s
        event_date_spc[0] = event_date_spc[0].lstrip("0")
        event_date_spc[1] = event_date_spc[1].lstrip("0")
        
        # compares clicked on button info with date info in event_date_spc. Displays events if they are the same
        if int(event_date_spc[0]) == month and int(event_date_spc[2]) == year:
          # num_events is incremented as events are displayed on the selected day
            num_events += 1
            event_name = event["event_name"]
            event_time = event["event_time"]
            # checks to make sure events are only displayed once
            if num_runs == 0:
                event_brief_label = ("Events scheduled for {}/{}/{}".format(month, days,year))
                Label(
                    day_gui,
                    text=event_brief_label,
                    bg='sky blue',
                    font=('times', 16)).pack()
                
                open_day_back = Button(
                    day_gui,
                    text="Go back",
                    bg="lemon chiffon",
                    font=("times"),
                    command=lambda: day_back(count)).pack(side=BOTTOM)
                
                add_button = Button(
                    day_gui,
                    width="20",
                    height="3",
                    text='Add an event',
                    bg='lemon chiffon',
                    font=('times', 16),
                    command=lambda: add_event(events, i, count, year)).pack(
                        side=BOTTOM)
                
                num_runs += 1

            event_button = Button(day_gui, width = "20", height = "3",text = "{} {}".format(event_name, event_time), bg = 'pink', font = ('times', 16), command = lambda event_name = event_name, event_date = event_date, event_time = event_time : open_actions(event_name, event_date, event_time, events_day, events, i, count, year)).pack()
    
    # if num_events == 0, there are no events on the selected day        
    if num_events == 0:
      Label(
          day_gui,
          text="No events scheduled for this day.",
          bg='sky blue',
          font=('times', 16)).pack()

        #creates an add button that calls add_event
      add_button = Button(
          day_gui,
          width="20",
          height="3",
          text='Add an event',
          bg='lemon chiffon',
          font=('times', 16),
          command=lambda: add_event(events, i, count, year)).pack()
      open_day_back = Button(
          day_gui,
          text="Go back",
          bg="lemon chiffon",
          font=("times"),
          command=lambda: day_back(count)).pack(side=BOTTOM)

def day_back(count):
    '''# takes user back to month display for month selected'''
    day_gui.withdraw()
    open_month(count)


def start_Cal(num_opens):
    '''Create a GUI window, displays original window allowing user to input year'''
    # allows month display to be withdrawn if using back button to change the year
    if num_opens > 0:
        new_gui.withdraw()
    global gui
    
# ------- START ATTRIBUTED CODE SECTION -------
# Code created with the help of GeeksforGeeks
# https://www.geeksforgeeks.org/python-gui-calendar-using-tkinter/
    gui = Tk()

    # Set the background colour of GUI window
    gui.config(background="white")

    # set the name of tkinter GUI window
    gui.geometry("600x600")

    # Create a CALENDAR : label with specified font and size
    cal = Label(gui, text="CALENDAR", bg="white", font=("times", 28))
    cal.place(relx=0.5, rely=0.5)

    # Create a Enter Year : label
    year = Label(gui, text="Enter Year: ", bg="sky blue", font=('times', 12))
    year.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Create a text entry box for filling or typing the information.
    global year_field
    year_field = Entry(gui)

    # Create a Show Calendar Button and attached to showCal function
    Show = Button(
        gui,
        text="Show Calendar",
        fg="Black",
        bg="lemon chiffon",
        font=('times', 12),
        command=showCal)

    # Create a Exit Button and attached to exit function
    Exit = Button(
        gui,
        text="Exit",
        fg="Black",
        bg="lemon chiffon",
        font=('times', 12),
        command=exit)

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure.
    cal.grid(row=1, column=2)

    year.grid(row=2, column=2)

    year_field.grid(row=3, column=2)

    Show.grid(row=4, column=2)

    Exit.grid(row=6, column=2)
# --------- END ATTRIBUTED CODE SECTION ---------

    # num_opens is incremented everytime original gui is opened
    num_opens += 1

# starts calendar with num_opens equaled to 0
start_Cal(0)

# start the GUI
gui.mainloop()

'''References: 
https://www.geeksforgeeks.org/python-gui-calendar-using-tkinter/
https://effbot.org/tkinterbook/grid.htm, 
https://stackoverflow.com/questions/55985356/switch-between-multiple-windows-in-tkinter, 
https://www.geeksforgeeks.org/python-grid-method-in-tkinter/,
https://www.tutorialspoint.com/destroy-method-in-tkinter-python, 
https://www.tutorialspoint.com/python/tk_pack.htm,
https://stackoverflow.com/questions/20125967/how-to-set-default-text-for-a-tkinter-entry-widget
https://www.youtube.com/watch?v=qC3FYdpJI5Y
https://www.youtube.com/watch?v=CKeFRDXYwcA
Jordan's suggested reorg
  num_events = 0
  for each event:
    if (event month matches current month):
    print event info
      num_events += 1
  if (num_events == 0):
    print "No events"'''

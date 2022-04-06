from tkinter import *
from tkinter import messagebox

TOMATO = '#FF6347'

class App:
    def __init__(self, parent, state=True):
        self.parent = parent
        self.name, self.age, self.phone = StringVar(), StringVar(), BooleanVar()
        self.state = state   # TRUE means collecting data STATE. FALSE means displaying data.
        self.people = People_Manager()
        self.index = 0
        
        self.widgets()
    
    def widgets(self):
        paddings = {'padx':5, 'pady':5}
        self.super_frame = Frame()
        self.super_frame.pack(expand=TRUE)
        
        title_frame = Frame(self.super_frame, bg=TOMATO)
        self.title_label = Label(title_frame, text="", bg=TOMATO)
        self.title_button = Button(title_frame, text="", command=lambda: self.state_changer())
        
        self.title_label.grid(column=0, padx=20, pady=20)
        self.title_button.grid(row=0, column=1, padx=20, pady=20)
        title_frame.grid(row=0, column=0, columnspan=2)
        
        context_frame = Frame(self.super_frame)
        Label(context_frame, text="Name:").grid()
        Label(context_frame, text="Age:").grid()
        Label(context_frame, text="Phone:").grid()
        context_frame.grid(row=1, column=0, padx=10, pady=20)
        
        self.entry_display_frame = Frame(self.super_frame)
        # entry_display_frame's children is managed by the state_manager function
        self.entry_display_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=20)
        
        self.controls_frame = Frame(self.super_frame)
        # children also controled by state_manager function
        self.controls_frame.grid(row=2, column=0, columnspan=2)
    
        self.state_manager()
    
    def state_changer(self):
        if self.state == True:
            self.state = not self.state
            self.state_manager()
        elif self.state == False:
            self.state = not self.state
            self.state_manager()
    
    def state_manager(self):
        if self.state == True:
            
            self.title_label['text'] = 'Collecting data'
            self.title_button['text'] = 'Show people data'
            
            try:
                self.people.call_person(0)
            except:
                self.title_button['state'] = DISABLED
        
            for child in self.entry_display_frame.winfo_children():
                child.destroy() # remove all children
            
            self.name_entry = Entry(self.entry_display_frame, textvariable=self.name)
            self.age_entry = Entry(self.entry_display_frame, textvariable=self.age)
            
            self.name.trace("w", lambda name, index, mode, sv=self.name: self.string_checker()) # allows us to "disallow" certain characters
            self.age.trace("w", lambda name, index, mode, sv=self.age: self.num_checker())
            
            self.name_entry.grid(columnspan=2)
            self.age_entry.grid(columnspan=2)
            
            Radiobutton(self.entry_display_frame, var=self.phone, value=True, text="Yes").grid(row=2, column=0)
            Radiobutton(self.entry_display_frame, var=self.phone, value=False, text="No").grid(row=2, column=1)
            
            for child in self.controls_frame.winfo_children():
                child.destroy()
            
            Button(self.controls_frame, text="Add person", command=lambda: self.add_person()).grid()
        
        elif self.state == False:
            
            self.title_label['text'] = 'Showing data'
            self.title_button['text'] = 'Collect data'
            
            for child in self.entry_display_frame.winfo_children():
                child.destroy()
            
            name, age, phone = self.people.call_person(self.index)[1][0:3]
            Label(self.entry_display_frame, text=f'{name}').grid()
            Label(self.entry_display_frame, text=f'{age}').grid()
            Label(self.entry_display_frame, text=f'{phone}').grid()
            
            for child in self.controls_frame.winfo_children():
                child.destroy()
            
            self.previous_button = Button(self.controls_frame, text="Previous", command=lambda: self.change_person(False))
            self.next_button = Button(self.controls_frame, text="Next", command=lambda: self.change_person(True))
            
            self.previous_button.pack(side=LEFT)
            self.next_button.pack(side=RIGHT)
            
            self.change_person(2)
    
    def string_checker(self):
        if any(c.isdigit() for c in self.name.get()):
            self.name_entry.delete((len(self.name.get())-1),END)
    
    def num_checker(self):
        if any(c.isalpha() for c in self.age.get()) or any(not c.isalnum() for c in self.age.get()) or len(self.age.get().strip()) > 3:
            self.age_entry.delete((len(self.age.get())-1),END)
            
    def add_person(self):
        if len(self.name.get().strip()) == 0 or len(self.age.get()) == 0:
            self.error("Name or age has been left blank!")
        else:
            self.people.add_person(self.name.get().strip(), self.age.get(), self.phone.get())
            self.age_entry.delete(0,END)
            self.name_entry.delete(0,END)
            self.title_button['state'] = NORMAL
        
    def change_person(self, command):
        if self.index == (self.people.call_person(0)[0])-1:
            self.next_button['state'] = DISABLED
        if self.index <= 0:
            self.previous_button['state'] = DISABLED
        if command == True:
            self.index += 1
            self.state_manager()
        elif command == False:
            self.index -= 1
            self.state_manager()
        
        
    def error(self, message):
        messagebox.showerror(title='Error', message=message)
    
class People_Manager():
    def __init__(self):
        self.people = []
    
    def add_person(self, name, age, phone):
        if phone == True:
            phone = "Has a phone"
        else:
            phone = "No phone"
        self.people.append((name, age, phone))
    
    def call_person(self, num):
        return len(self.people), self.people[num]   # returns the number of people and a person's data

if __name__ == '__main__':
    root = Tk()
    App(root)
    root.title("Collecting Data")
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()
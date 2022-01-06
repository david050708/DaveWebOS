from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter.scrolledtext import ScrolledText
import datetime as dt
from time import strftime
import pytz
import subprocess
import tkinterweb as tw
from tkinter import *
import tkinter.ttk as ttk
import os
import shutil
from functools import partial
import tkinter.ttk as ttk
import datetime as dt
from tkinter import simpledialog
from functools import partial
import datetime
import time

def file_explorer():
    dir = askdirectory()

    #Creating window
    root = Tk()
    root.title("File manager")
    root.configure(background = "white")
    root.geometry("950x500")
    root.resizable(0,0)

    #Folder and File images
    folder_icon_png = PhotoImage(master=root, file =r"iconfinder_folder_299060.png")

    file_icon_png = PhotoImage(master=root, file =r"iconfinder_File_104851.png")
    python_icon_png= PhotoImage(master=root, file= r"python_file.png")

    #file and folder frame images
    folder_icon_for_display= folder_icon_png.subsample(5,5)
    file_icon_for_display= file_icon_png.subsample(5,5)
    python_icon_for_display= python_icon_png.subsample(5,5)

    #actions in the dropdown menu
    actions= [
        "go in",
        "pick file to move",
        "copy",
        "delete",
        "rename",
        ]

    global action
    action= StringVar()
    action.set(actions[0])

    #variable for file to move
    file_to_move= None

    file_to_copy= None


    #adding files
    def add_files_to_frame(scrollable_frame,current_dir,button_action):
        global files
        files = os.listdir(current_dir)


        column= 0
        row= 1


        btn= []

        for i in range(len(files)):
            if ".DS_Store" in files:
                files.pop(files.index(".DS_Store"))
            if ".vscode" in files:
                files.pop(files.index(".vscode"))

        #backward button
        global backward_button
        backward_button = Button(scrollable_frame, text= "<", padx= 10, command= lambda: go_back(current_dir))
        backward_button.grid(column= 0, row= 0)

        #menu to decide action
        global drop
        drop= OptionMenu(scrollable_frame, action, *actions)
        drop.grid_propagate(0)
        drop.grid(column= 1, row= 0, columnspan= 3, padx=80)

        #here button to move file to that directory/folder
        global here_button
        here_button= Button(
        scrollable_frame, 
        text= "move file here",
        state= DISABLED,
        command= move_file
        )

        #paste button
        global paste
        paste= Button(
            scrollable_frame,
            text= "paste here",
            state= DISABLED,
            command=paste_file
            
        )

        #add button
        global plus
        plus= Button(
            scrollable_frame,
            text= "+",
            padx= 10,
            command= adding
        )
        plus.grid(row=0, column= 4)


        #adds files to frame 
        for i in range(len(files)):
            fullname = os.path.join(current_dir, files[i])

            #checks if the file is a folder
            if os.path.isdir(fullname) == True:
                button= Button(
                    scrollable_frame,
                    text= str(files[i]),
                    image= folder_icon_for_display,
                    pady=10,
                    padx= 10,
                    compound = TOP,
                    wraplength= 120,
                    command= lambda c=i: button_action(current_dir, btn[c].cget("text"))
                )
                btn.append(button)
                button.grid(column= column, row =row)
                column += 1
                if column >= 5:
                    column= 0
                    row+= 1
            #check if the file is not a folder
            else:
                if str(files[i]).endswith(".py"):
                    button= Button(
                        scrollable_frame,
                        text= str(files[i]),
                        image= python_icon_for_display,
                        padx= 10,
                        pady= 10,
                        wraplength= 100,
                        compound = TOP,
                        command= lambda c=i: button_action(current_dir, btn[c].cget("text"))
                    )
                    button.grid(column= column, row= row)
                    btn.append(button)
                    column+=1
                    if column >= 5:
                        column= 0
                        row += 1
                else:
                    button= Button(
                        scrollable_frame,
                        text= str(files[i]),
                        image= file_icon_for_display,
                        padx= 10,
                        pady= 10,
                        wraplength= 120,
                        compound = TOP,
                        command= lambda c=i: button_action(current_dir, btn[c].cget("text"))
                    )
                    btn.append(button)
                    button.grid(column= column, row= row)
                    column +=1 
                    if column >= 5:
                        column= 0
                        row += 1


    #changing directories
    def button_action(current_dir, name):
        global state
        global old_dir
        global new_dir_path
        global file_to_move
        global file_to_copy

        state = action.get()

        if state == "go in":
            #writes the new directory and changes the current working directory
            new_dir_path= os.path.join(current_dir, name)

            if os.path.isdir(new_dir_path):
                os.chdir(new_dir_path)
                new_dir = os.getcwd()

                #destroys all the frames and packs them with new files
                container.destroy()
                tree_frame.destroy()
                creating_frame(new_dir)
                create_tree_frame()
                add_files_to_tree("", new_dir)
            else:
                if name.endswith(".txt"):
                    pass
                
                else:
                    subprocess.call(("open", new_dir_path))

            if file_to_move is not None:
                #enabling here button
                here_button.configure(state= NORMAL)
                here_button.grid(row= 0, column= 4)
                plus.grid_forget()
            
            if file_to_copy is not None:
                #enabling paste button
                paste.configure(state= NORMAL)
                paste.grid(row= 0, column= 4)
                plus.grid_forget()

        if state == "pick file to move":
            #file to move
            file_to_move= os.path.join(current_dir, name)

            #deleting the copy file so no overlap happens
            file_to_copy= None

            #going back to go in mode
            action.set(actions[0])

            #enabling here button
            here_button.configure(state= NORMAL)
            here_button.grid(row= 0, column= 4)

            #deleting paste button
            paste.grid_forget()
            plus.grid_forget()
        
        if state == "copy":

            #copied file
            file_to_copy= os.path.join(current_dir, name)

            #deleting moving file to avoid overlap
            file_to_move= None

            #going back to go in mode
            action.set(actions[0])

            #enabling paste button
            paste.configure(state= NORMAL)
            paste.grid(row=0, column= 4)

            #deleting here button
            here_button.grid_forget()
            plus.grid_forget()
        
        if state == "delete":
            #file to delete
            file_to_delete= os.path.join(current_dir, name)

            action.set(actions[0])
            shutil.move(file_to_delete, "/usercode/Bin")

            button_action(current_dir, "")
        
        if state == "rename":
            renaming(name)



    #function to move a file to a new place
    def move_file():
        global file_to_move
        print(file_to_move)

        working_dir = os.getcwd()

        if file_to_move == working_dir:
            #creates a warning window
            error = Toplevel()
            error.title("Same directory")
            error.geometry("150x150")
            error.propagate(0)
            error.resizable(0,0)

            #a canvas to set a red color to the window
            error_canvas = Frame(
                error, 
                width= 200, 
                height= 200, 
                bg= "red"
                )
            error_canvas.pack_propagate(0)
            error_canvas.pack()

            #warning sign
            warning_sign= Label(
                error_canvas,
                text= "WARNING",
                bg= "red"
            )
            warning_sign.pack()

            #message with the problem
            label_message= Label(
                error_canvas, 
                text= "You can\'t put the \nselected file here",
                bg= "red"
                )
            label_message.pack()
        else:
            try:
                #move file into new dir
                shutil.move(file_to_move, os.getcwd())

                file_to_move = None

                #updates the frame
                button_action(working_dir, "")

            except Exception:
                #creates a warning window
                error = Toplevel()
                error.title("Same directory")
                error.geometry("150x150")
                error.propagate(0)
                error.resizable(0,0)

                #a canvas to set a red color to the window
                error_canvas = Frame(
                    error, 
                    width= 200, 
                    height= 200, 
                    bg= "red"
                    )
                error_canvas.pack_propagate(0)
                error_canvas.pack()

                #warning sign
                warning_sign= Label(
                    error_canvas,
                    text= "WARNING",
                    bg= "red"
                )
                warning_sign.pack()

                #message with the problem
                label_message= Label(
                    error_canvas, 
                    text= "You can\'t put the \nselected file here",
                    bg= "red"
                    )
                label_message.pack()
    #pasting file
    def paste_file():
        global file_to_copy

        #pastes the copied file into the current working dir
        shutil.copy(file_to_copy, os.getcwd())

        #deletes the old copied file
        file_to_copy= None
        
        #updates the frame
        button_action(os.getcwd(), "")

    #renaming a file
    def renaming(name):

        old_name= name

        root.title("Changing the name of the file: {}".format(name))

        #ungriding all top buttons
        drop.grid_forget()
        backward_button.grid_forget()
        here_button.grid_forget()
        paste.grid_forget()

        #adding entry box
        entry= Entry(scrollable_frame)
        entry.grid(row=0, column= 0, columnspan= 2)

        #adding confirm and cancel buttons
        confirm= Button(
            scrollable_frame,
            text= "confirm",
            padx= 10,
            command= lambda: rename(old_name,entry.get())
        )

        root.bind(
            "<Return>",
            (lambda event: rename(old_name,entry.get()))
            )

        confirm.grid(row=0, column= 2)


        cancel= Button(
            scrollable_frame,
            text= "cancel",
            padx= 10,
            command= canceling
        )
        cancel.grid(row=0, column= 3)

    def rename(old_name,new_name):
        #changes the name of the file
        os.rename(old_name, new_name)

        #reloads the page
        action.set(actions[0])
        creating_frame(os.getcwd())
        create_tree_frame()
        add_files_to_tree("", os.getcwd())



    def canceling():
        root.title("File manager")
        action.set(actions[0])
        creating_frame(os.getcwd())
        create_tree_frame()
        add_files_to_tree("", os.getcwd())

    #adding files
    def adding():
        pass

    #going back
    def go_back(current_dir):
        #separates the current directory per word and takes the last directory off the path
        old_dir_split = current_dir.split("/")
        old_dir_split.pop()

        #Joins the dir which is the same as the directory before the current one
        new_dir= "/".join(old_dir_split)

        #changes the directory 
        os.chdir(new_dir)

        #destroys the current frames and creates new frames with the files of the new directory
        container.destroy()
        tree_frame.destroy()
        creating_frame(new_dir)
        create_tree_frame()
        add_files_to_tree("", new_dir)

        #Checks if there is a current file it can move
        if file_to_move is not None:
            #enabling here button
            here_button.configure(state= NORMAL)
            here_button.grid(row= 0, column= 4)
            plus.grid_forget()
        
        if file_to_copy is not None:
            paste.configure(state= NORMAL)
            paste.grid(row=0, column= 4)
            plus.grid_forget()


    #creating frame
    def creating_frame(current_dir):
        global row
        global column

        #Frame for files
        global container
        container=Frame(root,width=750,height=500,bd=1, bg= "white")
        container.grid(row=0, column= 2)
        container.grid_propagate(0)

        #scrollable frame for file display
        global scrollable_frame
        canvas=Canvas(container, width= 720, height= 500, bg= "white")
        scrollable_frame=Frame(canvas, bg= "white")
        myscrollbar=Scrollbar(container,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="right",fill="y")
        canvas.pack(side="left", fill= "both")
        canvas.create_window((0,0),window=scrollable_frame,anchor='nw')
        canvas.pack_propagate(0)
        scrollable_frame.bind(
            "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
            )
        )

        add_files_to_frame(scrollable_frame, current_dir, button_action)

    creating_frame(dir)

    #tree view images
    folder_icon_for_tree= folder_icon_png.subsample(30,30)
    file_icon_for_tree= file_icon_png.subsample(30,30)
    python_icon_for_tree= python_icon_png.subsample(25,25)

    def create_tree_frame():
            #Frame for tree view
        global tree_frame
        tree_frame = Frame(root, bg = "grey", width = 200, height = 500)
        tree_frame.grid(row = 0, column =1)
        tree_frame.grid_propagate(0)

        #scrollable frame for tree files
        tree_canvas = Canvas(tree_frame, width= 187, height= 500, bg= "grey")
        scrollable_treeframe= Frame(tree_canvas, bg= "grey")
        tree_scrollbar= Scrollbar(tree_frame, orient="vertical", command= tree_canvas.yview)
        horizontal_tree_scrollbar= Scrollbar(tree_frame, orient= "horizontal", command= tree_canvas.xview)
        tree_canvas.configure(yscrollcommand= tree_scrollbar.set) #xscrollcommand= horizontal_tree_scrollbar.set

        tree_scrollbar.pack(side="right", fill= "y")
        #horizontal_tree_scrollbar.pack(side= "bottom", fill= "x")
        tree_canvas.pack(side="left", fill= "both")
        tree_canvas.create_window((0,0), window= scrollable_treeframe, anchor= "nw")
        scrollable_treeframe.bind(
            "<Configure>",
            lambda e: tree_canvas.configure(
                scrollregion=tree_canvas.bbox("all")    
            )    
        )
        global tree
        tree = ttk.Treeview(scrollable_treeframe, height= 100)

        tree.column("#0", minwidth= 190, stretch= FALSE)
        tree.heading("#0", text= "Files in current folder", anchor= W)

    create_tree_frame()

    #adding files to the tree frame
    def add_files_to_tree(parent,current_dir):
        #getting current dir
        files = os.listdir(current_dir)

        tree_item= []

        for i in range(len(files)):
            if ".DS_Store" in files:
                files.pop(files.index(".DS_Store"))
            if ".vscode" in files:
                files.pop(files.index(".vscode"))
        index = 1
        #adding the files in the view
        for i in range(len(files)):
            fullname = os.path.join(current_dir, files[i])
            if os.path.isdir(fullname) == True:
                folder = tree.insert(
                    parent, 
                    index, 
                    text= str(files[i]), 
                    image= folder_icon_for_tree
                    )
                tree_item.append(folder)

                add_files_to_tree(folder, fullname)
                index += 1
            else:
                if str(files[i]).endswith(".py"):
                    file = tree.insert(
                        parent, 
                        index,  
                        text= str(files[i]), 
                        image= python_icon_for_tree
                        )
                    tree_item.append(file)
                    index+= 1
                else:
                    file = tree.insert(
                        parent, 
                        index,  
                        text= str(files[i]), 
                        image= file_icon_for_tree
                        )
                    tree_item.append(file)
                    index+= 1
        tree.pack(side= TOP, fill= X)


    add_files_to_tree("",dir)






    #runs the window
    root.mainloop()

oswindows = Tk()
oswindows.attributes("-fullscreen", True)
oswindows.title("DaveWebOS")

def notepad():
    app = Tk()
    app.title("DaveWebOS Text Editor")
    app.geometry("300x300")

    editor = ScrolledText(app, fg="#232323", bg="white")
    editor.pack(fill=BOTH, expand=1)
    editor.focus()

    file_path = ""

    def new():
        editor.delete(1.0, END)
    
    def open_file(event=None):
        global text, file_path
        open_path = askopenfilename(filetypes=[("Text Files", "*.txt")])
        file_path = open_path

        with open(open_path, "r") as file:
            text = file.read()
            editor.delete(1.0, END)
            editor.insert(1.0, text)
    app.bind("<Control-o>", open_file)

    def save_file(event=None):
        global text, file_path
        if file_path == '':
            save_path = asksaveasfilename(defaultextension = "*.txt", filetypes=[("Text Files", "*.txt")])
            file_path = save_path
        
        else:
            save_path = file_path
        with open(save_path, "w") as file:
            text = editor.get(1.0, END)
            file.write(text)
    app.bind("<Control-s>", save_file)

    menu = Menu(app)

    file_menu = Menu(menu, tearoff=0)
    new_menu = Menu(menu, tearoff=0)

    menu.add_cascade(label="File", menu=file_menu)
    menu.add_cascade(label="New", menu=new_menu)

    file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)

    new_menu.add_command(label="New", command=new)

    app.config(menu=menu)

    app.mainloop()

def clock():
    root = Tk()
    root.title('Clock')
    
    # This function is used to
    # display time on the label
    def time():
        string = dt.datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S %p")
        lbl.config(text = string)
        lbl.after(1000, time)
    
    # Styling the label widget so that clock
    # will look more attractive
    lbl = Label(root, font = ('calibri', 40, 'bold'),
                background = '#232323',
                foreground = 'white')
    
    # Placing clock at the centre
    # of the tkinter window
    lbl.pack()
    time()
    
    root.mainloop()

def powerpoint():
    brows = Tk()
    brows.title("PowerPoint")
    website = tw.HtmlFrame(brows)
    website.load_website("https://slidebean.com/")
    website.pack(fill="both", expand=1)
    brows.mainloop()

def browser():
    brows = Tk()
    brows.title("InterSurfer")
    website = tw.HtmlFrame(brows)
    website.load_website("www.google.com")
    website.pack(fill="both", expand=1)
    brows.mainloop()

def builtinide():
    window = Tk()
    # set title for window
    window.title("Visual IDE")
    window.attributes('-alpha',0.97)
    # create and configure menu
    menu = Menu(window)
    window.config(menu=menu)
    # create editor window for writing code 
    editor = ScrolledText(window, font=("Consolas 14 bold"), wrap=None)
    editor.pack(fill=BOTH, expand=1)
    editor.focus()
    file_path = ""
    # function to open files
    def open_file(event=None):
        global code, file_path
        #code = editor.get(1.0, END)
        open_path = askopenfilename(filetypes=[("Python File", "*.py"), ("HTML File", "*.html"), ("CSS File", "*.css"), ("Ruby File", "*.rb")])
        file_path = open_path
        with open(open_path, "r") as file:
            code = file.read()
            editor.delete(1.0, END)
            editor.insert(1.0, code)
    window.bind("<Control-o>", open_file)
    # function to save files
    def save_file(event=None):
        global code, file_path
        if file_path == '':
            save_path = asksaveasfilename(defaultextension = ".py", filetypes=[("Python File", "*.py"), ("HTML File", "*.html"), ("CSS File", "*.css"), ("Ruby File", "*.rb")])
            file_path =save_path
        else:
            save_path = file_path
        with open(save_path, "w") as file:
            code = editor.get(1.0, END)
            file.write(code) 
    window.bind("<Control-s>", save_file)
    # function to save files as specific name 
    def save_as(event=None):
        global code, file_path
        #code = editor.get(1.0, END)
        save_path = asksaveasfilename(defaultextension = ".py", filetypes=[("Python File", "*.py"), ("HTML File", "*.html"), ("CSS File", "*.css"), ("Ruby File", "*.rb")])
        file_path = save_path
        with open(save_path, "w") as file:
            code = editor.get(1.0, END)
            file.write(code) 
    window.bind("<Control-S>", save_as)
    # function to execute the code and
    # display its output
    def run(event=None):
        global code, file_path
        '''
        code = editor.get(1.0, END)
        exec(code)
        '''    
        cmd = f"python {file_path}"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        output, error =  process.communicate()
        # delete the previous text from
        # output_windows
        output_window.delete(1.0, END)
        # insert the new output text in
        # output_windows
        output_window.insert(1.0, output)
        # insert the error text in output_windows
        # if there is error
        output_window.insert(1.0, error)
    window.bind("<F5>", run)
    # function to close IDE window
    def close(event=None):
        window.destroy()
    window.bind("<Control-q>", close)
    # define function to cut 
    # the selected text
    def cut_text(event=None):
            editor.event_generate(("<<Cut>>"))
    # define function to copy 
    # the selected text
    def copy_text(event=None):
            editor.event_generate(("<<Copy>>"))
    # define function to paste 
    # the previously copied text
    def paste_text(event=None):
            editor.event_generate(("<<Paste>>"))
    # create menus
    file_menu = Menu(menu, tearoff=0)
    edit_menu = Menu(menu, tearoff=0)
    run_menu = Menu(menu, tearoff=0)
    view_menu = Menu(menu, tearoff=0)
    # add menu labels
    menu.add_cascade(label="File", menu=file_menu)
    menu.add_cascade(label="Edit", menu=edit_menu)
    menu.add_cascade(label="Run", menu=run_menu)
    menu.add_cascade(label ="View", menu=view_menu)
    # add commands in flie menu
    file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
    file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=save_as)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=close)
    # add commands in edit menu
    edit_menu.add_command(label="Cut", command=cut_text) 
    edit_menu.add_command(label="Copy", command=copy_text)
    edit_menu.add_command(label="Paste", command=paste_text)
    run_menu.add_command(label="Run", accelerator="F5", command=run)
    # function to display and hide status bar
    show_status_bar = BooleanVar()
    show_status_bar.set(True)
    def hide_statusbar():
        global show_status_bar
        if show_status_bar:
            status_bars.pack_forget()
            show_status_bar = False 
        else :
            status_bars.pack(side=BOTTOM)
            show_status_bar = True
            
    view_menu.add_checkbutton(label = "Status Bar" , onvalue = True, offvalue = 0,variable = show_status_bar , command = hide_statusbar)
    # create a label for status bar
    status_bars = ttk.Label(window,text = "\t\t\tPython\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCharacters: 0 Words: 0\t\t\t", background="blue", foreground="white")
    status_bars.pack(side = BOTTOM)
    # function to display count and word characters
    text_change = False
    def change_word(event = None):
        global text_change
        if editor.edit_modified():
            text_change = True
            word = len(editor.get(1.0, "end-1c").split())
            chararcter = len(editor.get(1.0, "end-1c").replace(" ",""))
            status_bars.config(text = f"\t\t\tPython\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCharacters: {chararcter} Words: {word}\t\t\t", background="blue", foreground="white")
        editor.edit_modified(False)
    editor.bind("<<Modified>>",change_word)
    # create output window to display output of written code
    output_window = ScrolledText(window, height=10)
    output_window.config(fg="white", bg="black")
    output_window.pack(fill=BOTH, expand=1)
    window.mainloop()


def start(event=None):
    global start_bt
    start_bt.pack_forget()
    start_bt.place_forget()

    startwindow = Tk()
    startwindow.geometry("350x450+500+300")
    startwindow.title("Title")
    startwindow.overrideredirect(True)
    bg_colour="#232323"
    startwindow.configure(bg=bg_colour)
    startwindow.attributes("-alpha", 0.97)

    start_bar1 = Frame(startwindow, bg="#232323", relief="flat", bd=0)
    start_bar1.grid(row=0, column=0, columnspan=12, sticky="WE")

    start_label = Label(start_bar1, text="Start\t\t\t"+"                             ", bg="#232323", fg="white")
    start_label.grid(row=0, column=2)

    def builtinide():
        global start_bt
        startwindow.destroy()
        start_bt.pack_forget()
        x = StringVar()
        start_bt = Button(oswindows, text="Start", bg="#232323", fg="white", command=start)
        start_bt.place(x=0, y=710)

        window = Tk()
        # set title for window
        window.title("Visual IDE")
        window.attributes('-alpha',0.97)
        # create and configure menu
        menu = Menu(window)
        window.config(menu=menu)
        # create editor window for writing code 
        editor = ScrolledText(window, font=("Consolas 14 bold"), wrap=None)
        editor.pack(fill=BOTH, expand=1)
        editor.focus()
        file_path = ""
        # function to open files
        def open_file(event=None):
            global code, file_path
            #code = editor.get(1.0, END)
            open_path = askopenfilename(filetypes=[("Python File", "*.py"), ("HTML File", "*.html"), ("CSS File", "*.css"), ("Ruby File", "*.rb")])
            file_path = open_path
            with open(open_path, "r") as file:
                code = file.read()
                editor.delete(1.0, END)
                editor.insert(1.0, code)
        window.bind("<Control-o>", open_file)
        # function to save files
        def save_file(event=None):
            global code, file_path
            if file_path == '':
                save_path = asksaveasfilename(defaultextension = ".py", filetypes=[("Python File", "*.py"), ("HTML File", "*.html"), ("CSS File", "*.css"), ("Ruby File", "*.rb")])
                file_path =save_path
            else:
                save_path = file_path
            with open(save_path, "w") as file:
                code = editor.get(1.0, END)
                file.write(code) 
        window.bind("<Control-s>", save_file)
        # function to save files as specific name 
        def save_as(event=None):
            global code, file_path
            #code = editor.get(1.0, END)
            save_path = asksaveasfilename(defaultextension = ".py", filetypes=[("Python File", "*.py"), ("HTML File", "*.html"), ("CSS File", "*.css"), ("Ruby File", "*.rb")])
            file_path = save_path
            with open(save_path, "w") as file:
                code = editor.get(1.0, END)
                file.write(code) 
        window.bind("<Control-S>", save_as)
        # function to execute the code and
        # display its output
        def run(event=None):
            global code, file_path
            '''
            code = editor.get(1.0, END)
            exec(code)
            '''    
            cmd = f"python {file_path}"
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, shell=True)
            output, error =  process.communicate()
            # delete the previous text from
            # output_windows
            output_window.delete(1.0, END)
            # insert the new output text in
            # output_windows
            output_window.insert(1.0, output)
            # insert the error text in output_windows
            # if there is error
            output_window.insert(1.0, error)
        window.bind("<F5>", run)
        # function to close IDE window
        def close(event=None):
            window.destroy()
        window.bind("<Control-q>", close)
        # define function to cut 
        # the selected text
        def cut_text(event=None):
                editor.event_generate(("<<Cut>>"))
        # define function to copy 
        # the selected text
        def copy_text(event=None):
                editor.event_generate(("<<Copy>>"))
        # define function to paste 
        # the previously copied text
        def paste_text(event=None):
                editor.event_generate(("<<Paste>>"))
        # create menus
        file_menu = Menu(menu, tearoff=0)
        edit_menu = Menu(menu, tearoff=0)
        run_menu = Menu(menu, tearoff=0)
        view_menu = Menu(menu, tearoff=0)
        # add menu labels
        menu.add_cascade(label="File", menu=file_menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        menu.add_cascade(label="Run", menu=run_menu)
        menu.add_cascade(label ="View", menu=view_menu)
        # add commands in flie menu
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=close)
        # add commands in edit menu
        edit_menu.add_command(label="Cut", command=cut_text) 
        edit_menu.add_command(label="Copy", command=copy_text)
        edit_menu.add_command(label="Paste", command=paste_text)
        run_menu.add_command(label="Run", accelerator="F5", command=run)
        # function to display and hide status bar
        show_status_bar = BooleanVar()
        show_status_bar.set(True)
        def hide_statusbar():
            global show_status_bar
            if show_status_bar:
                status_bars.pack_forget()
                show_status_bar = False 
            else :
                status_bars.pack(side=BOTTOM)
                show_status_bar = True
                
        view_menu.add_checkbutton(label = "Status Bar" , onvalue = True, offvalue = 0,variable = show_status_bar , command = hide_statusbar)
        # create a label for status bar
        status_bars = ttk.Label(window,text = "\t\t\tPython\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCharacters: 0 Words: 0\t\t\t", background="blue", foreground="white")
        status_bars.pack(side = BOTTOM)
        # function to display count and word characters
        text_change = False
        def change_word(event = None):
            global text_change
            if editor.edit_modified():
                text_change = True
                word = len(editor.get(1.0, "end-1c").split())
                chararcter = len(editor.get(1.0, "end-1c").replace(" ",""))
                status_bars.config(text = f"\t\t\tPython\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCharacters: {chararcter} Words: {word}\t\t\t", background="blue", foreground="white")
            editor.edit_modified(False)
        editor.bind("<<Modified>>",change_word)
        # create output window to display output of written code
        output_window = ScrolledText(window, height=10)
        output_window.config(fg="white", bg="black")
        output_window.pack(fill=BOTH, expand=1)
        window.mainloop()

    def browser():
        global start_bt
        startwindow.destroy()
        start_bt.pack_forget()
        x = StringVar()
        start_bt = Button(oswindows, text="Start", bg="#232323", fg="white", command=start)
        start_bt.place(x=0, y=710)

        brows = Tk()
        brows.title("InterSurfer")
        website = tw.HtmlFrame(brows)
        website.load_website("www.google.com")
        website.pack(fill="both", expand=1)
        brows.mainloop()

    def clock():
        global start_bt
        startwindow.destroy()
        start_bt.pack_forget()
        x = StringVar()
        start_bt = Button(oswindows, text="Start", bg="#232323", fg="white", command=start)
        start_bt.place(x=0, y=710)

        root = Tk()
        root.title('Clock')
        
        # This function is used to
        # display time on the label
        def time():
            string = dt.datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S %p")
            lbl.config(text = string)
            lbl.after(1000, time)
        
        # Styling the label widget so that clock
        # will look more attractive
        lbl = Label(root, font = ('calibri', 40, 'bold'),
                    background = '#232323',
                    foreground = 'white')
        
        # Placing clock at the centre
        # of the tkinter window
        lbl.pack()
        time()
        
        root.mainloop()

    def terminal():
        global start_bt
        startwindow.destroy()
        start_bt.pack_forget()
        x = StringVar()
        start_bt = Button(oswindows, text="Start", bg="#232323", fg="white", command=start)
        start_bt.place(x=0, y=710)

    #setting up the terminal and root window

        terminal = Tk()
        terminal.title("DaveWebOS Terminal")
        terminal.geometry("500x500")

        terminal_frme = Frame(terminal, bg="#232323")
        terminal_frme.pack(fill=BOTH, expand=YES)
        #this is the terminal code

        def theinputthatisneededtobeasked():
            x = StringVar()
            arrow = Label(terminal, text="->", bg="#232323", fg="white")
            arrow.place(x=0, y=0)
            # the labels
            output = Label(terminal, bg="#232323", fg="white", text="->")
            output.place(x=1, y=0)
            # the input dialog
            while True:
                COMMAND = simpledialog.askstring(title="COMMAND", prompt="->:")
                if 'typevr' in COMMAND:
                    output.config(text="DaveWebOS [Version: 1.1]")
                elif 'exit' in COMMAND:
                    terminal.destroy()
                    COMMAND.destroy()
                elif 'help' in COMMAND:
                    output.config(text="DaveWebOS [Version: 1.1]\nList of commands:\ntypevr == Returns the version of the WebOS\ndevs == Shows the names of developers of DaveWebOS\nexit == Terminal closes\nhelp == Displayes list of commands\ncontact == Displays the mail address to contact DeltaDev\ntitle == Prints out the title of the terminal\ndate == Prints the date and time\necho == prints out second variable of the command\n CLS == Clears the screen\nimage == Coming soon....")
                elif 'devs' in COMMAND:
                    output.config(text="DEVS:\nOnni3000\ndj050708\nraghav\nhat\nphx-ph")
                elif 'contact' in COMMAND:
                    output.config(text="Email: dev.delta.1@gmail.com")
                elif 'tittle' in COMMAND:
                    output.config(text="DaveWebOS Terminal")
                elif 'date' in COMMAND:
                    output.config(text=datetime.datetime.now())
                elif 'echo' in COMMAND:
                    texttobeprinted = COMMAND.replace("echo ", "")
                    output.config(text=texttobeprinted)
                elif 'CLS' in COMMAND:
                    output.config(text="Cleared")
                    time.sleep(1)
                    output.config(text=None)
                else:
                    output.config(text="Unknown Command\nType 'help' to view all the commands")
                
        theinputthatisneededtobeasked()
        terminal.mainloop()

    def notepad():
        global start_bt
        startwindow.destroy()
        start_bt.pack_forget()
        x = StringVar()
        start_bt = Button(oswindows, text="Start", bg="#232323", fg="white", command=start)
        start_bt.place(x=0, y=710)

        app = Tk()
        app.title("DaveWebOS Text Editor")
        app.geometry("300x300")

        editor = ScrolledText(app, fg="#232323", bg="white")
        editor.pack(fill=BOTH, expand=1)
        editor.focus()

        file_path = ''

        def new():
            editor.delete(1.0, END)
        
        def open_file(event=None):
            global text, file_path
            open_path = askopenfilename(filetypes=[("Text Files", "*.txt")])
            file_path = open_path

            with open(open_path, "r") as file:
                text = file.read()
                editor.delete(1.0, END)
                editor.insert(1.0, text)
        app.bind("<Control-o>", open_file)

        def save_file(event=None):
            global text, file_path
            if file_path == '':
                save_path = asksaveasfilename(defaultextension = "*.txt", filetypes=[("Text Files", "*.txt")])
                file_path = save_path
            
            else:
                save_path = file_path
            with open(save_path, "w") as file:
                text = editor.get(1.0, END)
                file.write(text)
        app.bind("<Control-s>", save_file)

        def save_as():
            global code, file_path
            #code = editor.get(1.0, END)
            save_path = asksaveasfilename(defaultextension = ".py", filetypes=[("Python File", "*.py"), ("HTML File", "*.html"), ("CSS File", "*.css"), ("Ruby File", "*.rb")])
            file_path = save_path
            with open(save_path, "w") as file:
                code = editor.get(1.0, END)
                file.write(code) 

        menu = Menu(app)

        file_menu = Menu(menu, tearoff=0)
        new_menu = Menu(menu, tearoff=0)

        menu.add_cascade(label="File", menu=file_menu)
        menu.add_cascade(label="New", menu=new_menu)

        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
        file_menu.add_command(label="Save As", accelerator="Ctrl+S", command=save_as)

        new_menu.add_command(label="New", command=new)

        app.config(menu=menu)

        app.mainloop()

    def dest():
        startwindow.destroy()
        global start_bt
        start_bt.pack_forget()
        x = StringVar()
        start_bt = Button(oswindows, text="Start", bg="#232323", fg="white", command=start)
        start_bt.place(x=0, y=710)

    closebt = Button(start_bar1, text="X", bg="#232323", fg="white", command=dest, relief="groove", width=0)
    closebt.grid(row=0, column=6, sticky="E")

    date_and_time = Label(startwindow, text=f"{dt.datetime.now():%a, %b %d %Y}", fg="white", bg="#232323", font=("helvetica", 12))
    date_and_time.grid(row=2, column=0)

    DaveOSTextEditorbt = Button(startwindow, text="Text Editor", bg="#232323", fg="white", command=notepad)
    DaveOSTextEditorbt.grid(row=11, column=0)

    clockbt = Button(startwindow, text="Clock     ", bg="#232323", fg="white", command=clock)
    clockbt.grid(row=40, column=0)

    browserbt = Button(startwindow, text="InterSurfer", bg="#232323", fg="white", command=browser)
    browserbt.grid(row=69, column=0)

    idebt = Button(startwindow, text="Visual IDE", bg="#232323", fg="white", command=builtinide)
    idebt.grid(row=98, column=0)

    terbt = Button(startwindow, text="Terminal", bg="#232323", fg="white", command=terminal)
    terbt.grid(row=127, column=0)

    startwindow.mainloop()

start_bar = Frame(oswindows, bg="#232323", bd=0)
start_bar.pack(expand=1)

x = StringVar()
start_bt = Button(oswindows, text="Start", bg="#232323", fg="white", command=start)
start_bt.place(x=0, y=710)

builtinidebtimage = PhotoImage(file="IDE.png")
x = StringVar()
builtinidebt = Button(oswindows, image=builtinidebtimage, command=builtinide)
builtinidebt.place(x=50, y=50)
builtinidelabel = Label(oswindows, text="Visual IDE")
builtinidelabel.place(x=52, y=130)

clockbtimage = PhotoImage(file="Clock.png")
x = StringVar()
clockbt = Button(oswindows, image=clockbtimage, command=clock)
clockbt.place(x=200, y=50)
clocklabel = Label(oswindows, text="Clock")
clocklabel.place(x=220, y=130)

browserbtimage = PhotoImage(file="InterSurfer.png")
x = StringVar()
browserbt = Button(oswindows, image=browserbtimage, command=browser)
browserbt.place(x=350, y=50)
browserlabel = Label(oswindows, text="InterSurfer")
browserlabel.place(x=354, y=130)

file_explorerbtimage = PhotoImage(file="File_Explorer.png")
x = StringVar()
file_explorerbt = Button(oswindows, image=file_explorerbtimage, command=file_explorer)
file_explorerbt.place(x=500, y=50)
file_explorerlabel = Label(oswindows, text="File Explorer")
file_explorerlabel.place(x=490, y=130)

powerpointbtimage = PhotoImage(file="Powerpoint.png")
x = StringVar()
powerpointbt = Button(oswindows, image=powerpointbtimage, command=powerpoint)
powerpointbt.place(x=650, y=50)
powerpointlabel = Label(oswindows, text="Powerpoint")
powerpointlabel.place(x=650, y=130)

def shutdown():
    oswindows.destroy()
    exit()
    
def restart():
    pass
    
def sleep():
    pass
    
def logoff():
    pass

menubar = Menu(oswindows)
#adding wifi menu
power_menu = Menu(menubar, tearoff=0)
#adding a place for wifi menu
menubar.add_cascade(label='Power', menu=power_menu)
power_menu.add_command(label ='Shutdown', command = shutdown)
power_menu.add_command(label ='Restart', command = restart)
power_menu.add_command(label ='Sleep', command = sleep)
power_menu.add_command(label ='Log Off', command = logoff)

oswindows.config(menu=menubar)
oswindows.mainloop()

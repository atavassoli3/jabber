import tkinter as tk
import socket 
import select 
import sys 
from _thread import *
import app

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        #username label and text entry box
        usernameLabel = tk.Label(self, text="Username").grid(row=0, column=0)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=username).grid(row=0, column=1)  

        #password label and password entry box
        passwordLabel = tk.Label(self,text="Password").grid(row=1, column=0)  
        password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable=password, show='*').grid(row=1, column=1)

        loginUserButton = tk.Button(self, text ="Login", command = lambda: app.login(username.get(), password.get())).grid(row=4, column=1) 
        createUserButton = tk.Button(self, text ="Create User", command = lambda: app.create(username.get(), password.get())).grid(row=5, column=1) 

# Holds all of the users that are registered 
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="Users (\U00002713 - Online, \U0000274C - Offline)")
        label.pack(side="top")

        users = app.index()
        usersBox = tk.Listbox(self, height=400, width=200)
        count = 0
        for user in users:
            # Check if online
            usersBox.insert(count, "\U0000274C"+user['user'])
        usersBox.pack()

class Page3(Page):
    def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Chat")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Login", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Search", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Chat", command=p3.lift)
        
        #b2["state"] ="disabled"
        #b3["state"] ="disabled"

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()

def connectToServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Gets the hostname of the computer
    hostname = socket.gethostname()
    # Gets the IP address from the hostname
    IP_address = socket.gethostbyname(hostname)
    # Statically set to work on port 8000 
    Port = 8000
    print(hostname, IP_address, Port)
    server.connect((IP_address, Port))
    while True: 
    
        # maintains a list of possible input streams 
        sockets_list = [socket.socket(), server] 

        """ There are two possible input situations. Either the 
        user wants to give manual input to send to other people, 
        or the server is sending a message to be printed on the 
        screen. Select returns from sockets_list, the stream that 
        is reader for input. So for example, if the server wants 
        to send a message, then the if condition will hold true 
        below.If the user wants to send a message, the else 
        condition will evaluate as true"""
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
    
        for socks in read_sockets: 
            if socks == server: 
                message = socks.recv(2048) 
                print(message.decode()) 
            else: 
                message = sys.stdin.readline() 
                server.send(message) 
                sys.stdout.write("<{}}>") 
                sys.stdout.write(message) 
                sys.stdout.flush() 
    server.close() 

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
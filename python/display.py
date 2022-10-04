from tkinter import ttk
from tkinter import *   # Import tkinter
import databaseconn


try:
    with open('../creds.txt', 'r') as r:  # !
        creds = r.readlines()
        username = creds[0].rstrip()
        passw = creds[1].rstrip()
except:
    raise Exception(
        'Please create a creds.txt file with your username on the first line and password on the second line')


def main():
    root = Tk()

    application = Product(root)
    root.mainloop()


class Product:
    def __init__(self, window):
        self.wind = window
        self.wind.title("Client Saver")
        self.wind.geometry("1012x425")
        self.wind.minsize(1012, 425)

        self.db = databaseconn.DatabaseConnection(
            'localhost', username, passw, 'lawyerdb')
        self.db_ = self.db.__enter__()
        self.db_cursor = self.db_.cursor()

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text="Register a new client")
        frame.grid(row=0, column=0, sticky=W,  padx=4, pady=4)

        # Name Input
        Label(frame, text="Name: ").grid(row=0, column=0)
        self.name = Entry(frame)
        self.name.grid(row=0, column=1)

        # Rut Input
        Label(frame, text="Rut: ").grid(row=1, column=0)
        self.rut = Entry(frame)
        self.rut .grid(row=1, column=1, padx=10, pady=5, sticky=W + E)

        # Phone Input
        Label(frame, text="Phone: ").grid(row=2, column=0)
        self.phone = Entry(frame)
        self.phone.grid(row=2, column=1, padx=10, pady=5, sticky=W + E)

        # Email Input
        Label(frame, text="Email: ").grid(row=3, column=0)
        self.email = Entry(frame)
        self.email.grid(row=3, column=1, padx=10, pady=5, sticky=W + E)

        # Button Add Client
        ttk.Button(frame, text="Save client", command=self.send).grid(
            row=4, columnspan=5, sticky=W + E)

        # Table
        self.tree = ttk.Treeview(window, columns=(
            "#0", "#1", "#2", "#3", "#4"), show="headings", height=10)
        self.tree.grid(row=5, column=0, pady=5, padx=5, columnspan=1)
        self.tree.heading("#1", text="id", anchor=CENTER)
        self.tree.heading("#2", text="Name", anchor=CENTER)
        self.tree.heading("#3", text="Rut", anchor=CENTER)
        self.tree.heading("#4", text="Phone", anchor=CENTER)
        self.tree.heading("#5", text="Email", anchor=CENTER)

        self.displayData()

        # Button Delete Client
        ttk.Button(self.wind, text="Delete Client", command=self.delete_client).grid(
            row=6, column=0, columnspan=1, sticky=W + E, padx=5)

    def send(self):
        self.name1 = self.name.get()
        self.rut2 = self.rut.get()
        self.phone3 = self.phone.get()
        self.email4 = self.email.get()
        databaseconn.intro_database(
            self.db_, self.db_cursor, self.name1, self.rut2, self.phone3, self.email4)
        self.tree.delete(*self.tree.get_children())
        self.displayData()

    def delete_client(self):
        databaseconn.delet_client(self.db_, self.db_cursor, self.tree.item(
            self.tree.selection())['values'][5])
        self.tree.item(self.tree.focus())
        self.tree.delete(*self.tree.get_children())
        self.displayData()
        # print(self.wind.winfo_reqwidth())
        # print(self.wind.winfo_reqheight())

    def displayData(self):
        self.db_cursor.execute("SELECT * FROM clientes")
        rows = self.db_cursor.fetchall()
        for n, row in enumerate(rows):
            self.tree.insert("", 0, values=[n] + list(row[1:]) + [row[0]])


# if '__main__' == __name__:
main()

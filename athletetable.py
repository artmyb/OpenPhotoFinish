import tkinter as tk
from tkinter import ttk

class EditableTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editable Table")

        self.tree = ttk.Treeview(root, columns=("lane","id","name","affiliation","license","time","place"), show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("id", text="ID")

        # Add sample data
        self.tree.insert("", "end", values=("John", "25"))
        self.tree.insert("", "end", values=("Alice", "30"))
        self.tree.insert("", "end", values=("Bob", "22"))

        self.tree.pack(padx=10, pady=10)

        # Enable editing
        self.tree.bind("<Double-1>", self.edit_cell)

    def edit_cell(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        col_id = column.split("#")[-1]

        # Check if the clicked cell is editable
        if col_id in ["1", "2"]:
            self.tree.item(item, values=(self.tree.set(item, "Name"), self.tree.set(item, "Age")), tags="editable")
            self.tree.item(item, tags=("editable",))

if __name__ == "__main__":
    root = tk.Tk()
    app = EditableTableApp(root)
    root.mainloop()

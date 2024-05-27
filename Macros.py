import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
import pyautogui
import time
import json
import threading
import keyboard

class InputSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Input Simulator (Macros)")
        self.commands = []
        self.running = False
        self.looping = False
        self.integer_variables = {}  # Initialize integer variables dictionary
        self.loop_start_index = 0  # Initialize loop start index
        self.available_commands = [
            "moveTo", "click", "type", "press", "hotkey", "scroll", 
            "loop", "loop_start_point", "delay", 
            "create_int", "get_int", "inc_int", "dec_int"
        ]
        self.create_widgets()
        self.update_mouse_position()
    
    def create_widgets(self):
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Add labels to display mouse coordinates
        self.mouse_position_label_x = tk.Label(self.root, text="Mouse X: 0")
        self.mouse_position_label_x.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.mouse_position_label_y = tk.Label(self.root, text="Mouse Y: 0")
        self.mouse_position_label_y.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        self.command_entry = ttk.Combobox(self.root, values=self.available_commands, width=50)
        self.command_entry.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        self.command_entry.bind("<Return>", lambda event: self.add_command())
        self.command_entry.bind("<KeyRelease>", self.update_suggestions)
        self.command_entry.focus_set()  # Set focus to the command entry field

        self.add_button = tk.Button(self.root, text="Add Command", command=self.add_command)
        self.add_button.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        self.run_button = tk.Button(self.root, text="Run Commands", command=self.run_commands)
        self.run_button.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

        self.stop_button = tk.Button(self.root, text="Stop Commands", command=self.stop_commands)
        self.stop_button.grid(row=2, column=2, padx=10, pady=5, sticky="nsew")
        self.stop_button.config(state="disabled")

        self.clear_button = tk.Button(self.root, text="Clear Commands", command=self.clear_commands)
        self.clear_button.grid(row=2, column=3, padx=10, pady=5, sticky="nsew")

        self.commands_listbox = tk.Listbox(self.root, width=50, height=10)
        self.commands_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.commands_listbox.bind("<Double-Button-1>", self.edit_command)  # Bind double-click to edit command
        # Bind events for drag-and-drop functionality
        self.commands_listbox.bind("<ButtonPress-1>", self.on_listbox_button_press)
        self.commands_listbox.bind("<B1-Motion>", self.on_listbox_motion)
        # Bind the "<Delete>" key event to the method for deleting list items
        self.commands_listbox.bind("<Delete>", self.delete_selected_item)
        
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.commands_listbox.yview)
        self.scrollbar.grid(row=4, column=3, sticky="ns")
        self.commands_listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.export_button = tk.Button(self.root, text="Export Commands", command=self.export_commands)
        self.export_button.grid(row=5, column=1, padx=10, pady=5, sticky="nsew")

        self.import_button = tk.Button(self.root, text="Import Commands", command=self.import_commands)
        self.import_button.grid(row=5, column=2, padx=10, pady=5, sticky="nsew")
        
        self.help_button = tk.Button(self.root, text="?", command=self.open_help_panel)
        self.help_button.grid(row=5, column=3, padx=10, pady=5, sticky="nsew")


    def update_mouse_position(self):
        x, y = pyautogui.position()
        self.mouse_position_label_x.config(text=f"X: {x}")
        self.mouse_position_label_y.config(text=f"Y: {y}")
        self.root.after(100, self.update_mouse_position)  # Update every 100 ms


    def open_help_panel(self):
        # Define the function to open the help panel with descriptions
        help_panel = tk.Toplevel(self.root)
        help_panel.title("Command Descriptions")

        help_panel.resizable(False, False)

        # Add general description label
        general_description = "General: The commands can be reorganized with drag and drop. They can be edited with 'double click' and deleted with 'del'."
        general_label = tk.Label(help_panel, text=general_description, anchor='w')
        general_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Create labels with descriptions for each command
        descriptions = {
            "moveTo x y": "move the mouse pointer to the specified coordinates, eg: moveTo 100 400",
            "click": "click the mouse at the current mouse pointer position",
            "type": "types input eg: type Hello => Hello",
            "press": "eg: Press tab",
            "hotkey": "eg: hotkey ctrl v",
            "scroll": "Scrolls, eg: scoll 1000 => scrolls 1000 px",
            "loop": "starts the commands from the beginng if loop_start_point is not defined. Can be stopped with the \"ESC\" Button",
            "loop_start_point": "sets the Starting point for the loop to the next item",
            "delay": "eg: delay 1 delays for one second",
            "create_int": "creates a variable, eg: create_int a 10",
            "get_int": "gets the variable and writes its value, eg: get_int a => 10",
            "inc_int": "increases the value of the variable, eg: inc_int a 1 => a = 11",
            "dec_int": "decreases the value of the variable, eg: dec_int a 1 => a = 9",
            # Add descriptions for other commands...
        }

        for i, (command, description) in enumerate(descriptions.items(), start=1):
            label = tk.Label(help_panel, text=f"{command}: {description}", anchor='w')
            label.grid(row=i, column=0, padx=10, pady=5, sticky="nesw")

    def update_suggestions(self, event):
        typed_text = self.command_entry.get()
        if typed_text:
            suggestions = [cmd for cmd in self.available_commands if cmd.startswith(typed_text)]
            self.command_entry['values'] = suggestions
        else:
            self.command_entry['values'] = self.available_commands

    def add_command(self):
        command = self.command_entry.get()
        if command:
            index = self.commands_listbox.size()
            if self.validate_command(command, index):
                self.commands.append(command)
                self.commands_listbox.insert(tk.END, command)
                self.command_entry.delete(0, tk.END)
                self.commands_listbox.yview(tk.END)  # Scroll to the bottom
            #else:
            #    messagebox.showerror("Error", "Invalid command.")

    def validate_command(self, command, index=None):
        parts = command.split()
        if not parts:
            return False
        action = parts[0]

        if action == "create_int":
            variable_name = parts[1]
            # Check if the variable name is already created
            for i in range(self.commands_listbox.size()):
                existing_command = self.commands_listbox.get(i)
                if i != index and existing_command.startswith("create_int") and existing_command.split()[1] == variable_name:
                    messagebox.showerror("Error", f"Variable '{variable_name}' is already created.")
                    return False
        elif action in ["get_int", "inc_int", "dec_int"]:
            variable_name = parts[1]
            # Check if there is a create_int for the variable_name with a smaller index
            found = False
            for i in range(index):
                existing_command = self.commands_listbox.get(i)
                if existing_command.startswith("create_int") and existing_command.split()[1] == variable_name:
                    found = True
                    break
            if not found:
                messagebox.showerror("Error", f"Variable '{variable_name}' has not been created.")
                return False
        return True

    def edit_command(self, event):
        selection = self.commands_listbox.curselection()
        if selection:
            index = selection[0]
            command = self.commands_listbox.get(index)
            new_command = self.askstring_with_size("Edit Command", "Modify the command:", initialvalue=command)
            if new_command:
                if self.validate_command(new_command, index):
                    self.commands[index] = new_command
                    self.commands_listbox.delete(index)
                    self.commands_listbox.insert(index, new_command)
                #else:
                #    messagebox.showerror("Error", "Invalid command.")
    
    def askstring_with_size(self, title, prompt, **kwargs):
        class CustomDialog(simpledialog.Dialog):
            def __init__(self, parent, title=None, prompt=None, **kwargs):
                self.prompt = prompt
                self.initialvalue = kwargs.get('initialvalue', '')
                super().__init__(parent, title)

            def body(self, master):
                self.geometry("400x120")
                self.resizable(False, False)
                tk.Label(master, text=self.prompt).grid(row=0, column=0)
                self.entry = tk.Entry(master, width=50)
                self.entry.grid(row=1, column=0)
                self.entry.insert(0, self.initialvalue)
                return self.entry

            def apply(self):
                self.result = self.entry.get()

        dialog = CustomDialog(self.root, title, prompt, **kwargs)
        return dialog.result

    def delete_command(self):
        selection = self.commands_listbox.curselection()
        if selection:
            index = selection[0]
            self.commands_listbox.delete(index)
            self.commands.pop(index)

    def delete_selected_item(self, event):
        selection = self.commands_listbox.curselection()
        if selection:
            self.delete_command()

    def clear_commands(self):
        self.commands = []
        self.commands_listbox.delete(0, tk.END)
        self.integer_variables.clear()  # Clear all integer variables

    def run_commands(self):
        if not self.commands:
            messagebox.showerror("Error", "No commands to run.")
            return
        self.running = True
        self.stop_button.config(state="normal")
        pyautogui.hotkey('alt', 'tab')  # Simulate Alt+Tab to switch windows
        time.sleep(1)  # Short delay to ensure the window switch is complete

        # Ensure the commands run in a new thread to keep the GUI responsive
        def execute_commands():
            while self.running:
                for command in self.commands[self.loop_start_index:]:
                    if not self.running:  # Check if stop button is pressed
                        break
                    self.execute_command(command)
                if not self.looping:
                    break
            # Clear integer variables after command execution
            self.integer_variables.clear()
        
            self.stop_button.config(state="disabled")
            self.running = False

        threading.Thread(target=execute_commands).start()
        # Listen for the 'esc' key press to stop the loop
        keyboard.on_press_key('esc', self.stop_commands)

    def stop_commands(self, event=None):
        self.running = False
        self.looping = False
        keyboard.unhook_all()  # Unhook the keyboard listener

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return
        action = parts[0]

        try:
            if action == "moveTo":
                x, y = int(parts[1]), int(parts[2])
                pyautogui.moveTo(x, y)
            elif action == "click":
                pyautogui.click()
            elif action == "type":
                text = " ".join(parts[1:])
                pyautogui.typewrite(text)
            elif action == "press":
                key = parts[1]
                pyautogui.press(key)
            elif action == "hotkey":
                keys = parts[1:]
                pyautogui.hotkey(*keys)
            elif action == "scroll":
                amount = int(parts[1])
                pyautogui.scroll(amount)
            elif action == "loop":
                self.looping = True
            elif action == "loop_start_point":
                self.loop_start_index = self.commands.index(command) + 1
            elif action == "delay":
                delay_time = float(parts[1])
                time.sleep(delay_time)
            elif action == "create_int":
                variable_name = parts[1]
                value = int(parts[2])
                self.create_integer_variable(variable_name, value)
            elif action == "get_int":
                variable_name = parts[1]
                self.get_integer_variable(variable_name)
            elif action == "inc_int":
                variable_name = parts[1]
                value = int(parts[2])
                self.increment_integer_variable(variable_name, value)
            elif action == "dec_int":
                variable_name = parts[1]
                value = int(parts[2])
                self.decrement_integer_variable(variable_name, value)
            else:
                print(f"Unknown command: {command}")
        except Exception as e:
            print(f"Error executing command {command}: {e}")

    def create_integer_variable(self, variable_name, value):
        self.integer_variables[variable_name] = value

    def get_integer_variable(self, variable_name):
        value = self.integer_variables.get(variable_name)
        if value is not None:
            pyautogui.typewrite(str(value))  # Ensure value is a string
        else:
            print(f"Integer variable '{variable_name}' not found.")

    def increment_integer_variable(self, variable_name, value):
        current_value = self.integer_variables.get(variable_name, 0)
        self.integer_variables[variable_name] = current_value + value

    def decrement_integer_variable(self, variable_name, value):
        current_value = self.integer_variables.get(variable_name, 0)
        self.integer_variables[variable_name] = current_value - value

    def import_commands(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                imported_commands = json.load(file)
                for command in imported_commands:
                    index = len(self.commands)
                    if self.validate_command(command, index):
                        self.commands.append(command)
                        self.commands_listbox.insert(tk.END, command)
                        if command.startswith("create_int"):
                            variable_name = command.split()[1]
                            self.integer_variables[variable_name] = int(command.split()[2])
            messagebox.showinfo("Info", "Commands imported successfully!")

    def export_commands(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.commands, file)
            messagebox.showinfo("Info", "Commands exported successfully!")

    def on_listbox_button_press(self, event):
        # Save the index of the selected item
        self.drag_start_index = self.commands_listbox.nearest(event.y)

    def on_listbox_motion(self, event):
        # Get the current index under the mouse cursor
        current_index = self.commands_listbox.nearest(event.y)
        if current_index != self.drag_start_index:
            # Move the item to the new position in the Listbox
            item = self.commands.pop(self.drag_start_index)
            self.commands.insert(current_index, item)
            self.commands_listbox.delete(self.drag_start_index)
            self.commands_listbox.insert(current_index, item)
            # Update the drag start index
            self.drag_start_index = current_index


if __name__ == "__main__":
    root = tk.Tk()
    # Set the initial size of the window
    root.geometry("600x600")  # Set the width and height as desired
    root.minsize(width=600, height=400)
    app = InputSimulatorApp(root)
    root.mainloop()

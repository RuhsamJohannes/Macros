import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
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
        self.create_widgets()

    def create_widgets(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        self.instructions = tk.Label(self.root, text="Enter your commands (e.g., moveTo 100 100, click, type Hello, press enter, hotkey ctrl c, loop, create_int a 10, get_int a, inc_int a 2, dec_int a 1):")
        self.instructions.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.command_entry = tk.Entry(self.root, width=50)
        self.command_entry.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        self.command_entry.bind("<Return>", lambda event: self.add_command())

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


        self.commands_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.commands_listbox.yview)



    def add_command(self):
        command = self.command_entry.get()
        if command:
            self.commands.append(command)
            self.commands_listbox.insert(tk.END, command)
            self.command_entry.delete(0, tk.END)
            self.commands_listbox.yview(tk.END)  # Scroll to the bottom

    def edit_command(self, event):
        selection = self.commands_listbox.curselection()
        if selection:
            index = selection[0]
            command = self.commands_listbox.get(index)
            new_command = simpledialog.askstring("Edit Command", "Modify the command:", initialvalue=command)
            if new_command:
                self.commands[index] = new_command
                self.commands_listbox.delete(index)
                self.commands_listbox.insert(index, new_command)

    def delete_command(self):
        selection = self.commands_listbox.curselection()
        if selection:
            index = selection[0]
            del self.commands[index]
            self.commands_listbox.delete(index)

    #this Button is not implemented anymore, is it?
    def delete_key_pressed(self, event):
        self.delete_command()
    
    def delete_selected_item(self, event):
        # Get the index of the selected item
        selected_index = self.commands_listbox.curselection()
        if selected_index:
            # Delete the selected item from the listbox and the commands list
            del self.commands[selected_index[0]]
            self.commands_listbox.delete(selected_index[0])

    def clear_commands(self):
        self.commands = []
        self.commands_listbox.delete(0, tk.END)

    def run_commands(self):
        if not self.running:
            self.running = True
            #self.root.withdraw()
            self.stop_button.config(state="normal")
            pyautogui.hotkey('alt', 'tab')  # Simulate Alt+Tab to switch windows
            time.sleep(1)  # Short delay to ensure the window switch is complete
            while self.running:
                for command in self.commands:
                    if not self.running:  # Check if stop button is pressed
                        break
                    self.execute_command(command)
                if not self.looping:
                    self.stop_button.config(state="disabled")
                    self.root.deiconify()
                    self.running = False
                    messagebox.showinfo("Info", "Commands executed successfully!")
                    break

    def stop_commands(self):
        self.running = False
        self.looping = False

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
        # Create a new integer variable
        self.integer_variables[variable_name] = value

    def get_integer_variable(self, variable_name):
        # Retrieve the value of an integer variable
        value = self.integer_variables.get(variable_name)
        if value is not None:
            pyautogui.typewrite(value)
        else:
            print(f"Integer variable '{variable_name}' not found.")

    def increment_integer_variable(self, variable_name, value):
        # Increment the value of an integer variable
        current_value = self.integer_variables.get(variable_name, 0)
        self.integer_variables[variable_name] = current_value + value

    def decrement_integer_variable(self, variable_name, value):
        # Decrement the value of an integer variable
        current_value = self.integer_variables.get(variable_name, 0)
        self.integer_variables[variable_name] = current_value - value


    def import_commands(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.commands = json.load(file)
            self.commands_listbox.delete(0, tk.END)
            for command in self.commands:
                self.commands_listbox.insert(tk.END, command)
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

    def run_commands(self):
        if not self.running:
            self.running = True
            self.stop_button.config(state="normal")
            pyautogui.hotkey('alt', 'tab')  # Simulate Alt+Tab to switch windows
            time.sleep(1)  # Short delay to ensure the window switch is complete

            # Define a function to execute commands in a separate thread
            def execute_commands_thread():
                loop_start_index = 0
                for i, command in enumerate(self.commands):
                    if command.startswith("loop"):
                        loop_start_index = i + 1
                        break

                while self.running:
                    for command in self.commands:
                        if not self.running:  # Check if stop button is pressed
                            break
                        self.execute_command(command)
                    if not self.looping:
                        break
                self.stop_button.config(state="disabled")
                self.running = False
                #messagebox.showinfo("Info", "Commands executed successfully!")
            
            # Start a new thread to execute commands
            threading.Thread(target=execute_commands_thread).start()

            # Listen for the 'esc' key press to stop the loop
            keyboard.on_press_key('esc', self.stop_commands)

    def stop_commands(self, event=None):
        self.running = False
        self.looping = False
        keyboard.unhook_all()  # Unhook the keyboard listener


if __name__ == "__main__":
    root = tk.Tk()
    app = InputSimulatorApp(root)
    root.mainloop()

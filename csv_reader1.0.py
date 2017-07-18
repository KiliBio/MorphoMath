#!/usr/bin/python
'''Code written in Python 3.5 by KiliBio'''

import tkinter as tk
import tkinter.messagebox
import csv
import os
import numpy as np

'''Current issues:  Develop two modes!
                First mode: Finds the statistically significant ratios in different individual of the same species(done)
                Second mode: Finds the statistically significant ratios which distinguish different species'''
'''Current issues: Pickle temporary files, to make the program faster!'''
'''Current issues: Save the Output-File in an Excel Format'''
'''Current issues: Write a second part of the program where you can extent the dataset to make it more significant!
   ---> so you can add the information of any particular new flower and compare it the existent data'''

class Csv_Evaluate(tk.Tk):
    '''main class'''
    def __init__(self, *arg, **kwargs):
        '''__init__ function to initiate the automatic function to create the widgets'''
        tk.Tk.__init__(self, *arg, **kwargs)

        ### sets the size of the main window automatically to the size of the screen
        self.master_width, self.master_height = self.winfo_screenwidth(), self.winfo_screenheight()
        ### geometry determines the actual window size
        self.geometry('%dx%d+0+0' % (self.master_width/2, self.master_height/2))
        ### icon in the upper-left corner
        tk.Tk.iconbitmap(self,
                         default="C:/morphoMathicon2.ico")
        ### title of the window
        tk.Tk.wm_title(self, "Result Evaluator")

        self.file_names = []

        self.mainframe = tk.Frame(self)
        self.mainframe["bg"] = "AntiqueWhite2"
        self.mainframe.pack(side="top", fill="both", expand=True)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)  # weight --> prioritizes things

        self.main_label = tk.Label(self)
        self.main_label["text"] = "Result Evaluator"
        self.main_label["font"] = "Courier 10 bold"
        self.main_label.pack(side="top", anchor="center", padx=5, pady=5)

        self.explain_label = tk.Label(self)
        self.explain_label["text"] = "Upload all .csv files, which were created by MorphoMath and \n" \
                                     "which you want to compare, specify the output-file and give it a go. \n"\
                                     "1. Type name of file|2. Hit Enter|3. Repeat|4. Click All Done!"
        self.explain_label["font"] = "Courier 9"
        self.explain_label.pack(side="top", anchor="center", padx=5, pady=5)

        ### Canvas in which all other labels and the entry areas are saved
        self.all_in_one_canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.all_in_one_canvas.config(width=self.winfo_screenwidth()/2, height=self.winfo_screenheight()/2)

        self.in_canvas_frame = tk.Frame(self.all_in_one_canvas, background="#ffffff")
        ### adds a scrollbar, which is not really necessary
        self.right_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.all_in_one_canvas.yview)
        self.all_in_one_canvas.configure(yscrollcommand=self.right_scrollbar.set)
        self.right_scrollbar.pack(side="right", fill="y")
        self.all_in_one_canvas.pack(side="top", fill="x", expand=True)

        self.all_in_one_canvas.create_window((4, 4), window=self.in_canvas_frame,
                                             anchor="n", tags="self.frame")

        self.in_canvas_frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.all_in_one_canvas.configure(scrollregion=self.all_in_one_canvas.bbox("all"))

    def populate(self):
        '''This function populates the center of the window with the input area'''
        ### head-label: tells the user that this is the point specifier
        self.path_label = tk.Label(self.in_canvas_frame)
        self.path_label["text"] = "PATH: C:/output"
        self.path_label["font"] = "Courier 7"
        self.path_label.pack(side="top", anchor="center", padx=5, pady=5)

        self.file_name_label = tk.Label(self.in_canvas_frame)
        self.file_name_label["text"] = "File-Name (without extension)"
        self.file_name_label["font"] = "Courier 9 bold"
        self.file_name_label.pack(side="top", anchor="center", padx=5, pady=5)

        self.file_name_entry = tk.Entry(self.in_canvas_frame)
        self.file_name_entry["bg"] = "mint cream"
        self.file_name_entry["fg"] = "grey25"
        self.file_name_entry["bd"] = 2
        self.file_name_entry["cursor"] = "xterm"
        self.file_name_entry["width"] = 80
        self.file_name_entry.pack(side="top", anchor="center", padx=5, pady=5)
        self.file_name_entry.bind("<Return>", self.return_upload)

        self.output_frame = tk.Frame(self.in_canvas_frame)
        self.output_frame.config(width=80, height=30)
        self.output_frame.pack(side="top", fill="x", anchor="center")

        ### upload button: here on the third position since the side=bottom feature is weird
        self.upload_button = tk.Button(self.in_canvas_frame,
                                       command=self.upload_button_func)
        self.upload_button["text"] = "✅ ALL DONE ✅"
        self.upload_button["font"] = "Courier 10 bold"
        self.upload_button["bg"] = "Olivedrab2"
        self.upload_button["padx"] = 10
        self.upload_button["pady"] = 10
        self.upload_button.pack(side="bottom", anchor="center", padx=5, pady=5)

        self.output_file_entry = tk.Entry(self.in_canvas_frame)
        self.output_file_entry["bg"] = "mint cream"
        self.output_file_entry["fg"] = "grey25"
        self.output_file_entry["bd"] = 2
        self.output_file_entry["cursor"] = "xterm"
        self.output_file_entry["width"] = 80
        self.output_file_entry.pack(side="bottom", anchor="center", padx=5, pady=5)

        self.output_file_label = tk.Label(self.in_canvas_frame)
        self.output_file_label["text"] = "Name of Output-File (without extension)"
        self.output_file_label["font"] = "Courier 9 bold"
        self.output_file_label.pack(side="bottom", anchor="center", padx=5, pady=5)

    def return_upload(self, event):
        '''Check here if all files have the same number of rows!!!!!'''
        try:
            ### if the entered file exists the file name is appened to the file name list
            f = open("C:/output" +
                     self.file_name_entry.get() + ".csv")
            f.close()

            self.entry_file_name = self.file_name_entry.get()
            self.file_names.append(self.entry_file_name)

            self.value_label = tk.Label(self.output_frame)
            self.value_label.config(width=80, height=1)
            self.value_label["font"] = "Courier 9"
            self.value_label["bg"] = "SeaGreen1"
            self.value_label["fg"] = "black"
            self.value_label.pack(side="top", anchor="center", pady=1)
            ### this adds the number of the point and the actual number to the point-list
            self.value_label.configure(text="(%d) %s" % (len(self.file_names), self.entry_file_name))

            self.file_name_entry.delete(0, 'end')
            return self.file_names, self.entry_file_name

        except IOError:
            ### if the entered file does not exist in the path
            tkinter.messagebox.showinfo("Error Message", "Entered file couldn't be found in path.")

    def upload_button_func(self):
        '''is called when "Upload-Button" is pressed'''

        self.sample_size = len(self.file_names)
        ### formats the first entered file, which acts as a blueprint in format for the output-file
        self.first_to_file_write()
        ### formats all the other entered files and appends their content horizontally to the output-file
        self.every_other_file_append()
        ### analyzes the overall file and writes it all in one big file
        self.analyzer()
        self.write_to_mother()
        print("File analyzed.")

        ### deletes the temporary files
        os.remove(self.temp_file1_path)
        os.remove(self.temp_file2_path)
        print("Both temporary files deleted")

        ### terminates the program
        self.quit()

    def first_to_file_write(self):
        '''formats the first entered file, which acts as a blueprint in format for the output-file'''
        ### gets first file name
        self.first_file_name = self.file_names.pop(0)

        ### creates the output file with the specified file name
        self.output_file_path = "C:/output" + \
                                self.output_file_entry.get() + ".csv"

        '''it will be writing to the final output file'''
        with open(self.output_file_path, mode='w', buffering=-1, encoding=None, errors=None, newline=None) \
                as write_csv_file:
            write_csv_file_writer = csv.writer(write_csv_file, lineterminator='\n')

            '''the first file, which acts as a blueprint is opened and read here'''
            with open("C:/output/" + self.first_file_name + ".csv",
            mode='r', buffering=-1, encoding=None, errors=None, newline=None) as read_csv_file:
                read_csv_file_reader = csv.reader(read_csv_file)  # csvfilereader stores the content of the csv file

                ### "print_all" is a Flag variable, which will be flipped if a certain word is found
                print_all = False

                for row in read_csv_file_reader:
                    #? WHY DOES A WHILE-ELSE FUNCTION HERE NOT WORK?
                    if print_all == True:
                        if len(row) == 0:
                            pass
                        else:
                            ### after the print_all flag is true each line is just read and written to the output-file
                            write_csv_file_writer.writerow(row)

                    else:
                        ### while print_all remains false
                        for field in row:
                            if field == 'FILE NAME':
                                ### finding the file name and writes the file name to the file
                                write_csv_file_writer.writerow([row[0], row[1]])
                            elif field == "--------RATIO BETWEEN EACH DISTANCES--------":
                                ### once this line is found the rest, will be printed
                                print_all = True
                            else:
                                pass
            ### when all the lines of the files have been read the reader is closed and the writer is closed
            read_csv_file.close()
        write_csv_file.close()

    def every_other_file_append(self):
        '''formats every file and appends its content to the "motherfile", by working with 2 temporary files'''
        self.temp_file1_path = "C:/output/temp_file1.csv"
        self.temp_file2_path = "C:/output/temp_file2.csv"

        ### the while loop, loops over all files entered until there are no more
        while self.file_names != []:
            self.file_name = self.file_names.pop(0)
            self.file_name_path = "C:/output/" \
                                  + self.file_name + ".csv"

            self.format_file()          ### formats the file
            self.merge_files()          ### merges the file with the existing file
            self.write_to_mother()      ### overwrites the content of both to the mother-file

    def format_file(self):
        '''this function makes each of the current files equal in their content'''

        '''the first temporary file, which will be the formatted version of the entered file'''
        with open(self.temp_file1_path, mode='w', buffering=-1, encoding=None, errors=None, newline=None) \
                as temp1_csv_file:
            temp1_csv_file_writer = csv.writer(temp1_csv_file, lineterminator='\n')

            '''the n'th entered file is uploaded here, 
            to access the information for the formatted version in temp-file'''
            with open(self.file_name_path, mode='r', buffering=-1, encoding=None, errors=None, newline=None) \
                    as read_csv_file:
                read_csv_file_reader = csv.reader(read_csv_file)
                print_all = False
                for row in read_csv_file_reader:
                    if len(row) == 0:
                        pass
                    elif len(row) >= 1:
                        if row[0] == 'FILE NAME':  # finding the file name
                            temp1_csv_file_writer.writerow([row[1]])
                        elif row[0] == "--------RATIO BETWEEN EACH DISTANCES--------":
                            print_all = True
                        elif print_all == True:
                            temp1_csv_file_writer.writerow([row[1]])
                        else:
                            pass
            read_csv_file.close()
        temp1_csv_file.close()

    def merge_files(self):
        '''this function merges the first "blueprint" file and the n'th file'''

        '''the second temporary file is storing the information of both files'''
        with open(self.temp_file2_path, mode='w', buffering=-1, encoding=None, errors=None, newline=None) \
                as temp2_csv_file:
            temp2_csv_file_writer = csv.writer(temp2_csv_file, lineterminator='\n')

            '''the first "blueprint" file - mother row - blueprint file'''
            with open(self.output_file_path, mode='r', buffering=-1, encoding=None, errors=None, newline=None) \
                    as mother_csv_file:
                mother_csv_file_reader = csv.reader(mother_csv_file)

                '''the n'th entered file - daugther row '''
                with open(self.temp_file1_path, mode='r', buffering=-1, encoding=None, errors=None,newline=None) \
                        as read_csv_file:
                    read_csv_file_reader = csv.reader(read_csv_file)  # csvfilereader stores the content of the csv file

                    for mum_row, dau_row in zip(mother_csv_file_reader, read_csv_file_reader):
                        if len(mum_row) == 0:
                            pass
                        elif len(mum_row) >= 1:
                            write_to_file_list = [dau_row[0]]
                            for element in range(len(mum_row)):
                                write_to_file_list.insert(-1, mum_row[element])
                            temp2_csv_file_writer.writerow(write_to_file_list)
                        else:
                            pass
                read_csv_file.close()
            mother_csv_file.close()
        temp2_csv_file.close()
        print("File appended")

    def write_to_mother(self):
        '''this function just overwrites the information from the second temp file to the output "mother" file'''

        '''openes the "motherfile"'''
        with open(self.output_file_path, mode='w', buffering=-1, encoding=None, errors=None, newline=None) \
                as mother_csv_file:
            mother_csv_file_writer = csv.writer(mother_csv_file, lineterminator='\n')

            '''opens the secondary temporary file where is the information is stored for now'''
            with open(self.temp_file2_path, mode='r', buffering=-1, encoding=None, errors=None, newline=None) \
                    as read_csv_file:
                read_csv_file_reader = csv.reader(read_csv_file)
                for row in read_csv_file_reader:
                    mother_csv_file_writer.writerow(row)
            read_csv_file.close()
        mother_csv_file.close()


    def analyzer(self):
        '''analyzes the data as compressed in the "mother" file'''
        print("Analyzing file...")
        '''the second temporary file is used again to store the analyzed data'''
        with open(self.temp_file2_path, mode='w', buffering=-1, encoding=None, errors=None, newline=None) \
                as temp2_csv_file:
            temp2_csv_file_writer = csv.writer(temp2_csv_file, lineterminator='\n')
            '''opens the motherfile'''
            with open(self.output_file_path, mode='r', buffering=-1, encoding=None, errors=None, newline=None) \
                    as mother_csv_file:
                mother_csv_file_reader = csv.reader(mother_csv_file, lineterminator='\n')

                analyze_from_here = False

                for row in mother_csv_file_reader:
                    if len(row) == 0:
                        pass
                    elif len(row) >= 1:
                        if row[0] == 'FILE NAME':
                            first_row = []
                            for element in range(len(row)):
                                first_row.append(row[element])
                            first_row.insert(1, "")
                            temp2_csv_file_writer.writerow(first_row)
                            temp2_csv_file_writer.writerow(["SAMPLE SIZE", self.sample_size])
                        elif row[0] == "1ST DIST/2ND DIST":
                            row_to_write = ['AVERAGE', 'STAND_DIV']
                            for element in range(len(row)):
                                row_to_write.insert(-2, row[element])
                            print(row_to_write)
                            row_to_write.insert(1, "SIGNICANCE")
                            temp2_csv_file_writer.writerow(row_to_write)
                            analyze_from_here = True
                        elif analyze_from_here == True:

                            # strips of the index and space columns and converts the strings into floats
                            current_row = row[1:]
                            current_row = [element for element in current_row if element != ""]
                            current_row = [float(element) for element in current_row if isinstance(element, str)]

                            # calculating the average and standard deviation
                            average_of_num = (sum(current_row)/len(current_row))
                            sum_of_dev = 0
                            for element in current_row:
                                sum_of_dev += (element-average_of_num)**2
                            stand_dev = np.sqrt(sum_of_dev/(len(current_row)-1))
                            #stand_error = stand_dev/np.sqrt(len(current_row))

                            write_to_file_list = ["%0.4f" % average_of_num, "%0.4f" % stand_dev]

                            for element in range(len(row)):
                                write_to_file_list.insert(-2, row[element])

                            if stand_dev < average_of_num *0.01:
                                write_to_file_list.insert(1, "###")
                                temp2_csv_file_writer.writerow(write_to_file_list)
                            elif stand_dev < average_of_num *0.05:
                                write_to_file_list.insert(1, "##")
                                temp2_csv_file_writer.writerow(write_to_file_list)
                            elif stand_dev < average_of_num *0.1:
                                write_to_file_list.insert(1, "#")
                                temp2_csv_file_writer.writerow(write_to_file_list)
                            else:
                                write_to_file_list.insert(1, "")
                                temp2_csv_file_writer.writerow(write_to_file_list)
                                #print("AFTER:", write_to_file_list)
                        else:
                            pass
                    else:
                        pass
                else:
                    temp2_csv_file_writer.writerow(['', '###', 'STANDARD DEVIATION SMALLER THAN 1% OF THE AVERAGE'])
                    temp2_csv_file_writer.writerow(['', '##', 'STANDARD DEVIATION SMALLER THAN 5% OF THE AVERAGE'])
                    temp2_csv_file_writer.writerow(['', '#', 'STANDARD DEVIATION SMALLER THAN 10% OF THE AVERAGE'])
            mother_csv_file.close()
        temp2_csv_file.close()

if __name__ == "__main__":
    application = Csv_Evaluate()
    application.mainloop()


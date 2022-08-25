from datetime import timedelta
from Entities.Day import Day
from Entities.Student import Student
from Entities.Bot import Bot
from Entities.Admin import Admin
import datetime 
import random
import threading
from io import StringIO


class OTProgrammer:

    def __init__(self):
        self.bot = Bot(self)
        self.admin = Admin(self.bot)
        self.bot.chats = []

    def read_classroom(self, chat_index):
        # reads data from file starting by the classroom keyword

        search_for_keyword = True
        line_number = 1
        students = []
        students_line_number = 0
        keyword_chars_counter = 0
        keyword_found = False

        while search_for_keyword:
            line_number = 1

            classrooms = ""
            try:
                classrooms = open("classrooms.csv", "r")
            except:
                self.bot.send_message("", chat_index, "Errore Server")
                print("Verified exception number: 3")
                exit()

            keyword = self.bot.read_message("Scrivi la parola chiave che identifica la tua classe",
                                            StringIO,
                                            self.bot.chat_index)
            self.bot.variable_controls(self.bot.chat_index, keyword, StringIO)

            for line in classrooms:
                if keyword_found == False:
                    if keyword in line and keyword != "" and keyword != " " and line_number%2 != 0:
                        keyword_chars_counter = 0
                        line_keyword = ""
                        line_keyword_found = False
                        i = 0

                        while line_keyword_found == False:

                            if line[i+11] == "]":
                                line_keyword_found = True
                            else:
                                line_keyword += line[i+11]
                            i += 1

                        for i in range(len(keyword)):
                            if line_keyword[i] == keyword[i]:

                                keyword_chars_counter += 1

                        if keyword_chars_counter == len(line_keyword):

                            self.bot.send_message("", self.bot.chat_index, "_Parola chiave trovata_")
                            students_line_number = line_number + 1
                            search_for_keyword = False
                            keyword_found = True

                line_number += 1

            if search_for_keyword:
                self.bot.send_message("", self.bot.chat_index, "_Parola chiave inesistente_")
                new_class = self.bot.read_message("Vuoi creare una nuova classe?", StringIO, self.bot.chat_index)
                self.bot.variable_controls(self.bot.chat_index, new_class, StringIO)

                if "si" in new_class.lower():
                    self.write_classroom(self.bot.chat_index)
                    search_for_keyword = False

        #read students
        counter = 1
        classrooms.seek(0)

        for line in classrooms:
            if counter == students_line_number:
                students = line.split("-")
            counter += 1

        #add students to the classroom arraylist
        for i in range(len(students)-1):
            self.bot.chats[self.bot.chat_index].classroom.append(Student(students[i],i+1))

        classrooms.close()

    def check_commands(self, chat_index, variable):
        # checks if the variable is equals to the menu command, if it is goes back to menu

        if variable.lower() == "/menu":
            self.show_menu(chat_index, "")
        elif variable == "/newclass":
            self.show_menu(chat_index, "newclass")
        elif variable == "/useclass":
            self.show_menu(chat_index, "useclass")
        elif variable == "/noclass":
            self.show_menu(chat_index, "noclass")
        elif variable == "/help":
            self.show_menu(chat_index, "help")


    def write_classroom(self, chat_index):
        # input classroom names and write them in the file

        insert_name = True
        keyword = ""                        # to identify a classroom
        keyword_already_token = False
        keyword_is_right = False
        keyword_is_long_enough = False

        # read keyword
        while keyword_is_right == False:
            classrooms = open("classrooms.csv", "r")

            keyword = self.bot.read_message(
                "Scegli una parola chiave per identificare la tua classe _(almeno 8 caratteri)_",
                StringIO,
                chat_index)
            self.bot.variable_controls(chat_index, keyword, StringIO)

            if len(keyword) < 8:
                self.bot.send_message("",
                                      chat_index,
                                      "_Errore! La parola chiave deve essere lunga almeno 8 caratteri_")
                keyword_is_long_enough = False
            else:
                keyword_is_long_enough = True
                keyword_already_token = False
                # checks if the keyword is already token
                line_number = 1
                for line in classrooms:

                    if keyword in line and keyword != "" and keyword != " " and line_number%2 != 0:
                        keyword_chars_counter = 0
                        line_keyword = ""
                        line_keyword_found = False
                        i = 0

                        while line_keyword_found == False:

                            if line[i+11] == "]":
                                line_keyword_found = True
                            else:
                                line_keyword += line[i+11]
                            i += 1

                        for i in range(len(keyword)):
                            if line_keyword[i] == keyword[i]:

                                keyword_chars_counter += 1

                        if keyword_chars_counter == len(line_keyword):
                            self.bot.send_message("", chat_index, "_La parola chiave è gia stata presa_")
                            keyword_already_token = True

                    line_number += 1

            if keyword_already_token == False and keyword_is_long_enough == True:
                keyword_is_right = True
                self.bot.send_message("", chat_index, "_Parola chiave accettata_")

        # read students surname, create student object and inserts it into classroom
        student_number = 1
        while insert_name == True:
            surname = self.bot.read_message("Cognome dello studente " + str(student_number) + "\n /stop ",
                                            StringIO,
                                            chat_index)
            self.bot.variable_controls(chat_index, surname, StringIO)

            if surname == "/stop":
                insert_name = False

            else:
                self.bot.chats[chat_index].classroom.append(Student(surname,student_number))
            student_number += 1

        # writes data on file
        classrooms = open("classrooms.csv", "a")
        classrooms.write("classroom=[" + keyword + "]\n")
        for i in range(len(self.bot.chats[chat_index].classroom)):
            classrooms.write(str(self.bot.chats[chat_index].classroom[i].surname) + "-")
        classrooms.write("\n")
        classrooms.close()

        self.bot.send_message("", chat_index, "_OK! La classe è stata salvata con successo_")

    def weekday_from_english_to_italian(self, weekday):
        # translates weekday from english to italian

        if weekday == "Monday":
            return "Lunedì"
        elif weekday == "Tuesday":
            return "Martedì"
        elif weekday == "Wednesday":
            return "Mercoledì"
        elif weekday == "Thursday":
            return "Giovedì"
        elif weekday == "Friday":
            return "Venerdì"
        elif weekday == "Saturday":
            return "Sabato"
        elif weekday == "Sunday":
            return "Domenica"

    def day_name_from_weekday(self, weekday):                        #return string equivalent of weekday integer

        if weekday == 0:
            return "Lunedì"
        if weekday == 1:
            return "Martedì"
        if weekday == 2:
            return "Mercoledì"
        if weekday == 3:
            return "Giovedì"
        if weekday == 4:
            return "Venerdì"
        if weekday == 5:
            return "Sabato"
        if weekday == 6:
            return "Domenica"

    def day_spawner(self, date, chat_index):                        #spawns interrogation days objects

        weekday = date.strftime('%A')
        day = Day(date, weekday)
        self.bot.chats[chat_index].interrogation_days.append(day)

        self.bot.chats[chat_index].days_object_counter += 1

    def date_calculator(self, daysdelta, chat_index):
        # calculate the date of the days selected from daysdelta

        if self.bot.chats[chat_index].days_object_counter == 0:
            self.day_spawner(self.bot.default_days[chat_index].date, chat_index)
        else:
            new_date = self.bot.chats[chat_index].interrogation_days[
                           self.bot.chats[chat_index].days_object_counter-1].date + timedelta(daysdelta)
            self.day_spawner(new_date, chat_index)

    def output_interrogation_plan(self, chat_index):
        # output the interrogation plan

        students_counter = 0
        interrogationplan_output = ""
        interrogation_days_c = 0

        for j in range(len(self.bot.chats[chat_index].interrogation_days)-1):
            if self.bot.chats[chat_index].interrogation_days[j+1].weekday == self.bot.chats[chat_index].interrogation_days[0].weekday:
                interrogation_days_c += 1

        for i in range(len(self.bot.chats[chat_index].interrogation_days)):

            if len(self.bot.chats[chat_index].interrogation_days[i].interrogated_students) > 0:

                if self.bot.chats[chat_index].interrogation_days[i-1].weekday != self.bot.chats[chat_index].interrogation_days[i].weekday:
                    interrogationplan_output += "*" + str(self.weekday_from_english_to_italian(
                        self.bot.chats[chat_index].interrogation_days[i].weekday)) + \
                                                ":* " + \
                                                str(self.bot.chats[chat_index].interrogation_days[i].date) + "\n"

                elif interrogation_days_c == len(self.bot.chats[chat_index].interrogation_days)-1:
                    interrogationplan_output += "*" + str(self.weekday_from_english_to_italian(
                        self.bot.chats[chat_index].interrogation_days[i].weekday)) +\
                                                ":* " + \
                                                str(self.bot.chats[chat_index].interrogation_days[i].date) + "\n"

                elif i == 0:
                    interrogationplan_output += "*" + str(self.weekday_from_english_to_italian(
                        self.bot.chats[chat_index].interrogation_days[i].weekday)) + \
                                                ":* " + \
                                                str(self.bot.chats[chat_index].interrogation_days[i].date) + "\n"

            for j in range(self.bot.chats[chat_index].students_per_day):
                if students_counter < len(self.bot.chats[chat_index].classroom):

                    interrogationplan_output += " • " + str(self.bot.chats[chat_index].interrogation_days[i].interrogated_students[j].surname) + "\n"
                    students_counter += 1

        self.bot.send_message("", chat_index, "Il piano di interrogazioni di *" + str(self.bot.chats[chat_index].school_subject) + "* è:" + "\n" + interrogationplan_output)

        ratings_file = open("ratings.csv", "r")
        user_did_rate = False

        for line in ratings_file:
            if str(self.bot.chats[chat_index].chat_id) in line:
                user_did_rate = True
                break

        ratings_file.close()

        if user_did_rate == False:
            ratings_file = open("ratings.csv", "a")
            self.bot.show_rating_keyboard(chat_index)
            bot_rating = self.bot.read_message("", StringIO, chat_index)
            self.bot.send_message("", chat_index, "Grazie per il tuo feedback!")
            ratings_file.write(str(self.bot.chats[chat_index].chat_id) + " - " + str(
                self.bot.get_user_infos()) + " - " + bot_rating[2:] + "\n")

            ratings_file.close()

        while True:
            self.bot.show_one_button_keyboard(chat_index,
                                              "Premi START per calcolare un nuovo piano di interrogazioni", "START")
            back_to_menu = self.bot.read_message("", StringIO, chat_index)
            if back_to_menu == "START":
                self.bot.show_menu(chat_index, "")

    def students_distributor(self, chat_index):
        # destribute for each day a nuber of students
        students_counter = 0
        random.shuffle(self.bot.chats[chat_index].classroom) # shuffle array classroom
        for i in range(len(self.bot.chats[chat_index].interrogation_days)):
            for _ in range(self.bot.chats[chat_index].students_per_day):
                if students_counter < len(self.bot.chats[chat_index].classroom):
                    self.bot.chats[chat_index].interrogation_days[i].interrogated_students.append(
                        self.bot.chats[chat_index].classroom[students_counter])
                    students_counter += 1

    def days_calculator(self, alternating_mode, chat_index):
        # calculate the delta of the days in the array "selected_days"
        self.bot.chats[chat_index].selected_days.sort()
        loop_counter = 0
        loop = True

        if alternating_mode:
            index_of_default_date = self.bot.chats[chat_index].selected_days.index(
                self.bot.default_days[chat_index].date.weekday())
            for i in range(index_of_default_date-1, len(self.bot.chats[chat_index].selected_days)):
                if loop_counter < int(self.bot.chats[chat_index].students_number/self.bot.chats[chat_index].students_per_day)+1:
                    if i == len(self.bot.chats[chat_index].selected_days)-1:
                        daysdelta = -(self.bot.chats[chat_index].selected_days[i]-self.bot.chats[chat_index].selected_days[0])+14
                    else:
                        daysdelta = -(self.bot.chats[chat_index].selected_days[i]-self.bot.chats[chat_index].selected_days[i+1])
                    loop_counter += 1
                    self.date_calculator(daysdelta, chat_index)
            while loop:
                for i in range(len(self.bot.chats[chat_index].selected_days)):
                    if loop_counter < int(self.bot.chats[chat_index].students_number/self.bot.chats[chat_index].students_per_day)+1:
                        if i == len(self.bot.chats[chat_index].selected_days)-1:
                            daysdelta = -(self.bot.chats[chat_index].selected_days[i]-self.bot.chats[chat_index].selected_days[0])+14
                            i = 0
                        else:
                            daysdelta = -(self.bot.chats[chat_index].selected_days[i]-self.bot.chats[chat_index].selected_days[i+1])
                        loop_counter += 1
                        self.date_calculator(daysdelta, chat_index)
                if loop_counter == int(self.bot.chats[chat_index].students_number/self.bot.chats[chat_index].students_per_day)+1:
                    loop = False

        else:
            index_of_default_date = self.bot.chats[chat_index].selected_days.index(
                self.bot.default_days[chat_index].date.weekday())
            for i in range(index_of_default_date-1, len(self.bot.chats[chat_index].selected_days)):
                if loop_counter < int(self.bot.chats[chat_index].students_number/self.bot.chats[chat_index].students_per_day)+1:
                    if i == len(self.bot.chats[chat_index].selected_days)-1:
                        daysdelta = -(self.bot.chats[chat_index].selected_days[i]-self.bot.chats[chat_index].selected_days[0])+7
                    else:
                        daysdelta = -(self.bot.chats[chat_index].selected_days[i]-self.bot.chats[chat_index].selected_days[i+1])
                    loop_counter += 1
                    self.date_calculator(daysdelta, chat_index)
            while loop:
                for i in range(len(self.bot.chats[chat_index].selected_days)):
                    if loop_counter < int(self.bot.chats[chat_index].students_number/self.bot.chats[chat_index].students_per_day)+1:
                        if i == len(self.bot.chats[chat_index].selected_days)-1:
                            daysdelta = -(self.bot.chats[chat_index].selected_days[i]-self.bot.chats[chat_index].selected_days[0])+7
                            i = 0
                        else:
                            daysdelta = -(self.bot.chats[chat_index].selected_days[i]-self.bot.chats[chat_index].selected_days[i+1])
                        loop_counter += 1
                        self.date_calculator(daysdelta, chat_index)
                if loop_counter == int(self.bot.chats[chat_index].students_number/self.bot.chats[chat_index].students_per_day)+1:
                    loop = False

    def input_data(self, chat_index, generic_mode):
        # input informations needed to calculate the interrogation plan
        loop = True
        counter = 0
        # default_date_weekday = [""] * 7

        if generic_mode == True:
            redo = True
            while redo:
                self.bot.chats[chat_index].students_number = self.bot.read_message(
                    "Numero di studenti nella classe", int, chat_index)
                self.bot.chats[chat_index].students_number = int(self.bot.chats[chat_index].students_number)
                if self.bot.chats[chat_index].students_number > 100:
                    self.bot.send_message("", chat_index, "_Numero troppo grande, massimo 100 studenti_")
                else:
                    redo = False
            self.generic_mode(self.bot.chats[chat_index].students_number)
        else:
            self.bot.chats[chat_index].students_number = len(self.bot.chats[chat_index].classroom)
        self.bot.chats[chat_index].students_per_day = self.bot.read_message(
            "Numero di studenti interrogati al giorno", int, chat_index)
        self.bot.chats[chat_index].students_per_day = int(self.bot.chats[chat_index].students_per_day)
        self.bot.chats[chat_index].school_subject = self.bot.read_message("Materia dell'interrogazione", StringIO, chat_index)

        # input date of the first interrogation day
        self.bot.send_message("", chat_index, "_Scrivi la data del primo giorno dell'interrogazione_")

        while loop:

            year = self.bot.read_message("*Anno*", int, chat_index)
            year = int(year)

            month = self.bot.read_message("*Mese* (numero)", int, chat_index)
            month = int(month)

            day = self.bot.read_message("*Giorno* (numero)", int, chat_index)
            day = int(day)

            try:
                default_date = datetime.date(year, month, day)
                if default_date.weekday() == 6:
                    self.bot.send_message("", chat_index, "_La data inserita corrisponde a domenica, usane una valida_")
                else:
                    loop = False

            except:
                self.bot.send_message("", chat_index, "_Errore! Data inconsistente, usane una valida_")
                print("Verified exception number: 4")


        #create object of the first interrogation day (default day)
        default_weekday = default_date.strftime('%A')
        self.bot.default_days[chat_index] = Day(default_date, default_weekday)
        #default_date_weekday[default_days[chat_index].date.weekday()] = "*"

        alternating_mode = "0"
        # alternating_mode = readMessage("*/0 - tutte le settimane\n/1 - settimane alternate*",StringIO,chat_index)

        if alternating_mode == "/0" or alternating_mode == "0":
            alternating_mode = False
        elif alternating_mode == "/1" or alternating_mode == "1":
            alternating_mode = True
        else:
            self.bot.send_message("", chat_index, "_Errore! Dato inserito inconsistente, torno al menu principale_")


        #input interrogation days of the week
        days_selectable = True

        message_to_show = "*Scegli i giorni della settimana in cui si svolgeranno le interrogazioni*\n\n" + \
                          "_puoi selezionare più volte lo stesso giorno per dire " \
                          "che in quel giorno si interroghera' piu' ore_\n\n" + \
                          "❌ *-> cancella i giorni della settimana selezionati\n\n✅ -> " \
                          "calcola il piano di interrogazioni* \n\n" + \
                          "_la data precedentemente selezionata corrisponde a: _ *" + \
                          str(self.weekday_from_english_to_italian(self.bot.default_days[chat_index].weekday)) + "*"
        self.bot.show_weekdays_keyboard(chat_index, message_to_show)

        while days_selectable == True:

            if counter > 0:
                days = ""
                self.bot.chats[chat_index].selected_days.sort()
                for i in range(len(self.bot.chats[chat_index].selected_days)):
                    days = days + str(self.day_name_from_weekday(self.bot.chats[chat_index].selected_days[i]) + "  ")

                self.bot.send_message("", chat_index, "hai scelto:" + "\n*" + days + "*")

            day = self.bot.read_message("scegli un giorno", StringIO, chat_index)

            try:
                if "Conferma" in day:
                    if self.bot.default_days[chat_index].date.weekday() not in self.bot.chats[chat_index].selected_days:
                        self.bot.send_message("", chat_index, "_Errore, devi inserire anche " +
                                              str(self.weekday_from_english_to_italian(
                                                  self.bot.default_days[chat_index].weekday)) + "_")
                    else:
                        self.bot.remove_keyboard(chat_index, "_Sto calcolando il piano delle interrogazioni..._")
                        return alternating_mode
                elif "Cancella" in day:
                    if counter != 0:
                        self.bot.send_message("", chat_index, "_Giorni cancellati con successo_")
                        self.bot.chats[chat_index].selected_days.clear()
                        self.bot.delete_messge(chat_index, self.bot.get_message_id(chat_index) - 2, False)
                    else:
                        self.bot.send_message("", chat_index, "_Non hai giorni da eliminare_")
                    counter = 0
                else:
                    day = self.weekday_from_day_name(day)

                    if day >= 0 and day <= 5:
                        counter += 1
                        self.self.bot.chats[chat_index].selected_days.append(int(day))
                        if counter != 1:
                            self.bot.delete_messge(chat_index, self.bot.get_message_id(chat_index) - 2, False)

                    else:
                        self.bot.send_message("", chat_index, "_Dato inconsistente_")
            except:
                self.bot.send_message("", chat_index, "_Errore! Dato inserito inconsistente_")
                print("Verified exception number: 5")

    def weekday_from_day_name(self, weekday):

        if weekday == "Lunedì":
            return 0
        elif weekday == "Martedì":
            return 1
        elif weekday == "Mercoledì":
            return 2
        elif weekday == "Giovedì":
            return 3
        elif weekday == "Venerdì":
            return 4
        elif weekday == "Sabato":
            return 5
        else:
            return 6

    def generic_mode(self, students_number):

        for i in range(students_number):
            self.self.bot.chats[self.bot.chat_index].classroom.append(Student(str(i+1), i+1))


def main():
    ot_programmer = OTProgrammer()
    global update
    global update_id
    global messages_counter 
    global thread_updater
    global exceptions
    exceptions = 0
    messages_counter = 0
    
    ot_programmer.bot.update_id = ot_programmer.bot.get_update_id()
    ot_programmer.bot.update = ot_programmer.bot.get_last_update(ot_programmer.bot.url)

    try:
        thread_updater = threading.Thread(target=ot_programmer.bot.updater)
        chat_getter = threading.Thread(target=ot_programmer.bot.get_chat)
    except:
        while True:
            ot_programmer.bot.send_message("", 0, "An error occurred")

    thread_updater.start()
    chat_getter.start()


if __name__ == "__main__":
    main()

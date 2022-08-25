import time
import datetime
import requests as requests
import json
from Entities.Chat import Chat, Message
from io import StringIO
import threading
import os


class Bot:
    def __init__(self, parent):
        self.token = ""
        self.url = f"https://api.telegram.org/bot{self.token}/"
        self.week = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
        self.threads = []
        self.chats = []
        self.default_days = [0] * 1000
        self.update_id = 0
        self.chat_id = 0
        self.thread_wait = 0
        self.messages_counter = 0
        self.admin_mode = False
        self.admin_id = 0
        self.chat_index = 0
        self.chat = 0
        self.is_text_message = False
        self.update = 0
        self.parent = parent

    def variable_controls(self, chat_index, variable, type):
        # controls for variable integrity

        self.check_commands(chat_index, variable)
        if type == int:
            return self.check_if_int(chat_index, variable)

    def read_message(self, output, type, chat_index):
        # waits for the client to send a message and read it

        try:
            self.send_message("", chat_index, output)
            # print(chats[chat_index].received_messages[len(chats[chat_index].received_messages)-1].message_id)
            message = self.chats[chat_index].received_messages[
                len(self.chats[chat_index].received_messages) - 1].message_id
            while True:
                time.sleep(0.5)
                if self.chats[chat_index].received_messages[
                        len(self.chats[chat_index].received_messages) - 1].message_id != message:
                    message = self.chats[chat_index].received_messages[
                        len(self.chats[chat_index].received_messages) - 1].text

                    self.variable_controls(chat_index, message, type)
                    self.update_id += 1
                    return message
        except:
            print("ReadMessage Exception")
            self.show_menu(chat_index, "")

    def get_last_update(self, req):
        # try:
        loop = True
        self.update_id = self.get_update_id()
        counter = 0
        # try:
        response = requests.get(req + "getUpdates")
        response = response.json()
        result = response["result"]
        total_updates = len(result) - 1

        # # except:
        #     self.send_message(0, "last update error, retry in 30 seconds")
        #     time.sleep(30)
        #     self.get_last_update(self.url)

        if self.messages_counter == 10:
            while loop:
                if result != []:

                    response = requests.get(req + "getUpdates?offset=" + str(self.update_id + 1))
                    response = response.json()
                    result = response["result"]

                    counter += 1
                else:
                    response = requests.get(req + "getUpdates")
                    response = response.json()
                    result = response["result"]

                    counter += 1

                if result != []:
                    print("new offset!")
                    self.messages_counter = 0
                    return result[0]

        return result[total_updates]  # get last record message update

        # except:
        #     print("connection error")
        #     self.get_last_update(req)

    def send_message(self, chat_id, chat_index, message):  # send message
        try:
            if chat_index == "":
                params = {"chat_id": chat_id, "text": message, "parse_mode": "markdown"}
            elif chat_id == "":
                params = {"chat_id": self.chats[chat_index].chat_id, "text": message, "parse_mode": "markdown"}
            response = requests.post(self.url + "sendMessage", data=params)
            return response
        except:
            print("connection error")
            self.send_message(chat_id, chat_index, message)

    def get_chat_id(self):
        while True:
            # try:
            self.chat_id = self.update["message"]["chat"]["id"]
            return self.chat_id
            # except:
            #     time.sleep(0.5)
            #     # print("Verified exception number: 9")

    def get_date(self, chat_index):

        if self.get_chat_id() == self.chats[chat_index].chat_id:
            date = self.update["message"]["date"]
            return date

    def get_message_id(self, chat_index):  # get message ID

        # try:
        if self.get_chat_id() == self.chats[chat_index].chat_id:
            message_id = self.update["message"]["message_id"]

        # except:
        #     if self.get_chat_id() == self.chats[chat_index].chat_id:
        #         message_id = update["edited_message"]["message_id"]
        # try:
            return message_id
        # except:
        #     self.get_message_id(chat_index)

    def get_message_text(self, chat_index):  # get message text

        self.is_text_message = True

        # try:
        if self.get_chat_id() == self.chats[chat_index].chat_id:
            message_text = self.update["message"]["text"]
            self.is_text_message = True
            return message_text

        # except:
        #     print("", end="")

    def get_user_infos(self):
        # get username, first name and last name of the user

        first_name = ""
        username = ""
        last_name = ""

        try:
            first_name = self.update["message"]["chat"]["first_name"]
        except:
            pass
        try:
            username = self.update["message"]["chat"]["username"]
        except:
            pass
        try:
            last_name = self.update["message"]["chat"]["last_name"]
        except:
            pass

        return first_name, username, last_name

    def delete_messge(self, chat_index, message_id, wait):
        if wait:
            time.sleep(3)
        # try:
            requests.get(self.url + "deleteMessage?chat_id=" + str(self.chats[chat_index].chat_id) +
                         "&message_id=" + str(message_id))
        # except:
        #     print("connection error")
        #     self.delete_messge(chat_index, message_id, wait)

    def send_perplexed_emoji(self, chat_index):
        self.send_message("", chat_index, "🤔")
        self.delete_messge(chat_index, self.get_message_id(chat_index) + 1, True)

    def remove_keyboard(self, chat_index, message):
        reply_markup = {'remove_keyboard': True}
        remove_keyboard_object = json.dumps(reply_markup)
        params = {"chat_id": self.chats[chat_index].chat_id, "text": message, "parse_mode": "markdown",
                  "reply_markup": remove_keyboard_object}
        # try:
        response = requests.post(self.url + "sendMessage", data=params)
        # except:
        #     print("connection error")
        #     self.remove_keyboard(chat_index, message)

        print("remove ", response)

    def show_one_button_keyboard(self, chat_index, message, button_string):
        reply_markup = {'keyboard': [
            [button_string]
        ],
            'resize_keyboard': True,
            'one_time_keyboard': True
        }

        keyboard_object = json.dumps(reply_markup)
        params = {"chat_id": self.chats[chat_index].chat_id, "text": message, "parse_mode": "markdown",
                  "reply_markup": keyboard_object}
        # try:
        response = requests.post(self.url + "sendMessage", data=params)
        # except:
        #     print("connection error")
        #     self.show_one_button_keyboard(chat_index, message, button_string)

        print(response)

    def show_rating_keyboard(self, chat_index):
        reply_markup = {'keyboard': [
            ['😣 1', '🙁 2', '🙂 3', '😃 4', '🤩 5']
        ],
            'resize_keyboard': True
        }

        keyboard_object = json.dumps(reply_markup)

        params = {"chat_id": self.chats[chat_index].chat_id,
                  "text": "Che voto daresti a questo bot?",
                  "parse_mode": "markdown",
                  "reply_markup": keyboard_object}
        # try:
        response = requests.post(self.url + "sendMessage", data=params)
        print("Rating restult")

        # except:
        #     print("connection error")
        #     self.show_rating_keyboard(chat_index)

        print(response)

    def show_weekdays_keyboard(self, chat_index, message):
        reply_markup = {'keyboard': [
            ['Lunedì', 'Martedì', 'Mercoledì'],
            ['Giovedì', 'Venerdì', 'Sabato', ],
            ['❌ Cancella', '✅ Conferma']
        ]
        }

        keyboard_object = json.dumps(reply_markup)
        # print(keyboard_object)
        params = {"chat_id": self.chats[chat_index].chat_id, "text": message, "parse_mode": "markdown",
                  "reply_markup": keyboard_object}
        # try:
        response = requests.post(self.url + "sendMessage", data=params)
        # except:
        #     print("connection error")
        #     self.show_weekdays_keyboard(chat_index, message)

    def show_menu_keyboard(self, chat_index, message):
        reply_markup = {'keyboard': [
            ['❄️ /newclass', '⚡️ /noclass'],
            ['🔥 /useclass', '❔ /help']
        ],
            'resize_keyboard': True
        }

        keyboard_object = json.dumps(reply_markup)
        # print(keyboard_object)
        params = {"chat_id": self.chats[chat_index].chat_id, "text": message, "parse_mode": "markdown",
                  "reply_markup": keyboard_object}
        # try:
        response = requests.post(self.url + "sendMessage", data=params)
        # except:
        #     print("connection error")
        #     self.show_menu_keyboard(chat_index, message)

        print(response)

    def help(self, chat_index, wait):

        self.send_message("", chat_index, "\nO.T.Programmer è il bot che permette di calcolare i "
                                          "piani per le interrogazioni programmate." +
                                          "\n\nCon il comando */newclass* hai la possibilità di "
                                          "creare una nuova classe. Ti verrà chiesto di scegliere "
                                          "una parola chiave che la identificherà univocamente, "
                                          "\n\nUna volta creata la classe, potrai utilizzarla con "
                                          "il comando */useclass*, che andrà a leggere in automatico "
                                          "gli studenti associati alla parola chiave. " +
                                          "\n\nSe non hai voglia di creare una classe, puoi usare "
                                          "la modalità */noclass*. Non dovrai inserire nessuno studente, "
                                          "basterà scrivere da quante persone è composta la tua classe, "
                                          "il programma ritornerà i numeri dell'elenco come riferimento "
                                          "per gli studenti della tua classe." +
                                          "\n\nQuando hai scelto la modalità, sarà necessario inserire "
                                          "alcune informazioni sul piano di interrogazioni che hai "
                                          "intenzione di programmare: il nome della materia "
                                          "dell’interrogazione, "
                                          "la data del primo giorno delle interrogazioni, "
                                          "quanti studenti devono essere interrogati al giorno "
                                          "e i giorni della settimana in cui si verificheranno "
                                          "le interrogazioni (puoi scegliere più volte lo stesso "
                                          "giorno per indicare che si interrogherà più ore in "
                                          "quel giorno della settimana). " +
                                          "\n\nIl bot è ancora in beta, puoi segnalare bug o"
                                          " eventuali migliorie qui:\nlorenzo.abati@istitutoberetta.edu.it")
        if wait:
            self.show_one_button_keyboard(chat_index, "Premi back per tornare al menu principale", "BACK")
            self.read_message("", StringIO, chat_index)
            self.show_menu(chat_index, "")

    def commands_only_at_startup(self, chat_index):
        self.help(chat_index, False)

    def check_if_int(self, chat_index, variable):
        # controls if the variable is int (if its not goes abck to menu)

        # try:
        int(variable) + 1
        # except:
        #     self.send_message("", chat_index, "_Errore! Dato inserito inconsistente, torno al menu principale_")
        #     print("Verified exception number: 2")
        #     self.show_menu(chat_index, "")

        return True

    def refresh_values(self, chat_index):
        # refresh variable values (needed to run multiple times the program without restarting it)

        self.chats[chat_index].classroom.clear()
        self.chats[chat_index].selected_days.clear()
        self.chats[chat_index].interrogation_days.clear()
        self.chats[chat_index].days_object_counter = 0
        self.chats[chat_index].students_per_day = 0
        self.chats[chat_index].students_number = 0

    def show_menu(self, chat_index, choose):
        self.refresh_values(chat_index)

        if choose == "":
            self.show_menu_keyboard(chat_index, "-\n*MENU PRINCIPALE*\n-\n\n" +
                               "-\n" +
                               "*❄️ /newclass -> crea una nuova classe*\n\n" +
                               # "-\n"+
                               "*🔥 /useclass -> usa una classe già esistente*\n\n" +
                               # "-\n"+
                               "*⚡️ /noclass -> usa numeri dell'elenco*\n\n" +
                               # "-\n"+
                               "*❔ /help -> funzionamento del bot*\n" +
                               "-")

        while True:
            time.sleep(0.5)
            access = False
            # to avoid the execution of the other functions when the client doesn't enter a valid command (*)

            generic_mode = False
            if choose == "":
                menu = self.read_message("", StringIO, chat_index)
            else:
                menu = "/" + choose

            if "/useclass" in menu:
                self.remove_keyboard(chat_index, "_USECLASS_")
                self.parent.read_classroom(chat_index)
                access = True
            elif "/newclass" in menu:
                self.remove_keyboard(chat_index, "_NEWCLASS_")
                self.parent.write_classroom(chat_index)
                access = True
            elif "/noclass" in menu:
                self.remove_keyboard(chat_index, "_NOCLASS_")
                generic_mode = True
                access = True
            elif "/help" in menu:
                self.remove_keyboard(chat_index, "_ISTRUZIONI_")
                # os.system
                self.help(chat_index, True)
            elif menu == "admin":
                # admin_menu(chat_index)
                pass
            elif menu != "/useclass" and menu != "/newclass" and menu != "/help" and menu != "/noclass":
                self.send_perplexed_emoji(chat_index)

            if access:  # (*)
                mode = self.parent.input_data(chat_index, generic_mode)
                self.parent.days_calculator(mode, chat_index)
                self.parent.students_distributor(chat_index)
                self.parent.output_interrogation_plan(chat_index)

    def updater(self):
        while True:
            time.sleep(self.thread_wait)
            time.sleep(0.5)
            self.update = self.get_last_update(self.url)

    def get_chat(self):
        self.chat_index = 0
        message_id = ""
        self.is_text_message = False
        test_message_id = 0

        while True:

            time.sleep(0.5)
            chat_id_in_chats = False
            chat_id = self.get_chat_id()

            if chat_id is None:
                time.sleep(0.6)
                chat_id = self.get_chat_id()

            for i in range(len(self.chats)):

                if chat_id == self.chats[i].chat_id:
                    chat_id_in_chats = True
                    break

            for i in range(len(self.chats)):
                if chat_id == self.chats[i].chat_id:
                    self.chat_index = i

            if chat_id_in_chats:
                result = self.get_message_text(self.chat_index)

                if result == None:
                    self.is_text_message = False

                    if exceptions == 0 \
                            or test_message_id != self.get_message_id(self.chat_index) \
                            and test_message_id != 0:
                        test_message_id = self.get_message_id(self.chat_index)
                        self.send_perplexed_emoji(self.chat_index)
                        print("Exception number: 8")
                        exceptions += 1

                if self.is_text_message:
                    # print("is text message")
                    # get message and add it to his chat

                    if len(self.chats[self.chat_index].received_messages) == 0:
                        message = Message(self.chats[self.chat_index].chat_id, self.get_message_id(self.chat_index),
                                          self.get_message_text(self.chat_index))
                        self.chats[self.chat_index].received_messages.append(message)
                        message_id = self.get_message_id(self.chat_index)
                        print("-----------\nnew MSG: " + str(self.get_user_infos()) + "\ntime: " + str(
                            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\ntext: " + str(
                            self.chats[self.chat_index].received_messages[
                                len(self.chats[self.chat_index].received_messages) - 1].text))

                        if message.chat_id != self.admin_id and self.admin_mode == True:
                            self.send_message(self.admin_id, "", "-----------\nnew MSG: " + str(
                                self.get_user_infos()) + "\ntime: " + str(
                                datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\ntext: " + str(
                                self.chats[self.chat_index].received_messages[
                                    len(self.chats[self.chat_index].received_messages) - 1].text))
                        self.messages_counter += 1

                        exceptions = 0

                    elif message_id != self.get_message_id(self.chat_index):
                        message = Message(self.chats[self.chat_index].chat_id, self.get_message_id(self.chat_index),
                                          self.get_message_text(self.chat_index))
                        self.chats[self.chat_index].received_messages.append(message)
                        message_id = self.get_message_id(self.chat_index)
                        print("-----------\nnew MSG: " + str(self.get_user_infos()) + "\ntime: " + str(
                            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\ntext: " + str(
                            self.chats[self.chat_index].received_messages[
                                len(self.chats[self.chat_index].received_messages) - 1].text))

                        if message.chat_id != self.admin_id and self.admin_mode == True:
                            self.send_message(self.admin_id, "", "-----------\nnew MSG: " + str(self.get_user_infos()) + "\ntime: " + str(
                                datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\ntext: " + str(
                                self.chats[self.chat_index].received_messages[len(self.chats[self.chat_index].received_messages) - 1].text))
                        self.messages_counter += 1

                        exceptions = 0
                # else:
                #     print("is not text message")

            else:
                # add chat with new chat id in chats[]
                self.chat = Chat(chat_id)
                self.chats.append(self.chat)

                for i in range(len(self.chats)):
                    if chat_id == self.chats[i].chat_id:
                        self.chat_index = i
                chat_id_is_in_file = False
                chats_file = open("chats.csv", "r")

                for line in chats_file:
                    if str(self.chats[self.chat_index].chat_id) in line:
                        chat_id_is_in_file = True
                chats_file.close()

                if chat_id_is_in_file == False:
                    chats_file = open("chats.csv", "a")
                    chats_file.write(str(self.chats[self.chat_index].chat_id) + " - " + str(self.get_user_infos()) + "\n")
                    chats_file.close()

                print("-----------\nnew USR: " + str(self.get_user_infos()) + "\nchat id: " + str(
                    self.chats[self.chat_index].chat_id) + "\ntime: " + str(
                    datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\nCHAT_INDEX: " + str(self.chat_index))
                self.commands_only_at_startup(self.chat_index)
                thread = threading.Thread(target=self.show_menu, args=(self.chat_index, "",))
                thread.start()
                self.threads.append(thread)

    def get_update_id(self):
        # try:
            while True:
                time.sleep(0.5)
                response = requests.get(self.url + "getUpdates")
                response = response.json()
                result = response["result"]
                total_updates = len(result) - 1
                if result != []:
                    return result[total_updates]["update_id"]
        # except:
        #     print("connection error")
        #     self.get_update_id()

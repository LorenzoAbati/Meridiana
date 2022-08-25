import hashlib
from io import StringIO


class Admin:

    def __init__(self, bot):
        self._bot = bot

    def admin_menu(self, chat_index):
        wrong_password = True
        global admin_id, admin_mode
        print("Admin mode requested")
        self._bot.remove_keyboard(chat_index, "_ADMIN MODE_")

        while wrong_password:

            password = hashlib.sha256(self._bot.read_message("Enter password: ",
                                                             StringIO,
                                                             chat_index).encode()).hexdigest()

            if password == "6d2f74c76ddfb91030c3997c0591d1b15888bb8194c8c840f18716f41c2e8a86":
                wrong_password = False
                self._bot.send_message("", chat_index, "*ACCESS GRANTED*")

                message_id = self._bot.get_message_id(chat_index)
                self._bot.delete_messge(chat_index, message_id, False)
            else:
                self._bot.send_message("", chat_index, "*ACCESS DENIED*")

        while True:

            admin_menu = self._bot.read_message(
                "ADMIN MENU" +
                "\n - /broadcast = broadcast a message to all bot members" +
                "\n - /enablegetmessages = receive all messages sent to this bot (while online)" +
                "\n - /disablegetmessages = disable get messages" +
                "\n - /sendmessage = send message from chat id", StringIO, chat_index)

            if admin_menu == "/broadcast":
                message_to_broadcast = self._bot.read_message("message to broadcast:", StringIO, chat_index)
                try:
                    self._bot.broadcast_message(message_to_broadcast)
                    self._bot.send_message("", chat_index, "Broadcast success")
                except:
                    self._bot.send_message("", chat_index, "Broadcast error")

            elif admin_menu == "/enablegetmessages":

                admin_mode = True
                admin_id = self._bot.chats[chat_index].received_messages[
                    len(self._bot.chats[chat_index].received_messages) - 1].chat_id
                self._bot.send_message("", chat_index, "get massages enabled")

            elif admin_menu == "/disablegetmessages":

                admin_mode = False
                self._bot.send_message("", chat_index, "get massages disabled")

            elif admin_menu == "/sendmessage":
                print("ajsdba")
                try:
                    chat_id = self._bot.read_message("chat id to send message", int, chat_index)
                    message = self._bot.read_message("message to send", StringIO, chat_index)
                    self._bot.send_message(chat_id, "", message)
                    self._bot.send_message("", chat_index, "message sent successfully")
                except:
                    self._bot.send_message("", chat_index, "an arror occurred")

    def broadcast_message(self, message):
        # broadcast a messages to all the chats

        chat_ids_from_file = []
        chats_file = open("chats.csv", "r")
        chat_id = [] * 2

        for line in chats_file:
            chat_id = line.split("-")
            chat_ids_from_file.append(chat_id)

        for i in range(len(chat_ids_from_file)):
            print("message sent to: " + chat_ids_from_file[i][1])
            self._bot.send_message(chat_ids_from_file[i][0], "", message)

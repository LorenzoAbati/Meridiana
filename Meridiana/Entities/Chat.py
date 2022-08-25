class Chat:

    days_object_counter = 0
    students_per_day = 0
    students_number = 0
    school_subject = ""

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.received_messages = []
        self.classroom = []
        self.selected_days = []
        self.interrogation_days = []


class Message(Chat):

    def __init__(self, chat_id, message_id, text):
        super().__init__(chat_id)

        self.message_id = message_id
        self.text = text

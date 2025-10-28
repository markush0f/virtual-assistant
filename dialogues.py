import customtkinter as ctk


class DialogueApp(ctk.CTk):
    def __init__(self, dialogues):
        super().__init__()

        self.dialogues = dialogues
        self.index = 0

        self.title("ABAMA Jr.Suite")

        width, height = 500, 150

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        pos_x = (screen_w // 2) - (width // 2)
        pos_y = (screen_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        self.label = ctk.CTkLabel(
            self,
            text=self.dialogues[self.index],
            font=("Arial", 16),
            wraplength=300,
            justify="center",
        )
        self.label.pack(pady=20, padx=10)

        self.button = ctk.CTkButton(
            self, text="▶", width=100, command=self.next_dialogue
        )
        self.button.pack(pady=10)

        self.bind("<Return>", lambda event: self.next_dialogue())

    def next_dialogue(self):
        self.index += 1
        if self.index < len(self.dialogues):
            self.label.configure(text=self.dialogues[self.index])


if __name__ == "__main__":

    dialogues = [
        "No somos nada pero puedes rodar conmigo",
        "Creí escucharte decir que ese pussy es mio.",
        "Co-Co-Con mis negros y mixtos antitusivo.",
        "Subidos al techo solar tirando signos",
        "Oh no, en la Suburban LT",
        "O las lágrimas o el humo empañaron el Bagatelle",
        "Estoy preocupado por Yuki, estas Pascuas estoy pa el",
        "No pal hate, van a hablar de mí hasta que le baje al flex",
        "Y estoy saucin', no te escucho",
        "la-la-la-la 😌",

    ]

    ctk.set_appearance_mode("dark") 
    ctk.set_default_color_theme("blue")

    app = DialogueApp(dialogues)
    app.mainloop()

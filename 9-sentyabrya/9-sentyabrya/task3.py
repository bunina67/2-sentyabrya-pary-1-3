class MediaPlayer:
    def open(self, file):
        self.filename = file

    def play(self):
        print(f"Воспроизведение {self.filename}")

media1 = MediaPlayer()
media2 = MediaPlayer()

media1.open("file1.mp3")
media2.open("file2.mp4")

media1.play()
media2.play()
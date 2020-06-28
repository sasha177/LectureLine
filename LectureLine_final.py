import time
import wikipedia
import speech_recognition as sr
import pyttsx3
import string
from LectureLine_wordstoignore import common_words
import wikipediaapi

print()
print()
name = input("Enter your name: ")
print("Hello", name + "! Thank you for choosing LectureLine. Lets get started!")
time.sleep(2)
print("Soon, LectureLine will start listening for the lecture and make your notes!")
time.sleep(2)
print("When you are ready for LectureLine to begin, please let us know!")


while 1:
    ready = input("Ready to begin? (Y/N): ")
    if ready == "Y" or ready == "y":
        n = 1
        break

r = sr.Recognizer()
important_words = []

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

speech = ""

while n == 1:
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            speech = MyText
            MyText = MyText.lower()
            break
    except sr.UnknownValueError:
        print("No speech detected.")

file = open("thelecture_transcription.txt", "w")
file.write(MyText)
file.close()


class KeywordFinder:
    def __init__(self, train_file):
        self.keys = {}
        with open(train_file, 'r') as tf:
            translator = str.maketrans('', '', string.punctuation)
            for line in tf:
                words = line.translate(translator).lower().split()
                for word in words:
                    if word in common_words:
                        continue
                    factor = 1 / len(words)
                    if word in self.keys:
                        self.keys[word] = [0, self.keys[word][1] + 1, self.keys[word][2] + factor]
                    else:
                        self.keys[word] = [0, 1, factor]

        for word in self.keys:
            self.keys[word] = [self.keys[word][1] * self.keys[word][2], self.keys[word][1], self.keys[word][2]]

        s = [(k, self.keys[k]) for k in sorted(self.keys, key=self.keys.get)]
        for k, v in s:
            if v[1] > 1:
                important_words.append(k)
                #print(k, v) #prints words that are important


if __name__ == '__main__':
    kf = KeywordFinder('thelecture_transcription.txt')

print()
print()
print()
print()
print("Notes:")

import requests

data = {
  'text': speech
}

response = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)
print(response.text)

links = []
for x in important_words:
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(x)
    page88 = wikipedia.page(x)
    url = page88.images[0]
    print(url)
    print(page_py.fullurl)
    links.append(page_py.fullurl)
    links.append(url)


space = " , "
while 1:
    print99 = input("Would you like to save these notes? (Y/N): ")
    if print99 == "Y" or print99 == "y":
        name77 = input("What would you like to name these notes?: ")
        notesname = str(name77) + ".txt"
        file = open(notesname, "w")
        file.write(response.text)
        file.write(space)
        for x in links:
            file.write(x)
            file.write(space)
        file.close()
        print("Your notes have been saved!")
        break
    else:
        print("No problem!")
        break


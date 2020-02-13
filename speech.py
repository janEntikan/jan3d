from random import uniform

consonants = "mnptkswlj"
vowels = "iueoa"
SYLLABLES = {
    "":0,
    "n":0,
        }
i = 1
for vowel in vowels:
    SYLLABLES[vowel] = i
    i += 1
for consonant in consonants:
    for vowel in vowels:
        SYLLABLES[consonant+vowel] = i
        i += 1

class Speech:
    def __init__(self, voice):
        self.voice = voice
        self.pitch = 1
        self.pitch_speed = 0.01
        self.talking = [("",1,1)]

    def say(self, input):
        self.time = 0
        self.time_in_sample = 0
        words = input.split();
        pitch = 1.4

        for w, word in enumerate(words):
            syllables = [word] # TODO: split the word in syllables
            for s, syllable in enumerate(syllables):
                if w == len(words) -1:
                    length = 0.4
                else:
                    length = uniform(0.2, 0.35)
                pitch -= 0.05
                self.talking.append((syllable, length, pitch))
        self.talking.append(("", 1, 1)) # add a pause after word
        self.play()

    def play(self, offset=0):
        if len(self.talking) > 0:
            self.voice.setTime(SYLLABLES[self.talking[0][0]]+offset)
            self.voice.play()
        else:
            self.voice.setPlayRate(0)
        self.voice.setVolume(0) # set volume to zero to battle pop


    def update(self, task):
        if len(self.talking) > 0:
            dt = globalClock.getDt()
            self.time += dt
            self.time_in_sample += dt

            if self.talking[0][0] == "":
                self.voice.setVolume(0)
            else:
                self.voice.setVolume(1)
            
            if self.pitch < self.talking[0][2]:
                self.pitch += self.pitch_speed
            if self.pitch > self.talking[0][2]:
                self.pitch -= self.pitch_speed
            self.voice.setPlayRate(self.pitch)

            if self.time > self.talking[0][1]:
                self.time = 0
                self.time_in_sample = 0
                self.talking.pop(0)
                self.play()
            elif self.time_in_sample > 1:
                restart_time = 0.8
                self.time_in_sample = restart_time
                self.play(0.8)

        return task.cont
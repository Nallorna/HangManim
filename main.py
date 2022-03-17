from manimlib import *

class cTextbox(Textbox): #Förändrar objektet Textbox så den får en annan färg samt  tar bort möjligheten att inaktivera den
    CONFIG = {
        "value_type": np.dtype(object),

        "box_kwargs": {
            "width": 6,
            "height": 2,
            "fill_color": BLUE_D,
            "fill_opacity": 0,
            "stroke_width": 0,
        },
        "text_kwargs": {
            "color": BLACK,
            "font_size": 100,
        },
        "text_buff": 0,
        "isInitiallyActive": True,
        "active_color": BLUE_D,
        "deactive_color": BLACK,
    }
    def box_on_mouse_press(self, mob, event_data):
        pass

class cNumberPlane(NumberPlane):  #Ändrar färgen på backgrunden
    CONFIG = {
        "axis_config": {
            "stroke_color": WHITE,
            "stroke_width": 0,
            "include_ticks": False,
            "include_tip": False,
            "line_to_number_buff": SMALL_BUFF,
            "label_direction": DR,
            "number_scale_val": 1,
        },
        "y_axis_config": {
            "label_direction": DR,
        },
        "background_line_style": {
            "stroke_color": GREY_A,
            "stroke_width": 2,
            "stroke_opacity": 1,
        },
        # Defaults to a faded version of line_config
        "faded_line_style": None,
        "x_line_frequency": 4,
        "y_line_frequency": 4,
        "faded_line_ratio": 4,
        "make_smooth_after_applying_functions": True,
    }


class cTitle(Title): #Ändrar färgen på titel mobjectet som visas längts upp på skärmen
    CONFIG = {
        "scale_factor": 1,
        "include_underline": True,
        "underline_width": FRAME_WIDTH - 2,
        # This will override underline_width
        "match_underline_width_to_text": True,
        "underline_buff": SMALL_BUFF,
    }


class HangWord:
    #Klassvariabel
    _amount_initiated = 0 #Klassvariabel för att ser hur många objekt som är instansierade.

    def __new__(cls, word): #Förhindrar att fler än ett "Word" objekt att existera, samt förhindrar inkorrekta ord att instansieras.
        if cls._amount_initiated > 0:
            raise Exception("Only one \"Word\" object can be initiated")
        elif type(word) == str and str(word).isalpha():
            return object.__new__(cls)
            cls._amount_initiated += 1
        else:
            raise TypeError()

    def __init__(self, word): #Instansierar objektet samt delar upp ordet i en dictionary där key'n är bokstaven och value'n är vad som visas (Value'n är antigen "_" eller bokstaven där både är inkapsalde av "{ }"
        self._word = {}
        self.guessed = []
        for n in word.upper():
            n = n + str(len([x for x in self._word if n in x]))
            self._word[n] = "{\_}"

    def __str__(self): #Istället för "show_word" (Skriver ut ordet)
        return "".join(self._word.values())

    def __len__(self): #Istället för "get_lengt" (Skrivet ut ordets längd)
        return len(self._word)

    def __eq__(self, guess): #Istället för "reveal_all" (Kollar om en gissning på ordet är korrekt. Om gissningar är korrekt visas alla bokstäverna)
        if type(guess) == str and str(guess).isalpha():
            guess_validity = guess == "".join(filter(lambda x: not x.isnumeric(), "".join(self._word.keys())))
            if guess_validity:
                for key in self._word.keys():
                    self._word[key] = "".join(filter(lambda x: not x.isnumeric(), key))
            return guess_validity
        else:
            raise TypeError()

    def __contains__(self, letter): #Istället för "reveal_one" (Kollar om en bokstav finns i ordet. Om bokstaven finns blir denna synlig)
        if type(letter) == str:
            if len(letter) == 1 and str(letter).isalpha():
                if letter not in self.guessed:
                    letter_in_word = len([x for x in self._word if letter in x])
                    for n in range(letter_in_word):
                        self._word[letter + str(n)] = "{" + letter + "}"
                    self.guessed.append(letter)
                else:
                    letter_in_word = False
                return bool(letter_in_word)
            else:
                raise ValueError()
        else:
            raise TypeError()

    def all_revealed(self): #Kollar om alla bokstäver är synliga
        return "".join(self._word.values()) == "".join(filter(lambda x: not x.isnumeric(), "".join(self._word.keys())))


class HangManim(Scene):
    CONFIG = {"random_seed": None} #Gör så slumpmässiga saker sker (Används inte i programmet, men kan va bra ha)
    pendinganimations = [] #En lista för alla animationerna som skall ske samtidigt


    def construct(self):
        self.add(cNumberPlane()) #Lägger till bakgrundsbilden
        self.healthleft = 7 #Antalet liv kvar
        self.wordclass = HangWord("CAPITULATE") #Ordet
        self.animationon = False #Används för att identifiera om en animation är igång
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z', ]

        self.word = Tex(str(self.wordclass), font_size=100, color=BLACK).center().shift([0, -1.75, 0]) #Ordet man ska gissa (Visas)
        self.health = Tex("{ Guesses \quad left: \quad} { " + str(self.healthleft) + " }", font_size=50,
                          color=BLACK).shift([0, 2.25, 0]) #Hur mycket liv som är kvar (Visas)
        self.input = cTextbox().center().shift([0, 0.25, 0]) #För att visa ens input
        self.title = cTitle("HangManim", font_size=25, color=BLACK) #Titeln

        self.manim_alphabet = Group() #En mobejct grupp för alfabetet längst ner
        for letter in self.alphabet:
            self.manim_alphabet += Text(text=letter, font_size=30, color=GREY_E)
        self.manim_alphabet.arrange_in_grid(2, buff=0.35).shift([0, -3, 0])

        self.intro()
        self.add(self.title,self.input, self.word, self.health, self.manim_alphabet) #Lägger till alla mobject för spelet
        self.wait()

    def intro(self): # Ett kort intro där spelets namn visas
        gametitle = Text("HangManim", font_size=150, color=BLACK).shift([0, 0.5, 0])
        self.play(FadeIn(gametitle))
        self.wait(1)
        self.play(FadeOut(gametitle))

    def ending(self): #Visar antigen gameover eller victory (När spelet är slut)
        if self.wordclass.all_revealed():
            text, colour = "VICTORY", GREEN
        else:
            text, colour = "GAMEOVER", RED
        self.Animate()
        self.wait(0.5)
        self.mobjects.clear()
        self.add(cNumberPlane())
        self.play(FadeIn(Text(str(text), font_size=150, color=colour).shift([0, 0.5, 0])))
        self.wait()

    def on_key_press(self, symbol, modifiers): #Håller koll på vilka knappttryck användaren gör
        char = chr(symbol)

        if self.input.isActive and not self.animationon: #Kolla så ingen animations är igång och så input mobjectet är aktiverat
            old_value = self.input.get_value()
            new_value = old_value
            if old_value in self.wordclass.guessed:
               new_value = ""
            elif char.isalpha():
                new_value = old_value + char.upper()
            elif symbol == PygletWindowKeys.BACKSPACE:
                new_value = old_value[:-1] or ''
            elif symbol == PygletWindowKeys.ENTER and old_value:
                new_value = ""
                self.answer()
            self.input.set_value(new_value)

            return False

    def answer(self): #Aktiveras när "enter" har klickats på. Kollar om ens gissning är ordet (Om gissningen är längre en 1 bokstav), om bokstaven finns i ordet och uppdaterar livet eller ordet.
        guess = self.input.get_value().upper()
        self.input.set_value("")
        if len(guess) != 1:
            correct = guess == self.wordclass
        else:
            correct = guess in self.wordclass
            self.update_alpha(guess, correct)
        if correct:
            self.word = self.update_word()
        else:
            self.health = self.lower_health(len(guess))
        if self.wordclass.all_revealed() or self.healthleft == 0:
            self.ending()
        else:
            self.Animate()

    def Animate(self): #Funktion som gör så flera animationer kan animeras samtidigt
        self.animationon = True
        self.play(*self.pendinganimations, run_time=2)
        self.pendinganimations.clear()
        self.animationon = False

    def update_word(self): #Updaterar ordet som visas
        new_word = Tex(str(self.wordclass), font_size=100, color=BLACK)
        if not self.wordclass.all_revealed():
            new_word.match_width(self.word)
            new_word.match_points(self.word)
            new_word.align_to(self.word, DOWN)

        self.pendinganimations.append(FadeTransformPieces(self.word, new_word))

        return new_word

    def update_alpha(self, guess, boolean): #Updaterar alfabetet så en bokstav antigen blir grön (rätt gissning) eller röd (fel gissning)
        for letter in guess:
            try:
                if boolean:
                    colour = "#009200"
                else:
                    colour = "#8b0000"
                self.pendinganimations.append(
                    FadeToColor(self.manim_alphabet[self.alphabet.index(letter)], color=colour))
            except:
                pass

    def lower_health(self, amount): #Minskar spelaren liv (Ungefär på samma sätt som update_word)
        if amount > self.healthleft:
            amount = self.healthleft
        self.healthleft -= amount
        new_word = Tex("{ Guesses \quad left: \quad} { " + str(self.healthleft) + " }", font_size=50, color=BLACK)
        new_word.match_width(self.health)
        new_word.match_points(self.health)
        new_word.align_to(self.health, DOWN)
        self.pendinganimations.append(FadeTransformPieces(self.health, new_word))

        return new_word

    # Alla funktioner under tar bort viss  interaktiv funktionalitet som kan få programmet att inte fungera som det ska
    def on_mouse_motion(self, point, d_point):
        pass
    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        pass
    def on_mouse_scroll(self, point, offset):
        pass

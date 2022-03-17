# HangManim - Dokumentation
Det finns en rapport som beskriver hur du gjort samt en utvärdering av fördelar och nackdelar med ditt upplägg

## Programmet
Grunden till HangManim är ett bibliotek som heter Manim samt Hangman-spelet
### Manim - GUI:n

#### Vad är det?
Biblioteket som ligger i grunden till självaste GUI:n är Manim. Manim är ett videoanimerings bibliotek skapat för att animera matematik-videor. I Manim finns det en interaktiv funktionalitet för att man skall kunna dynamiskt kunna testa videon och testa olika alternativ. Däremot går denna interaktivitet användas som en, ytterst begränsad, GUI.Biblioteket som ligger i grunden till självaste GUI:n är Manim. Manim är ett videoanimerings bibliotek skapat för att animera matematik-videor. I Manim finns det en interaktiv funktionalitet för att man skall kunna dynamiskt kunna testa videon och testa olika alternativ. Däremot går denna interaktivitet användas som en, ytterst begränsad, GUI. 
#### Begränsningar
Då Manim är gjort för videoanimering finns det tydliga begränsningar i funktionaliteten. Mobject:en, de grundläggande elementen i GUI:n, är i grunden inte gjorda för att förändras utifrån olika typer av inputs. Därav uppstår svårigheter med att skapa en spel-funktionalitet. 

Ett av de största problemen är prestandan av programmet. Då varje Mobject måste individuellt animeras innan de kan visas eller förändras kan det ibland ta lång tid för att spelet ska uppdateras efter en input. Detta blev också problematiskt då inputen gick snabbare än förändringarna, vilket kunde resultera i att programmet kraschade eller visade felaktigheter. Detta problem löste jag via att stoppa all input medan en animation förbereddes och visades.

Manim är gjort för en linjär process utan loopar. Detta är för att en video bara behöver förhandsvisas och inte vänta på att användaren klickar på en knappt. Detta fixade jag via att kalla en wait-metod utan slut. Därav kunde jag ha klass funktioner som programmet loopade igenom utan att det stängde av sig själv.

#### Möjligheter
Manim är gjort för att vara vackert. Det är gjort för att ha animationer som ser professionella ut och sker flytande. Detta gör så att programmet ser mer modernt ut, i jämförelse med Tkinter, och gör så att förändringarna i GUI:n ser naturligt ut. 

Det finns också flera olika Mobjects i Manim som kan användas som widgets i GUI:n. Allt från text till knappar. I mitt program använder jag mig endast av Tex-mobjects, LaTeX text, och en inputbox för att kunna visualisera bokstäverna man skriver in. 

Animeringsmässigt har manim flera olika alternativ. Ett sätt för att förenkla animationerna och positionera mobjectens bättre är groups. Jag använde groups för alfabeten för att placera de jämnt och kunna ändra bokstäversfärger via att komma åt varje mobejct precis som en lista. En annan typ av group som jag använde var LaTex Groups. Detta betyder att varje bokstav i min text kan hanteras som ett mobject. Något som gjorde animationsmetoden FadeTransformPieces som endast transformerar en bokstav och inte hela ordet möjlig.

#### Vad är Scene och klassen HangManim?
I Manim är allt uppbyggt av Scener som är strukturerade så att animationerna sker i construct(self). I grunden ska det mesta ske i construct men då jag ville ha interaktivitet behövde jag skapa egna metoder som kallades på beroende på användarens input. För att få användarens input använde jag metoden on_key_press, som finns naturligt i Manim, med förändringar till vilka symboler som var tillåtna och vad som händer beroende på vilken knapp som trycktes.

För att uppdatera antalet liv och ordet man skulle gissa på behövde jag skapa en kopia av mobjectet där stringen är updaterad och animera en transformation från det gamla mobjectet till det nya

#### HangManim:s klassvariabler
De klassvariablerna som finns är:

    CONFIG = {"random_seed": None}
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z', ]
    pendinganimations = []

Den variablen som är relevant att ta upp är pendinganimations. Denna variabel används för att samla alla animationer som skall genomföras och sen genomför dem samtidigt via min egen animation-funktion. 

#### Vad gör de andra klasserna?
De andra klasserna jag har är subklasser av olika mobjects där jag ändrar i CONFIG för att ändra olika färger, text-typsnitt etc 

### Hangman – Funktionaliteten
Jag valde att självaste ordet och hur programmet håller koll på om en gissning är i ordet och om alla bokstäver är gissade på fick vara Hangman-spelets Word klass.
#### Vad är nytt/gammalt
Allt är mer eller mindre samma förutom hur textsträngen är uppbyggd.  Skillnaden ligger i att varje bokstav är inkappslad av ”{” + bokstav + ”}” för att Tex-mobjectet skulle fungera. Annars är allt likadant, förutom namnet som blev HangWord.
##### Varför
Anledningen till att jag inte anpassade HangWord yttligare är för att självaste bokstavsbytet, animationerna och hanteringen av mobjecten fick vara i Manims Scene-klass. Detta då komplexiteten i att göra så HangWord ärvde av Tex-klassen.

## Utvärdering
Programmet saknar viss funktionalitet som jag i grunden hade velat inkludera. Dock blev det oerhört svårt och prestanda krävande på grund av Manim begränsningar. Dock fungerar programmet som ett spel, med accepterar prestanda, och kraschar inte. 

### Fördelar
Den huvudsakliga fördelen är det estetiska. Programmet ser bra ut och animeringarna är, enligt mig, vackra. Spelet är lätt att förstå utan förklaring vilket jag ser som en fördel då det är svårt att inkludera en ”guide” i programmet
### Nackdelar
Manim är den största begränsningen. Mycket funktionalitet såsom olika spelare, bestämma eget ord, köra om spelet samt en förklaring till hur spelet fungerar blev antigen oerhört svårt eller opartiskt.  Olika antal spelare hade försämrat prestandan väsentligt och öka risken för att programmet kraschar på grund av överbelastning. Det skulle också vara svårt att använda samma knappt, i detta fall ”enter”, för att göra olika saker. Då strukturen är för en video blir det svårt att ha flera olika ”sidor” i programmet vilket försvårar konstruktionen av en huvudmeny etc. 

## Övrigt
För att köra programmet måste man köra det i terminalen



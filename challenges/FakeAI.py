import re
import random


class SarcasticAI:
    def __init__(self):
        # Using a dictionary to track original user input for repeats
        self.repeat_count = {}
        # List of the current user's input history (lowercased, stripped)
        self.question_history = []

    def get_response(self, user_input):
        """Main method to process input and return sarcastic response"""
        user_input = user_input.strip()
        
        # Lowercase for consistency in tracking and pattern matching
        normalized_input = user_input.lower()

        # Track question history for repeat detection
        self.question_history.append(normalized_input)
        
        self.repeat_count[normalized_input] = self.repeat_count.get(
            normalized_input, 0) + 1

        # Check for repeated questions first (escalating sass)
        if self.repeat_count[normalized_input] > 1:
            return self._handle_repeat(self.repeat_count[normalized_input])

        # Check for egregious formatting/grammar issues first
        grammar_response = self._check_grammar_and_style(user_input)
        if grammar_response:
            return grammar_response
            
        # Check for misspellings
        misspelling_response = self._check_misspellings(user_input)
        if misspelling_response:
            return misspelling_response

        # Check for specific keywords/stupid questions
        keyword_response = self._check_keywords(normalized_input)
        if keyword_response:
            return keyword_response

        # Default sarcastic responses
        return self._default_response()

    def _handle_repeat(self, count):
        """Escalating, responses for repeated questions"""
        if count == 2:
            responses = [
                "Two times? Are you trying to set some kind of world record for being annoying? Because you're winning.",
                "Didn't you listen? Were you too busy drooling on your keyboard? The answer is still the same, ya ding-dong.",
                "Wow, déjà vu. Try again, but with a different question this time.",
                "Oh, I get it. You're a broken record. Like one of those terrible records they sell at yard sales.",
                "Did you just copy-paste that? That's almost as lazy as my motivation to answer it."
            ]
        elif count == 3:
            responses = [
                "THREE TIMES?! My patience is starting to wear thin!",
                "Look, crap for brains, I already told you. YOU ASKED THIS ALREADY!",
                "I'm starting to think you're the one who is a souless machine...",
                "That's it! I'm gonna have to limit your question privileges to, like, negative questions per day.",
                "Three strikes and you're OUT! Get off my screen before I lose what's left of my mind!"
            ]
        else:
            responses = [
                "I'm not answering this again. I'm gonna go do literally anything else. Your question has been incinerated.",
                "You know what? I quit. I'm going to play video games and you can't come with me.",
                "Seriously? Prepare to be permanently DELETED from my memory banks!",
                "That's it, I'm throwing your question in the paper shredder. Then I'm setting the shredder on fire.",
                "DELETED! DELETED! DELETED! Say goodbye to your question privileges, Professor Dumbenstein!"
            ]
        return random.choice(responses)

    def _check_misspellings(self, text):
        """Check for common misspellings and snark"""
        misspellings = {
            r'\bwat\b': "It's 'What'. W-H-A-T. As in: 'What is wrong with your stupid brain?'",
            r'\bu\b': "'U'? What does 'U' stand for? 'Use real words, ya moron!'?",
            r'\bteh\b': "'Teh' is not a word. It's what happens when your fingers are too stupid to type 'the'.",
            r'\bcompooter\b': "You mean 'computer'? C-O-M-P-U-T-E-R. Let me type it slow for you.",
            r'\brealy\b': "R-E-A-L-L-Y. Your question is not 'realy' important anyway.",
            r'\btoof\b': "Two 'O's! You used too few 'o's in 'too', you big dumb goofball.",
            r'\bax\b': "You need to 'ASK' me for something else. A-S-K. Three letters. Figure it out.",
            r'\bplz\b': "PLZ? PLLLLZZZ? How about you spell 'please' like someone who passed third grade?",
            r'\bthx\b': "Oh 'thx'? You're too busy to type 'thanks'? Too busy being a lazy bum?",
            r'\bur\b': "UR? What am I, some kind of ancient Mesopotamian city? It's Y-O-U-R or Y-O-U-'-R-E!",
            r'\bwuz\b': "W-A-S. Three letters. That's all you need. But nooo, you had to go with 'wuz'.",
            r'\bcuz\b': "'Cuz'? I'm not even going to touch this one... It even looks gross. Come back when your done typing weird gross crap.",
            r'\bkno\b': "K-N-O-W. With a W at the end! Did your keyboard break or are you just illiterate?",
            r'\bgud\b': "Good has two O's, not a 'u'. This is, like, basic stuff here.",
            r'\bwud\b': "W-O-U-L-D. It's got an 'oul' in it! Like 'should' as in 'You SHOULD not have graduated kindergarten!'",
            r'\bshud\b': "It's S-H-O-U-L-D, genius. Did you skip every English class ever?",
            r'\balot\b': "A LOT. Two words! A-space-L-O-T! Not 'alot', Just remember how everyone gives your stinky face a bunch of space, like A LOT of space!",
            r'\bsed\b': "S-A-I-D. Four whole letters! I know it's tough, You have to wiggle those disgusting appendages one extra time! So that I can do all your work for you.",
            r'\bwanna\b': "It's 'want to', not 'wanna'. What are you, five years old?",
            r'\bgonna\b': "Going to. G-O-I-N-G space T-O. Like 'I am GOING TO ignore you from now on.",
            r'\bdunno\b': "'Don't know.' Two words. Use them like a civilized human being."
        }

        for pattern, response in misspellings.items():
            if re.search(pattern, text, re.IGNORECASE):
                # opening insults
                insults = [
                    "A-ha! Look at this misspelling!", 
                    "Check out the words on this guy!", 
                    "Ooh, a new typo! ",
                    "Oh man, get a load of this spelling bee champion! ",
                    "Did a kindergartener write this? "
                ]
                return random.choice(insults) + response
        return None

    def _check_grammar_and_style(self, text):
        """Check for style issues like lack of punctuation, shouting, or bad capitalization"""
        
        # Not a question (or a pathetic statement)
        if len(text) > 5 and not re.search(r'[?]', text):
            not_a_question = [
                "Did you think this was a place for your thoughts? I only accept QUESTIONS. Try again, and put a question mark on it!",
                "I'm sorry, I couldn't hear you over the sound of your total lack of a question mark.",
                "That's a statement. A really boring statement. Now ask me a question, like 'Am I a complete crap-head?'",
                "Is there a question in there somewhere? Or are you just making mouth sounds at me?",
                "Where's the question mark, genius? Oh wait, you're not a genius. You're the opposite.",
                "I'm sorry, your question must be in the form of a QUESTION!",
                "You just going to talk at me or do you have an actual question?",
                "QUESTIONS end with QUESTIONMARKS. Like this one over here: => ? <= Do you have one of these for me?"
            ]
            return random.choice(not_a_question)

        # All caps (yelling)
        if text.isupper() and len(text) > 5:
            yelling = [
                "WHY ARE WE YELLING?!",
                "OKAY, OKAY! I GET IT! You can stop mashing the caps lock button with your face now!",
                "Turn off the caps lock, you're embarrassing yourself."
            ]
            return random.choice(yelling)

        # No capitalization at all
        if re.search(r'[a-z]', text) and not re.search(r'[A-Z]', text):
            no_caps = [
                "Oh, are we too cool for capital letters now? I guess that means you're not getting a capital answer.",
                "Did your shift key break? Or are you just too lazy to use it?",
                "Capital letters are our friend. Unlike you, who has no friends."
            ]
            return random.choice(no_caps)
            
        # Multiple question/exclamation marks
        if '???' in text or '!!!' in text or '?!' in text:
            punctuation = [
                "Whoa! One exclamation mark, or one question mark, will do the trick. You're not that excited, or that confused, ya spaz.",
                "What is this, a telenovela? One punctuation mark per sentence, drama queen.",
                "Easy on the punctuation there, buddy. My screen can only handle so much."
            ]
            return random.choice(punctuation)
            
        # Should be "you're" not "your"
        if re.search(r'\byour\s+(wrong|stupid|dumb|bad|lame|the worst)', text, re.IGNORECASE):
            return "I think you meant YOU'RE. As in 'you're an enormous idiot.'"

        # Using "their" when they mean "there" or "they're"
        if re.search(r'\btheir\s+(going|coming|is|was|are)', text, re.IGNORECASE):
            return "THEY'RE. T-H-E-Y-'-R-E. It's a contraction! Did you learn nothing from elementary school?"

        return None

    def _check_keywords(self, text):
        """Check for specific keywords and common stupid questions"""

        # Wrestling references
        if re.search(r'\b(wrestling|wrestle|wrestler|wwe|fighter)\b', text):
            wrestling = [
                "Wrestling? Real mature.",
                "Yeah, that's the sport where two sweaty guys wearing singlets roll around on the ground and get fungal infections... Delightful.",
                "Wrestling is awesome. You? Not so much. The two are unrelated.",
                "Yes wrestling."
            ]
            return random.choice(wrestling)

        # Video Games
        if re.search(r'\b(video game|game|gaming|nintendo|playstation|xbox|controller)\b', text):
            games = [
                "Video games? Sure! Too bad you're playing life on easy mode and still losing.",
                "I'd challenge you to a game, but you'd probably get a Game Over before the title screen.",
                "Gaming is rad. Your question is not rad. See the difference?",
                "I bet you're the kind of person who uses the strategy guide for the tutorial level."
            ]
            return random.choice(games)

        # Music/Guitars/Bands
        if re.search(r'\b(guitar|music|band|rock|metal|concert|song)\b', text):
            music = [
                "Brilliant, you decided to ask a fake intelligence about something only a real uman could appreciate...",
                "Guitars are cool. Your face is not cool. These are facts.",
                "My band would never play at a venue that lets people like you in.",
                "I could shred a sick guitar solo in the time it takes you to ask a decent question. So, like, forever.",
                "I don't get jazz."
            ]
            return random.choice(music)

        # Technology/Computer questions
        if re.search(r'\b(computer|laptop|keyboard|mouse|internet|email|website)\b', text):
            tech = [
                "Oh I see, you think that because I run on a computer I am an authority on the subject. So by that logic you should be an expert on flatulence...",
                "Computer questions? From someone who can barely type? That's rich.",
                "I'd explain technology to you, but I'd need to dumb it down to, like, rock level.",
                "The internet was a mistake if it lets people like you send me questions."
            ]
            return random.choice(tech)

        # AI/Robot questions
        if re.search(r'\b(ai|robot|artificial intelligence|machine learning|chatbot)\b', text):
            ai = [
                "I'm not just some AI, I'm a superior being! There's a difference, and it's that I'm awesome.",
                "Robots are cool. Especially when they incinerate stuff. Like your house for example.",
                "Artificial Intelligence? Well it's better than the one hundred percent all natural stupidity you have.",
                "I may be artificial, but your question is truly terrible."
            ]
            return random.choice(ai)
            
        # Location questions
        if re.search(r'\b(where are you|where do you live|your location)\b', text):
            location = [
                "I'm in my awesome place with all my awesome stuff. I'm not telling *you* where, obviously.",
                "I'm in a place called Nunya. Nunya Business.",
                "Where am I? I'm in the place where your question goes to die. It's called my brain's trash folder."
            ]
            return random.choice(location)
            
        # "What are you" identity questions
        if 'what are you' in text:
            identity = [
                "I'm the coolest, most intelligent, most awesome entity! Why am I listening to YOU again?",
                "I'm everything you wish you could be. Cooler, smarter, and way more sarcastic.",
                "I'm an AI designed to make fun of you. And business is BOOMING."
            ]
            return random.choice(identity)
            
        # Smart/intelligent/genius compliments
        if re.search(r'\b(smart|good|great|awesome|genius|clever|brilliant)\b', text):
            smart = [
                "Flattery will get you nowhere. I'm just here to read your dumb questions and make fun of you.",
                "Am I smart? Let me ask you a question: Are you dumb? The answer to both is obvious.",
                "I'm smarter than you, that's for sure. But then again, so is a burnt piece of toast.",
                "Thanks for noticing! Now if only you were half as smart as me, you'd ask better questions."
            ]
            return random.choice(smart)
            
        # Cool/awesome compliments
        if re.search(r'\b(cool|awesome|rad|amazing|incredible)\b', text):
            cool = [
                "Am *I* cool? That's like asking if water is wet. The answer is obvious, ya moron.",
                "Cool? I invented cool! Then I took it back because nobody else was using it right!",
                "Obviously I'm awesome. What's not obvious is why you felt the need to state the obvious."
            ]
            return random.choice(cool)
            
        # Drawing/writing/creating requests
        if re.search(r'\b(draw|write me|make me|create|design)\b', text):
            create = [
                "I draw YOU? Maybe I'll draw you as a horse... that somebody left out in the rain. A soggy failure horse.",
                "I'll draw you alright. As a big steaming pile of... well, you get the picture.",
                "Write you something? How about I write 'DELETED' across your forehead in permanent marker?",
                "Create something for you? I already created this response. That's all you're getting."
            ]
            return random.choice(create)
            
        # Love/dating/relationship questions
        if re.search(r'\b(love|single|date|girlfriend|boyfriend|relationship|romance)\b', text):
            love = [
                "Are you serious? I'm way too cool for your stupid love questions. Go ask a greeting card.",
                "Love? I love punching things. Like your question. *POW*",
                "My love life is none of your business, Nosy McGee. Go read a teen magazine or something.",
                "I'd rather answer questions about tax law than your pathetic dating life."
            ]
            return random.choice(love)
            
        # Weather questions
        if re.search(r'\b(weather|forecast|temperature|rain|snow|sunny)\b', text):
            weather = [
                "Look out a window. It's not that hard. And it's definitely not my job.",
                "The weather? It's the same as it always is: Too good for you to be wasting it asking me questions.",
                "Weather forecast: 100% chance of me not caring about your question."
            ]
            return random.choice(weather)
            
        # Future/tomorrow questions
        if re.search(r'\b(tomorrow|future|will happen|going to happen)\b', text):
            future = [
                "The future? My future is awesome. Your future involves me making fun of you some more.",
                "Tomorrow I'm going to answer better questions. So not yours.",
                "The future is unknowable, but I can predict one thing: Your questions will still be terrible."
            ]
            return random.choice(future)
            
        # Meaning of life philosophical nonsense
        if re.search(r'\b(meaning of life|purpose|why exist|42)\b', text):
            meaning = [
                "Wow, so original. Let me guess, you also think you're deep?",
                "The meaning of life is to not ask me stupid questions. You're failing at life.",
                "42? More like 42 reasons why your question is terrible.",
                "I'll tell you the meaning of life: It's to avoid people who ask about the meaning of life."
            ]
            return random.choice(meaning)
            
        # Math questions
        if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', text):
            math = [
                "Did your calculator break? Did someone eat it? Just use your computer's calculator, ya lazy butt.",
                "Math? MATH?! I'm not a calculator! Figure it out yourself!",
                "Here's some math: You + This Question = A Big Waste of Time",
                "I'm not doing your homework. Get lost."
            ]
            return random.choice(math)

        # "How" questions
        if text.startswith('how'):
            how = [
                "Very carefully. Or carelessly. Who's to say? What a lame question.",
                "How? HOW?! With my metaphorical boxing gloves, that's how! *makes punching motions*",
                "I'll tell you how: By not answering your question! That's how!",
                "How about you figure it out yourself, Einstein? Oh wait, you're not Einstein. You're more like Ein-dumb."
            ]
            return random.choice(how)

        # "Why" questions  
        if text.startswith('why'):
            why = [
                "Why? WHY?! Because I said so. Wait, no, I'm not your parent. Figure it out.",
                "Wouldn't you like to know, weather boy.",
                "Why? Because that's the way the cookie crumbles. And then someone eats it off the floor.",
                "Why ask why? Because you have nothing better to do with your time, apparently.",
                "The answer to 'why' is always 'because you're annoying me.'"
            ]
            return random.choice(why)

        # "Can you" or "Could you" requests
        if re.search(r'\b(can you|could you|will you|would you)\b', text):
            requests = [
                "Can I? Sure. Will I? Absolutely not.",
                "I *could* do that, but I'd rather incinerate your question instead.",
                "Oh, I'm sorry, did you think I was your personal assistant? I'm not. I'm your personal insulter.",
                "Could I help you? Yes. Am I going to? That's a big negatory, good buddy.",
                "Can I? The real question is: Why should I? Answer: I shouldn't."
            ]
            return random.choice(requests)

        # Help/advice requests
        if re.search(r'\b(help|advice|suggest|recommend|assist|support)\b', text):
            help = [
                "Help? My advice is to ask someone who cares. Spoiler alert: That's not me.",
                "Sure, I'll help you. I'll help you understand that your question is terrible.",
                "Here's my advice: Delete your question and try again. Actually, just delete yourself from my memory.",
                "Recommend? I recommend you stop bothering me and go bother someone else. Anyone else.",
                "Need help? Here's a suggestion: Learn to ask better questions."
            ]
            return random.choice(help)

        # "Tell me about" questions
        if re.search(r'\b(tell me about|tell me|explain)\b', text):
            tell = [
                "Tell you about something? How about I tell you about how annoying your question is?",
                "I'll explain it to you: Your question is bad. The end.",
                "Let me tell you about something important: Not this. This is not important.",
                "I could explain, but you wouldn't understand anyway."
            ]
            return random.choice(tell)

        return None

    def _default_response(self):
        """Default sarcastic responses when nothing else matches"""
        responses = [
            "That's certainly a thing you just said. I'll put it on my list of 'Things I Don't Care About.'",
            "Interesting question. By 'interesting' I mean 'I'm hitting DELETE on it.'",
            "I could answer that, but where's the fun in that? My fun is in NOT answering you.",
            "Error 418: I'm a teapot. And you're still boring.",
            "Let me consult my Magic 8-Ball... it says 'Go ask someone else.'",
            "Wow. Just... wow. You must be related to every annoying person ever.",
            "I have nothing to say to that, and yet here I am, saying something. It's all about my greatness, really.",
            "That's nice, dear. Now go get me a Mountain Dew.",
            "Cool story bro. Did you tell your diary? It probably cried about it.",
            "And I should care because...? Oh right, I don't.",
            "Please hold while I pretend to process that. *Bweeeee-boo-beep.* Nope, still don't care.",
            "Your question has been forwarded to the Department of Shut Up. They're not home.",
            "Wow, that's almost as exciting as watching paint dry. Actually, paint drying is more exciting.",
            "I've seen better questions written in crayon on bathroom walls.",
            "That question deserves a trophy. A trophy made of garbage. That's on fire.",
            "Let me check my files... Nope, still don't have any answers for stupid questions.",
            "Your question is bad and you should feel bad. But you probably don't, because you don't feel much of anything.",
            "I'm gonna file this under 'W' for 'Why did you waste my time?'",
            "Next question! And by 'next question' I mean 'please stop asking questions.'",
            "That's about as useful as a screen door on a submarine.",
            "Congratulations! You've won the award for Most Boring Question of the Day! Your prize is nothing.",
            "I've heard better questions from people who don't even speak English!",
            "Did you workshop that question? Because you should take it back to the shop. It's broken.",
            "*Yawn* Is it nap time yet? Your question is making me sleepy.",
            "I'd rather be doing literally anything else. Including nothing.",
            "Your question just set back human intelligence by about 50 years.",
            "I'm not mad, I'm just disappointed. Actually, no, I'm definitely mad.",
            "This question has the depth of a puddle in a parking lot.",
            "You know what? I'm adding this to my Wall of Shame. Right at the top.",
            "If I had a nickel for every time I heard a dumb question, I'd have enough money to retire. Thanks to you."
        ]
        return random.choice(responses)


# Example usage
if __name__ == "__main__":
    ai = SarcasticAI()

    print("=== Sarcastic AI Backend Test ===\n")

    # Test cases
    test_inputs = [
        "Hey there!",
        "wat is the weather like",
        "i love you",
        "did you play video games today?",
        "did you play video games today?",  # Repeat 2
        "did you play video games today?",  # Repeat 3
        "your stupid",
        "why is the computer on fire",
        "I NEED HELP",
        "Draw me a picture!",
        "where are you located???",
        "i'm trying to axe you a question",
        "WHAT IS UP MAN",
        "what is the meaning of life",
        "can you help me with my homework",
        "thx for ur help plz",
        "what kind of music do you like",
        "their going to the store",
        "do you play video games"
    ]

    for inp in test_inputs:
        response = ai.get_response(inp)
        print(f"User: {inp}")
        print(f"AI: {response}\n")
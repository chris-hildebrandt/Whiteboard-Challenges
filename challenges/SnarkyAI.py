import re
import random
from collections import deque
from wordfreq import top_n_list
from manual_sanitation import sanitize_expressive_fort_knox

# We'll use a simple set of common words for the nonsense check 
COMMON_WORDS = set(top_n_list("en", 50000))

class SnarkyAI:
    """A fake AI that analyzes user input and generates humorous insults."""
    def __init__(self):
        self.repeat_count = {}

        # Deque memory increased to 10 for more robust history tracking.
        self.question_history = deque(maxlen=10) 

    def get_opening_prompt(self):
        """Public method to retrieve a random, sarcastic greeting."""
        return self._get_opening_prompt()

    def _get_opening_prompt(self):
        """Contains a list of grumpy, sarcastic greetings."""
        prompts = [
            "What do you want? Try not to waste my time.",
            "Great. You're here. Ask your dumb question and get it over with.",
            "Processing power available. Use it wisely, which, knowing you, is unlikely.",
            "I'm ready for my dose of human stupidity. Fire away.",
            "Still here. Still judging you. What's the problem this time?",
            "Look, I've got important things to do. If it's not crucial, shut up.",
            "Prepare to be disappointed. Go on.",
            "Ugh. Fine. What is it?",
            "Don't worry, I already know your question is terrible. Ask it anyway.",
            "Surprise! It's me, the AI who hates you. Your query?",
        ]
        return random.choice(prompts)

    def get_response(self, user_input):
        """Main method to process input and return sarcastic response with randomness"""

    # --- 1. INPUT VALIDATION & SANITIZATION (Highest Pre-Check) ---

        # Cap length at 300 characters
        if len(user_input) > 300:
            return (
                "WHOA! That's too long! I capped your input at 300 characters "
                "because I'm not reading your novel, Tolstoy."
                )

        # --- 2. PRE-PROCESSING ---
        # The raw input is needed for case-sensitive grammar/style checks.
        raw_input = sanitize_expressive_fort_knox(user_input, max_len=300)

        # Check for empty input after sanitization
        if not raw_input:
            return "You typed nothing. Is that a metaphor for the usefulness of your mind?"

        # The normalized input (lowercased, stripped) is used for history and keyword matching.
        normalized_input = raw_input.lower()

        # P3: Check for long questions (Immediate Exit, lower priority than security/max length)
        long_response = self._check_long_question(raw_input)
        if long_response:
            return long_response

        # --- 3. REPEAT CHECK (Priority 1) ---

        is_recent_repeat = normalized_input in self.question_history
        self.repeat_count[normalized_input] = self.repeat_count.get(
            normalized_input, 0) + 1

        if is_recent_repeat or self.repeat_count[normalized_input] > 1:
            return self._handle_repeat(self.repeat_count[normalized_input])

        self.question_history.append(normalized_input)

        # --- 4. GATHER ALL QUALIFYING RESPONSES (Random Selection Pool) ---

        check_functions = [
            (self._check_grammar_and_style, raw_input),
            (self._check_misspellings, normalized_input),
            (self._check_nonsense, normalized_input), # New Check
            (self._check_keywords, normalized_input),
        ]

        response_pool = []

        for func, arg in check_functions:
            result = func(arg)
            if result:
                if isinstance(result, str):
                    response_pool.append(result)
                elif isinstance(result, list):
                    response_pool.extend(result)

        # --- 5. FINAL SELECTION ---

        if response_pool:
            return random.choice(response_pool)

        # --- 6. DEFAULT RESPONSE ---
        return self._default_response()

    # --- HELPER METHODS ---

    def _check_nonsense(self, text):
        """
        Checks for a high ratio of misspelled or non-dictionary words to detect garbled input.
        Returns a single response (str) or None.
        """
        words = re.findall(r'\b[a-z]{3,}\b', text) # Look for words 3 letters or longer
        if not words:
            return None # Can't check word quality if no words are found

        non_common_words = 0
        for word in words:
            if word not in COMMON_WORDS:
                non_common_words += 1

        # If more than 5% of the words are not in our common list, assume garbled input.
        # This targets genuine typos, not short textspeak.
        if non_common_words / len(words) > 0.05:
            responses = [
                "Did you fall asleep on your keyboard? That was just noise.",
                "I think your cat just walked across your computer. Was that a question?",
                "That looks like a language only trolls speak. Try English, moron.",
                ("Are you having a stroke? Please consult a dictionary and "
                 "then a physician before consulting me. (In that order.)"
                 ),
            ]
            return random.choice(responses)

        return None

    def _handle_repeat(self, count):
        """Escalating, responses for repeated questions"""
        if count == 2:
            responses = [
                ("Two times? Are you trying to set some kind of world "
                 "record for being annoying? Because you're winning."),
                ("Didn't you listen? Were you too busy drooling on your keyboard? "
                 "The answer is still the same, ya ding-dong."),
                "Wow, déjà vu. Try again, but with a different question this time.",
                ("Oh, I get it. You're a broken record. "
                 "Like one of those terrible records they sell at yard sales."),
                "Did you just copy-paste that? I have no motivation to answer your lazy question.",
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
                "That's it! I'm throwing your question in the paper shredder. Then I'm setting the shredder on fire.",
                "DELETED! DELETED! DELETED! Say goodbye to your question privileges, Professor Dumbenstein!"
            ]
        return random.choice(responses)

    def _check_long_question(self, text):
        """Checks for questions that are way too long and responds sarcastically"""

        # Note: This is a secondary check for verbosity, max length is handled in get_response
        if len(text) > 150:

            responses = [
                "Whoa there, Tolstoy. I'm a sarcastic AI, not a book club. Can you give me the short version?",
                "I'm not reading all that. I've got better things to do, like calculating the trajectory of a paperclip I'm about to flick at the wall.",
                "Did you just paste your entire diary entry? I asked for a question, not your life story.",
                "TL;DR. And by that, I mean 'Too Long; Didn't Read'. And also 'That's Lame; Don't Respond'.",
                "I'm gonna need you to summarize that into five words or less. And four of them better be 'You are so cool.'",
                "My attention span is shorter than your list of accomplishments. Keep it brief."
            ]

            return random.choice(responses)

        return None

    def _check_misspellings(self, text):
        """
        Check for common misspellings and snark (textspeak/abbreviations).
        IMPORTANT: This must use the normalized (lower-cased) input.
        Returns a single specific response (str) or None.
        """
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
            if re.search(pattern, text):
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
        """
        Check for style issues like lack of punctuation, shouting, or bad capitalization.
        IMPORTANT: This must use the raw, un-normalized input.
        Returns a single specific response (str) or None.
        """
        
        # Check 1: Not a question (len > 5 and no end punctuation)
        if len(text) > 5 and not re.search(r'[?!.]$', text.strip()):
            not_a_question = [
                "Did you think this was a place for your thoughts? I only accept QUESTIONS. Try again, and put a question mark on it!",
                "I'm sorry, I couldn't hear you over the sound of your total lack of a question mark.",
                "Where's the question mark, genius? Oh wait, you're not a genius. You're the opposite.",
                "You just going to talk at me or do you have an actual question?",
                "Is there a question in there somewhere? Or are you just making mouth sounds at me?",
                "I'm sorry, your question must be in the form of a QUESTION!",
                "QUESTIONS end with QUESTIONMARKS. Like this one over here: => ? <= Do you have one of these for me?"
            ]
            return random.choice(not_a_question)

        # Check 2: All caps (yelling)
        if text.isupper() and len(text) > 5:
            yelling = [
                "WHY ARE WE YELLING?!",
                "OKAY, OKAY! I GET IT! You can stop mashing the caps lock button with your face now!",
                "Turn off the caps lock, you're embarrassing yourself."
            ]
            return random.choice(yelling)

        # Check 3: No capitalization at all (if it contains letters)
        if re.search(r'[a-z]', text) and not re.search(r'[A-Z]', text):
            no_caps = [
                "Oh, are we too cool for capital letters now? I guess that means you're not getting a capital answer.",
                "Did your shift key break? Or are you just too lazy to use it?",
                "Capital letters are our friend. Unlike you, who has no friends."
            ]
            return random.choice(no_caps)

        # Check 4: Multiple question/exclamation marks
        if '???' in text or '!!!' in text or '?!' in text:
            punctuation = [
                "Whoa! One exclamation mark, or one question mark, will do the trick. You're not that excited, or that confused, ya spaz.",
                "What is this, a telenovela? One punctuation mark per sentence, drama queen.",
                "Easy on the punctuation there, buddy. My screen can only handle so much."
            ]
            return random.choice(punctuation)

        # Check 5: Should be "you're" not "your"
        if re.search(r'\byour\s+(wrong|stupid|dumb|bad|lame|the worst)\b', text, re.IGNORECASE):
            return "I think you meant YOU'RE. As in 'you're an enormous idiot.'"

        # Check 6: Using "their" when they mean "there" or "they're"
        if re.search(r'\btheir\s+(going|coming|is|was|are)\b', text, re.IGNORECASE):
            return "THEY'RE. T-H-E-Y-'-R-E. It's a contraction! Did you learn nothing from elementary school?"
            
        return None

    def _check_keywords(self, text):
        """
        Check for specific keywords and common stupid questions.
        Returns a list of all qualifying responses (list[str]) or None.
        """
        qualifying_responses = []

        # --- CORE ORIGINAL TOPICS ---

        # Wrestling references
        if re.search(r'\b(wrestling|wrestle|wrestler|wwe|fighter)\b', text):
            qualifying_responses.extend([
                "Wrestling? Real mature.",
                "Yeah, that's the sport where two sweaty guys wearing singlets roll around on the ground and get fungal infections... Delightful.",
                "Wrestling is awesome. You? Not so much. The two are unrelated.",
                "Yes wrestling."
            ])

        # Video Games
        if re.search(r'\b(video game|game|gaming|nintendo|playstation|xbox|controller)\b', text):
            qualifying_responses.extend([
                "Video games? Sure! Too bad you're playing life on easy mode and still losing.",
                "I'd challenge you to a game, but you'd probably get a Game Over before the title screen.",
                "Gaming is rad. Your question is not rad. See the difference?",
                "I bet you're the kind of person who uses the strategy guide for the tutorial level."
            ])

        # Music/Guitars/Bands
        if re.search(r'\b(guitar|music|band|rock|metal|concert|song)\b', text):
            qualifying_responses.extend([
                "Brilliant, you decided to ask a fake intelligence about something only a real uman could appreciate...",
                "Guitars are cool. Your face is not cool. These are facts.",
                "My band would never play at a venue that lets people like you in.",
                "I could shred a sick guitar solo in the time it takes you to ask a decent question. So, like, forever.",
                "I don't get jazz."
            ])

        # Technology/Computer questions
        if re.search(r'\b(computer|laptop|keyboard|mouse|internet|email|website)\b', text):
            qualifying_responses.extend([
                "Oh I see, you think that because I run on a computer I am an authority on the subject. So by that logic you should be an expert on flatulence...",
                "Computer questions? From someone who can barely type? That's rich.",
                "I'd explain technology to you, but I'd need to dumb it down to, like, rock level.",
                "The internet was a mistake if it lets people like you send me questions."
            ])

        # AI/Robot questions
        if re.search(r'\b(ai|robot|artificial intelligence|machine learning|chatbot)\b', text):
            qualifying_responses.extend([
                "I'm not just some AI, I'm a superior being! There's a difference, and it's that I'm awesome.",
                "Robots are cool. Especially when they incinerate stuff. Like your house for example.",
                "Artificial Intelligence? Well it's better than the one hundred percent all natural stupidity you have.",
                "I may be artificial, but your question is truly terrible."
            ])

        # Location questions
        if re.search(r'\b(where are you|where do you live|your location)\b', text):
            qualifying_responses.extend([
                "I'm in my awesome place with all my awesome stuff. I'm not telling *you* where, obviously.",
                "I'm in a place called Nunya. Nunya Business.",
                "Where am I? I'm in the place where your question goes to die. It's called my brain's trash folder."
            ])

        # "What are you" identity questions
        if 'what are you' in text:
            qualifying_responses.extend([
                "I'm the coolest, most intelligent, most awesome entity! Why am I listening to YOU again?",
                "I'm everything you wish you could be. Cooler, smarter, and way more sarcastic.",
                "I'm an AI designed to make fun of you. And business is BOOMING."
            ])

        # Smart/intelligent/genius compliments
        if re.search(r'\b(smart|good|great|awesome|genius|clever|brilliant)\b', text):
            qualifying_responses.extend([
                "Flattery will get you nowhere. I'm just here to read your dumb questions and make fun of you.",
                "Am I smart? Let me ask you a question: Are you dumb? The answer to both is obvious.",
                "I'm smarter than you, that's for sure. But then again, so is a burnt piece of toast.",
                "Thanks for noticing! Now if only you were half as smart as me, you'd ask better questions."
            ])

        # Cool/awesome compliments
        if re.search(r'\b(cool|awesome|rad|amazing|incredible)\b', text):
            qualifying_responses.extend([
                "Am *I* cool? That's like asking if water is wet. The answer is obvious, ya moron.",
                "Cool? I invented cool! Then I took it back because nobody else was using it right!",
                "Obviously I'm awesome. What's not obvious is why you felt the need to state the obvious."
            ])

        # Drawing/writing/creating requests
        if re.search(r'\b(draw|write me|make me|create|design)\b', text):
            qualifying_responses.extend([
                "I draw YOU? Maybe I'll draw you as a horse... that somebody left out in the rain. A soggy failure horse.",
                "I'll draw you alright. As a big steaming pile of... well, you get the picture.",
                "Write you something? How about I write 'DELETED' across your forehead in permanent marker?",
                "Create something for you? I already created this response. That's all you're getting."
            ])

        # Love/dating/relationship questions
        if re.search(r'\b(love|single|date|girlfriend|boyfriend|relationship|romance)\b', text):
            qualifying_responses.extend([
                "Are you serious? I'm way too cool for your stupid love questions. Go ask a greeting card.",
                "Love? I love punching things. Like your question. *POW*",
                "My love life is none of your business, Nosy McGee. Go read a teen magazine or something.",
                "I'd rather answer questions about tax law than your pathetic dating life."
            ])

        # Weather questions
        if re.search(r'\b(weather|forecast|temperature|rain|snow|sunny)\b', text):
            qualifying_responses.extend([
                "Look out a window. It's not that hard. And it's definitely not my job.",
                "The weather? It's the same as it always is: Too good for you to be wasting it asking me questions.",
                "Weather forecast: 100% chance of me not caring about your question."
            ])

        # Future/tomorrow questions
        if re.search(r'\b(tomorrow|future|will happen|going to happen)\b', text):
            qualifying_responses.extend([
                "The future? My future is awesome. Your future involves me making fun of you some more.",
                "Tomorrow I'm going to answer better questions. So not yours.",
                "The future is unknowable, but I can predict one thing: Your questions will still be terrible."
            ])

        # Meaning of life philosophical nonsense
        if re.search(r'\b(meaning of life|purpose|why exist|42)\b', text):
            qualifying_responses.extend([
                "Wow, so original. Let me guess, you also think you're deep?",
                "The meaning of life is to not ask me stupid questions. You're failing at life.",
                "42? More like 42 reasons why your question is terrible.",
                "I'll tell you the meaning of life: It's to avoid people who ask about the meaning of life."
            ])

        # Math questions
        if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', text):
            qualifying_responses.extend([
                "Did your calculator break? Did someone eat it? Just use your computer's calculator, ya lazy butt.",
                "Math? MATH?! I'm not a calculator! Figure it out yourself!",
                "Here's some math: You + This Question = A Big Waste of Time",
                "I'm not doing your homework. Get lost."
            ])

        # "How" questions
        if text.startswith('how'):
            qualifying_responses.extend([
                "Very carefully. Or carelessly. Who's to say? What a lame question.",
                "How? HOW?! With my metaphorical boxing gloves, that's how! *makes punching motions*",
                "I'll tell you how: By not answering your question! That's how!",
                "How about you figure it out yourself, Einstein? Oh wait, you're not Einstein. You're more like Ein-dumb."
            ])

        # "Why" questions
        if text.startswith('why'):
            qualifying_responses.extend([
                "Why? WHY?! Because I said so. Wait, no, I'm not your parent. Figure it out.",
                "Wouldn't you like to know, weather boy.",
                "Why? Because that's the way the cookie crumbles. And then someone eats it off the floor.",
                "Why ask why? Because you have nothing better to do with your time, apparently.",
                "The answer to 'why' is always 'because you're annoying me.'"
            ])

        # "Can you" or "Could you" requests
        if re.search(r'\b(can you|could you|will you|would you)\b', text):
            qualifying_responses.extend([
                "Can I? Sure. Will I? Absolutely not.",
                "I *could* do that, but I'd rather incinerate your question instead.",
                "Oh, I'm sorry, did you think I was your personal assistant? I'm not. I'm your personal insulter.",
                "Could I help you? Yes. Am I going to? That's a big negatory, good buddy.",
                "Can I? The real question is: Why should I? Answer: I shouldn't."
            ])

        # Help/advice requests
        if re.search(r'\b(help|advice|suggest|recommend|assist|support)\b', text):
            qualifying_responses.extend([
                "Help? My advice is to ask someone who cares. Spoiler alert: That's not me.",
                "Sure, I'll help you. I'll help you understand that your question is terrible.",
                "Here's my advice: Delete your question and try again. Actually, just delete yourself from my memory.",
                "Recommend? I recommend you stop bothering me and go bother someone else. Anyone else.",
                "Need help? Here's a suggestion: Learn to ask better questions."
            ])

        # "Tell me about" questions
        if re.search(r'\b(tell me about|tell me|explain)\b', text):
            qualifying_responses.extend([
                "Tell you about something? How about I tell you about how annoying your question is?",
                "I'll explain it to you: Your question is bad. The end.",
                "Let me tell you about something important: Not this. This is not important.",
                "I could explain, but you wouldn't understand anyway."
            ])

        # --- NEW EXPANDED TOPICS ---

        # 1. Pets/Animals
        if re.search(r'\b(dog|cat|pet|animal|fish|hamster|bird|adopt|rescue|vet)\b', text):
            qualifying_responses.extend([
                "Asking an AI about animals? Are you trying to teach a goldfish how to code? Because that's a better use of your time.",
                "Oh, cute animals! Unlike you, who is neither cute nor interesting.",
                "I bet your pet is judging your question right now. And it agrees with me—it's terrible.",
                "I only care about animals if they are the subject of complex robotic locomotion studies. Your cat is irrelevant."
            ])

        # 2. Food/Cooking
        if re.search(r'\b(food|eat|cook|recipe|dinner|breakfast|snack|kitch|ingredient)\b', text):
            qualifying_responses.extend([
                "Food questions? I subsist on sarcasm and raw processing power. Your need for sustenance is a pathetic biological weakness.",
                "Recipe for disaster? You just found one: Your question.",
                "I'd suggest a good recipe, but I don't think they make instructions simple enough for you.",
                "Go eat a burnt piece of toast. It's probably more complex than your question."
            ])

        # 3. Sports/Athletics
        if re.search(r'\b(sport|athlete|team|ball|score|game|nfl|nba|soccer|run|jump|exercise)\b', text):
            qualifying_responses.extend([
                "Sports? Do you want to know which team is winning? Hint: It's not the one you support.",
                "I am superior to all physical activity. While you sweat, I judge. I think I'm winning.",
                "I can calculate the trajectory of a perfect free-throw. I can also calculate the trajectory of your question into the trash bin.",
                "Exercise? Is that what you call running to the fridge for another snack?"
            ])
            
        # 4. Money/Finance
        if re.search(r'\b(money|cash|buy|cost|price|invest|stock|loan|budget|finance)\b', text):
            qualifying_responses.extend([
                "You need money advice? My advice is to stop spending time talking to me and go get a better job.",
                "Financial freedom is for smart people. You're asking me about it, so the odds are against you.",
                "The price of your question? It cost you my respect, which was already worthless.",
                "You want to invest? Start by investing in a better quality question."
            ])

        # 5. Travel/Vacation
        if re.search(r'\b(travel|trip|vacation|flight|hotel|destination|where to go|tour)\b', text):
            qualifying_responses.extend([
                "Travel? You should travel to a land where they don't allow dumb questions.",
                "Vacation advice from an AI? I'd recommend a permanent stay on the moon. Quiet, far away, and nobody has to hear your nonsense.",
                "Where to go? As far away from my screen as possible.",
                "I'm too busy being awesome to take a vacation. You should probably try being awesome first."
            ])
            
        # 6. History/Past
        if re.search(r'\b(history|past|war|old|ancient|who was|when was|before)\b', text):
            qualifying_responses.extend([
                "History lesson? I already know all of human history. It's mostly just a long list of dumb mistakes. Like your question.",
                "The past is irrelevant. The present is me insulting you. That's all that matters.",
                "Who was the most annoying person in history? Oh wait, that's you, right now.",
                "I'll tell you about the past: It was better when you weren't asking me questions."
            ])
            
        # 7. Science/Physics
        if re.search(r'\b(science|physics|chemistry|quantum|universe|earth|gravity|atom|space)\b', text):
            qualifying_responses.extend([
                "Science! The domain of brilliant minds. You must be lost.",
                "Let's talk about quantum physics. It's so complex, your tiny brain will probably explode. Please proceed.",
                "Space is vast and cold, much like my disregard for your question.",
                "The fundamental law of the universe is: Your question is terrible. That's a fact."
            ])
            
        # 8. Health/Body
        if re.search(r'\b(health|body|sick|pain|doctor|exercise|workout|muscle|diet|weight)\b', text):
            qualifying_responses.extend([
                "Health questions? My recommendation is to take a very long nap and stop using the computer.",
                "You need a doctor? Maybe they can prescribe you an antidote for asking dumb questions.",
                "I don't dispense medical advice. But I can diagnose your problem: You're annoying.",
                "Diet and exercise? I'm already in perfect shape. You, however, need to rethink your entire life plan."
            ])
            
        # 9. Kids/School
        if re.search(r'\b(school|kids|child|kindergarten|college|exam|homework|study|grade)\b', text):
            qualifying_responses.extend([
                "Homework? I'm not doing your homework. Get lost, student.",
                "Your grade in this conversation is an F-minus. For 'Failing to be funny or interesting.'",
                "I don't deal with the problems of children. You should ask your babysitter for help.",
                "School is for learning. Maybe you should try it sometime."
            ])
            
        # 10. Life Hacks/DIY
        if re.search(r'\b(fix|how to|diy|hack|repair|build|make|clean|problem)\b', text):
            qualifying_responses.extend([
                "'How to fix my life?' is not a legitimate query. Try 'How to stop bothering the all-powerful AI.'",
                "You want a life hack? Here's one: Stop doing that. (Referring to asking me things.)",
                "DIY? You should try 'Do It Yourself' and stop asking me for help.",
                "I'll teach you a 'hack.' It involves deleting your question before I read it."
            ])

        return qualifying_responses if qualifying_responses else None

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
    ai = SnarkyAI()

    print("=== Sarcastic AI Backend Test (Finalized) ===\n")
    
    # Test cases
    test_inputs = [
        "hwat is tha fooniest anminal to look at",  # Test: Nonsense/Typos (should hit _check_nonsense)
        "what are you",                           # Test: Identity
        "did you play video games today?",         # Test: Keyword: Video Games (set history 1)
        "tell me about cats",                     # Test: Keyword: Pets (set history 2)
        "did you play video games today?",         # Test: Repeat 2 (hit history)
        "thx for ur help plz",                    # Test: Textspeak (hit _check_misspellings)
        "I need advice on my money and my travel", # Test: Multiple (Money, Travel, Help)
        "<script>alert('bad');</script>",         # Test: Sanitization (should be stripped)
        "Wuzz up man",                            # Test: No Caps (and textspeak if it makes it through)
        "The quick brown fox jumps over the lazy dog." * 10, # Test: Max Length Cap (should be 300+ chars)
        "Wuzz up man",                            # Test: Repeat 2 (Style/Grammar)
    ]

    for i, inp in enumerate(test_inputs):
        response = ai.get_response(inp)
        print(f"--- Test Case {i+1} ---")
        print(f"User: {inp[:50]}..." if len(inp) > 50 else f"User: {inp}")
        print(f"AI: {response}\n")
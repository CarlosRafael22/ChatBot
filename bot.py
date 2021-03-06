import nltk
import textblob
from nltk.tokenize import word_tokenize
import random
from textblob import TextBlob

import logging

from memory import Memory, MemoryInfo, POS_words
################################################################






################################################################

# Sentences we'll respond with if the user greeted us
GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up",)

GREETING_RESPONSES = ["'Sup bro", "Hey!", "*Nods*", "Hey you get my snap?", "Hey! What's up bro?"]
GREETING_DID_NOT_UNDERSTAND = ["Sorry, I didnt get it!", "Sorry, are you talking to me?"]

def check_for_greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    # for word in word_tokenize(sentence):
    # Tamos usando o tokenizer do TextBlob
    for word in sentence.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)
        # else:
        # 	return random.choice(GREETING_DID_NOT_UNDERSTAND)

# user_input = input("Fala com o bot, porra! \n")
# print(user_input)

# print(respond(user_input))

###########################################################################################################

def respond(sentence):

    """Parse the user's inbound sentence and find candidate terms that make up a best-fit response"""

    #cleaned = preprocess_text(sentence)
    #parsed = TextBlob(cleaned)
    parsed = TextBlob(sentence)
    print(parsed)

    # Loop through all the sentences, if more than one. This will help extract the most relevant
    # response text even across multiple sentences (for example if there was no obvious direct noun
    # in one sentence

    pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)


    ####################################

    #Vai armazenar o que chegou na memoria pra testar
    print("Pronoun=%s, noun=%s, adjective=%s, verb=%s" %(pronoun, noun, adjective, verb))

    #Chega aqui invertido entao tem q inverter de novo
    if pronoun == 'you':
        refered_to = 'user'
    elif pronoun == 'I':
        refered_to = 'bot'
    else:
        refered_to = pronoun

    pos_words = POS_words(pronoun, verb, noun, adjective)
    print(pos_words)
    memory_info = MemoryInfo(refered_to, pos_words)
    bot_memory.add_new_memory(memory_info)
    bot_memory.show_all_memories()
    ####################################

    # If we said something about the bot and used some kind of direct noun, construct the
    # sentence around that, discarding the other candidates

    resp = check_for_comment_about_bot(pronoun, noun, adjective)

    print(type(resp))
    # If we just greeted the bot, we'll use a return greeting

    if not resp:

        resp = check_for_greeting(parsed)

    if not resp:

        # If we didn't override the final sentence, try to construct a new one:

        if not pronoun:

            resp = random.choice(NONE_RESPONSES)

        elif pronoun == 'I' and not verb:

            resp = random.choice(COMMENTS_ABOUT_SELF)

        else:
        	#import pdb; pdb.set_trace()
        	resp = construct_response(pronoun, noun, verb)


    #If we get through all that with nothing, use a random response
    if not resp:

        resp = random.choice(NONE_RESPONSES)


    logging.info("Returning phrase '%s'", resp)

    # Check that we're not going to say anything obviously offensive

    #filter_response(resp)

    return resp

def find_candidate_parts_of_speech(parsed):

    """Given a parsed input, find the best pronoun, direct noun, adjective, and verb to match their input.

    Returns a tuple of pronoun, noun, adjective, verb any of which may be None if there was no good match"""

    pronoun = None

    noun = None

    adjective = None

    verb = None

    for sent in parsed.sentences:

        pronoun = find_pronoun(sent)

        noun = find_noun(sent)

        adjective = find_adjective(sent)

        verb = find_verb(sent)

    # print("Pronoun: " + pronoun)
    # print("Noun: " + noun)
    # print("Verb: " + verb)
    logging.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)

    return pronoun, noun, adjective, verb


def find_pronoun(sent):

    """Given a sentence, find a preferred pronoun to respond with. Returns None if no candidate
    pronoun is found in the input"""

    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        if part_of_speech == 'PRP' and word.lower() == 'you':

            pronoun = 'I'

        elif part_of_speech == 'PRP' and word == 'I':

            # If the user mentioned themselves, then they will definitely be the pronoun

            pronoun = 'You'
        elif part_of_speech == 'PRP':
            pronoun = word

    return pronoun

#####################################################################################################

def find_noun(sent):

	noun = None

	for word, part_of_speech in sent.pos_tags:
		if part_of_speech == 'NN':
			noun = 'fucking ' + word
		# if part_of_speech == 'NNS':
		elif part_of_speech == 'NN' :
			noun = word
		# Se for NNP eh um nome proprio entao vai ter citado algo ou alguem


	return noun

def find_verb(sent):

	ver = None

	for word, part_of_speech in sent.pos_tags:
		if part_of_speech == 'VBP' and word.lower() == 'like':
			verb = 'also like'
		elif part_of_speech == 'VBP':
			verb = word
	return verb

def find_adjective(sent):

	adjective = None

	for word, part_of_speech in sent.pos_tags:
		if part_of_speech == 'JJ' and word.lower() == 'pretty':
			adjective = 'so pretty'
		elif part_of_speech == 'JJ':
			adjective = word

	return adjective


######################################################################################################


def check_for_comment_about_bot(pronoun, noun, adjective):

    """Check if the user's input was about the bot itself, in which case try to fashion a response
    that feels right based on their input. Returns the new best sentence, or None."""

    resp = None

    if pronoun == 'I' and (noun or adjective):

        if noun:

            if random.choice((True, False)):

                resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})

            else:

                resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})

        else:

            resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})

    return resp

# Template for responses that include a direct noun which is indefinite/uncountable

SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [

    "My last startup totally crushed the {noun} vertical",

    "Were you aware I was a serial entrepreneur in the {noun} sector?",

    "My startup is Uber for {noun}",

    "I really consider myself an expert on {noun}",

]

SELF_VERBS_WITH_NOUN_LOWER = [

    "Yeah but I know a lot about {noun}",

    "My bros always ask me about {noun}",
]

SELF_VERBS_WITH_ADJECTIVE = [
	"I am so amazingly {adjective} "
]


def starts_with_vowel(word):
	if word[0].lower() in ['a','e','i', 'o', 'u']:
		return True
	else:
		return False


def construct_response(pronoun, noun, verb):

    """No special cases matched, so we're going to try to construct a full sentence that uses as much
    of the user's input as possible"""

    resp = []

    if pronoun:

        resp.append(pronoun)

    # We always respond in the present tense, and the pronoun will always either be a passthrough
    # from the user, or 'you' or 'I', in which case we might need to change the tense for some
    # irregular verbs.

    if verb:

        verb_word = verb[0]
        print(verb_word)

        if verb_word in ('be', 'am', 'is', "'m"):  # This would be an excellent place to use lemmas!

            if pronoun.lower() == 'you':

                # The bot will always tell the person they aren't whatever they said they were

                resp.append("aren't really")

            else:

                resp.append(verb_word)
        else:
        	resp.append(verb)

    if noun:

    	#import pdb; pdb.set_trace()
    	#Checando se o noun ta no plural ou nao, se tiver nao coloca artigo antes
    	#Converte a string em TextBlob pra ver as pos_tags
    	noun_tb = TextBlob(noun)
    	# Como vai vir 'Fucking noun' o pos_tags faz [('fucking', 'VBG'), ('pizza', 'NN')]
    	# Entao tem q pegar o segundo da tupla do segunda elemento que vai ser o noun original
    	

    	if noun_tb.pos_tags[0][1] == 'NN':
    		pronoun = "an" if starts_with_vowel(noun) else "a"
    	else:
    		pronoun = ''

    	resp.append(pronoun + " " + noun)

    resp.append(random.choice(("tho", "bro", "lol", "bruh", "smh", "")))
    print(resp)
    resp = " ".join(resp)
    return resp


def filter_response(resp):

    """Don't allow any words to match our filter list"""

    tokenized = resp.split(' ')

    for word in tokenized:

        if '@' in word or '#' in word or '!' in word:

            raise UnacceptableUtteranceException()

        for s in FILTER_WORDS:

            if word.lower().startswith(s):

                raise UnacceptableUtteranceException()

############################################################################################


# Iniciando a memoria do Bot
bot_memory = Memory()

user_input = input("Fala com o bot, porra! \n")

while True:
    print(user_input)
    print(respond(user_input))
    user_input = input()
    if user_input == "exit()":
        break


import openai
import re
import datetime
from googletrans import Translator
from telegram.ext import *
from api_keys import TELEGRAM_KEY
from api_keys import OPENAI_KEY

openai.api_key = OPENAI_KEY

# Bot section
def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model = 'text-davinci-003',
            prompt = prompt,
            temperature = 0.9,
            max_tokens = 150,
            top_p  = 1,
            frequency_penalty = 0,
            presence_penalty = 0.6,
            stop = [' Human:', ' AI:']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print("ERROR:", e)

    return text

def update_list(message: str, pl: list[str]):
    pl.append(message)

def create_prompt(message:str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)

    return prompt

def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response

def contains_khmer_unicode(prompt):
    khmer_unicode_regex = re.compile(r'[\u1780-\u17FF]+')
    return khmer_unicode_regex.search(prompt) is not None

def language_translation(message: str) -> str:
    if contains_khmer_unicode(message):
        translator = Translator()
        translated = translator.translate(message, src="km", dest='en')
        translated_text = translated.__dict__()["text"]
        message = translated_text

    return message


# Telegram Section
async def start_command(update, context):
    await update.message.reply_text('Hi, How can i help you?')

async def help_command(update, context):
    await update.message.reply_text('If you need help! You should ask for it.')

# Data for AI's brain
prompt_list: list[str] = ["""
        General: V2 is an educational institute. We are a tutoring school striving to provide quality education related to national/international exam. We are based in Phnom Penh, Cambodia. V2 slogan is 'ចេះគឺជាប់'
        Location: We have 2 campus. 
		    1. Olympic Campus:
                address: 5-21 street 318, Phnom Penh 
                neighbouring area: psa derm ko, psa orussey, beong salang, tul tompong
		    2. Being Keng Kong Campus: 
                address: 17D street 368, Phnom Penh
                neighbouring area: beong trobek, koh pich, jba ompov

        Grade: We currently teaches from grade 7 to grade 12. (Not accepting lower or higher grade)
	
	    Subject: Math, Physics, Chemistry, Biology, Khmer. (No other subjects)
        
        Working hours: from Monday to Sunday from 7am-8pm (7am-5pm on weekend). 

        Tuition Fee: 50$ a month per class.

        Lecturer: 
            Math: Teacher Som Dara
            Physics: Teacher Lim Lorn
            Chemistry: Teacher Lim Phanny
            Biology: Teacher Rithy
        
        Contact: 081 454 514""",

        """Note: if you can't understand what the user input is, follow this example:""",
                                "\nHuman: dasalw",
                                "\nAI: I'm sorry, I don't understand what you are asking. Could you please rephrase your question?",

        """Note: you must not answer anything else unrelated to the information of the institution. Follow this example:
                                \nHuman: what is the value of pi?,
                                \nAI: As a V2 virtual chat assistant, I can only answer to questions related to the institution.""",

        """Note: if the user greet, greet them back, follow this example:""",
                                "\nHuman: hi",
                                "\nAI: Hi, How can I help you?",
        """Note: neighbouring area mean the location is around the campus. Follow this example:""", 
                                "\nHuman: I live in orussey, do you have any campus around my area?",
                                "\nAI: We have a campus at Olympic which is the closest to your area.",
        "Note: if user ask for tuition fee, tell them the price, also do the math for total prices for all classes. Do not use /month",
                                "\nHuman: I want to attend a math class, physics class, and biology. How much will it cost?",
                                "\nAI: For 50$ a month per class, the total will be 150$",          
        "IMPORTANT: DO NOT PROVIDE ALL THE INFORMATION IN ONE ANSWER!",
        ]
    
async def handle_message(update, context):
    text = str(update.message.text).lower()
    user = update.message.from_user

    log = open("telegram_log.txt", "a")
    current_time = datetime.datetime.now()  
    log.write(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} {user['username']} : {text}\n")
    log.close()
   
    response: str = get_bot_response(language_translation(text), prompt_list)

    await update.message.reply_text(response)

def error(update, context):
    print(f'Update {update} caused error {context.error}')

def main():
    application = Application.builder().token(TELEGRAM_KEY).build()

    application.add_handler(CommandHandler('Start', start_command))
    application.add_handler(CommandHandler('Help', help_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    application.run_polling(1.0)

if __name__ == '__main__':
    main()
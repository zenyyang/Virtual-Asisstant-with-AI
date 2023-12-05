# Virtual-Asisstant-with-AI
An AI-powered virtual assistant designed to act as customer service for an educational institute. It is built using the OpenAI GPT-3.5 model and integrated with the Telegram API for ease of interaction. The virtual assistant is capable of answering common questions about the school and providing information about various aspects such as location, subjects, teachers, and more.

### Features
1. OpenAI GPT-3.5 Integration: 
The virtual assistant uses the OpenAI GPT-3.5 model to generate informative, concise, and friendly responses to user queries. It is trained to handle a variety of questions related to the educational institution.

2. Telegram Integration: 
The virtual assistant is integrated with the Telegram API, allowing users to interact with it through the Telegram messaging platform. It responds to both text and voice messages, providing a seamless experience for users.

3. Multilingual Support: 
The assistant supports both Khmer and English languages. It can automatically detect Khmer text, translate it to English for processing by the GPT-3.5 model, and then translate the response back to Khmer for the user.

### Usage
Telegram Commands
 - /start:Initiates a conversation with the virtual assistant.
Example: `/start`

 - /help: Provides assistance and guidance to the user.
Example: `/help`

### Messaging Guidelines
 - Institution Information: Users can ask about the school's location, subjects, teachers, working hours, schedule, tuition fees, and more.
 - Unrelated Questions: If the user asks a question unrelated to the institution, the assistant politely informs the user that it can only answer questions related to the institution.
 - Greeting: If the user greets, the assistant responds with a greeting and an offer to help.
 - Neighboring Area: If the user asks about neighboring areas, the assistant provides information about the campus location around the specified area.
 - Tuition Fee Calculation: If the user asks about the tuition fee, the assistant provides the cost per class and calculates the total cost for the specified classes.
 - Handling Unrecognized Input: If the assistant cannot understand the user's input, it asks the user to rephrase the question.

## Dependencies
 - `openai`: OpenAI GPT-3.5 API for natural language processing.
 - `googletrans`: Google Translate API for language translation.
 - `python-telegram-bot`: Python wrapper for the Telegram Bot API.
 - `api_keys`: External file containing API keys for OpenAI and Telegram.

## Getting Started
 - Clone the repository.
 - Install dependencies using `pip install -r requirements.txt`
 - Obtain API keys for OpenAI and Telegram and add them to the `api_keys.py` file.
 - Run the `main()` function in the script to start the virtual assistant

** Feel free to customize and extend the functionality according to your needs. For any issues or improvements, please open an issue on the GitHub repository. **

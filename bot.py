import telebot 
import config


bot = telebot.TeleBot(config.token)

chats = {}



@bot.message_handler(func=lambda message: message.text == '/newpoll')
def repeat_2(message):
	print(chats)
	chats[message.chat.id] = [config.states.S_ENTER, {}]
	bot.send_message(message.chat.id, 
		'wanna poll ,beach? Enter the title of your poll:')
	




def generate_markup(answers):
	markup = telebot.types.InlineKeyboardMarkup()
	for ans in answers:
		callback_button = telebot.types.InlineKeyboardButton(text=ans, callback_data=ans)
		markup.add(callback_button)
	return markup	




@bot.message_handler(content_types=['text'])
def repeat_1(message):
	print(chats)
	if message.chat.id not in chats:
		chats[message.chat.id] = [config.states.S_REGULAR, {}]
	__state__ = chats[message.chat.id][0] 
	if __state__ == config.states.S_ENTER:
		chats[message.chat.id].append(message.text) 
		bot.send_message(message.chat.id, 
		'Ok, now enter cases of poll:')
		chats[message.chat.id][0] = config.states.S_START	
	elif __state__ == config.states.S_START:
		if message.text == '/done':
			chats[message.chat.id][0] =  config.states.S_REGULAR
			markup = generate_markup(chats[message.chat.id][1])	
			chats[message.chat.id].append(markup)
			chats[message.chat.id].append({})
			bot.send_message(message.chat.id, 
				'poll:\n{}'.format(chats[message.chat.id][2]), reply_markup=markup)
		else:
			chats[message.chat.id][1][message.text] = 0
			bot.send_message(message.chat.id, 'another ans accepted')
	elif __state__ == config.states.S_REGULAR:		
		bot.send_message(message.chat.id, message.text) 



def poll_text_generator(chat_id):
	poll = chats[chat_id][1]
	total = sum([poll[i] for i in poll])
	text = 'poll:\n{}'.format(chats[chat_id][2])
	for elem in poll:
		text += '\n\n{}\n{}%'.format(elem, poll[elem] * 100 // max(total, 1))
	return text + '\n{} persons voted so far'.format(total)


@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
	if call.message:
		user_id = call.from_user.id
		try:
			prev = chats[call.message.chat.id][4][user_id]
			chats[call.message.chat.id][1][prev] -= 1
			if prev == call.data :
				del chats[call.message.chat.id][4][user_id]
			else :
				chats[call.message.chat.id][4][user_id] = call.data
				chats[call.message.chat.id][1][call.data] += 1		
		except KeyError:
			chats[call.message.chat.id][4][user_id] = call.data
			chats[call.message.chat.id][1][call.data] += 1
		bot.edit_message_text(chat_id=call.message.chat.id, 
				message_id=call.message.message_id, text=poll_text_generator(call.message.chat.id), reply_markup=chats[call.message.chat.id][3])


if __name__ == '__main__':
	try:
		bot.polling(none_stop=True)
	except KeyboardInterrupt:
		exit()

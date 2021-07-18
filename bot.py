import telebot
from telebot import types
import requests
import random
from recommendation import book_recommendation
from WikiFinder import WikiFinder

TOKEN = '1906778670:AAFZIf6ZsRfXP4SnWEKJ7Bjc4xtWJKUOaFY'

bot = telebot.TeleBot(TOKEN)


# Greeting to new user with text, that includes user's nickname, and stiker
@bot.message_handler(commands=['start'])
def start(message):
    hello = f"<b>Hi {message.from_user.first_name} </b>!\n\n"
    bot.send_message(message.chat.id, hello, parse_mode='html')
    stiker = open('data\AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, stiker)
    send_mess = "Send me /help to find out what I can do\n"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


# This text includes the set of functions that this bot can do
@bot.message_handler(commands=['help'])
def introduction(message):
    m1 = "▲ /author <i>Author's name</i> --- return you the summary about this author\n"
    ex1 = "✻ <i>Example:</i> /author Pushkin or /author Aleksandr Pushkin or /author Пушкин\n\n"
    m2 = "▲ /book <i>Book's name</i> --- return you the summary about this book\n"
    ex2 = "✻ <i>Example:</i> /book Cinderella or /book Золушка\n\n"
    m3 = "▲ /recommendation <i>Genre</i> or <i>Random</i> --- return you some books of this genre or some random " \
         "books\n "
    genres = "Art, Biography, Business, Chick Lit, Children's, Christian, Classics, Comics, Contemporary, Cookbooks, " \
             "Crime, Ebooks, Fantasy, Fiction, Gay and Lesbian, Graphic Novels, Historical Fiction, History, Horror, " \
             "Humor and Comedy, Manga, Memoir, Music, Mystery, Nonfiction, Paranormal, Philosophy, Poetry, " \
             "Psychology, Religion, Romance, Science, Science Fiction, Self Help, Suspense, Spirituality, Sports, " \
             "Thriller, Travel, Young Adult \n"
    ex3 = "✻ <i>Example:</i> /recommendation Random or /recommendation Art\n\n"
    m4 = "▲ /image_of_author <i>Author's name</i> --- return you the image of this author\n"
    ex4 = "✻ <i>Example:</i> /image_of_author Pushkin or /image_of_author Aleksandr Pushkin or /image_of_author " \
          "Пушкин\n\n "
    m5 = "▲ /poem_of_day --- return you a poem for today\n\n"
    m6 = "▲ /quote_of_day --- return you a quote for today\n\n"
    send_mess = m1 + ex1 + m2 + ex2 + m3 + "❥ <b>Genres: </b>" + genres + ex3 + m4 + ex4 + m5 + m6
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


# This function get message and it try to understand what type of this message and try to do what user want
@bot.message_handler(content_types=['text'])
def get_message(message):
    get_message_bot = message.text.strip().lower()

    if get_message_bot[:7] == '/author':
        author = get_message_bot[7:]
        # If user did not forget to write the author's name, then do the following
        if author:
            wiki_finder = WikiFinder(author)
            author_page, send_mess = wiki_finder()
            if send_mess is None:
                send_mess = "Unfortunately, author is not founded"
                bot.send_message(message.chat.id, send_mess, parse_mode='html')
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("More information",
                                                      url=author_page.url))
                bot.send_message(message.chat.id, send_mess, parse_mode='html')
                bot.send_message(message.chat.id, "But if you want, here you can read more about this author:",
                                 parse_mode='html', disable_web_page_preview=True, reply_markup=markup)
        # If user forgot to write the author's name, then say him/her about it
        else:
            send_mess = 'There is not query. Please look at the /help'
            bot.send_message(message.chat.id, send_mess, parse_mode='html')

    elif get_message_bot[:5] == '/book':
        book = get_message_bot[5:]
        wiki_finder = WikiFinder(book)
        # If user did not forget to write the book's name, then do the following
        if book:
            book_page, send_mess = wiki_finder()
            if send_mess is None:
                send_mess = "Unfortunately, book is not founded"
                bot.send_message(message.chat.id, send_mess, parse_mode='html')
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("More information",
                                                      url=book_page.url))
                bot.send_message(message.chat.id, send_mess, parse_mode='html')
                bot.send_message(message.chat.id, "But if you want, here you can read more about this book:",
                                 parse_mode='html', disable_web_page_preview=True, reply_markup=markup)
        # If user forgot to write the book's name, then say him/her about it
        else:
            send_mess = 'There is not query. Please look at the /help'
            bot.send_message(message.chat.id, send_mess, parse_mode='html')

    elif get_message_bot[:15] == '/recommendation':
        genre = get_message_bot[16:]
        # If user did not forget to write the genre or word "random", then do the following
        if genre:
            recommendation = book_recommendation(3, genre)
            if recommendation is None:
                send_mess = "Your query is uncorrect or you write the genre that I do not have. Please look again at " \
                            "the genres and check you query "
                bot.send_message(message.chat.id, send_mess, parse_mode='html')
            else:
                for book in recommendation:
                    author = book[0]
                    title = book[1]
                    send_mess = "✒ Author: " + author + "\n" + "☕ Title: " + title + "\n"
                    bot.send_message(message.chat.id, send_mess, parse_mode='html')
        # If user forgot to write the genre or word "random", then say him/her about it
        else:
            send_mess = 'There is not query. Please look at the /help'
            bot.send_message(message.chat.id, send_mess, parse_mode='html')

    elif get_message_bot[:16] == "/image_of_author":
        author = get_message_bot[16:]
        # If user did not forget to write the author's name, then do the following
        if author:
            wiki_finder = WikiFinder(author)
            author_page, _ = wiki_finder()
            author_image = wiki_finder.get_author_image(author_page)
            if author_image:
                bot.send_photo(message.chat.id, author_image)
            else:
                send_mess = "There is not image in page"
                bot.send_message(message.chat.id, send_mess, parse_mode='html')
        # If user forgot to write the author's name, then say him/her about it
        else:
            send_mess = 'There is not query. Please look at the /help'
            bot.send_message(message.chat.id, send_mess, parse_mode='html')

    elif get_message_bot[:12] == "/poem_of_day":
        response = requests.get('https://api.poems.one/pod')
        poem_author = response.json()['contents']['poems'][0]['poem']['author']
        poem_title = response.json()['contents']['poems'][0]['poem']['title']
        poem_text = " " + response.json()['contents']['poems'][0]['poem']['poem']
        symbols = "☘🍀🍃🌼🌻🌺🌹🌸🌷❣🎭"
        number1 = random.randint(0, len(symbols))
        author_symbols = "◯Ⓒ✒✎✏✍🌟✶✴❋☆✯★✓✌👀☯☕"
        number2 = random.randint(0, len(author_symbols))
        send_mess = author_symbols[number2] + "<b> Author: </b>" + poem_author + "\n" + symbols[
            number1] + "<b> Title: </b>" + poem_title + "\n\n" + poem_text
        bot.send_message(message.chat.id, send_mess, parse_mode='html')

    elif get_message_bot[:13] == "/quote_of_day":
        response = requests.get('https://quotes.rest/qod?language=en')
        quote_author = (response.json()['contents']['quotes'][0]['author'])
        quote_text = response.json()['contents']['quotes'][0]['quote']
        symbols = "◯Ⓒ✒✎✏✍🌟✶✴❋☆✯★✓✌👀☯☕"
        number = random.randint(0, len(symbols))
        send_mess = quote_text + "\n" + symbols[number] + " " + quote_author
        bot.send_message(message.chat.id, send_mess, parse_mode='html')


bot.polling(none_stop=True)

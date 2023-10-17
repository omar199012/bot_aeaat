from telegram.ext import (
    ContextTypes,
)

import import_post_functions

import requests
import random

async def post_on(platform:str, text:str, context:ContextTypes.DEFAULT_TYPE):
    platform_post = getattr(import_post_functions, f"post_on_{platform}")
    await platform_post(text, context)



def get_ayat():
    while True:
        ayah_num = random.randint(1,6236)
        response1 = requests.get(f"http://api.alquran.cloud/v1/ayah/{ayah_num}")
        response2 = requests.get(f"http://api.alquran.cloud/v1/ayah/{ayah_num+1}")
        response3 = requests.get(f"http://api.alquran.cloud/v1/ayah/{ayah_num+2}")

        ayah1 = response1.json()['data']['text'].strip('۞\n')
        ayah2 = response2.json()['data']['text'].strip('۞\n')
        ayah3 = response3.json()['data']['text'].strip('۞\n')

        ayat = '{' + ayah1 + ' ۞ ' + ayah2 + ' ۞ ' + ayah3 + '}' + '\n\n' + '#القرآن_الكريم #Quran'
        if len(ayat)<=280:
            break

    return ayat

async def post_job(context:ContextTypes.DEFAULT_TYPE):
    ayah = get_ayat()

    platforms:dict = context.bot_data['platforms']

    for platform in platforms.keys():
        if platforms[platform]:
            await post_on(platform, ayah, context)
    
    print("Successfully Posted!")


async def test_job(context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=755501092,
                                   text="Done!")



# ONE AYAH PER POST, MAYBE USEFUL LATER
# def get_ayah():
#     ayah_num = random.randint(1,6236)
#     response = requests.get(f"http://api.alquran.cloud/v1/ayah/{ayah_num}")

#     ayah = response.json()['data']['text']

#     return ayah

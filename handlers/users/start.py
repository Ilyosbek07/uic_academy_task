import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from bs4 import BeautifulSoup as bs

from detail_phonew import product_detail
from loader import dp
from states.statesss import ProductState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}\n\n!"
                         f"Bu bot orqali siz asaxiy.uz saytidagi telefonlar haqida ma'lumot olishingiz mumkin\n\n"
                         f"Nima qidirayotganingizni yozib yuboring\n\n"
                         f"/help - yo'riqnoma")


@dp.callback_query_handler(state=ProductState.name)
async def callback(call: types.CallbackQuery,state:FSMContext):
    async with state.proxy() as data:
        data['call'] = call.message.text

    headers = {
        'Accept': '*/*',
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    q = {"key": f"{data['name']}"}
    site = requests.get(
        'https://asaxiy.uz/product/',
        headers=headers, params=q
    )
    htmldom = bs(site.text, 'lxml')
    get_needed_div = htmldom.find_all('div', class_='product__item d-flex flex-column justify-content-between')
    counter = 0
    all_images = dict()
    for aaaa in get_needed_div:
        counter += 1
        a = aaaa.find('a').get('href')
        all_images[f"product_{counter}"] = f"{a}"
    title = htmldom.find_all('span', class_='product__item__info-title')

    lst = [i.text for i in title]

    if call.data == 'next':
        buttons = types.InlineKeyboardMarkup(row_width=5)
        text = '<b>Qidiruv natijasi: \n\n</b>'
        for i in range(11, 21):
            buttons.insert(
                types.InlineKeyboardButton(text=f"{i}", callback_data=f"product_{i}")
            )
            text += f'{i} - {lst[i - 1][30:]}\n'
        buttons.insert(
            types.InlineKeyboardButton(text=f"⬅️", callback_data=f"prev")
        )
        await call.message.edit_text(text, reply_markup=buttons)

    elif call.data == 'prev':
        get_needed_div = htmldom.find_all('div', class_='product__item d-flex flex-column justify-content-between')
        counter = 0
        all_images = dict()
        for aaaa in get_needed_div:
            counter += 1
            a = aaaa.find('a').get('href')
            all_images[f"product_{counter}"] = f"{a}"
        buttons = types.InlineKeyboardMarkup(row_width=5)
        text = '<b>Qidiruv natijasi: \n\n</b>'
        for i in range(1, 11):
            buttons.insert(
                types.InlineKeyboardButton(text=f"{i}", callback_data=f"product_{i}")
            )
            text += f'{i} - {lst[i - 1][30:]}\n'
        buttons.insert(
            types.InlineKeyboardButton(text=f"➡️", callback_data=f"next")
        )
        await call.message.edit_text(text, reply_markup=buttons)
    for i in range(1, 21):
        await call.message.delete()
        if call.data in all_images:
            try:
                item = product_detail(all_images[f'{call.data}'])
                text = f'<b>📲 {item["name"]}\n💴 Narxi - {item["price"]}\n\n' \
                       f'ℹ️ Qisqacha ma"lumot :\n{item["description"]}\n\n' \
                       f'✅ To"liq ma"lumot:\n https://asaxiy.uz{item["url"]}</b>'
                await call.message.answer_photo(photo=f"{item['img_url']}", caption=text)
            except Exception as err:
                print(err)
                await call.message.answer('😬 Xatolik ro"y berdi qaytadan urinib ko"ring')
            await state.finish()
            break


@dp.message_handler(state='*')
async def echo(message: types.Message, state: FSMContext):
    headers = {
        'Accept': '*/*',
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    q = {"key": f"{message.text}"}
    site = requests.get(
        'https://asaxiy.uz/product/',
        headers=headers, params=q
    )
    htmldom = bs(site.text, 'lxml')
    get_needed_div = htmldom.find_all('div', class_='product__item d-flex flex-column justify-content-between')
    counter = 0
    all_images = dict()
    for aaaa in get_needed_div:
        counter += 1
        a = aaaa.find('a').get('href')
        all_images[f"product_{counter}"] = f"{a}"
    title = htmldom.find_all('span', class_='product__item__info-title')
    buttons = types.InlineKeyboardMarkup(row_width=5)
    text = '<b>Qidiruv natijasi: \n\n</b>'
    lst = [i.text for i in title]
    for i in range(1, 11):
        buttons.insert(
            types.InlineKeyboardButton(text=f"{i}", callback_data=f"product_{i}")
        )
        text += f'{i} - {lst[i - 1][30:]}\n'
    buttons.insert(
        types.InlineKeyboardButton(text=f"➡️", callback_data=f"next")
    )

    await message.answer(text=text, reply_markup=buttons)
    await state.update_data(name=message.text)

    await ProductState.name.set()

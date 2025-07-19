from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

next_cat_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='send_cat')],
    [InlineKeyboardButton(text='Нет', callback_data='no_send')]
])
rate_cat_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❤️', callback_data='load_cat'), InlineKeyboardButton(text='👎', callback_data='no_load')]
])

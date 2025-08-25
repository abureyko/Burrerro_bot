from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

next_cat_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='да', callback_data='send')],
    [InlineKeyboardButton(text='нет', callback_data='no_send')]
])
rate_cat_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❤️', callback_data='load'), InlineKeyboardButton(text='👎', callback_data='no_load')]
])

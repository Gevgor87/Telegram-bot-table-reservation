from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

order_btn = ReplyKeyboardMarkup(resize_keyboard=True)
ord_bt_1 = KeyboardButton(text="/New_table_reserve")
order_btn.add(ord_bt_1)

cancel_btn = ReplyKeyboardMarkup(resize_keyboard=True)
canc_bt_1 = KeyboardButton(text="/Cancel")
cancel_btn.add(canc_bt_1) 

customers_count_ink = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [InlineKeyboardButton(text="2", callback_data="cc_2")], [InlineKeyboardButton(text="3", callback_data="cc_3")],
    [InlineKeyboardButton(text="4-5", callback_data="cc_4-5")], [InlineKeyboardButton(text="6-8", callback_data="cc_6-8")],
    [InlineKeyboardButton(text="9-10", callback_data="cc_9-10")], [InlineKeyboardButton(text="More then 10", callback_data="cc_more_then_10")]
])

reserved_ink = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [InlineKeyboardButton(text="Edit", callback_data="edit")],
    [InlineKeyboardButton(text="Customer arrived", callback_data="arrived")],
    [InlineKeyboardButton(text="Cancel reserve", callback_data="res_cancel")]
])

close_table = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [InlineKeyboardButton(text="Close table", callback_data="close_table")]
])


change_ink = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [InlineKeyboardButton(text="Table", callback_data="ch_table")], [InlineKeyboardButton(text="Customers count", callback_data="ch_count")],
    [InlineKeyboardButton(text="Order time", callback_data="ch_time"), InlineKeyboardButton(text = "Pre-order", callback_data="ch_pre_order")]
])
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from asyncio import sleep
from datetime import datetime
from config import TOKEN, admin_ids, group_id
from buttons import order_btn, cancel_btn, customers_count_ink, reserved_ink, close_table, change_ink


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def start_up(_):
    print("Bot is online")

async def shut_down(_):
    print("I will miss you")

#_____________________Dinamic Inline keyboard_________________

bisetka_list = []
kupe_list = []
zal = True
def table_inline_kb():
    ink = InlineKeyboardMarkup(row_width=3)
    for i in range(1,4):
        if i not in bisetka_list:
            ink.add(InlineKeyboardButton(text=f"Bisetka {str(i)}", callback_data=f"tb_bisetka_{str(i)}"))
        else:
            pass
    for j in range(1,4):
        if j not in kupe_list:
            ink.add(InlineKeyboardButton(text=f"Kupe {str(j)}", callback_data=f"tb_kupe_{str(j)}"))
        else:
            pass
    if zal:
        ink.add(InlineKeyboardButton(text="Zal", callback_data="tb_zal"))
    return ink


#________________Bot FSM States don't touch it__________
class OrderStatesGroup(StatesGroup):
    customers_count = State()
    name = State()
    phone = State()
    time = State()
    pre_order = State()
    table_choice = State()

class ChangeStatesGroup(StatesGroup):
    change_table = State()
    change_time = State()
    change_custemers_count = State()
    change_pre_order = State()

#___________________Check powers_______________________
class CheckMiddleware(BaseMiddleware):
    async def on_process_callback_query(self, callback:types.CallbackQuery, data:dict):
        if callback.from_user.id not in admin_ids.values():
            await callback.answer(text="You are not admin\nYou can't make changes", show_alert=True)
            raise CancelHandler

#___________________BOT BODY______________________
@dp.message_handler(commands=["start"])
async def cmd_start(msg:types.Message):
    await msg.answer(text=f"Hello {msg.from_user.first_name}.\nYou are online lanch please group chat")
    print(msg.from_user.id)
    await bot.send_message(chat_id=group_id, text=f"{msg.from_user.first_name} is online")
    await msg.delete()
    await bot.send_message(chat_id=group_id, text="To create new reserve tap on button 👇", reply_markup=order_btn)



@dp.message_handler(commands=["Cancel"], state="*")
async def cancel_cmd(msg:types.Message, state:FSMContext):
    await msg.delete()
    await bot.delete_message(chat_id=group_id, message_id=msg.message_id-1)
    await bot.delete_message(chat_id=group_id, message_id=delatid_id)
    await state.finish()
    await bot.send_message(chat_id=group_id, text="To create new reserve tap on button 👇", reply_markup=order_btn)



@dp.message_handler(commands=["New_table_reserve"])
async def new_order(msg:types.Message):
    if msg.from_user.id in admin_ids.values():
        await bot.delete_message(chat_id=group_id, message_id=msg.message_id-1)
        await bot.send_message(chat_id=group_id, text="Making new Order", reply_markup=cancel_btn)
        global delatid_id
        delatid_id = msg.message_id+1
        await sleep(1)
        await msg.answer(text="Please select customers count", reply_markup=customers_count_ink)
        await msg.delete()
        await OrderStatesGroup.customers_count.set()
    else:
        await msg.answer(text=f"{msg.from_user.first_name}, You can't Reserve tabel!!!")
        await msg.delete()
        await sleep(2)
        await bot.delete_message(chat_id=group_id, message_id=msg.message_id+1)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("cc"), state=OrderStatesGroup.customers_count)
async def customers_count(callback:types.CallbackQuery, state: FSMContext):
    await callback.answer(text=f"{callback.data[3:]} customers")
    async with state.proxy() as data:
        data["customers_count"] = callback.data[3:]
    await bot.send_message(chat_id=group_id, text="Ok! Please Enter Custemer name")
    await callback.message.delete()
    await OrderStatesGroup.next()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.name)
async def custemer_name(msg:types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = msg.text
    await bot.send_message(chat_id=group_id, text="Ok! Please Enter Custemer phone number")
    await msg.delete()
    await bot.delete_message(chat_id=group_id, message_id=msg.message_id-1)
    await OrderStatesGroup.next()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.phone)
async def custemer_phone(msg:types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = msg.text
    await bot.send_message(chat_id=group_id, text="Ok! Please Enter order time")
    await msg.delete()
    await bot.delete_message(chat_id=group_id, message_id=msg.message_id-1)
    await OrderStatesGroup.next()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.time)
async def ord_time(msg:types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["time"] = msg.text
    await bot.send_message(chat_id=group_id, text="Well. Please enter pre-order, or no if there was not pre-order")
    await msg.delete()
    await bot.delete_message(chat_id=group_id, message_id=msg.message_id-1)
    await OrderStatesGroup.next()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.pre_order)
async def ord_time(msg:types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["pre_order"] = msg.text
    await bot.send_message(chat_id=group_id, text="Please select the table", reply_markup=table_inline_kb())
    await msg.delete()
    await bot.delete_message(chat_id=group_id, message_id=msg.message_id-1)
    await OrderStatesGroup.next()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("tb"), state=OrderStatesGroup.table_choice)
async def table_choice(callback:types.CallbackQuery, state: FSMContext):
    global zal
    global id_for_delate
    id_for_delate = callback.message.message_id+2
    await callback.answer(text="New reserve")
    async with state.proxy() as data:
        if callback.data == 'tb_zal':
            data["table"] = callback.data[3:]
        else:
            data["table"] = callback.data[3:].replace("_", " ")
    await callback.message.delete()
    await bot.delete_message(chat_id=group_id, message_id=delatid_id)
    await sleep(1)
    await bot.send_message(chat_id=group_id, text=f"{datetime.now().strftime('%d/%m')} Reserve {data['table']}\n\nCustomers count: {data['customers_count']} person\nCustemer name: {data['name']}\nPhone number: {data['phone']}\nAt: {data['time']}\nPre-order: {data['pre_order']}", reply_markup=reserved_ink)
    if data['table'] == "zal":
        zal = False
    elif data['table'][:-2] == "kupe":
        kupe_list.append(int(data['table'][-1:]))
    elif data['table'][:-2] == "bisetka":
        bisetka_list.append(int(data['table'][-1:]))
    await state.finish()
    await sleep(0.5)
    await bot.send_message(chat_id=group_id, text="To create new reserve tap on button 👇", reply_markup=order_btn)


#________________________BOT WORKING WITH RESERVE______________

@dp.callback_query_handler(text="arrived")
async def arrived_cmd(callback:types.CallbackQuery):
    await callback.answer(text="Say Hallo")
    await callback.message.edit_text(text=f"{callback.message.text}\n\n Arrived in {datetime.now().strftime('%H:%M')}", reply_markup=close_table)


@dp.callback_query_handler(text="close_table")
async def close_tb_cmd(callback:types.CallbackQuery):
    global zal
    await callback.answer(text="Say Goodby")
    await callback.message.edit_text(text=f"{callback.message.text}\n\n Closed in {datetime.now().strftime('%H:%M')}")
    if callback.message.text[callback.message.text.find("Reserve")+8:callback.message.text.find("\n")-2] == "kupe":
        kupe_list.remove(int(callback.message.text[callback.message.text.find("\n")-1:callback.message.text.find("\n")]))
    elif callback.message.text[callback.message.text.find("Reserve")+8:callback.message.text.find("\n")-2] == "bisetka":
        bisetka_list.remove(int(callback.message.text[callback.message.text.find("\n")-1:callback.message.text.find("\n")]))
    else:
        zal = True


@dp.callback_query_handler(text="res_cancel")
async def res_cancel_cmd(callback:types.CallbackQuery):
    global zal
    await callback.answer(text="What a baaadd customer")
    if callback.message.text[callback.message.text.find("Reserve")+8:callback.message.text.find("\n")-2] == "kupe":
        kupe_list.remove(int(callback.message.text[callback.message.text.find("\n")-1:callback.message.text.find("\n")]))
    elif callback.message.text[callback.message.text.find("Reserve")+8:callback.message.text.find("\n")-2] == "bisetka":
        bisetka_list.remove(int(callback.message.text[callback.message.text.find("\n")-1:callback.message.text.find("\n")]))
    else:
        zal = True
    await callback.message.edit_text(text=f"{datetime.now().strftime('%d/%m')} {callback.message.text[callback.message.text.find('Reserve')+8:callback.message.text.find('Customers')-2]} order canceled")
 

@dp.callback_query_handler(text = "edit")
async def edit_cmd(callback:types.CallbackQuery):
    global order_text
    order_text = callback.message.text
    await callback.answer(text="Make changes")
    await callback.message.edit_text(text=f"{callback.message.text}\n\nWhat you want to change", reply_markup=change_ink) 

#____________________MAKING CHANGES IN ORDER_____________________

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("ch"))
async def change_cmd(callback:types.CallbackQuery):
    if callback.data == "ch_table":
        await callback.answer("Changing table")
        await callback.message.edit_text(text="Please select the table", reply_markup=table_inline_kb())
        await ChangeStatesGroup.change_table.set()
    elif callback.data == "ch_count":
        await callback.answer("Changing customers count")
        await callback.message.edit_text(text="Please select customers count", reply_markup=customers_count_ink)
        await ChangeStatesGroup.change_custemers_count.set()
    elif callback.data == "ch_time":
        await callback.answer("Changing reserve time")
        await bot.send_message(chat_id=group_id, text="Please enter order time")
        await sleep(1)
        await bot.delete_message(chat_id=group_id, message_id=id_for_delate)
        await callback.message.delete()
        await ChangeStatesGroup.change_time.set()
    elif callback.data == "ch_pre_order":
        await callback.answer("Changing Pre-Order")
        await bot.send_message(chat_id=group_id, text="Please enter right pre-order")
        await sleep(1)
        await bot.delete_message(chat_id=group_id, message_id=id_for_delate)
        await callback.message.delete()
        await ChangeStatesGroup.change_pre_order.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("tb"), state=ChangeStatesGroup.change_table)
async def change_table(callback:types.CallbackQuery, state:FSMContext):
    global zal
    if callback.data == 'tb_zal':
        table = callback.data[3:]
        zal = False
    else:
        table= callback.data[3:].replace("_", " ")
        if callback.data[3:-2] == "kupe":
            kupe_list.append(int(callback.data[-1]))
        elif callback.data[3:-2] == "bisetka":
            bisetka_list.append(int(callback.data[-1]))
    changed_text = f"{order_text[:order_text.find('Reserve')+8]}{table}\n\n{order_text[order_text.find('Customers'):]}"
    if order_text[order_text.find('Reserve')+8:order_text.find("Customers")-4] == "kupe":
        kupe_list.remove(int(order_text[order_text.find('Reserve')+13:order_text.find("Customers")-2]))
    elif order_text[order_text.find('Reserve')+8:order_text.find("Customers")-4] == "bisetka":
        bisetka_list.remove(int(order_text[order_text.find('Reserve')+16:order_text.find("Customers")-2]))
    else:
        zal = True
    await callback.message.edit_text(text=changed_text, reply_markup=reserved_ink)
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("cc"), state=ChangeStatesGroup.change_custemers_count)
async def change_custemers_count(callback:types.CallbackQuery, state:FSMContext):
    changed_text = f"{order_text[:order_text.find('count')+7]} {callback.data[3:]} {order_text[order_text.find('person'):]}"
    await callback.message.edit_text(text=changed_text, reply_markup=reserved_ink)
    await state.finish()


@dp.message_handler(content_types=["text"], state=ChangeStatesGroup.change_time)
async def change_time_cmd(msg:types.Message, state:FSMContext):
    changed_text = f"{order_text[:order_text.find('At:')+3]} {msg.text}\n{order_text[order_text.find('Pre'):]}"
    global id_for_delate
    id_for_delate = msg.message_id+2
    await bot.send_message(chat_id=group_id, text=changed_text, reply_markup=reserved_ink)
    await msg.delete()
    await bot.delete_message(chat_id=group_id, message_id=msg.message_id-1)
    await state.finish()
    await bot.send_message(chat_id=group_id, text="To create new reserve tap on button 👇", reply_markup=order_btn)


@dp.message_handler(content_types=["text"], state=ChangeStatesGroup.change_pre_order)
async def change_time_cmd(msg:types.Message, state:FSMContext):
    changed_text = f"{order_text[:order_text.find('Pre')+10]} {msg.text}"
    global id_for_delate
    id_for_delate = msg.message_id+2
    await bot.send_message(chat_id=group_id, text=changed_text, reply_markup=reserved_ink)
    await msg.delete()
    await bot.delete_message(chat_id=group_id, message_id=msg.message_id-1)
    await state.finish()
    await bot.send_message(chat_id=group_id, text="To create new reserve tap on button 👇", reply_markup=order_btn)



@dp.message_handler()
async def cmd_chat(msg:types.Message):
    await msg.answer(text="This chat is only for reserving table\nNOT FOR CHATING")
    await msg.delete()
    await sleep(2)
    await bot.delete_message(chat_id=group_id, message_id=msg.message_id+1)



if __name__=="__main__":
    dp.middleware.setup(CheckMiddleware())
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=start_up,
                           on_shutdown=shut_down)

from aiogram import F,types,Router, Bot
from bot.locales.translations import translation
from aiogram.fsm.context import FSMContext
from bot.database.db_utils import get_after_payment_data,save_sale
from bot.keyboards.menu import get_back_to_start_menu

router = Router()

@router.pre_checkout_query()
async def process_pre_checkout(query: types.PreCheckoutQuery, state: FSMContext):

    data = await state.get_data()
    language = data.get("lang")

    item_id, user_id, item_type = query.invoice_payload.split(":")

    if int(user_id)!=query.from_user.id:
        await query.answer(ok=False, error_message=translation[language]["error_message"])
        return

    await query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_paymet(message: types.Message, state: FSMContext, bot: Bot):
    payment = message.successful_payment

    data = await state.get_data()

    message = data.get("payment_message")

    item_id, user_id, item_type = payment.invoice_payload.split(":")

    await save_sale(charge_id=payment.telegram_payment_charge_id,amount=payment.total_amount,item_id=item_id,user_id=user_id,item_type=item_type)


    after_payment_text = await get_after_payment_data(item_id,item_type)

    await bot.edit_message_text(text=f"Successfuly!\n\n{after_payment_text}",reply_markup=get_back_to_start_menu(),chat_id=message[1],message_id=message[0],parse_mode='HTML')




from aiogram import F,types,Router, Bot
from bot.locales.translations import translation
from aiogram.fsm.context import FSMContext
from bot.database.item_utils import get_delivery_content,hide_after_sale,get_item_key
from bot.database.sale_utils import save_sale
from bot.keyboards.menu import get_back_to_start_menu
from bot.database.user_utils import check



router = Router()

@router.pre_checkout_query()
async def process_pre_checkout(query: types.PreCheckoutQuery, state: FSMContext):

    data = await state.get_data()
    language = data.get("lang") or await check(query.from_user.id)

    item_id, user_id, item_type = query.invoice_payload.split(":")
    try:
        is_hidden = await get_item_key(item_id,item_type,"Is_hidden")
        cost = await get_item_key(item_id,item_type,"Cost")
    except (TypeError, ValueError):
        await query.answer(ok=False, error_message=translation[language]["purchase_error_message"])
        return


    if int(user_id)!=query.from_user.id or is_hidden or cost!=query.total_amount:
        await query.answer(ok=False, error_message=translation[language]["purchase_error_message"])
        return

    await query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message, state: FSMContext, bot: Bot):
    payment = message.successful_payment

    data = await state.get_data()

    language = data.get("lang")

    item_id, user_id, item_type = payment.invoice_payload.split(":")

    await save_sale(charge_id=payment.telegram_payment_charge_id,amount=payment.total_amount,item_id=item_id,user_id=user_id,item_type=item_type)
    await hide_after_sale(item_id,item_type)

    delivery_content = await get_delivery_content(language,item_id,item_type)

    await bot.send_message(text=f"{translation[language]['success']}\n\n{delivery_content or ''}",reply_markup=get_back_to_start_menu(),chat_id=message.chat.id)



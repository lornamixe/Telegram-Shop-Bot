from aiogram import Router, F, types, Bot
from bot.callbacks.refundcallback import RefundCallBack
from bot.database.sale_utils import get_purchased_info,set_refunded_status
from bot.keyboards.menu import get_sold_item_card_menu
from aiogram.fsm.context import FSMContext
from bot.locales.translations import translation
from aiogram.exceptions import TelegramBadRequest

router = Router()

@router.callback_query(RefundCallBack.filter())
async def refund(call: types.CallbackQuery,state: FSMContext, callback_data: RefundCallBack, bot: Bot):
    await call.answer()

    _, charge_id, _, _, _, user_id, _, status = await get_purchased_info(callback_data.id)
    data = await state.get_data()

    language = data.get("lang")

    if status == 1:
        return


    try:
        await bot.refund_star_payment(user_id=user_id,telegram_payment_charge_id=charge_id)
    except TelegramBadRequest:
        await call.message.edit_text(text=translation[language]["refund_error_message"],reply_markup=call.message.reply_markup)
        return

    await set_refunded_status(callback_data.id)

    keyboard = get_sold_item_card_menu(language,True,callback_data.id,callback_data.page,1)
    await call.message.edit_text(text=translation[language]["refund_success"], reply_markup=keyboard)


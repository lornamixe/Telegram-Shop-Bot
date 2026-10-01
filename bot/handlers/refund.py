from aiogram import Router, F, types, Bot
from bot.callbacks.refundcallback import RefundCallBack
from bot.database.sale_utils import get_info_for_refund,set_refunded_status
from bot.keyboards.menu import get_sold_item_card_menu
from aiogram.fsm.context import FSMContext
from bot.locales.translations import translation

router = Router()

@router.callback_query(RefundCallBack.filter())
async def refund(call: types.CallbackQuery,state: FSMContext, callback_data: RefundCallBack, bot: Bot):

    charge_id, user_id = await get_info_for_refund(callback_data.id)
    data = await state.get_data()

    language = data.get("lang")


    ok = await bot.refund_star_payment(user_id=user_id,telegram_payment_charge_id=charge_id)

    if ok:
        
        await set_refunded_status(callback_data.id)

        keyboard = get_sold_item_card_menu(language,True,callback_data.id,callback_data.page,1)

        await call.message.edit_text(text=translation[language]["success"], reply_markup=keyboard)
    else:
        await call.message.edit_text(text=translation[language]["refund_error_message"],reply_markup=call.message.reply_markup)


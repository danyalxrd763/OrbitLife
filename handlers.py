from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import add_user,add_expense,get_expenses
router=Router()
@router.message(CommandStart())
async def start(m:Message):
 add_user(m.from_user.id,m.from_user.first_name or "User")
 await m.answer("👋 Привет! Я OrbitLife. Напиши: Потратил 500 на кофе")
@router.message(F.text.lower()=="мои расходы")
async def exp(m:Message):
 data=get_expenses(m.from_user.id)
 if not data: return await m.answer("Расходов пока нет.")
 t="💰 Твои расходы:\n"; total=0
 for a,c in data:
  t+=f"• {c}: {a:g} ₽\n"; total+=a
 await m.answer(t+f"\nИтого: {total:g} ₽")
@router.message(F.text)
async def add(m:Message):
 txt=m.text.strip()
 if not txt.lower().startswith("потратил"): return await m.answer("Например: Потратил 500 на кофе")
 p=txt.split(); amt=float(p[1].replace(",", ".")); cat=" ".join(p[3:]) or "Другое"
 add_expense(m.from_user.id,amt,cat)
 await m.answer(f"✅ Записал: {cat} — {amt:g} ₽")

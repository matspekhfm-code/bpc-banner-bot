import os
import math
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def kira_banner(width_inch, height_inch, jenis_banner, job_kerajaan=False, ada_design=True, finishing=None, paip_size=None):
    def bulat_inci_ke_kaki(inc):
        if inc % 12 != 0:
            inc = math.ceil(inc / 12) * 12
        return inc / 12

    width_ft = bulat_inci_ke_kaki(width_inch)
    height_ft = bulat_inci_ke_kaki(height_inch)

    if job_kerajaan:
        harga_kaki = 2.50
    else:
        harga_per_jenis = {
            "320g": 1.70,
            "320gUV": 4.00,
            "380g": 2.50,
            "380gUV": 4.20
        }
        harga_kaki = harga_per_jenis.get(jenis_banner, 0)

    luas = width_ft * height_ft
    harga_asas = luas * harga_kaki
    eyelet = math.ceil((width_ft + height_ft) / 2)
    kos_eyelet = eyelet * 1
    total = harga_asas + kos_eyelet

    if finishing == "lipat":
        total += (width_ft + height_ft) * 2

    if finishing == "paip" and paip_size in [2, 3, 4]:
        harga_paip = {2: 6, 3: 15, 4: 22}
        total += harga_paip[paip_size]

    if not ada_design:
        total += 20

    return math.ceil(total)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hai Bos! 😄\n"
        "Format kira:\n"
        "/kira <lebar_inci> <tinggi_inci> <jenis_banner> <kerajaan(y/n)> <ada_design(y/n)> <finishing> <paip_size>\n"
        "Contoh:\n/kira 33 25 320g n n lipat 0"
    )

async def kira(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        w = float(context.args[0])
        h = float(context.args[1])
        jenis = context.args[2]
        kerajaan = context.args[3].lower() == "y"
        design = context.args[4].lower() == "y"
        finishing = context.args[5].lower()
        paip_size = int(context.args[6]) if finishing == "paip" else None

        total = kira_banner(w, h, jenis, kerajaan, design, finishing, paip_size)
        await update.message.reply_text(f"Harga banner: RM{total}")
    except:
        await update.message.reply_text("Format salah Bos! Taip /start untuk tengok contoh.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("kira", kira))
app.run_polling()

from flask import Flask, render_template, request, jsonify
import wikipediaapi
import random
import datetime
import re
from nltk.chat.util import Chat, reflections

app = Flask(__name__)


def turkce_gun_isimlerini_cek():
    gunler = {
        "Monday": "Pazartesi",
        "Tuesday": "Salı",
        "Wednesday": "Çarşamba",
        "Thursday": "Perşembe",
        "Friday": "Cuma",
        "Saturday": "Cumartesi",
        "Sunday": "Pazar"
    }
    return gunler

pairs = [
    ["merhaba", ["Merhaba! Sana nasıl yardımcı olabilirim?"]],
    ["nasılsın", ["İyiyim, teşekkür ederim! Sen nasılsın?"]],
    ["(?i)^.*\\bnasılsın(ız)?\\b.*$", ["İyiyim, teşekkür ederim! Sen nasılsın?"]],
    ["(?i)^.*\\b(hissettiğin|hissediyorsun|hissetmek|hissediyorum)\\b.*$", ["İyiyim, teşekkür ederim! Sen nasıl hissediyorsun?"]],
    ["(?i)^.*\\bgidiyor( mu| nasıl| iyi)?\\b.*$", ["Gayet iyi gidiyor, senin nasıl gidiyor?"]],
    ["(.*) adın ne", ["Ben akıllı bir chatboot'um. Senin adın ne?"]],
    ["adın ne", ["Ben akıllı bir chatboot'um. Senin adın ne?"]],
    ["ismin ne", ["Ben akıllı bir chatboot'um. Senin adın ne?"]],
    ["(.*) ismin ne", ["Ben akıllı bir chatboot'um. Senin adın ne?"]],
    ["(?i)^.*\\biyi(yim| hissediyorum| gidiyor)?\\b.*$",
    ["İyi olduğunuza sevindim. Yardım edebileceğim bir konu var mı?"]],
    ["(?i)^.*\\bkötü(yüm| hissediyorum| gidiyor)?\\b.*$",
    ["Kendini kötü hissetmene üzüldüm. Her zaman sana destek olacağımı unutma. Yardım edebileceğim bir konu var mı?"]],
    ["teşekkürler", ["Rica ederim, Yardım edebildiğime sevindim. Başka sorunuz varmı?"]],
    ["benim adım (.*)", ["Merhaba, %1! Tanıştığımıza memnun oldum."]],
    ["(.*) hava (.*)", ["Hava durumu bilgisi için şehir adı söylemelisin."]],
    ["(.*) saat kaç", ["Şu an saat " + datetime.datetime.now().strftime("%H:%M")]],
    ["(.*) günlerden ne", ["Bugün " + turkce_gun_isimlerini_cek().get(datetime.datetime.now().strftime("%A"), "Bilinmeyen gün")]],
    ["bana bir şaka yap", [
        "Neden matematik kitabı üzgündü? Çünkü çok fazla problemi vardı! 😂",
        "İki balık karşılaşmış, biri diğerine ‘Nasılsın?’ demiş, diğeri ‘Su gibiyim!’ 😆",
        "Telefonun şarjı neden bitti? Çünkü ‘konuşarak’ anlaşmaya çalışıyordu! 😄"
    ]],
    ["(.*) hakkında bilgi ver", ["Wikipedia'dan bilgi arıyorum..."]],
    ["(.*) hesapla (.*)", ["Matematik işlemi yapıyorum..."]],
    ["(.*)", ["Üzgünüm, bunu anlayamadım. Daha farklı bir şekilde sorabilir misin?"]]
]

chatbot = Chat(pairs, reflections)


def get_wikipedia_summary(topic):
    try:
        wiki_wiki = wikipediaapi.Wikipedia(language='tr', user_agent='MyChatbot/1.0 (http://mychatbot.com; myemail@example.com)')
        page = wiki_wiki.page(topic)
        if page.exists():
            return page.summary[:300] + "..."
        else:
            return "Üzgünüm, bu konuda bilgi bulamadım."
    except Exception as e:
        return "Bir hata oluştu: " + str(e)

def get_random_weather():

    weathers = ["Güneşli", "Yağmurlu", "Bulutlu", "Rüzgarlı", "Karla karışık yağmur"]
    temp = random.randint(-5, 35)
    condition = random.choice(weathers)  
    return f"Sıcaklık: {temp}°C, Hava Durumu: {condition}"

def process_user_input(user_input):
    user_input = user_input.lower()

    if "hakkında bilgi ver" in user_input:
        topic = user_input.replace("hakkında bilgi ver", "").strip()
        return get_wikipedia_summary(topic)

    elif "hava nasıl" in user_input:
        return get_random_weather()

    elif "hesapla" in user_input:
        try:
            expression = re.search(r"hesapla (.*)", user_input).group(1)
            result = eval(expression)
            return f"Sonuç: {result}"
        except:
            return "Geçerli bir işlem gir."

    else:
        return chatbot.respond(user_input)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')
    response = process_user_input(user_input)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
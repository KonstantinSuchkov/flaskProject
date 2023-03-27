from flask import Blueprint, render_template
from datetime import datetime
import pytz


trymore_app = Blueprint('trymore_app', __name__, url_prefix='/', static_folder='../static')


def text_to_mp3(text='', language='ru'):
    from gtts import gTTS
    text = text.replace('\n', '')
    my_audio = gTTS(text=text, lang=language, slow=False)
    file_name = 'text1'
    my_audio.save(f'{file_name}.mp3')
    return render_template('trymore/list.html')


@trymore_app.route("/audio", endpoint="audio")
def audio():
    import vlc
    import time
    p = vlc.MediaPlayer("file:///text1.mp3")
    p.play()
    time.sleep(10)
    result = 'done'
    return render_template('trymore/list.html', result=result)


@trymore_app.route("/", endpoint="list")
def trymore_list():
    print("list")
    return render_template('trymore/list.html')


@trymore_app.route('/test')
def test_time():
    moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
    print("Hello")
    print(moscow_time)
    return render_template('trymore/list.html', moscow_time=moscow_time)


@trymore_app.route('/weather')
def weather():
    import requests
    url = 'https://api.open-meteo.com/v1/forecast?latitude=55.63&longitude=37.32&current_weather=True'
    r = requests.get(url)
    result = r.json()
    current_weather = f'На данный момент в Москве {result["current_weather"]["temperature"]} C.'

    return render_template('trymore/list.html', current_weather=current_weather)

from django.shortcuts import render
from datetime import datetime, timedelta
import requests
from decouple import config


def get_description(description):
    # Usando o match do python(switch case) para traduzir a descrição

    match description['main'].lower():
        case "clear":
            return "Céu limpo";
        
        case "clouds":
            match description['description'].lower():
                case "few clouds":
                    return "Poucas nuvens"
                case "scattered clouds":
                    return "Nublado"
                case "broken clouds":
                    return "Nuvens cirrus"
                case _:
                    return "Céu encoberto"
            
        case "drizzle":
            return "Chuva rápida"
        case "rain":
            return "Chuva"
        case "thunderstorm":
            return "Tempestade"
        
        case "snow":
            return "Neve"
        case "mist" | "fog" | "haze":
            return "Névoa"
        case "tornado":
            return "tornado"
        case _:
            return "Não identificado"

def get_time(timezone):
    # Pegando a data e hora atual
    current_time = timedelta(seconds=timezone)
    date = datetime.utcnow() + current_time
    
    # Formatando para, Hora:Minutos
    return date.strftime("%H:%M")

def get_hr(atual, update):
    # Atualiza os próximos horarios, para as próximas previsões que são 3 em 3 hrs
    horario = datetime.strptime(atual, '%H:%M')
    intervalo = timedelta(hours=(3*update))
    novo_horario = horario + intervalo

    return novo_horario.strftime("%H:00")

def get_style(hora):
    # Style do css da página para quando for dia e quando for noite
    if int(hora[:2]) > 5 and int(hora[:2]) < 18:
        return {"bg": "#e5ecf4", "cor": "#0c1019"}
    else:
        return {"bg": "#313745", "cor": "#fff"}


def get_icon(icon, horario):
    # Retorna o tipo do icone e o wallpaper com base no horario e clima
    wallpaper = ''
    if int(horario[:2]) > 5 and int(horario[:2]) < 18:
        periodo = 'd'
    else:
        periodo = 'n'

    if icon[:2] in ['01', '02', '04']:
        wallpaper = 'claro'
    else:
        wallpaper = 'chuva'

    #return [str(icon[:2] + periodo), str(wallpaper) + periodo]
    return [str(icon[:2] + periodo), 'chuvan']


# Função da página inicial
def index(request):
    try:
        # Se o método for post
        if request.method == 'POST':
            API_KEY = config("API_KEY")

            # pega a cidade vindo do html  
            city = request.POST.get('city')

            # criando a rota da url da api   
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'

            # convertendo a resposta da api para um json   
            response = requests.get(url).json()
            

            # Formatando alguns dados usando as funções
            formatted_time = get_time(response['city']['timezone'])
            description = get_description(response['list'][0]['weather'][0])
            data_style = get_style(formatted_time)

            # Pegando as infos do icone e do wallpaper com base no tempo
            icon, wallpaper = get_icon(response['list'][0]['weather'][0]['icon'], formatted_time)
            

            # Dicionário com os dados
            data_weather = {
                'city': response['city']['name'],
                'country_code': response['city']['country'],
                'time': formatted_time,

                'icon': icon,
                
                'description': description,
                
                'temperature': str(round(response['list'][0]['main']['temp'])) + ' °C',
                'sensation': 'Sensação: ' + str(round(response['list'][0]['main']['feels_like'])) + ' °C',

                'wind': 'Vento: ' + str(response['list'][0]['wind']['speed']) + 'km/h',
                'humidity': 'Humidade: ' + str(response['list'][0]['main']['humidity']) + '%',
                
                }
            
            # Lista das próximas 4 previsões
            more_data = []
            for i in range(1, 5):
                horario = get_hr(formatted_time, i)
                more_data.append({
                    "horario": horario,
                    "icon": get_icon(response['list'][i]['weather'][0]['icon'], horario)[0],
                    "temp": str(round(response['list'][i]['main']['temp'])) + ' °C'
                    })
        

        # Se o método for GET cria o dicionário vazio
        else:
            data_weather = {}
            more_data = {}
            data_style = {}
            wallpaper = ''
        context = {'data_weather': data_weather, "more_data": more_data, "data_style": data_style, "wallpaper": wallpaper}
        return render(request, 'index.html', context)
    except:
            return render(request, '404.html')
        
    

import main
import requests
import json
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_modal import Modal 
import streamlit.components.v1 as components
from streamlit_extras.row import row



API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OTk2YWYzOWJjMTkzYmYzY2ExMjFhMTkzNmYzNWQxNCIsInN1YiI6IjY1MDMyZTk3NmEyMjI3MDExYTdjMTIyZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.QrfVjDnfS4l6r2ROfDccGykw48Ll-0VelUOHgYZcPh0'
url = "https://api.themoviedb.org/3/movie/popular"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

todos = json.loads(response.content)

f = todos['results']


with st.sidebar:
    ind = st.text_input(
            label="Indicação do chat GPT",
            placeholder="Informe um tema ou assunto"
    )


    API_KEY = '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'
    id_modelo = "gpt-3.5-turbo"
    link = "https://api.openai.com/v1/chat/completions"
    headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

    body_mensagem = {
            "model": id_modelo,
            "messages": [{"role": "user",
                    "content": f"Me indique um filme a partir da seguinte palavra-chave: {ind}"}]

}

    body_mensagem = json.dumps(body_mensagem)
    requisicao = requests.post(link, headers=headers,data=body_mensagem)

    resposta = requisicao.json()
    mensagem = resposta["choices"][0]['message']['content']



    st.markdown(mensagem)



row1 = row(5,vertical_align="top",gap="large")
row2 = row(5,vertical_align="top",gap="large")
for item in f [0:5]:
        z = (item['poster_path'])
        t = (item['title'])
        o = (item['overview'])
        url_image = (f"https://image.tmdb.org/t/p/w500{z}")
        row1.image(url_image,width=220)
        
        open_modal = row2.button(f"{t}")
        modal = Modal(f'  {t}',f'{o}',max_width=400)
        if open_modal:
            modal.open()

        if  modal.is_open():
             with modal.container():
                st.write(f"{o}")

            
row3 = row(5,vertical_align="top",gap="large")
row4 = row(5,vertical_align="top",gap="large")
for item in f [5:10]:
        z = (item['poster_path'])
        t = (item['title'])
        o = (item['overview'])
        url_image = (f"https://image.tmdb.org/t/p/w500{z}")
        row3.image(url_image,width=220)
        
        open_modal = row4.button(f"{t}")
        modal = Modal(f'{t}',f'{o}',max_width=600)
        if open_modal:
            modal.open()

        if  modal.is_open():
             with modal.container():
                st.write(f"{o}")   
            

row5 = row(5,vertical_align="top",gap="large")
row6 = row(5,vertical_align="top",gap="large")
for item in f [10:15]:
        z = (item['poster_path'])
        t = (item['title'])
        o = (item['overview'])
        url_image = (f"https://image.tmdb.org/t/p/w500{z}")
        row5.image(url_image,width=220)
        
        open_modal = row6.button(f"{t}")
        modal = Modal(f'{t}',f'{o}',max_width=600)
        if open_modal:
            modal.open()

        if  modal.is_open():
             with modal.container():
                st.write(f"{o}")
           

row7 = row(5,vertical_align="top",gap="large")
row8 = row(5,vertical_align="top",gap="large")
for item in f [15:20]:
        z = (item['poster_path'])
        t = (item['title'])
        o = (item['overview'])
        url_image = (f"https://image.tmdb.org/t/p/w500{z}")
        row7.image(url_image,width=220)
        
        open_modal = row8.button(f"{t}")
        modal = Modal(f'{t}',f'{o}',max_width=600)
        if open_modal:
            modal.open()

        if  modal.is_open():
             with modal.container():
                st.write(f"{o}")

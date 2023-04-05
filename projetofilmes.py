import requests
import json
import tkinter as tk
from datetime import datetime

API_KEY = 'dc2b8b90301cacba34fc154f972b3963'
BASE_URL = f'https://api.themoviedb.org/3/'


class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry('1080x720')
        self.master.title('Lista de Filmes')
        self.filmes_lista = tk.Listbox(self.master, width=80)
        self.filmes_lista.pack(fill=tk.BOTH, expand=True)

        # Adiciona um campo de pesquisa
        self.pesquisa_entrada = tk.Entry(self.master)
        self.pesquisa_entrada.pack(side=tk.LEFT, padx=10, pady=10)

        # Adiciona um botão para pesquisar filmes
        self.pesquisar_botao = tk.Button(
            self.master, text='Pesquisar', command=self.pesquisar_filmes)
        self.pesquisar_botao.pack(side=tk.LEFT, padx=10, pady=10)

        self.obter_filmes_botao = tk.Button(
            self.master, text='Obter Filmes', command=self.obter_filmes)
        self.obter_filmes_botao.pack(side=tk.LEFT, padx=10, pady=10)

    def obter_filmes(self):
        ENDPOINT = 'movie/popular'

        params = {
            'api_key': API_KEY,
            'language': 'pt-BR',
            'page': 1
        }

        response = requests.get(BASE_URL + ENDPOINT, params=params)

        if response.status_code == 200:
            data = json.loads(response.text)
            filmes = data['results']
            self.filmes_lista.delete(0, tk.END)
            for filme in filmes:
                titulo = filme['title']
                nota = filme['vote_average']
                data_lancamento = datetime.strptime(
                    filme['release_date'], '%Y-%m-%d').strftime('%Y')
                id_filme = filme['id']

                # Obter informações de streaming
                endpoint_streaming = f'movie/{id_filme}/watch/providers'
                params_streaming = {
                    'api_key': API_KEY,
                }
                response_streaming = requests.get(
                    BASE_URL + endpoint_streaming, params=params_streaming)
                streaming_data = json.loads(response_streaming.text)
                if response_streaming.status_code == 200:
                    providers = streaming_data.get('results', {}).get('BR', {})
                    streaming_platforms = [
                        provider.get('provider_name') for provider in providers.get('flatrate', [])]
                    if streaming_platforms:
                        plataformas = ', '.join(streaming_platforms)
                    else:
                        plataformas = 'Não disponível'

                    item = f'Filme: {titulo} {data_lancamento} - Nota ({nota:.1f}) - Plataforma(s): {plataformas}'
                else:
                    item = f'Filme: {titulo} {data_lancamento} - Nota ({nota:.1f}) - Plataforma(s): Não disponível'

                self.filmes_lista.insert(tk.END, item)
        else:
            tk.messagebox.showerror('Erro', 'Erro ao obter a lista de filmes.')

    def pesquisar_filmes(self):
        pesquisa = self.pesquisa_entrada.get()
        ENDPOINT = 'search/movie'

        params = {
            'api_key': API_KEY,
            'language': 'pt-BR',
            'query': pesquisa,
            'page': 1
        }

        response = requests.get(BASE_URL + ENDPOINT, params=params)

        if response.status_code == 200:
            data = json.loads(response.text)
            filmes = data['results']
            self.filmes_lista.delete(0, tk.END)
            for filme in filmes:
                titulo = filme['title']
                nota = filme['vote_average']
                data_lancamento = datetime.strptime(
                    filme['release_date'], '%Y-%m-%d').strftime('%Y')
                id_filme = filme['id']

                # Obter informações de streaming
                endpoint_streaming = f'movie/{id_filme}/watch/providers'
                params_streaming = {
                    'api_key': API_KEY,
                }
                response_streaming = requests.get(
                    BASE_URL + endpoint_streaming, params=params_streaming)
                streaming_data = json.loads(response_streaming.text)
                if response_streaming.status_code == 200:
                    providers = streaming_data.get('results', {}).get('BR', {})
                    streaming_platforms = [
                        provider.get('provider_name') for provider in providers.get('flatrate', [])]
                    if streaming_platforms:
                        plataformas = ', '.join(streaming_platforms)
                    else:
                        plataformas = 'Não disponível'

                    item = f'Filme: {titulo} {data_lancamento} - Nota ({nota:.1f}) - Plataforma(s): {plataformas}'
                else:
                    item = f'Filme: {titulo} {data_lancamento} - Nota ({nota:.1f}) - Plataforma(s): Não disponível'

                self.filmes_lista.insert(tk.END, item)
        else:
            tk.messagebox.showerror('Erro', 'Erro ao obter a lista de filmes.')

    def obter_plataforma(self, filme_id):
        ENDPOINT = f"https://apis.justwatch.com/content/titles/movie/{filme_id}/locale/pt_BR"

        response = requests.get(ENDPOINT)

        if response.status_code == 200:
            data = json.loads(response.text)
            if data.get('offers'):
                return data['offers'][0]['provider_name']
            else:
                return 'Plataforma não encontrada'
        else:
            return 'Erro ao obter a plataforma'


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

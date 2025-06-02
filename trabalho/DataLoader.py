import pandas as pd

class DataLoader:
    def __init__(self, caminho_csv):
        self.caminho_csv = caminho_csv
        self.data = None

    def carregar_dados(self):

        self.data = pd.read_csv(self.caminho_csv)

        #Tratamento de dados
        # Remover espaços em branco nos nomes das colunas
        self.data["monsterkills"] = self.data["monsterkills"].fillna(0)
        self.data["minionkills"] = self.data["minionkills"].fillna(0)
        self.data["total cs"] = self.data["total cs"].fillna(self.data["minionkills"] + self.data["monsterkills"])
        self.data.columns = self.data.columns.str.strip()

        # Alguns dados estão faltando, então vamos preencher com valores padrão
        self.data["teamname"] = self.data["teamname"].fillna("time desconhecido")
        
        # Colunas que serão mantidas do dataset
        cols = [
        'gameid', 'league', 'split', 'participantid', 'side', 'position', 'playername',
        'teamname', 'champion', 'ban1', 'ban2', 'ban3', 'ban4', 'ban5',
        'gamelength', 'result', 'kills', 'deaths', 'assists',
        'teamkills', 'teamdeaths','firstblood', 'firsttower',
        'towers', 'wardsplaced', 'totalgold', 'total cs'
        ]

        self.data = self.data[cols]
         
        self.data["split"] = self.data["split"].fillna("Season 2022")
        
        self.data["split"] = self.data["split"].replace("", "Season 2022")
        
        self.data["split"] = self.data["split"].astype(str)
        # Renomear colunas para português
        self.data.rename(columns={
        'league': 'liga',
        'split': 'temporada',
        'participantid': 'id_participante',
        'playername': 'jogador',
        'champion': 'campeao',
        'gameid': 'id_partida',
        'side': 'lado',
        'position': 'posicao',
        'teamname': 'time',
        'gamelength': 'tempo_partida',
        'result': 'resultado',
        'kills': 'abates',
        'deaths': 'mortes',
        'assists': 'assistencias',
        'teamkills': 'abates_time',
        'teamdeaths': 'mortes_time',
        'firstblood': 'primeiro_abate',
        'firsttower': 'primeira_torre',
        'towers': 'torres',
        'wardsplaced': 'sentinelas_colocadas',
        'totalgold': 'ouro_total',
        'total cs': 'total_creeps',
        'ban1': 'banimento_1',
        'ban2': 'banimento_2',
        'ban3': 'banimento_3',
        'ban4': 'banimento_4',
        'ban5': 'banimento_5'
         }, inplace=True)
        return self.data    
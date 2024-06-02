import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import consts

# Função para ler JSON e extrair tempos de consulta
def read_json_to_df(filepath, tempo_col_name, time_key):
    with open(filepath, 'r') as file:
        data = json.load(file)
    actions = data['actions']
    df = pd.DataFrame(actions)
    df = df[['id', time_key]]
    df.columns = ['id', tempo_col_name]
    
    # Extrair informações adicionais
    nodes = data['nodes']
    shards = data['shards']
    time_python_function = data['time_python_function']
    
    return df, nodes, shards, time_python_function

# Ler os arquivos JSON
linear_search, nodes, shards, time_linear = read_json_to_df(f"./logs/{consts.LINEAR_SEARCH_PATH}.json", 'tempo_linear_search', 'time_python')
linear_msearch, _, _, time_msearch = read_json_to_df(f"./logs/{consts.LINEAR_MSEARCH_PATH}.json", 'tempo_linear_msearch', 'time')
parallel_search, _, _, time_parallel = read_json_to_df(f"./logs/{consts.PARALLEL_SEARCH}.json", 'tempo_parallel_search', 'time')

# Mesclar os DataFrames com base na coluna 'id'
df = linear_search.merge(linear_msearch, on='id').merge(parallel_search, on='id')

# Criar a figura e os subplots
fig, axs = plt.subplots(4, 1, figsize=(10, 20), gridspec_kw={'hspace': 0.7})
plt.subplots_adjust(left=0.048, bottom=0.067, right= 0.985, top=0.96)
fig.text(0.05, 0.95, f'Nodes: {nodes}, Shards: {shards}\n')

# Definir os limites dos eixos x e y
x_limits = (df['id'].min(), df['id'].max())
y_limits = (0,.11) # (min(df['tempo_linear_search'].min(), df['tempo_linear_msearch'].min()), max(df['tempo_linear_search'].max(), df['tempo_linear_msearch'].max()))

# Subplot 1: Linear Search
axs[0].plot(df['id'], df['tempo_linear_search'], label='Linear Search', color='blue')
axs[0].set_xlabel('ID', labelpad=-9)
axs[0].set_ylabel('Tempo (s)')
axs[0].set_title('Linear Search')
axs[0].grid(True)
axs[0].text(0.88, 0.95, f'Tempo: {time_linear:.2f} s', transform=axs[0].transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
axs[0].set_xlim(x_limits)
axs[0].set_ylim(y_limits)

# Subplot 2: Linear MSearch
axs[1].plot(df['id'], df['tempo_linear_msearch'], label='Linear MSearch', color='red')
axs[1].set_xlabel('ID', labelpad=-9)
axs[1].set_ylabel('Tempo (s)')
axs[1].set_title('Linear MSearch')
axs[1].grid(True)
axs[1].text(0.88, 0.95, f'Tempo: {time_msearch:.2f} s', transform=axs[1].transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
axs[1].set_xlim(x_limits)
axs[1].set_ylim(y_limits)

# Subplot 3: Parallel Search
axs[2].plot(df['id'], df['tempo_parallel_search'], label='Parallel Search', color='green')
axs[2].set_xlabel('ID', labelpad=-9)
axs[2].set_ylabel('Tempo (s)')
axs[2].set_title('Parallel Search')
axs[2].grid(True)
axs[2].text(0.88, 0.95, f'Tempo: {time_parallel:.2f} s', transform=axs[2].transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
axs[2].set_xlim(x_limits)
axs[2].set_ylim(y_limits)

# Subplot 4: Combined
axs[3].plot(df['id'], df['tempo_linear_search'], label='Linear Search', color='blue')
axs[3].plot(df['id'], df['tempo_linear_msearch'], label='Linear MSearch', color='red')
axs[3].plot(df['id'], df['tempo_parallel_search'], label='Parallel Search', color='green')
axs[3].set_xlabel('ID', labelpad=-9)
axs[3].set_ylabel('Tempo (s)')
axs[3].set_title('Comparação dos Tempos de Resposta das Consultas')
axs[3].grid(True)
axs[3].set_xlim(x_limits)
axs[3].set_ylim(y_limits)

# Ajustar a legenda para fora do gráfico
axs[3].legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Ajustar layout
#plt.tight_layout()

nome_arquivo = f'grafico_shards_{shards}_nodes_{nodes}.png'
# Caminho completo do arquivo
caminho_arquivo = os.path.join('./graficos', nome_arquivo)

# Salvar o gráfico em um arquivo com o caminho especificado
plt.savefig(caminho_arquivo)
plt.show()

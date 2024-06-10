import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import argparse
import consts
from datetime import datetime
import metrics

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

def main():
    parser = argparse.ArgumentParser(description='Executa uma função específica com base no parâmetro passado.')
    parser.add_argument('nodes', help='Quantidade de nodes')
    parser.add_argument('shards', help='Quantidade de shards')
    parser.add_argument('folder_name', nargs="?", default="", help='Nome da pasta')
    args = parser.parse_args()
    
    print("Gerando gráficos de comparação...")

    folder_name = args.folder_name
    if(folder_name == "") or (folder_name is None): 
        folder_name = f".{consts.SEPARATOR_PATH}{consts.LOGS_PATH}"

    # Ler os arquivos JSON
    linear_search, nodes, shards, time_linear = read_json_to_df(f"{folder_name}linear_search_nodes_{args.nodes}_shards_{args.shards}.json", 'tempo_linear_search', 'time_es')
    linear_msearch, _, _, time_msearch = read_json_to_df(f"{folder_name}linear_msearch_nodes_{args.nodes}_shards_{args.shards}.json", 'tempo_linear_msearch', 'time')
    parallel_search, _, _, time_parallel = read_json_to_df(f"{folder_name}parallel_search_nodes_{args.nodes}_shards_{args.shards}.json", 'tempo_parallel_search', 'time')

    # Mesclar os DataFrames com base na coluna 'id'
    df = linear_search.merge(linear_msearch, on='id').merge(parallel_search, on='id')
    df['linear_minus_msearch'] = df['tempo_linear_search'] - df['tempo_linear_msearch']
    df['linear_minus_parallel'] = df['tempo_linear_search'] - df['tempo_parallel_search']

    # Criar a figura e os subplots
    fig, axs = plt.subplots(6, 1, figsize=(10, 20), gridspec_kw={'hspace': 0.7})
    plt.subplots_adjust(left=0.048, bottom=0.067, right= 0.985, top=0.96)
    fig.text(0.05, 0.95, f'Nodes: {nodes}, Shards: {shards}\n')

    # Definir os limites dos eixos x e y
    x_limits = (df['id'].min(), df['id'].max())
    y_limits = (0,.05) #(min(df['tempo_linear_search'].min(), df['tempo_linear_msearch'].min()), max(df['tempo_linear_search'].max(), df['tempo_linear_msearch'].max()))

    # Função para criar e salvar cada subplot
    def create_subplot(ax, data, label, color, title, time):
        ax.plot(df['id'], data, label=label, color=color)
        ax.set_xlabel('ID', labelpad=-9)
        ax.set_ylabel('Tempo (s)')
        ax.set_title(title)
        ax.grid(True)
        if time is not None:
            ax.text(0.88, 0.95, f'Tempo: {time:.2f} s', transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)

    # Subplot 1: Linear Search
    create_subplot(axs[0], df['tempo_linear_search'], 'Linear Search', 'blue', 'Linear Search', time_linear)

    # Subplot 2: Linear MSearch
    create_subplot(axs[1], df['tempo_linear_msearch'], 'Linear MSearch', 'red', 'Linear MSearch', time_msearch)

    # Subplot 3: Parallel Search
    create_subplot(axs[2], df['tempo_parallel_search'], 'Parallel Search', 'green', 'Parallel Search', time_parallel)

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
    axs[3].legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

    # Subplot 5: Combinação linear_search x linear_msearch
    create_subplot(axs[4], df['linear_minus_msearch'], 'Linear Search - Linear Msearch', 'purple', 'Linear Search - Linear Msearch', None)

    # Subplot 6: Combinação linear_search x parallel_search
    create_subplot(axs[5], df['linear_minus_parallel'], 'Linear Search - Parallel Search', 'teal', 'Linear Search - Parallel Search', None)

    # Salvar a figura com todos os subplots
    fig_all_path = f'{folder_name}/grafico_nodes_{nodes}_shards_{shards}.png'
    plt.savefig(fig_all_path)
    # plt.show()

    # Salvar cada subplot individualmente
    subplot_titles = [
        ('Linear Search', 'tempo_linear_search', 'blue', time_linear),
        ('Linear MSearch', 'tempo_linear_msearch', 'red', time_msearch),
        ('Parallel Search', 'tempo_parallel_search', 'green', time_parallel),
        ('Comparação dos Tempos de Resposta das Consultas', None, None, None),
        ('Linear Search - Linear Msearch', 'linear_minus_msearch', 'purple', None),
        ('Linear Search - Parallel Search', 'linear_minus_parallel', 'teal', None)
    ]

    for i, (title, column, color, time) in enumerate(subplot_titles):
        fig, ax = plt.subplots(figsize=(10, 4))
        if column:
            create_subplot(ax, df[column], title, color, title, time)
        else:
            ax.plot(df['id'], df['tempo_linear_search'], label='Linear Search', color='blue')
            ax.plot(df['id'], df['tempo_linear_msearch'], label='Linear MSearch', color='red')
            ax.plot(df['id'], df['tempo_parallel_search'], label='Parallel Search', color='green')
            ax.set_xlabel('ID', labelpad=-9)
            ax.set_ylabel('Tempo (s)')
            ax.set_title(title)
            ax.grid(True)
            ax.set_xlim(x_limits)
            ax.set_ylim(y_limits)
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
        
        # Caminho completo do arquivo
        fig_path = f'{folder_name}/grafico_{title.replace(" ", "_").lower()}_nodes_{nodes}_shards_{shards}.png'
        plt.savefig(fig_path)
        plt.close(fig)


    # Precision e recall
    print("Gerando gráficos de precision e recall...")
    
    with open(consts.RESULT_ANSWERS_PATH, 'r') as answers_file:
        answers = json.load(answers_file)

    with open(f"{folder_name}linear_search_nodes_{nodes}_shards_{shards}.json", 'r') as found_file:
        log = json.load(found_file)
    metrics.precision_at_k(log, answers, 10, folder_name, f"linear_search_nodes_{nodes}_shards_{shards}")
    metrics.recall_at_k(log, answers, 10, folder_name, f"linear_search_nodes_{nodes}_shards_{shards}")

if __name__ == '__main__':
    main()
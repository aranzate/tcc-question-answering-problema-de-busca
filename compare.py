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
    mean = data['mean']
    variance = data['variance']
    standard_deviation = data['standard_deviation']
    
    return df, nodes, shards, time_python_function, mean, variance, standard_deviation

def main():
    parser = argparse.ArgumentParser(description='Executa uma função específica com base no parâmetro passado.')
    parser.add_argument('nodes', help='Quantidade de nodes')
    parser.add_argument('shards', help='Quantidade de shards')
    parser.add_argument('folder_name', nargs="?", default="", help='Nome da pasta')
    args = parser.parse_args()
    
    print("GRAFICOS: Gera gráficos de comparação com " + str(args.nodes) + " node(s) e " + str(args.shards) + " shard(s).")

    folder_name = args.folder_name
    if(folder_name == "") or (folder_name is None): 
        folder_name = f".{consts.SEPARATOR_PATH}{consts.LOGS_PATH}"

    # Ler os arquivos JSON
    linear_search, nodes, shards, time_linear, mean_linear, variance_linear, standard_deviation_linear = read_json_to_df(f"{folder_name}n{args.nodes}_s{args.shards}_log_linear_search.json", 'tempo_linear_search', 'time')
    linear_msearch, _, _, time_msearch, mean_msearch, variance_msearch, standard_deviation_msearch = read_json_to_df(f"{folder_name}n{args.nodes}_s{args.shards}_log_linear_msearch.json", 'tempo_linear_msearch', 'time')
    parallel_search, _, _, time_parallel, mean_parallel, variance_parallel, standard_deviation_parallel = read_json_to_df(f"{folder_name}n{args.nodes}_s{args.shards}_log_parallel_search.json", 'tempo_parallel_search', 'time')

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
    y_limits = (0,.15) #(min(df['tempo_linear_search'].min(), df['tempo_linear_msearch'].min()), max(df['tempo_linear_search'].max(), df['tempo_linear_msearch'].max()))

    # Função para criar e salvar cada subplot
    def create_subplot(ax, data, label, color, title, time=None, mean=None, variance=None, standard_deviation=None):
        ax.plot(df['id'], data, label=label, color=color)
        ax.set_xlabel('ID', labelpad=-9)
        ax.set_ylabel('Tempo (s)')
        ax.set_title(title)
        ax.grid(True)

        text=""
        if time is not None:
            text += f'Tempo total: {time:.2f}s'
        if(mean is not None):
             text += f'\nMédia: {mean}s\n'
        if(variance is not None):
             text += f'Variância: {variance}s\n'
        if(standard_deviation is not None):
             text += f'Desvio Padrão: {standard_deviation}s'
        if(text != ""):
            #ax.text(0.70, 1.143,  text, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
            ax.text(0.69, 1.13, text, transform=ax.transAxes, fontsize=10, verticalalignment='top',bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
        
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)

    # Subplot 1: Linear Search
    create_subplot(axs[0], df['tempo_linear_search'], 'Linear Search', 'blue', 'Linear Search', time_linear, mean_linear, variance_linear, standard_deviation_linear )

    # Subplot 2: Linear MSearch
    create_subplot(axs[1], df['tempo_linear_msearch'], 'Linear MSearch', 'red', 'Linear MSearch', time_msearch, mean_msearch, variance_msearch, standard_deviation_msearch)

    # Subplot 3: Parallel Search
    create_subplot(axs[2], df['tempo_parallel_search'], 'Parallel Search', 'green', 'Parallel Search', time_parallel, mean_parallel, variance_parallel, standard_deviation_parallel)

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
    create_subplot(axs[4], df['linear_minus_msearch'], 'Linear Search minus Linear Msearch', 'purple', 'Linear Search minus Linear Msearch')

    # Subplot 6: Combinação linear_search x parallel_search
    create_subplot(axs[5], df['linear_minus_parallel'], 'Linear Search minus Parallel Search', 'teal', 'Linear Search minus Parallel Search')

    # Salvar a figura com todos os subplots
    fig_all_path = f'{folder_name}/n{nodes}_s{shards}_-_graficos.png'
    plt.savefig(fig_all_path)
    # plt.show()

    # Salvar cada subplot individualmente
    subplot_titles = [
        (f"n{nodes} s{shards} - Linear Search", 'tempo_linear_search', 'blue', time_linear, mean_linear, variance_linear, standard_deviation_linear),
        (f"n{nodes} s{shards} - Linear MSearch", 'tempo_linear_msearch', 'red', time_msearch, mean_msearch, variance_msearch, standard_deviation_msearch),
        (f"n{nodes} s{shards} - Parallel Search", 'tempo_parallel_search', 'green', time_parallel, mean_parallel, variance_parallel, standard_deviation_parallel),
        (f"n{nodes} s{shards} - Comparação dos Tempos de Resposta das Consultas", None, None, None, None, None, None),
        (f"n{nodes} s{shards} - Linear Search minus Linear Msearch", 'linear_minus_msearch', 'purple', None, None, None, None),
        (f"n{nodes} s{shards} - Linear Search minus Parallel Search", 'linear_minus_parallel', 'teal', None, None, None, None)
    ]

    for i, (title, column, color, time, mean, variance, standard_deviation) in enumerate(subplot_titles):
        fig, ax = plt.subplots(figsize=(10, 4))
        if column:
            create_subplot(ax, df[column], title, color, title, time, mean, variance, standard_deviation)
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
        fig_path = f'{folder_name}/{title.replace(" ", "_").lower()}.png'
        plt.savefig(fig_path)
        plt.close(fig)


    # Precision e recall
    print("GRAFICOS: Gera gráficos de precision e recall com " + str(nodes) + " node(s) e " + str(shards) + " shard(s).")
    
    with open(consts.RESULT_ANSWERS_PATH, 'r') as answers_file:
        answers = json.load(answers_file)

    with open(f"{folder_name}n{nodes}_s{shards}_log_linear_search.json", 'r') as found_file:
        log = json.load(found_file)
    metrics.precision_at_k(log, answers, 10, folder_name, f"n{nodes} s{shards} - Linear Search")
    metrics.recall_at_k(log, answers, 10, folder_name, f"n{nodes} s{shards} - Linear Search")

if __name__ == '__main__':
    main()
import pandas as pd
import json
import argparse
import consts
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

def read_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)

    time_python_function=data['time_python_function']
    mean=data['mean']
    variance=data['variance']
    standard_deviation=data['standard_deviation']
    
    return time_python_function, mean, variance, standard_deviation


def main():
    parser = argparse.ArgumentParser(description='Executa uma função específica com base no parâmetro passado.')
    parser.add_argument('folder_name', nargs="?", default="", help='Nome da pasta')
    args = parser.parse_args()
    
    print("GRAFICOS: Gera gráficos de comparação com todos os logs")

    folder_name = args.folder_name
    if(folder_name == "") or (folder_name is None): 
        folder_name = f".{consts.SEPARATOR_PATH}{consts.LOGS_PATH}"

    nodes_list = [1,2,3,4]
    shards_list = [1,2,4,8,12,16,32]

    time_python_function_total = []

    for nodes in nodes_list:
        time_python_function_ls = []
        time_python_function_lm = []
        time_python_function_ps = []

        for shards in shards_list:

            time_python_function, _, _, _ = read_json(f"{folder_name}n{nodes}_s{shards}_log_linear_search.json")
            time_python_function_ls.append(time_python_function)

            time_python_function, _, _, _ = read_json(f"{folder_name}n{nodes}_s{shards}_log_linear_msearch.json") 
            time_python_function_lm.append(time_python_function)

            time_python_function, _, _, _ = read_json(f"{folder_name}n{nodes}_s{shards}_log_parallel_search.json")
            time_python_function_ps.append(time_python_function)

        time_python_function_total.append(time_python_function_ls)
        time_python_function_total.append(time_python_function_lm)
        time_python_function_total.append(time_python_function_ps)

    pprint(time_python_function_total)

        
            
        

    # Dados
    x = shards_list
    y = time_python_function_total # np.random.rand(12, 7) * 10  # Exemplos de valores de tempo em segundos para cada gráfico
    title = 'Tempo Python(s) X Quantidade de Shards'

    # Configurações da grade de gráficos
    fig, axes = plt.subplots(4, 3, figsize=(15, 20))
    fig.suptitle(title, fontsize=16)

    # Títulos das linhas e colunas
    linhas_titulo = ['n1', 'n2', 'n3', 'n4']
    colunas_titulo = ['L. Search', 'L. Msearch', 'Parallel Search']

    # Gerar gráficos
    for i in range(4):
        for j in range(3):
            ax = axes[i, j]
            y_values = y[i*3 + j]
            ax.plot(x, y_values, marker='o', linestyle='-', color='b')
            ax.set_xlabel('Shards')
            ax.set_ylabel('Tempo (s)')
            ax.set_ylim(0, 210)
            #ax.set_title(f'Gráfico {i*4 + j + 1}')
            ax.set_title(f'')
            ax.set_xticks(x)
            ax.grid(True)

    # Adicionar títulos às linhas e colunas
    for ax, col in zip(axes[0], colunas_titulo):
        ax.set_title(col, fontsize=14, pad=20)

    for ax, row in zip(axes[:,0], linhas_titulo):
        ax.set_ylabel(row, rotation=0, fontsize=14, labelpad=40)

    # plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    # plt.show()

    # Caminho completo do arquivo
    fig_path = f'{folder_name}/results_{title.replace(" ", "_").lower()}.png'
    plt.savefig(fig_path)
    plt.close(fig)



if __name__ == '__main__':
    main()
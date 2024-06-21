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

def read_json2(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)

    return data


def params():
    result = [
        {
            "param": "time_python_function",
            "title": "Tempo de Execução da Função(s) X Quantidade de Shards",
            "min": 0,
            "max": 210,
            "total": [],
            "ls": [],
            "lm": [],
            "ps": []
        },
        {
            "param": "mean",
            "title": "Média do Tempo de Busca por Query X Quantidade de Shards",
            "min": 0,
            "max": 0.08,
            "total": [],
            "ls": [],
            "lm": [],
            "ps": []
        },
        {
            "param": "variance",
            "title": "Variância do Tempo de Busca por Query X Quantidade de Shards",
            "min": 0,
            "max": 0.0006,
            "total": [],
            "ls": [],
            "lm": [],
            "ps": []
        },
        {
            "param": "standard_deviation",
            "title": "Desvio Padrão do Tempo de Busca por Query X Quantidade de Shards",
            "min": 0,
            "max": 0.02,
            "total": [],
            "ls": [],
            "lm": [],
            "ps": []
        },
    ]

    return result

def get_data(nodes_list, shards_list, folder_name):

    attributes = params()        
    # time_python_function_total = []
    # mean_total = []

    for nodes in nodes_list:

        for attribute in attributes:
            attribute["ls"] = []
            attribute["lm"] = []
            attribute["ps"] = []
        # time_python_function_ls = []
        # time_python_function_lm = []
        # time_python_function_ps = []

        # mean_ls = []
        # mean_lm = []
        # mean_ps = []

        for shards in shards_list:

            json_data = read_json2(f"{folder_name}n{nodes}_s{shards}_log_linear_search.json")
            for attribute in attributes:
                attribute["ls"].append(json_data[attribute["param"]])
            # time_python_function_ls.append(time_python_function)
            # mean_ls.append(mean)

            json_data = read_json2(f"{folder_name}n{nodes}_s{shards}_log_linear_msearch.json") 
            for attribute in attributes:
                attribute["lm"].append(json_data[attribute["param"]])
            # time_python_function, mean, _, _ = read_json(f"{folder_name}n{nodes}_s{shards}_log_linear_msearch.json") 
            # time_python_function_lm.append(time_python_function)
            # mean_lm.append(mean)

            json_data = read_json2(f"{folder_name}n{nodes}_s{shards}_log_parallel_search.json")
            for attribute in attributes:
                attribute["ps"].append(json_data[attribute["param"]])
            # time_python_function, mean, _, _ = read_json(f"{folder_name}n{nodes}_s{shards}_log_parallel_search.json")
            # time_python_function_ps.append(time_python_function)
            # mean_ps.append(mean)

        for attribute in attributes:
            attribute["total"].append(attribute["ls"])
            attribute["total"].append(attribute["lm"])
            attribute["total"].append(attribute["ps"])

        # time_python_function_total.append(time_python_function_ls)
        # time_python_function_total.append(time_python_function_lm)
        # time_python_function_total.append(time_python_function_ps)

        # mean_total.append(mean_ls)
        # mean_total.append(mean_lm)
        # mean_total.append(mean_ps)

    return attributes


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

    attributes = get_data(nodes_list, shards_list, folder_name)

    # time_python_function_total = []

    # for nodes in nodes_list:
    #     time_python_function_ls = []
    #     time_python_function_lm = []
    #     time_python_function_ps = []

    #     for shards in shards_list:

    #         time_python_function, _, _, _ = read_json(f"{folder_name}n{nodes}_s{shards}_log_linear_search.json")
    #         time_python_function_ls.append(time_python_function)

    #         time_python_function, _, _, _ = read_json(f"{folder_name}n{nodes}_s{shards}_log_linear_msearch.json") 
    #         time_python_function_lm.append(time_python_function)

    #         time_python_function, _, _, _ = read_json(f"{folder_name}n{nodes}_s{shards}_log_parallel_search.json")
    #         time_python_function_ps.append(time_python_function)

    #     time_python_function_total.append(time_python_function_ls)
    #     time_python_function_total.append(time_python_function_lm)
    #     time_python_function_total.append(time_python_function_ps)

    # pprint(time_python_function_total)

    
    for attribute in attributes:
        # Dados
        min = attribute["min"]
        max = attribute["max"]
        y = attribute["total"] # time_python_function_total # np.random.rand(12, 7) * 10  # Exemplos de valores de tempo em segundos para cada gráfico
        title = attribute["title"] # 'Tempo Python(s) X Quantidade de Shards'
        
        columns_title = ['L. Search', 'L. Msearch', 'Parallel Search']
        x = shards_list

        # Configurações da grade de gráficos
        fig, axes = plt.subplots(len(nodes_list), len(columns_title), figsize=(15, 20))
        fig.suptitle(title, fontsize=16)

        # Títulos das linhas e colunas
        linhas_titulo = ['n' + str(nodes) for nodes in nodes_list] # ['n1', 'n2', 'n3', 'n4']

        # Gerar gráficos
        for i in range(len(nodes_list)):
            for j in range(len(columns_title)):
                ax = axes[i, j]
                y_values = y[i*len(columns_title) + j]
                ax.plot(x, y_values, marker='o', linestyle='-', color='b')
                ax.set_xlabel('Shards')
                ax.set_ylabel('Tempo (s)')
                ax.set_ylim(min, max)
                #ax.set_title(f'Gráfico {i*4 + j + 1}')
                ax.set_title(f'')
                ax.set_xticks(x)
                ax.grid(True)

        # Adicionar títulos às linhas e colunas
        for ax, col in zip(axes[0], columns_title):
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
    
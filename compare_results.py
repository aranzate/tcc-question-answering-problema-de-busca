import json
import argparse
import consts
import matplotlib.pyplot as plt

def read_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)

    return data

def create_empty_attribute(param, title, min_value, max_value):
    return {
        "param": param,
        "title": title,
        "min": min_value,
        "max": max_value,
        "total": [],
        "ls": [],
        "lm": [],
        "ps": []
    }

def get_filled_attributes(attributes, nodes_list, shards_list, folder_name):
    for nodes in nodes_list:
        for attribute in attributes:
            attribute["ls"] = []
            attribute["lm"] = []
            attribute["ps"] = []

        for shards in shards_list:
            json_data = read_json(f"{folder_name}n{nodes}_s{shards}_log_linear_search.json")
            for attribute in attributes:
                attribute["ls"].append(json_data[attribute["param"]])

            json_data = read_json(f"{folder_name}n{nodes}_s{shards}_log_linear_msearch.json") 
            for attribute in attributes:
                attribute["lm"].append(json_data[attribute["param"]])

            json_data = read_json(f"{folder_name}n{nodes}_s{shards}_log_parallel_search.json")
            for attribute in attributes:
                attribute["ps"].append(json_data[attribute["param"]])

        for attribute in attributes:
            attribute["total"].append(attribute["ls"])
            attribute["total"].append(attribute["lm"])
            attribute["total"].append(attribute["ps"])

    return attributes


def main():
    parser = argparse.ArgumentParser(description='Cria gráficos de comparação entre os logs da pasta.')
    parser.add_argument('folder_name', nargs="?", default="", help='Nome da pasta')
    parser.add_argument('--nodes_list', type=int, nargs='*', default=[1, 2, 3, 4], help='Lista de nós')
    parser.add_argument('--shards_list', type=int, nargs='*', default=[1, 2, 4, 8, 12, 16, 32], help='Lista de shards')
    args = parser.parse_args()
    args = parser.parse_args()

    folder_name = args.folder_name
    if(folder_name == "") or (folder_name is None): 
        folder_name = f".{consts.SEPARATOR_PATH}{consts.LOGS_PATH}"

    nodes_list = args.nodes_list
    shards_list = args.shards_list
    empty_attributes = [
        create_empty_attribute("time_python_function", "Tempo de Execução da Função(s) X Quantidade de Shards", 0, 210),
        create_empty_attribute("mean", "Média do Tempo de Busca por Query X Quantidade de Shards", 0, 0.08),
        create_empty_attribute("variance", "Variância do Tempo de Busca por Query X Quantidade de Shards", 0, 0.0006),
        create_empty_attribute("standard_deviation", "Desvio Padrão do Tempo de Busca por Query X Quantidade de Shards", 0, 0.024)
    ]

    attributes = get_filled_attributes(empty_attributes, nodes_list, shards_list, folder_name)

    print("GRAFICOS: Gera gráficos de comparação com todos os logs")

    for attribute in attributes:
        columns_title = ['L. Search', 'L. Msearch', 'Parallel Search']
        rows_title = ['n' + str(nodes) for nodes in nodes_list] # ['n1', 'n2', 'n3', 'n4']
        x = shards_list
        y = attribute["total"] 
        min = attribute["min"]
        max = attribute["max"]
        title = attribute["title"] 
        
        fig, axes = plt.subplots(len(nodes_list), len(columns_title), figsize=(15, 20))
        fig.suptitle(title, fontsize=16)        

        for i in range(len(nodes_list)):
            for j in range(len(columns_title)):
                ax = axes[i, j]
                y_values = y[i*len(columns_title) + j]
                ax.plot(x, y_values, marker='o', linestyle='-', color='b')
                ax.set_xlabel('Shards')
                ax.set_ylabel('Tempo (s)')
                ax.set_ylim(min, max)
                ax.set_title(f'')
                ax.set_xticks(x)
                ax.grid(True)

        # Adicionar títulos às linhas e colunas
        for ax, col in zip(axes[0], columns_title):
            ax.set_title(col, fontsize=14, pad=20)
        for ax, row in zip(axes[:,0], rows_title):
            ax.set_ylabel(row, rotation=0, fontsize=14, labelpad=40)

        # Salvar
        fig_path = f'{folder_name}/results_{title.replace(" ", "_").lower()}.png'
        plt.savefig(fig_path)
        plt.close(fig)


if __name__ == '__main__':
    main()
    
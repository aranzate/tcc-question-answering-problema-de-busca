import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import sys

def find_hits(log_search, id_searched):
    if(log_search['actions'][int(id_searched)-1]['id'] == int(id_searched)):
        return log_search['actions'][int(id_searched)-1]['hits']
    print("Erro: id de documento não corresponde.")
    sys.exit(1)


def precision_at_k(documentos_encontrados, documentos_relevantes, k_maximo, folder_name, fun_name):
    k_valores = range(1, k_maximo + 1)
    precisao_valores = []
    desvio_padrao_valores = []

    plt.figure(figsize=(20, 10))
    plt.subplots_adjust(wspace=0.7)
    for k in k_valores:
        precisoes = []
        for id, relevant_docs in documentos_relevantes.items():
            documentos_encontrados_query = find_hits(documentos_encontrados, id)
            k_documentos_encontrados = documentos_encontrados_query[:k]
            k_relevantes = [doc for doc in k_documentos_encontrados if doc in relevant_docs]
            precisao = len(k_relevantes) / k if k != 0 else 0
            precisoes.append(precisao)

        desvio_padrao_k = np.std(precisoes)
        desvio_padrao_valores.append(desvio_padrao_k)

        plt.subplot(1, len(k_valores), k)
        plt.boxplot(desvio_padrao_valores)
        plt.title(f'k={k}')
        plt.grid(True)
        plt.ylim(0, 0.5)  # Definindo limite para o eixo y

        media_aritmetica_k = np.mean(precisoes)
        precisao_valores.append(media_aritmetica_k)

    fig_path = f'{folder_name}/{fun_name.replace(" ", "_").lower()}_boxplot_at_k_{k_maximo}.png'
    plt.savefig(fig_path)

    # Plot do gráfico final
    plt.figure(figsize=(10, 6))
    plt.errorbar(k_valores, precisao_valores, yerr=desvio_padrao_valores, fmt='o-', ecolor='r', capsize=5)
    plt.xlabel('k')
    plt.ylabel('Precision@k (Média)')
    plt.title(f'{fun_name} - Precision@k Gráfico')
    plt.grid(True)
    plt.xticks(k_valores)
    # plt.ylim(0, 1)  # Definindo limite para o eixo y
    plt.tight_layout()

    fig_path = f'{folder_name}/{fun_name.replace(" ", "_").lower()}_precision_at_k_{k_maximo}.png'
    plt.savefig(fig_path)

        
def recall_at_k(documentos_encontrados, documentos_relevantes, k_maximo, folder_name, fun_name):
    k_valores = range(1, k_maximo + 1)
    recall_valores = []
    desvio_padrao_valores = []

    for k in k_valores:
        recalls = []
        for query_id, documentos in documentos_relevantes.items():
            documentos_encontrados_query = find_hits(documentos_encontrados, query_id)
            documentos_encontrados_k = documentos_encontrados_query[:k]
            documentos_relevantes_set = set(documentos)
            relevante_k = [doc for doc in documentos_encontrados_k if doc in documentos_relevantes_set]
            recall = len(relevante_k) / len(documentos) if len(documentos) != 0 else 0
            recalls.append(recall)
        
        media_recall_k = np.mean(recalls)
        desvio_padrao_recall_k = np.std(recalls)
        recall_valores.append(media_recall_k)
        desvio_padrao_valores.append(desvio_padrao_recall_k)

    # Plot do gráfico
    plt.figure(figsize=(10, 6))
    
    plt.subplot(1, 2, 1)
    plt.errorbar(k_valores, recall_valores, yerr=desvio_padrao_valores, fmt='o-', ecolor='r', capsize=5)
    plt.xlabel('k')
    plt.ylabel('Recall@k (Média)')
    plt.title(f'{fun_name} - Recall@k Gráfico')
    plt.grid(True)
    plt.xticks(k_valores)
    
    plt.subplot(1, 2, 2)
    plt.boxplot(desvio_padrao_valores)
    plt.xlabel('Desvio Padrão do Recall@k')
    plt.title('Boxplot do Desvio Padrão do Recall@k')
    plt.grid(True)
    plt.ylim(0, 0.5)
    
    plt.tight_layout()

    plt.title(f'{fun_name} - Boxplot')
    fig_path = f'{folder_name}/{fun_name.replace(" ", "_").lower()}_recall_at_k_{k_maximo}.png'
    plt.savefig(fig_path)
    
    #plt.show()

import matplotlib.pyplot as plt
import numpy as np

def precision_at_k(documentos_encontrados, documentos_relevantes, k_maximo):
        k_valores = range(1, k_maximo + 1)
        precisao_valores = []
        desvio_padrao_valores = []

        for k in k_valores:
            precisoes = []
            for id, relevant_docs in documentos_relevantes.items():
                documentos_encontrados_query = documentos_encontrados.get(id, [])
                k_documentos_encontrados = documentos_encontrados_query[:k]
                k_relevantes = [doc for doc in k_documentos_encontrados if doc in relevant_docs]
                precisao = len(k_relevantes) / k if k != 0 else 0
                precisoes.append(precisao)

            media_aritmetica_k = np.mean(precisoes)
            desvio_padrao_k = np.std(precisoes)
            
            precisao_valores.append(media_aritmetica_k)
            desvio_padrao_valores.append(desvio_padrao_k)

        # Plot do gráfico
        plt.figure(figsize=(10, 6))
        
        plt.subplot(1, 2, 1)
        plt.errorbar(k_valores, precisao_valores, yerr=desvio_padrao_valores, fmt='o-', ecolor='r', capsize=5)
        plt.xlabel('k')
        plt.ylabel('Precision@k (Média)')
        plt.title('Precision@k Gráfico')
        plt.grid(True)
        plt.xticks(k_valores)
        
        plt.subplot(1, 2, 2)
        plt.boxplot(desvio_padrao_valores)
        plt.xlabel('Desvio Padrão do Precision@k')
        plt.title('Boxplot do Desvio Padrão do Precision@k')
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
        


def recall_at_k(documentos_encontrados, documentos_relevantes, k_maximo):
    k_valores = range(1, k_maximo + 1)
    recall_valores = []
    desvio_padrao_valores = []

    for k in k_valores:
        recalls = []
        for query_id, documentos in documentos_relevantes.items():
            documentos_encontrados_query = documentos_encontrados.get(query_id, [])
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
    plt.title('Recall@k Gráfico')
    plt.grid(True)
    plt.xticks(k_valores)
    
    plt.subplot(1, 2, 2)
    plt.boxplot(desvio_padrao_valores)
    plt.xlabel('Desvio Padrão do Recall@k')
    plt.title('Boxplot do Desvio Padrão do Recall@k')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

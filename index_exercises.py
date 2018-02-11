import os
from nltk import word_tokenize


#1.Crear una clase que implemente un índice básico (se recomienda: BasicIndex).
#Para ello, dado un conjunto de documentos debe procesar sus textos obteniendo
#sus tokens sin stopwords, sin símbolos de puntuación y lematizados a ser posible.
#Estos tokens serán introducidos en una lista. Un diccionario debe relacionar estas
#listas de tokens con el documento de donde provienen. La clave es el nombre del
#documento y el valor es la lista de tokens.
#Crear una clase que implemente una consulta básica (se recomienda:
#BasicQuery). Esta debe de almacenar el índice creado y permitir al usuario
#introducir frases o una palabra suelta. Debe devolver los documentos en donde
#la palabra o palabras detectadas en la frase proporcionada por el usuario
#aparecen. Se recomienda de nuevo procesar la frase para crear tokens.


class BasicQuery(object):

    def __init__(self, path, extension):

        self.path = path
        self.extension = extension
        self.load_data()

    def load_data(self):

        ficheros = []
        path = self.path
        try:
            for file in os.listdir(self.path):
                if file.endswith(self.extension):
                    with open(path+'/'+file,'r', encoding='utf-8') as txt:
                        fichero_list = []
                        fichero_list.append(file)
                        fichero_list.append(txt.readlines())
                        ficheros.append(fichero_list)
            return {i[0]: (i[1]) for i in ficheros}
        except:
            raise Exception("No se pudo cargar el archivo de datos")


    def query(self,query):
        lista_de_resultados=[]
        for value, metadata in self.load_data().items():
            string = ''.join(sentence.upper() for sentence in metadata)
            if query.upper() in string:
                lista_de_resultados.append(value)
            else:
                pass
        if len(lista_de_resultados) > 0:
            lista_de_resultados_str = ', '.join(str(i) for i in lista_de_resultados)
            return "La query '{0}' se encuentra en los archivos: {1}".format(query,lista_de_resultados_str)
        else:
            return "La query '{0}' no se encuentra en ningun archivo".format(query)

index = BasicQuery('~/Downloads/Corpus_de_documentos-20180202','.txt')
print(index.query("The house was in England"))

#2.Crear una clase que implemente un índice invertido (se recomienda: InvertexIndex).
#Para ello hay que seguir las directrices proporcionadas en el ejercicio anterior
#modificando la estructura del índice. En este caso el diccionario debe ser de la siguiente
#manera: las claves deben ser los tokens detectados en todos los documentos, mientras
#que los valores deben ser una lista de nombres de los documentos donde aparecen esos
#tokens. La clase (se recomienda: InvertedQuery) que implemente la consulta debe ser
#igualmente similar a la del primer ejercicio.
#Ayuda:
#Aplicar exactamente las mismas instrucciones.

class InvertedQuery(object):

    def __init__(self, path, extension):

        self.path = path
        self.extension = extension
        self.load_data()

    def load_data(self):

        path = '/Users/javierllorente/Downloads/Corpus_de_documentos-20180202'
        try:
            invert_dict = {}
            for file in os.listdir('/Users/javierllorente/Downloads/Corpus_de_documentos-20180202'):
                if file.endswith(".txt"):
                    with open(path+'/'+file,'r', encoding='utf-8') as txt:
                        text = txt.readlines()
                        uniquewords = set()
                        for i in text:
                            words = word_tokenize(i)
                            for word in words:
                                if word.isalpha():
                                    uniquewords.add(word.upper())
                                else:
                                    pass
                        for uniqueword in uniquewords:
                            if uniqueword not in invert_dict:
                                invert_dict[uniqueword] = [file]
                            else:
                                invert_dict[uniqueword].append(file)
            return invert_dict
        except:
            raise Exception("No se pudo cargar el archivo de datos")

    def query(self,query):

        results = self.load_data()
        if query.upper() in results.keys():
            text_results = ','.join(str(word) for word in results[query.upper()])
            return print("EL resultado se encuentra en los siguientes textos {0}".format(text_results))
        else:
            return print("No tenemos el resultado disponible")

index = InvertedQuery('~/Downloads/Corpus_de_documentos-20180202','.txt')
print(index.query('portresses'))



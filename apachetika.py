from tikapp import TikaApp
import operator
from nltk import word_tokenize
from nltk.corpus import stopwords

#1.Crear una clase (se recomienda el nombre: TikaReader) que permita llevar a cabo
#las cuatro operaciones básicas de Tika en Python. Estas cuatro operaciones
#deben ir encapsuladas en un método propio de la clase. En el constructor de la
#clase (__init__) se debe pasar como parámetro el documento a procesar (se recomienda
#utilizar el proporcionado: crawler.pdf). El constructor también debe cargar el fichero jar
#del cliente de Tika.

class TikaReader(object):

    def __init__(self, path):
        self.tika_client = TikaApp(file_jar=path)

    def detect_type(self, doc):
        return self.tika_client.detect_content_type(doc)

    def detect_language(self, doc):
        return self.tika_client.detect_language(doc)

    def content(self,doc):
        return self.tika_client.extract_all_content(doc)

processor = TikaReader('~/Downloads/tika-app-1.16.jar')
doc = 'crawler.pdf'
processor.detect_type(doc)
processor.detect_language(doc)
processor.content(doc)


#2. Crear una clase (se recomienda el nombre: ProcessJSONTika) para procesar el JSON
#proporcionado por Tika en el método:
#extract_all_content(<fichero>, convert_to_obj=<True/False>)
#Esta clase debe obtener los siguientes métodos:
#A) Dado el JSON de procesamiento Tika escribir por consola los metadatos sobre
#autores, fecha de creación y fecha de modificación.
#B) Obtener el contenido (solo texto) del fichero JSON proporcionado por Tika.
#C) Generar un vocabulario descendente. Es decir, para cada palabra detectada indicar
#el número de ocurrencias de la misma en el texto. Devolver solo las diez más
#utilizadas. Se recomienda realizar una limpieza de stopwords, símbolos de
#puntuación y obtención de lemas para un desarrollo más preciso y óptimo.

class ProcessJSONTika(object):

    def __init__(self, path):
        self.tika_client = TikaApp(file_jar=path)

    def jsonprocessor(self,doc):
        return self.tika_client.extract_all_content(doc, convert_to_obj=True)[0]

    def author(self,doc):
        return self.jsonprocessor(doc).get('Author',None)

    def creationdate(self, doc):
        return self.jsonprocessor(doc).get('Creation-Date',None)

    def lastmodified(self, doc):
        return self.jsonprocessor(doc).get('Last-Modified',None)

    def all_content(self, doc):
        return self.jsonprocessor(doc)['X-TIKA:content']

    def top_10_words(self, doc):
        content = self.all_content(doc)
        words = word_tokenize(content)
        # stopwords
        stopWords = set(stopwords.words('english'))
        clean_words = [word for word in words if word.isalpha() and word not in stopWords]
        words_dic = {}
        for i in clean_words:
            if i in words_dic.keys():
                words_dic[i] += 1
            else:
                words_dic[i] = 1
        return sorted(words_dic.items(), key=operator.itemgetter(1), reverse=True)[:10]


Json = ProcessJSONTika('~/Downloads/tika-app-1.16.jar')
document = 'crawler.pdf'
tikaobject = Json.jsonprocessor(document)
tikaauthor = Json.author(document)
tikacreationdate = Json.creationdate(document)
tikalastmodified = Json.lastmodified(document)
tikatop10words = Json.top_10_words(document)





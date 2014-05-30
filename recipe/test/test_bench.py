import __init__
import unittest
from unittest import TestCase

import locale
from os import path
from PIL import Image
from datetime import datetime
from pymongo import MongoClient
import gridfs
from recipe.items import RecipeItem
from recipe.settings import IMAGES_STORE

class TestFunctions(TestCase):
    def setUp(self):
        self.item = self.create_item()
        self.access_database()

    def access_database(self): # PENDING move DB test to another file
        self.connection = MongoClient('localhost', 27017)
        self.db = self.connection.mock_db
        self.collection = self.db.mock_recipes
        self.fs = gridfs.GridFS(self.db)

    def tearDown(self):
        del self.item
        self.collection.drop()
        self.connection.close()        

    def test_datetime(self): 
        # PENDING should test recipe.pipelines.RecipePipeline-transform_date
        locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
        textdate = "Lunes, 21 de Abril de 2014 00:00"
        date = datetime.strptime(textdate,"%A, %d de %B de %Y %H:%M")
        self.assertEqual(date,datetime(2014, 4, 21, 0, 0))

    def test_item_creation(self):
        self.assertEqual(self.item["title"], u'Pan de cebolla y pipas')

    def test_item_missing_field(self):
        with self.assertRaises(KeyError):
            self.item["image"]

    def test_db_active(self):
        self.assertIsNotNone(self.connection)

    def test_db_add_element(self):
        self.collection.insert(dict(self.item))
        self.assertTrue(self.collection.count())
        
    def test_db_add_image_fs(self):
        image_path = "data/sample.jpg"
        image = open(image_path, 'r')
        img_id = self.fs.put(image)
        retrieve = self.fs.get(img_id)
        self.assertIsNotNone(retrieve)
        self.fs.delete(img_id)

    def create_item(self):
        item = RecipeItem()
        item["title"] = u'Pan de cebolla y pipas'
        item["category"] = u'Entrantes'
        item["link"] = u'http://www.1080recetas.com/recetas/entrantes/1362-receta-gratis-cocina-pan-cebolla-pipas-santa-rita-harinas'
        item["date"] = datetime(2014, 4, 21, 0, 0)
        item["tips"] = u'*En vez de sofrito de cebolla, puedes utilizar Cebolla Frita Santa Rita.'
        item["ingredients"] = [u'413g de',
                               u' Harina gran Fuerza Santa Rita',
                               u'270ml de Agua templada',
                               u'20g de Levadura de Panader\xeda',
                               u'1,5 cucharada peque\xf1a de Sal fina',
                               u'1 cucharada peque\xf1a de Az\xfacar',
                               u'2 cucharadas de sofrito de Cebolla*',
                               u'2 cucharadas de Pipas peladas ']

        item["description"] = u'Dentro de su gama de Harinas y s\xe9molas de trigo, Santa Rita cuenta con la Harina Gran Fuerza, indicada para todo tipo de boller\xeda, postres, panes especiales y todo tipo de recetas. Y nosotros la hemos probado para elaborar un delicioso Pan de cebolla y pipas, perfecto para acompa\xf1ar cualquier comida o para tostar y servir como base para nuestras tostas y aperitivos. Toma nota porque el resultado ha sido fant\xe1stico.'
        
        item["elaboration"] = [u'Lo primero que hay que hacer es el fermento. Para ello, diluye en medio vaso de agua la levadura de panader\xeda. Pasados 5 minutos a \xf1ade 2 cucharadas de Harina Gran Fuerza Santa Rita.',
                               u'D\xe9jalo reposar todo 1 hora.',
                               u'Mientras sofr\xede la cebolla en un poco de aceite de oliva. Una vez sofrita, d\xe9jala escurrir en papel de cocina para que absorba todo el aceite.',
                               u'Una vez haya fermentado, en un bol echa el resto de harina Santa Rita, con el fermento y el az\xfacar y comienza a mezclar.',
                               u'Cuando se hayan integrado bien todos los ingredientes, deja reposar la mezcla otra hora, en un bol cubierto con film de pl\xe1stico o un trapo de cocina y dentro del horno apagado. Ah\xed encontrar\xe1s la temperatura adecuada para que tenga lugar el fermento.',
                               u'Tras este tiempo es el momento de integrar la sal y amasar. Nosotros hemos seguido los pasos que nos indican en este v\xeddeo: ',
                               u'. ',
                               u'Una vez la textura es la deseada, es el momento de in                       tegrar a tu masa las pipas y la cebolla.',
                               u'Pega estos ingredientes a tu masa y est\xedrala un poco.',
                               u'Con ayuda de una esp\xe1tula corta la masa por la mitad y coloca una de las mitades encima de la otra.',
                               u'Con las manos aplasta y estira la masa y vuelve a cortarla por la mitad.',
                               u'Repite esta operaci\xf3n tantas veces como sea necesario hasta que la cebolla y las pipas est\xe9n integradas en tu pan.',
                               u'Una vez lo consigas, dale forma redonda a tu masa y col\xf3cala sobre una bandeja, cubierta con papel de horno.',
                               u'D\xe9jala reposar la masa otros 30 minutos. P\xedntala con un poco de aceite de oliva e introduce la bandeja en el horno apagado. ',
                               u'Tras este tiempo, saca la bandeja de horno y precali\xe9ntalo.\xa0 ',
                               u'Introduce el pan y d\xe9jalo durante 25 minutos a unos 220\xba con calor por arriba y por abajo.',
                               u'Una vez est\xe9 dorado s\xe1calo del horno y d\xe9jalo reposar sobre una rejilla.',
                               u'Y despu\xe9s ya puedes disfrutar de este delicioso pan.'],
        return item

if __name__ == '__main__':
    unittest.main()

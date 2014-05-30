from retrieve import ItemRetriever
rt = ItemRetriever()

i1 = rt.ReturnItemByNumber(322)
print "Retrieved item {0}".format(str(i1["title"]))
print "-------------------------------------------"
for key,value in i1.iteritems():
    print key, ">>>>", value
    print

i2 = rt.ReturnItemByLink("http://www.1080recetas.com/recetas/entrantes/1362-receta-gratis-cocina-pan-cebolla-pipas-santa-rita-harinas")
print "Retrieved item {0}".format(str(i2["title"]))
print "-------------------------------------------"
for key,value in i2.iteritems():
    print key, ">>>>", str(value)
    print

rt.ShowImageByNumber(1007)


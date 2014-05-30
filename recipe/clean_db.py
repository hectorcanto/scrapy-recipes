from retrieve import ItemRetriever
rt = ItemRetriever()
rt.ClearDB()
if not rt.collection.count():
    print "Now the collection is empty"

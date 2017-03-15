import bs4, logging, sys

def initiateFile(filehandler):
	filehandler.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
	filehandler.write('<key id="comment" for="node" attr.name="comment" attr.type="string"/>\n')
	filehandler.write('<key id="type" for="node" attr.name="type" attr.type="string"/>\n')
	filehandler.write('<key id="_id" for="node" attr.name="identity" attr.type="string"/>\n')
	filehandler.write('<key id="homepage" for="node" attr.name="homepage" attr.type="string"/>\n')
	filehandler.write('<key id="label_n" for="node" attr.name="label_n" attr.type="string"/>\n')
	filehandler.write('<key id="country" for="node" attr.name="country" attr.type="string"/>\n')
	filehandler.write('<key id="ProductPropertyNumeric_0" for="node" attr.name="ProductPropertyNumeric_0" attr.type="int"/>\n')
	filehandler.write('<key id="ProductPropertyNumeric_1" for="node" attr.name="ProductPropertyNumeric_1" attr.type="int"/>\n')
	filehandler.write('<key id="ProductPropertyNumeric_2" for="node" attr.name="ProductPropertyNumeric_2" attr.type="int"/>\n')
	filehandler.write('<key id="ProductPropertyNumeric_3" for="node" attr.name="ProductPropertyNumeric_3" attr.type="int"/>\n')
	filehandler.write('<key id="ProductPropertyNumeric_4" for="node" attr.name="ProductPropertyNumeric_4" attr.type="int"/>\n')
	filehandler.write('<key id="ProductPropertyNumeric_5" for="node" attr.name="ProductPropertyNumeric_5" attr.type="int"/>\n')
	filehandler.write('<key id="ProductPropertyTextual_0" for="node" attr.name="ProductPropertyTextual_0" attr.type="string"/>\n')
	filehandler.write('<key id="ProductPropertyTextual_1" for="node" attr.name="ProductPropertyTextual_1" attr.type="string"/>\n')
	filehandler.write('<key id="ProductPropertyTextual_2" for="node" attr.name="ProductPropertyTextual_2" attr.type="string"/>\n')
	filehandler.write('<key id="ProductPropertyTextual_3" for="node" attr.name="ProductPropertyTextual_3" attr.type="string"/>\n')
	filehandler.write('<key id="ProductPropertyTextual_4" for="node" attr.name="ProductPropertyTextual_4" attr.type="string"/>\n')
	filehandler.write('<key id="ProductPropertyTextual_5" for="node" attr.name="ProductPropertyTextual_5" attr.type="string"/>\n')
	filehandler.write('<key id="OfferWebPage" for="node" attr.name="OfferWebPage" attr.type="string"/>\n')
	filehandler.write('<key id="ValidFrom" for="node" attr.name="ValidFrom" attr.type="string"/>\n')
	filehandler.write('<key id="ValidTill" for="node" attr.name="ValidTill" attr.type="string"/>\n')
	filehandler.write('<key id="price" for="node" attr.name="price" attr.type="float"/>\n')
	filehandler.write('<key id="Delivery Days" for="node" attr.name="Delivery Days" attr.type="int"/>\n')
	filehandler.write('<key id="mbox_sha1sum" for="node" attr.name="mbox_sha1sum" attr.type="string"/>\n')
	filehandler.write('<key id="rating_0" for="node" attr.name="Rating_0" attr.type="int"/>\n')
	filehandler.write('<key id="rating_1" for="node" attr.name="Rating_1" attr.type="int"/>\n')
	filehandler.write('<key id="rating_2" for="node" attr.name="Rating_2" attr.type="int"/>\n')
	filehandler.write('<key id="rating_3" for="node" attr.name="Rating_3" attr.type="int"/>\n')
	filehandler.write('<key id="rating_4" for="node" attr.name="Rating_4" attr.type="int"/>\n')
	filehandler.write('<key id="rating_5" for="node" attr.name="Rating_5" attr.type="int"/>\n')

	filehandler.write('\t<graph id="G" edgedefault="undirected">\n')	


def endFile(filehandler):
	filehandler.write("\t</graph>\n")
	filehandler.write("</graphml>\n")

def writeEdges(filehandler, allEdges, _id):
	for each in allEdges:
		filehandler.write('\t<edge id="%d" source="%d" target="%d" label_n="%s"></edge>\n'%(_id, each[0], each[1], each[2]))
		_id+=1

def writeToFileWithNested(filehandler, data, dataNested, tabIndex):
	filehandler.write("\t"*tabIndex + '<node id="%d">\n'% data['_id'])		
#	filehandler.write("\t"*tabIndex + '<node>\n')		

	for each in data:
		filehandler.write("\t"*(tabIndex+1) + '<data key="%s">%s</data>\n'%(str(each), data[each]))

	for mainTag in dataNested:
		allData = dataNested[mainTag]
		for each in allData:
			filehandler.write("\t"*(tabIndex+1) + '<data key="%s_%s">%s</data>\n'%(str(mainTag), each["nr"], each.text))
			
	filehandler.write("\t"*tabIndex + '</node>\n')


def writeToFile(filehandler, data, tabIndex):
	filehandler.write("\t"*tabIndex + '<node id="%d">\n'% data['_id'])		
#	filehandler.write("\t"*tabIndex + '<node>\n')		

	for each in data:
		filehandler.write("\t"*(tabIndex+1) + '<data key="%s">%s</data>\n'%(str(each), data[each]))
	filehandler.write("\t"*tabIndex + '</node>\n')


def foo(filename, graphMLFileName, logger):
	allEdges = []
	_id = 1
	productTypeIdMap = {}
	productFeatureIdMap = {}
	producerIdMap = {}
	productIdMap = {}
	vendorIdMap = {}
	offerIdMap = {}
	personIdMap = {}
	reviewIdMap = {}
	graphMLFile = open(graphMLFileName, "w")
	soup = bs4.BeautifulSoup(open(filename, "r").read())
	defaultTabIndex = 2
	initiateFile(graphMLFile)


	#Making nodes for all producttypes
	logger.info("Started Reading all the product type nodes and writing it to the file")	
	z = soup.findAll(lambda tag:tag.name == "producttype" and
                len(tag.attrs) == 1)
	for each in z:
		label_n = each.find("label").text
		comment = each.find("comment").text
		pub = each.find("publisher").text
		pud = each.find("publishdate").text
		productTypeIdMap[each["id"]] = _id 
		subclass = None
		writeToFile(graphMLFile, {'_id':_id, 'type': 'Product Type', 'label_n':label_n , 'comment':comment }, defaultTabIndex)
		try:
			subclass = each.find("subclassof").text
			allEdges.append((int(subclass), _id, "subclass"))
		except Exception as e:
			logger.debug("Product Type subclass not found")
			logger.error(e)
		_id+=1
	logger.info("Finished Reading Product Type Tags. Total Nodes created in the graph till now = %d" % (_id-1))
	logger.info("Finished Reading Product Type Tags. Total Edges created in the graph till now = %d" % len(allEdges))

	logger.info("Started Reading all the product Feature nodes and writing it to the file")
	z = soup.findAll(lambda tag:tag.name == "productfeature" and
                len(tag.attrs) == 1)
	
	for each in z:
		label_n = each.find("label").text
		comment = each.find("comment").text
		pub = each.find("publisher").text
		pud = each.find("publishdate").text
		productFeatureIdMap[each["id"]] = _id 
		writeToFile(graphMLFile, {'_id':_id, 'type':'Product Feature', 'label_n':label_n , 'comment':comment }, defaultTabIndex)

		_id+=1

	logger.info("Finished Reading Product Feature Tags. Total Nodes created in the graph till now = %d" % (_id-1))
	logger.info("Finished Reading Product Feature Tags. Total Edges created in the graph till now = %d" % len(allEdges))

	
	logger.info("Started Reading all the Producer nodes and writing it to the file")
	z = soup.findAll(lambda tag:tag.name == "producer" and
                len(tag.attrs) == 1)
	for each in z:
		label_n = each.find("label").text
		comment = each.find("comment").text
		homepage = each.find("homepage").text
		country = each.find("country").text
		pub = each.find("publisher").text
		pud = each.find("publishdate").text
		producerIdMap[each["id"]] = _id 
		writeToFile(graphMLFile, {'_id':_id, 'type':'Product Feature', 'label_n':label_n , 'comment':comment, \
														'homepage':homepage, 'country':country }, defaultTabIndex)
		_id+=1

	logger.info("Finished Reading Producer Tags. Total Nodes created in the graph till now = %d" % (_id-1))
	logger.info("Finished Reading Producer Tags. Total Edges created in the graph till now = %d" % len(allEdges))


	logger.info("Started Reading all the Product nodes and writing it to the file")
	z = soup.findAll(lambda tag:tag.name == "product" and
                len(tag.attrs) == 1)
	for each in z:
		label_n = each.find("label").text
		comment = each.find("comment").text
		allEdges.append((producerIdMap[each.find("producer").text.strip()], _id, "produces"))
		types = each.findAll("type")
		for _type in types:
			allEdges.append((productTypeIdMap[_type.text.strip()], _id, "isTypeOf"))
		features = each.findAll("productfeature")
		for _feature in features:
			allEdges.append((_id, productFeatureIdMap[_feature.text.strip()],"hasFeature"))
		productIdMap[each["id"]] = _id 
		productPropertyTexts = each.findAll("productpropertytextual")
		productPropertyNumeric = each.findAll("productpropertynumeric")
		writeToFileWithNested(graphMLFile, {'_id':_id, 'type':'Product Nodes', 'label_n':label_n, 'comment':comment} ,\
				{'ProductPropertyTextual':productPropertyTexts, 'ProductPropertyNumeric':productPropertyNumeric}, defaultTabIndex)
		_id+=1
		
	logger.info("Finished Reading Product Tags. Total Nodes created in the graph till now = %d" % (_id-1))
	logger.info("Finished Reading Product Tags. Total Edges created in the graph till now = %d" % len(allEdges))

	

	logger.info("Started Reading all the Vendor nodes and writing it to the file")
	z = soup.findAll(lambda tag:tag.name == "vendor" and
                len(tag.attrs) == 1)
	for each in z:
		label_n = each.find("label").text
		comment = each.find("comment").text
		homepage = each.find("homepage").text
		country = each.find("country").text
		vendorIdMap[each["id"]] = _id 
		writeToFile(graphMLFile, {'_id':_id, 'type':'Vendor', 'label_n':label_n , 'comment':comment, \
														'homepage':homepage, 'country':country }, defaultTabIndex)
		_id+=1

	logger.info("Finished Reading Vendor Tags. Total Nodes created in the graph till now = %d" % (_id-1))
	logger.info("Finished Reading Vendor Tags. Total Edges created in the graph till now = %d" % len(allEdges))



	logger.info("Started Reading all the Offer nodes and writing it to the file")
	z = soup.findAll(lambda tag:tag.name == "offer" and
                len(tag.attrs) == 1)
	for each in z:
		price = each.find("price").text
		vf = each.findAll("validfrom")[0].text
		vt = each.findAll("validfrom")[1].text
		dd = each.find("deliverydays")
		offerIdMap[each["id"]] = _id
		prod = each.find("product").text
		vend = each.find("vendor").text
		offerWebPage = each.find("offerwebpage").text
		allEdges.append((productIdMap[prod], _id, "offeron"))
		allEdges.append((vendorIdMap[vend], _id, "offerby"))
		writeToFile(graphMLFile, {'_id':_id, 'type':'Offer', 'OfferWebPage':offerWebPage , 'price':price, \
														'DeliveryDays':dd, 'ValidFrom':vf, 'ValidTill':vt }, defaultTabIndex)

		_id+=1
	logger.info("Finished Reading Offer Tags. Total Nodes created in the graph till now = %d" % (_id-1))
	logger.info("Finished Reading Offer Tags. Total Edges created in the graph till now = %d" % len(allEdges))



	logger.info("Started Reading all the Person nodes and writing it to the file")
	z = soup.findAll(lambda tag:tag.name == "person" and
                len(tag.attrs) == 1)
	for each in z:
		name = each.find("name").text
		mbox_sha1sum = each.find("mbox_sha1sum").text
		country = each.find("country").text
		personIdMap[each["id"]] = _id
		writeToFile(graphMLFile, {'_id':_id, 'type':'Person', 'mbox_sha1sum':mbox_sha1sum , 'country':country}, defaultTabIndex)

		_id+=1
	logger.info("Finished Reading Person Tags. Total Nodes created in the graph till now = %d" % (_id-1))
	logger.info("Finished Reading Person Tags. Total Edges created in the graph till now = %d" % len(allEdges))


	logger.info("Started Reading all the Review nodes and writing it to the file")
	z = soup.findAll(lambda tag:tag.name == "review" and
                len(tag.attrs) == 1)
	for each in z:
		prod = each.find("reviewfor").text
		reviewer = each.find("reviewer").text
		title = each.find("title").text
		textD = each.find("text").text
		reviewDate = each.find("reviewdate").text
		ratings = each.findAll("rating")
		
		reviewIdMap[each["id"]] = _id
		allEdges.append((_id, productIdMap[prod], "reviewfor"))
		allEdges.append((personIdMap[reviewer], _id, "reviewby"))
		writeToFileWithNested(graphMLFile, {'_id':_id, 'type':'Rating', 'title':title, 'text':textD, 'reviewDate':reviewDate} ,\
				{'rating':ratings}, defaultTabIndex)
		_id+=1
		
	logger.info("Finished Reading Review Tags. Total Nodes created in the graph till now = %d" % (_id-1))
	logger.info("Finished Reading Review Tags. Total Edges created in the graph till now = %d" % len(allEdges))

	writeEdges(graphMLFile, allEdges, _id)
	endFile(graphMLFile)
	graphMLFile.close()




if __name__ == "__main__":
	logging.basicConfig(filename = "BSBM.log", level = logging.INFO)
	logger = logging.getLogger(__name__)
	USAGE="""
INCORRECT USAGE
There are three arguments. 
The first is the path of the XML file which is generated using BSBM tools.
The second is the path of the GraphML file, which needs to be created when this code is run.
python bsbm.py /path/to/xml/file /path/to/graphml/file
	"""	
	if len(sys.argv)!=3:
		print(USAGE)
		sys.exit(-10)
		
	foo(sys.argv[1], sys.argv[2], logger)


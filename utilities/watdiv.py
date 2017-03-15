
import re,sys

def extractNameAndNumber(s):
	return (re.search('^[A-Za-z]*', s).group(0) , re.search('[0-9]*$', s).group(0))

def initiateFile(filehandler):
	filehandler.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
	filehandler.write('\t<graph id="G" edgedefault="undirected">\n')	


def endFile(filehandler):
	filehandler.write("\t</graph>\n")
	filehandler.write("</graphml>\n")

def writeEdges(filehandler, allEdges, _id):
	for each in allEdges:
		filehandler.write('\t<edge id="%d" source="%d" target="%d" label_n="%s"></edge>\n'%(_id, each[0], each[1], each[2]))
		_id+=1

def writeToFile(filehandler, data, tabIndex):
	filehandler.write("\t"*tabIndex + '<node id="%d">\n'% data['_id'])		
	for each in data:
		filehandler.write("\t"*(tabIndex+1) + '<data key="%s">%s</data>\n'%(str(each), data[each]))
	filehandler.write("\t"*tabIndex + '</node>\n')

	

def foo(savedFilePath, ntFilePath, opFile):

	f = open(savedFilePath, 'r')


	NodeTypes = int(f.readline().strip())

	nodesPresent = ["City", "Offer", "Product", "Purchase", "Retailer", "Review", "SubGenre", "User", "Website"]

	_id = 0
	AgeGroupIdMap = {}
	CityIdMap = {}
	CountryIdMap = {}
	GenderIdMap = {}
	GenreIdMap = {}
	LanguageIdMap = {}
	OfferIdMap = {}
	ProductIdMap = {}
	ProductCategoryIdMap = {}
	PurchaseIdMap = {}
	RetailerIdMap = {}
	ReviewIdMap = {}
	RoleIdMap = {}
	SubGenreIdMap = {}
	TopicIdMap = {}
	UserIdMap = {}
	WebsiteIdMap = {}


	dictionary = {
			'AgeGroup' : AgeGroupIdMap,
			'City' : CityIdMap,
			'Country' : CountryIdMap,
			'Gender' : GenderIdMap,
			'Genre' : GenreIdMap,
			'Language' : LanguageIdMap,
			'Offer' : OfferIdMap,
			'Product' : ProductIdMap,
			'ProductCategory' : ProductCategoryIdMap,
			'Purchase' : PurchaseIdMap,
			'Retailer' : RetailerIdMap,
			'Review' : ReviewIdMap,
			'Role' : RoleIdMap,
			'SubGenre' : SubGenreIdMap,
			'Topic' : TopicIdMap,
			'User' : UserIdMap,
			'Website' : WebsiteIdMap
	}

	allEdges = []

	for i in range(NodeTypes):
		nodeType = f.readline().strip().split(":")[1].split(" ")
		for i in range(0, int(nodeType[1])+1):
			dictionary[nodeType[0]][str(i)] = {'_id' : _id}
			_id+=1
		print(nodeType, _id)

	f.close()

	graphMLFile = open(opFile, "w")

	defaultTabIndex = 2


	initiateFile(graphMLFile)
	#Parsing through the file to enter data into the nodes and create the edges

	f = open(ntFilePath, "r")
	countAttr = 1
	diffAttributes = {'type' : 1}
	for line in f:
		subject = line.strip().split("\t")[0].split("/")[-1][:-1]
		nameAndNumber = extractNameAndNumber(subject)
		predicate = line.strip().split("\t")[1].split("/")[-1].split(">")[0]
		if "#" in predicate:
			predicate = predicate.split("#")[-1]
		_object = line.strip().split("\t")[2]
		dictionary[nameAndNumber[0]][nameAndNumber[1]]['type']=nameAndNumber[0]	
		if "http" in _object:
			node2 = _object.split("/")[-1].split(">")[0]
			nameAndNumber2 = extractNameAndNumber(node2)
			allEdges.append((dictionary[nameAndNumber[0]][nameAndNumber[1]]['_id'],\
				dictionary[nameAndNumber2[0]][nameAndNumber2[1]]['_id'], predicate))
		else:
			_object = _object.split('"')[1].strip('"')
			dictionary[nameAndNumber[0]][nameAndNumber[1]][predicate]=_object
			if predicate not in diffAttributes:
				diffAttributes[predicate]=1
			countAttr+=1

	def writeMetaData(filehandler, attributes):
		for each in attributes:
			filehandler.write('<key id="%s" for="node" attr.name="%s" attr.type="string"/>\n' % (str(each), str(each)))

	writeMetaData(graphMLFile, diffAttributes)
	print("Started Writing To File")
	for each in dictionary:
		print("Writing for %s type of nodes"%each)
		for eachD in dictionary[each]:
			writeToFile(graphMLFile, dictionary[each][eachD], defaultTabIndex)

	writeEdges(graphMLFile, allEdges, _id)

	endFile(graphMLFile)

	for each in dictionary:
		print(each, len(dictionary[each]))

USAGE = """
Incorrect Usage.
Correct Usage Is 
python /path/to/file/savd.txt /path/to/file/watdiv.nt outputfile
"""
if __name__ == "__main__":
	if len(sys.argv)!=4:
		print(USAGE)
		sys.exit(-1)
	foo(sys.argv[1], sys.argv[2], sys.argv[3])
#print(len(allEdges))
#print(len(dic))
#print(dic)

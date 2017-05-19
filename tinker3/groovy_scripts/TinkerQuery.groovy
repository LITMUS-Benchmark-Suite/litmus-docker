
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x = GraphFactory.open(args[0])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"

no_of_times = Integer.parseInt(args[2])
println "==============Running The Queries=========="
for (i in 1..no_of_times) {
	println "################Run "+i+"##################"
	"sync".execute()
    "echo 3 > /proc/sys/vm/drop_caches".execute()
	println "======Query 1======"
	s = System.currentTimeMillis();
	x.V.count()
	println (System.currentTimeMillis() - s)
	
	"sync".execute().text
	"echo 3 > /proc/sys/vm/drop_caches".execute()
	println "======Query 2======"
	s = System.currentTimeMillis();
	x.E.count()
	println (System.currentTimeMillis() - s)
	
}
x.shutdown()

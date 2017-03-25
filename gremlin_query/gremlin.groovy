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

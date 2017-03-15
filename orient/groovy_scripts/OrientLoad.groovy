println "===============Loading the Graph Model============"
x = new OrientGraph("memory:"+args[0])
s = System.currentTimeMillis()
x.loadGraphML(args[1])
println System.currentTimeMillis() - s
println "===============Graph Model Loaded================="
x.shutdown()

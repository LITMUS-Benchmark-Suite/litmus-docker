t = System.currentTimeMillis()
x = GraphFactory.open(args[0])
s = System.currentTimeMillis()
x.io(graphml()).readGraph(args[1])
println System.currentTimeMillis() - s
x.close()

t = System.currentTimeMillis()
x = TinkerGraph.open()
s = System.currentTimeMillis()
x.io(graphml()).readGraph(args[0]);
println System.currentTimeMillis() - s

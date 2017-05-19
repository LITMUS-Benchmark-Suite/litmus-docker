t = System.currentTimeMillis()
x = TinkerGraph.open();
s = System.currentTimeMillis()
x.io(graphml()).readGraph(args[1])
println System.currentTimeMillis() - s
x.shutdown()

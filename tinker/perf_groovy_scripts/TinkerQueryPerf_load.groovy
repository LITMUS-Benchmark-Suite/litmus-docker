t = System.currentTimeMillis()
x = new TinkerGraph(args[0])
s = System.currentTimeMillis()
x.loadGraphML(args[1])
println System.currentTimeMillis() - s
x.shutdown()

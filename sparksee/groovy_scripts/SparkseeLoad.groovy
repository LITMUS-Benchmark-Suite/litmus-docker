import com.tinkerpop.blueprints.impls.sparksee.*

x = new SparkseeGraph(args[0])
s = System.currentTimeMillis()
x.loadGraphML(args[1])
println System.currentTimeMillis() - s
x.shutdown()

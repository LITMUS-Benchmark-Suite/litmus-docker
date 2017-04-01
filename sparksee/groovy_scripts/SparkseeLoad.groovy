import com.tinkerpop.blueprints.impls.sparksee.*

t = System.currentTimeMillis()
x = new SparkseeGraph(args[0]+t)
s = System.currentTimeMillis()
x.loadGraphML(args[1])
println System.currentTimeMillis() - s
x.shutdown()

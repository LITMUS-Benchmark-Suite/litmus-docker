import com.tinkerpop.blueprints.impls.sparksee.*

x = new SparkseeGraph(args[0])
x.loadGraphML(args[1])
x.shutdown()

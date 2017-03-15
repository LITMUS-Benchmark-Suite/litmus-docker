import com.tinkerpop.blueprints.impls.sparksee.*

x = new Neo4jGraph(args[0])
println "===============Loading the Graph Model============"
s = System.currentTimeMillis()
x.loadGraphML(args[1])
println System.currentTimeMillis() - s
println "===============Graph Model Loaded================="
x.shutdown()

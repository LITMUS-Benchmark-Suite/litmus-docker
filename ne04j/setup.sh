if which unzip >/dev/null; then
    echo "unzip exists. Continuing with the procedure"
else
    echo "Installing unzip"
    sudo apt-get install unzip
fi

if [ ! -d ../gremlin-groovy ]; then
	wget "http://www.tinkerpop.com/downloads/gremlin/gremlin-groovy-2.2.0.zip"
	unzip gremlin-groovy-2.2.0.zip
	mv gremlin-groovy-2.2.0 ../gremlin-groovy
fi


.PHONY: build deploy clean

build:
	rm -rf build
	python build.py

deploy: build
	ssh homeserver 'rm -rf /home/ruben/kotlinbyexample.temp'
	rsync -a build/ homeserver:/home/ruben/kotlinbyexample.temp
	ssh homeserver 'mkdir -p /home/ruben/kotlinbyexample && atomic-exchange /home/ruben/kotlinbyexample /home/ruben/kotlinbyexample.temp && rm -rf /home/ruben/kotlinbyexample.temp'

clean:
	rm -rf build

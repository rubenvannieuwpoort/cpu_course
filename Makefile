.PHONY: build deploy clean

build:
	rm -rf build
	python build.py

deploy: build
	ssh homeserver 'rm -rf /home/ruben/cpucourse.temp'
	rsync -a build/ homeserver:/home/ruben/cpucourse.temp
	ssh homeserver 'mkdir -p /home/ruben/cpucourse && atomic-exchange /home/ruben/cpucourse /home/ruben/cpucourse.temp && rm -rf /home/ruben/cpucourse.temp'

clean:
	rm -rf build

from shutit_module import ShutItModule

class shutit_funker(ShutItModule):

	def build(self, shutit):
		shutit.login('vagrant ssh swarm1')
		shutit.login('sudo su -')
		shutit send('mkdir -p funker_example')
		shutit.send('cd funker_example')
		shutit.send_file('handler.js','''
var funker = require('funker');

funker.handler(function(args, callback) {
  callback(args.x + args.y);
});''')
		shutit.send_file('package.json','''{
  "name": "app",
  "version": "0.0.1",
  "scripts": {
    "start": "node handler.js"
  },
  "dependencies": {
    "funker": "^0.0.1"
  }
}''')
		shutit.send_file('Dockerfile','''FROM node:7-onbuild''')
		shutit.send('docker build -t funker-add .')
		shutit.send('docker network create --attachable -d overlay funker')
		shutit.send('docker service create --name add --network funker add')
		shutit.send('docker run -it --net funker funker/python',expect='>>>')
		shutit.send('import funker',expect='>>>')
		shutit.send('funker.call("add", x=1, y=2)',expect='>>>')
		shutit.send('exit()')
		shutit.pause_point('')
		return True

def module():
		return shutit_funker(
			'git.shutit_funker.shutit_funker', 1994949609.0001,
			description='',
			maintainer='',
			delivery_methods=['bash'],
			depends=['shutit.tk.swarm.swarm']
		)

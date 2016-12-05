from shutit_module import ShutItModule

class shutit_funker(ShutItModule):

	def build(self, shutit):
		shutit.send('cd ' + shutit.cfg['tk.shutit.swarm.swarm']['vagrant_run_dir'])
		shutit.login('vagrant ssh swarm1')
		shutit.login('sudo su -')
		#shutit.begin_asciinema_session(title='Funker demo')
		shutit.send('eval $(docker-machine env swarm1)',note='Get on the leader')
		shutit.send('mkdir -p funker_example')
		shutit.send('cd funker_example')
		shutit.send_file('handler.js','''
var funker = require('funker');

funker.handler(function(args, callback) {
  callback(args.x + args.y);
});''',note='Create the nodejs handling function, which in this case adds the two passed-in numbers together.')
		shutit.send_file('package.json','''{
  "name": "app",
  "version": "0.0.1",
  "scripts": {
    "start": "node handler.js"
  },
  "dependencies": {
    "funker": "^0.0.1"
  }
}''',note='Create the file that allows us to package up the node app.')
		shutit.send_file('Dockerfile','''FROM node:7-onbuild''')
		shutit.send('docker build -t add .',note='Build the docker image that runs the function, and call it "add"')
		shutit.send('docker network create --attachable -d overlay funker',note='Create the "funker" network')
		shutit.send('docker service create --name add --network funker add',note='Create the add service, which runs in the funker network.')
		shutit.pause_point('docker run -it --net funker funker/python')
		#shutit.send('docker run -it --net funker funker/python',expect='>>>',note='Run up a python funker client')
		shutit.send('import funker',expect='>>>',note='Import the funker package')
		shutit.send('funker.call("add", x=1, y=2)',expect='>>>',note='Call the funker function with two args.')
		shutit.send('exit()')
		#shutit.end_asciinema_session()
		shutit.pause_point('')
		return True

def module():
		return shutit_funker(
			'git.shutit_funker.shutit_funker', 1994949609.0001,
			description='',
			maintainer='',
			delivery_methods=['bash'],
			depends=['tk.shutit.swarm.swarm']
		)

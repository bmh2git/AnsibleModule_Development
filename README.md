
![ansible image](https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.socallinuxexpo.org%2Fscale12x-supporting%2Fdefault%2Ffiles%2Flogos%2FAnsibleLogo_transparent_web.png&f=1 =10x10)
# A Short Guide To Developing Ansible Modules

## Setting up a sandbox
This KB includes a Vagrant file to start up a simple Ubuntu system.  The commands in
this KB will execute against this sandbox system.
To start up your sandbox simply execute:

	>cd $KB_HOME\systems
	>vagrant up

You should see output similar to the following:

	Bringing machine 'ansible_sys' up with 'virtualbox' provider...
	==> ansible_sys: Importing base box 'ubuntu/trusty64'...
	==> ansible_sys: Matching MAC address for NAT networking...
	==> ansible_sys: Checking if box 'ubuntu/trusty64' is up to date...
	==> ansible_sys: A newer version of the box 'ubuntu/trusty64' is available! You currently
	==> ansible_sys: have version '14.04'. The latest is version '20150821.0.1'. Run
	==> ansible_sys: `vagrant box update` to update.
	==> ansible_sys: Setting the name of the VM: Systems_ansible_sys_1441052760404_69890
	==> ansible_sys: Clearing any previously set forwarded ports...
	==> ansible_sys: Clearing any previously set network interfaces...
	==> ansible_sys: Preparing network interfaces based on configuration...
	    ansible_sys: Adapter 1: nat
	==> ansible_sys: Forwarding ports...
	    ansible_sys: 22 => 2222 (adapter 1)
	==> ansible_sys: Booting VM...
	. . .
	ansible_sys: VirtualBox Version: 5.0
	==> ansible_sys: Mounting shared folders...
	ansible_sys: /vagrant => /Users/hashbang/workspace/ws-misc/AnsibleModules/KB/Systems

Now with our Sandbox system up and running let's get started with our module development.

# Ansible Shell and Script Module
## Direct Command
The simplest way to execute a custom command against your inventory of systems is to
simply pass it as a parameter to the `script` module:

`ansible all -i ./hosts -m shell -a 'cat /var/log/dpkg.log'`


	. . .
	2015-06-03 21:28:26 status half-installed ruby-highline:all 1.6.20-1
	2015-06-03 21:28:26 status unpacked ruby-highline:all 1.6.20-1
	2015-06-03 21:28:26 status unpacked ruby-highline:all 1.6.20-1
	2015-06-03 21:28:27 install ruby-mixlib-authentication:all <none> 1.3.0-1
	2015-06-03 21:28:27 status half-installed ruby-mixlib-authentication:all 1.3.0-1
	. . .


## Direct Script
We can take things to the next level by capturing our commands into a shell script and then referencing that shell script directly.  
First let's get into the correct location in our KB workspace:

	>cd $KB_HOME\ReadyBake\script-module\Playbook

Once inside the script-module directory let's first take a look at what we are going to invoke.  

	#!/bin/sh
	if [ -f /var/log/dpkg.log ]
	then
	        cat /var/log/dpkg.log
	else
	        echo "No patching log file found."
	fi

As you can see it's just a beefed up rendition of our earlier command.
Let's run it now and see what we get:

	>cd $KB_HOME/ReadyBake/script-module/Playbook
	>ansible all -i ../hosts -m script -a 'scripts/fetch_patch_info.sh'

Our output . . .

	. . .
	2015-06-03 21:30:02 status unpacked puppet:all 3.4.3-1ubuntu1.1\r\n2015-06-03 21:30:02 status half-configured puppet:all 3.4.3-1ubuntu1.1\r\n2015-06-03 21:30:02 status triggers-awaited puppet:all 3.4.3-1ubuntu1.1\r\n2015-06-03 21:30:02 trigproc libc-bin:amd64 2.19-0ubuntu6.6 <none>\r\n2015-06-03 21:30:02 status half-configured libc-bin:amd64 2.19-0ubuntu6.6\r\n2015-06-03 21:30:02 status installed libc-bin:amd64 2.19-0ubuntu6.6\r\n2015-06-03 21:30:02 trigproc ureadahead:amd64 0.100.0-16 <none>\r\n2015-06-03 21:30:02 status half-configured ureadahead:amd64 0.100.0-16\r\n2015-06-03 21:30:02 status installed puppet:all 3.4.3-1ubuntu1.1\r\n2015-06-03 21:30:02 status installed chef:all 11.8.2-2\r\n2015-06-03 21:30:02 status installed ureadahead:amd64 0.100.0-16\r\n2015-06-03 21:30:04 startup packages purge\r\n2015-06-03 21:30:04 status installed grub-legacy-ec2:all 0.7.5-0ubuntu1.5\r\n2015-06-03
	. . .

That's a lot of output and it's rather difficult to process so let's work
on that next.
But before we go any further with the script it self let us move our work
into an ansible playbook.  Moving our work into a playbook gives us a more
powerful platform for developing, testing, and executing our work.

## Move work to a Playbook
Moving our work into a playbook is a rather direct transcription of our
earlier command into a yaml format:

	---
	- hosts: all
	  gather_facts: false
	  tasks:
	    - name: execute patch retrieval
	      script: scripts/fetch_patch_info.sh

We can validate our transcription by having ansible check our syntax:

`ansible-playbook -i ../hosts playbook-script.yml --syntax-check`

Ansible will report any playbook syntax errors to you.

Once we have our playbook in good sorts we will then execute it:

`ansible-playbook -i ../hosts playbook-script.yml`

**Hey!!! Where is my output!!**

Well, it's there we just didn't ask for it back.  So let us enhance our playbook
so we can get this info back to our screen.  We will do this by adding a 'register'
task to our existing task.
Our playbook will now read like:

	---
	- hosts: all
	  gather_facts: false
	  tasks:
	    - name: execute patch retrieval
	      script: scripts/fetch_patch_info.sh
				register: fpi
			- debug: var=fpi.stdout_lines

Let's run our changes . . .
	
	. . .
	"2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5",
	"2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5",
	"2015-04-06 20:52:55 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5",
	"2015-04-06 20:52:55 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5",
	"2015-04-06 20:52:55 status not-installed grub-legacy-ec2:all <none>"
				]
			}
		}
	}
	
	PLAY RECAP ********************************************************************
	127.0.0.1                  : ok=2    changed=1    unreachable=0    failed=0

This is much better and almost consumable at this point.
But now let's make our script a first class action by making it a module.

# Ansible Module development
## Set up for some testing
- `git clone https://github.com/ansible/ansible.git`
- Set your PYTHONPATH to the `ansible/lib` directory.
- Execute the test-module command hacking/test-module -m .../path/to/your/module/fetch_patch_info.py


#### Note: SSHPASS on Mac
- download the sshpass util from sourceforge: http://sourceforge.net/projects/sshpass/
- untar the packages: tar xvf sshpass-1.05.tar
- move in to build: cd sshpass-1.05
- configure: ./configure
- build: make
- install: sudo make install

We will continue to use our Sandbox system we set up earlier in this KB.

## Module development
Take a look at the module that has been implemented to deliver the same functionality as the shell command and the shell script from ealier.  The module can be found in:

	>$KB_HOME/standard-module/Playbook/library/fetch_patch_info.py
	
  Bascially it's just a python program that will open the dpkg.log file and return it's contents.  
  
Some key elements of the module implementation are:

- The script does the import of the Ansible dependencies at the bottom of the program so as not to through off the line number reference which we might get in an error message:
	
		from ansible.module_utils.basic import *
		if __name__ == "__main__":
	    	main()

- We leverage the AnsibleModule utility class.  This utility is provided by Ansible and all modules must use it if they are to be considered for adoption into Ansible Extras or Core:
	
		module = AnsibleModule(
	        argument_spec = dict(filter=dict(required=False)),
	        supports_check_mode=True
	        )

- All responses from the module must be json.  We can easily accomplish this by leveraging the helper methods found on the AnsibleModule class:
	
	  	(ret, data) = fetch_patch_info()
		if ret:
				module.exit_json(msg=module.jsonify(data),changed=False)
		else:
				module.fail_json(msg="Failed")


Once our module is complete we will save it in a local `library` subdirectory as `fetch_patch_info.py`.  There are many conventional locations to store your modules and many conventions to define a reference to them.  The easiest for our exercise here is to simply create a local `library` directory.  Ansible will see this directory and add it to the module-path it already knows about.

## Testing our module
Ansible provides a testing tool that will help us determine if we any issues with our implementation.  The testing tool helps to exercise the AnsibleModule utility that we are expected to use in our Modules.

First thing we need to do is to download the Ansible project from github: `git clone https://github.com/ansible/ansible.git`
This will create an ansible directory which in turn contains a hacking directory which has the tools we are interested in using.

In particular we are interested in using the `test-module` tool to test our fetch\_patch\_info module.
But before we can use the tool we will need to update our PYTHONPATH with the a reference to the ansbile/lib directory of the project we just cloned.
For example:

	export PYTHONPATH='/path/to/clone/ansible/lib:$PYTHONPATH'


We are going to execute our test at the parent level of the ansible project we just cloned and below is the syntax to execute a test:

	./ansible/hacking/test-module -m /path/to/our-project/Playbook/library/fetch_path_info.py
	
	
## Writing our playbook
Now that we have our module written we need to define our playbook.  The playbook should be defined at the same level as the library directory.  
Here is our playbook:

    ---
    - hosts: all
      gather_facts: false
      tasks:
        - name: execute patch retrieval
          fetch_patch_info:
          register: fpi
        - name: report
          debug: var=fpi

Note that even though we don't have any parameters to pass to our module we must end our reference to the module with a colon: `fetch_patch_info:`

## Running our Playbook
Now that we have done the following:

- Implemented our shellscript as an Ansbile module in Python.
- Validated our module with test-module
- Implemented a Playbook.

We are ready to run the module against our sandbox:

`ansible-playbook -i ../hosts playbook-module.yml`

and our output is:

	. . .
	"2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5",
	"2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5",
	"2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5",
	"2015-04-06 20:52:55 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5",
	"2015-04-06 20:52:55 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5",
	"2015-04-06 20:52:55 status not-installed grub-legacy-ec2:all <none>"
				]
			}
		}
	}

	PLAY RECAP 	********************************************************************
	127.0.0.1                  : ok=2    changed=1    unreachable=0    failed=0

## Making Modules Work Together
Up to this point this point we have taken our simple command line action, made it into a script, which we then refactored into a Module.  So now let's get some value (relative to this KB and not so much to a business :) ) from our new module by using it to report the current patch levels of all the systems in our inventory.  We already have a module that will fetch patch information from Ubuntu systems so now we just need to send that data to our audit/tracking system.
The contents of this KB contain a rest-service which will function as our audit system.  We will need to develop an additional module that will receive the output from our fetch\_patch\_info module and pass it along to our audit system.

First let's look at how our playbook will change:

	---
	- hosts: all
	  gather_facts: true
	  tasks:
	    - name: execute patch retrieval
	      fetch_patch_info:
	      register: fpi
	    - name: report
	      debug: var=fpi
	    - name: audit patch levels
	      delegate_to: 127.0.0.1
	      audit_patch_info:
	        data: "{{ fpi.msg }}"
	        host: "{{ ansible_hostname }}"

We changed a few things from earlier.  First off, we are now setting our `gather_facts` to *true*.  This will have the executing playbook pick up additional information that we will need to reference in our tasks - such as the hostname of the system each task is working on.  Next, you can see that we are taking advantage of `delegate_to` so that all of the rest calls made by the audit module will be executed from our ansible-host system and not the various nodes in our inventory.

Let's have a quick look at our audit module:

	#!/usr/bin/python

	import requests
	
	def audit_patch_info( module ):
	    _host = module.params.get('host')
	    _data = module.params.get('data')
	    split_data = _data.split('\\n')
	    for d in split_data:
	        res = requests.request('POST',"http://127.0.0.1:8989/audit", data=_host + " : " + d)
	    return True
	
	def main():
	    module = AnsibleModule(
	        argument_spec = dict(
	            data=dict(required=False),
	            host=dict(required=False)
	        ),
	        supports_check_mode=True
	    )
	
	    audit_patch_info( module )
	    module.exit_json(changed=False)
	
	from ansible.module_utils.basic import *
	if __name__ == "__main__":
	  main()	 
	  
Nothing should be surprising about the implemenation above.  As you can see the module will take the output from the `fetch_patch_info` module and send each patch record to our audit system with the associated host name.  Our audit system simply prints to the data to stdout but it could do something like update a database or something fantastic.

Let's run our patch auditing playbook.
First let's start up our audit service:

	cd $KB_HOME/ReadyBake/rest-module/rest-server
	python AuditService.py
	
Debugging is set to Error to help reduce noise so we aren't expecting any output yet.  So let's keep going.

Next let's run our playbook:

	cd $KB_HOME/ReadyBake/rest-module/Playbook
	ansible-playbook -i ../hosts playbook-rest.yml

As you can see, our playbook runs pretty much as it normally has up to this point:

	. . .
	 2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5\\n2015-04-06 20:52:51 purge grub-legacy-ec2:all 0.7.5-0ubuntu1.5 <none>\\n2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5\\n2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5\\n2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5\\n2015-04-06 20:52:55 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5\\n2015-04-06 20:52:55 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5\\n2015-04-06 20:52:55 status not-installed grub-legacy-ec2:all <none>\\n\""
	        }
	    }
	}
	
	TASK: [audit patch levels] **************************************************** 
	ok: [a1_sys -> 127.0.0.1]
	ok: [a2_sys -> 127.0.0.1]
	
	PLAY RECAP ******************************************************************** 
	a1_sys                     : ok=4    changed=0    unreachable=0    failed=0   
	a2_sys                     : ok=4    changed=0    unreachable=0    failed=0   
	  
But now if you take a look at the terminal window of our audit service you will see each patch reported:

	a1_sys : 2015-04-06 20:52:51 purge grub-legacy-ec2:all 0.7.5-0ubuntu1.5 <none>
	a2_sys : 2015-04-06 20:52:51 purge grub-legacy-ec2:all 0.7.5-0ubuntu1.5 <none>
	a1_sys : 2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5
	a2_sys : 2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5
	a1_sys : 2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5
	a2_sys : 2015-04-06 20:52:51 status config-files grub-legacy-ec2:all 0.7.5-0ubuntu1.5

Which is what we wanted to see!


## Making a Module Ansible ready
Ansible requires that modules align with certain conventions and standards in order to be considered for adoption into Extras/Core.
Here are a list of those items taken straight from the Ansible web site:

* The shebang should always be #!/usr/bin/python, this allows ansible_python_interpreter to work
* Documentation: Make sure it exists
	* required should always be present, be it true or false
	* If required is false you need to document default, even if its ‘null’
	* default is not needed for required: true
	* Remove unnecessary doc like aliases: [] or choices: []
	* The version is not a float number and value the current development version
	* The verify that arguments in doc and module spec dict are identical
	* For password / secret arguments no_log=True should be set
	* Requirements should be documented, using the requirements=[] field
	* Author should be set, name and github id at least
	* Made use of U() for urls, C() for files and options, I() for params, M() for modules?
	* GPL 3 License header
	* Does module use check_mode? Could it be modified to use it? Document it
	* Examples: make sure they are reproducible
	* Return: document the return structure of the module
* Exceptions: The module must handle them. (exceptions are bugs)
	* Give out useful messages on what you were doing and you can add the exception message to that.
	* Avoid catchall exceptions, they are not very useful unless the underlying API gives very good error messages pertaining the attempted action.
* The module must not use sys.exit() –> use fail_json() from the module object
* Import custom packages in try/except and handled with fail_json() in main() e.g.:

		try:
		  import foo
		  HAS_LIB=True
		except:
		   HAS_LIB=False
	    
* The return structure should be consistent, even if NA/None are used for keys normally returned under other options.
* Are module actions idempotent? If not document in the descriptions or the notes
* Import module snippets from ansible.module_utils.basic import * at the bottom, conserves line numbers for debugging.
* Call your main() from a conditional so that it would be possible to test them in the future example:

		 if __name__ == '__main__':
			main()
    
* Try to normalize parameters with other modules, you can have aliases for when user is more familiar with underlying API name for the option
* Being pep8 compliant is nice, but not a requirement. Specifically, the 80 column limit now hinders readability more that it improves it
* Avoid ‘action/command‘, they are imperative and not declarative, there are other ways to express the same thing
* Sometimes you want to split the module, specially if you are adding a list/info state, you want a _facts version
* If you are asking ‘how can I have a module execute other modules’ ... you want to write a role
* Return values must be able to be serialized as json via the python stdlib json library. basic python types (strings, int, dicts, lists, etc) are serializable. A common pitfall is to try returning an object via exit_json(). Instead, convert the fields you need from the object into the fields of a dictionary and return the dictionary.
* Do not use urllib2 to handle urls. urllib2 does not natively verify TLS certificates and so is insecure for https. Instead, use either fetch_url or open_url from ansible.module_utils.urls.

### Windows modules checklist
* Favour native powershell and .net ways of doing things over calls to COM libraries or calls to native executables which may or may not be present in all versions of windows
* modules are in powershell (.ps1 files) but the docs reside in same name python file (.py)
* look at ansible/lib/ansible/module_utils/powershell.ps1 for commmon code, avoid duplication
* start with:

		#!powershell
	then::
	
		<GPL header>

	then::
	
		# WANT_JSON # POWERSHELL_COMMON
* Arguments:
	* Try and use state present and state absent like other modules
	* You need to check that all your mandatory args are present:

			If ($params.state) {
    			$state = $params.state.ToString().ToLower()
    			If (($state -ne 'started') -and ($state -ne 'stopped') -and ($state -ne 'restarted')) {
        			Fail-Json $result "state is '$state'; must be 'started', 'stopped', or 'restarted'"
    			}
			}
	* Look at existing modules for more examples of argument checking.

* Results
	* The result object should allways contain an attribute called changed set to either $true or $false
	* Create your result object like this:

			$result = New-Object psobject @{
				changed = $false
				other_result_attribute = $some_value
			};

			If all is well, exit with a
			Exit-Json $result

	* Ensure anything you return, including errors can be converted to json.
	* Be aware that because exception messages could contain almost anything.
	* ConvertTo-Json will fail if it encounters a trailing in a string.
	* If all is not well use Fail-Json to exit.
* Have you tested for powershell 3.0 and 4.0 compliance?

Take a look at our `fetch_patch_info` module in the `$KB_HOME/ReadyBake/ansible-module` directory so see how our implementation would change in order to align with the above bullet items.

### Conventions/Recommendations
* If the module is addressing an object, the parameter for that object should be called ‘name’ whenever possible, or accept ‘name’ as an alias.
* If you have a company module that returns facts specific to your installations, a good name for this module is site_facts.
* Modules accepting boolean status should generally accept ‘yes’, ‘no’, ‘true’, ‘false’, or anything else a user may likely throw at them. The AnsibleModule common code supports this with “choices=BOOLEANS” and a module.boolean(value) casting function.
* Include a minimum of dependencies if possible. If there are dependencies, document them at the top of the module file, and have the module raise JSON error messages when the import fails.
* Modules must be self-contained in one file to be auto-transferred by ansible.
* If packaging modules in an RPM, they only need to be installed on the control machine and should be dropped into /usr/share/ansible. This is entirely optional and up to you.
* Modules must output valid JSON only. The toplevel return type must be a hash (dictionary) although they can be nested. Lists or simple scalar values are not supported, though they can be trivially contained inside a dictionary.
* In the event of failure, a key of ‘failed’ should be included, along with a string explanation in ‘msg’. Modules that raise tracebacks (stacktraces) are generally considered ‘poor’ modules, though Ansible can deal with these returns and will automatically convert anything unparseable into a failed result. If you are using the AnsibleModule common Python code, the ‘failed’ element will be included for you automatically when you call ‘fail_json’.
* Return codes from modules are actually not significant, but continue on with 0=success and non-zero=failure for reasons of future proofing.
* As results from many hosts will be aggregated at once, modules should return only relevant output. Returning the entire contents of a log file is generally bad form.

## Submitting a Module to Ansible
Once we feel that our module is ready for the world we should consider submitting it to Ansible for adoption.  The process to do this is as follows:

* fork the ansible git repository
* Add your module to the `extras` directory.
* Submit a pull request back to ansible.

The Ansible community will review the pull request and if no one has an issue with the module then it will eventually be adopted.

Some tips:

* If you have multiple modules to contribute back then create a pull request for each module.
* You should drum up some support for your modules.  Pull requests with higher interest are reviewed sooner.
* Be responsive and receptive to feedback from the community.


## Resources
<table>
<tr><td>http://docs.ansible.com</td></tr>
<tr><td>http://docs.ansible.com/ansible/developing_modules.html</td></tr>
</table>
## Dependencies
- Vagrant
- Ansible
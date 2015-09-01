#!/usr/bin/python
DOCUMENTATION='''
---
module: fetch_patch_info
short_description: retrieve patch info
description: This module will retrieve patch information from systems which use apt-get to install and manage system packages.
version_added: 0.0.1
author: quark
notes:
  This module will return information only from systems which use apt-get to install and manage packages.
requirements: 
  - the module expects the inventory system to use apt-get for managing system level packages.
options:
'''
EXAMPLES='''
---
- hosts: all
  gather_facts: true
  tasks:
    - name: fetch patch info
      fetch_patch_info:

---
- hosts: all
  gather_facts: true
  tasks:
    - name: fetch patch info
      action: fetch_patch_info
'''

def fetch_patch_info():
    f = None
    lines = None
    try:
        f = open('/var/log/dpkg.log')
        lines = f.read()
    except IOError as err:
        return False
    finally:
        if f != None:
            f.close()

    return True, lines

def main():
    module = AnsibleModule(
        argument_spec = dict(filter=dict(required=False)),
        supports_check_mode=True
    )

    # if check mode is indicated then we will simply return and not
    # execute anything.
    if module.check_mode:
        module.exit_json( changed=False )

    (ret, data) = fetch_patch_info()
    if ret: 
        module.exit_json(msg=module.jsonify(data),changed=False)
    else:
        module.fail_json(msg="Failed")


from ansible.module_utils.basic import *
if __name__ == "__main__":
    main()

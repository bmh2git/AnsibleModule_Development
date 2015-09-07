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

    ret = audit_patch_info( module )
    if ret:
        module.exit_json(changed=False)
    else:
        module.fail_json(msg="Failed")

from ansible.module_utils.basic import *
if __name__ == "__main__":
  main()

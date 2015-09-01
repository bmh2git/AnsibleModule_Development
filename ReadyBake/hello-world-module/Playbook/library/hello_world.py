#!/usr/bin/python


def main():
    module = AnsibleModule(
        argument_spec = dict(filter=dict(required=False)),
        supports_check_mode=True
    )

    module.exit_json(msg="Hello World", changed=False )       

from ansible.module_utils.basic import *
if __name__ == "__main__":
    main()

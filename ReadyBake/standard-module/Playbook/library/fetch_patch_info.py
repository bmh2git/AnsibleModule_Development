#!/usr/bin/python
__author__ = 'quark'


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

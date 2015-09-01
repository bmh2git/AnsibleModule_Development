#!/usr/bin/python
__author__ = 'hashbang'

from flask import Flask, request

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route("/audit",methods=['GET','POST'])
def auditAction():
    try:
        d = request.data
        print d
    except BaseException as be:
        app.logger.error( be )
        return False
    return "Audited"

if __name__ == "__main__":
    app.run(port=8989)

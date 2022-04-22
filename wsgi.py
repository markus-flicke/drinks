"""
Starter script for uWSGI to run. This is used for connecting the Python code to NGINX (server).
"""
from drinks import app

if __name__=="__main__":
    app.run()

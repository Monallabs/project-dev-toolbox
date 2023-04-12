import pytest
import os
import pytest
import os
import rpyc
import sys
import time
import logging
import justpy as jp
import ofjustpy as oj
from jpcore.justpy_app import uvicorn_server_control_center
import asyncio



module_path = os.path.dirname(os.path.realpath(__file__))
 
@pytest.fixture(scope="session", autouse=True)
def session_setup():
    server_port =  9324
    # ======== test setup; start browser + page loader service =======

    os.system(f"""
    python3 {module_path}/browser_page_loader_service.py {server_port} > browser_page_loader_service.out 2> browser_page_loader_service.err&
    """)
    time.sleep(6)

    retry_counter = 0
    while True:
        try:
            conn = rpyc.connect("localhost", server_port)
            break
        except Exception as e:
            retry_counter += 1
            pass
        if retry_counter == 6:
            print ("unable to setup test")
            sys.exit()
        
    

    # ============================== end =============================
    yield conn
    # ==================== test teardown: shutdown ===================

    
    try: 
        conn.root.stop()

    except Exception as e:
        print ("caught exception ", e)
    # ============================== end =============================
    pass


@pytest.fixture(autouse=True)
def per_test_setup():
    # launch uvicorn server
    app = oj.build_app()
    webserver_controller = uvicorn_server_control_center("localhost", 8000, app)
    asyncio.run(webserver_controller.start())
    asyncio.run(asyncio.sleep(1))

    yield app

    print ("tear down post test run")
    try:
        asyncio.run(webserver_controller.stop())
    except Exception as e:
        print ("usual exception when closing uvicorn server")
        
    asyncio.run(asyncio.sleep(10))
    #print (page_source)

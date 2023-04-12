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

import views
from py_tailwind_utils import (tstr,
                           W,
                           full,
                           jc,
                           twcc2hex,
                           bg,
                           onetonine,
                           fz,
                           get_color_instance,
                           outline,
                           offset,
                           black,
                           outline,
                           green,
                           W,
                            H,
                            screen,
                           conc_twtags,
                           hidden,
                           db,
                               invisible,
                               cc,
                               noop
                           )

# ============================ setup logs ============================
try:
    os.remove("test_selenium.log")
except:
    pass

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename="launcher.log",
                    level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)
# ================================ end ===============================
    
@pytest.fixture(scope="session", autouse=True)
def session_setup():
    server_port =  9324
    # ======== test setup; start browser + page loader service =======
    logger.info("setup everything for test")
    os.system(f"""
    python3 browser_page_loader_service.py {server_port} 2> browser_page_loader_service.err&
    """)
    time.sleep(6)

    try:
        conn = rpyc.connect("localhost", server_port)
    except Exception as e:
        print ("error in connection ", e)
        pass
    

    # ============================== end =============================
    yield conn
    # ==================== test teardown: shutdown ===================

    
    try: 
        conn.root.stop()
        logger.info("stopping service")
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
    
@pytest.mark.skip(reason="Skipping this test for now")
def test_test1(session_setup, per_test_setup):
    # define an app
    conn = session_setup 
    app = per_test_setup
    app.add_jproute("/sanity_check", views.wp_sanity_check)
    
    # use browser to load page, query, and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/sanity_check", "wp_sanity_check")

    # query the browser
    btn_text = conn.root.get_element_text("/btn1")
    assert "NOT CLICKED YET" == btn_text
    for i in range(5):
        conn.root.submit_element("/btn1")
        asyncio.run(asyncio.sleep(1))

    btn_text = conn.root.get_element_text("/btn1")
    assert f"I was clicked {i+1} times".upper() ==  btn_text

@pytest.mark.skip(reason="Skipping this test for now")
def test_components_part1(session_setup, per_test_setup):
    # Load the webpage
    conn = session_setup 
    app = per_test_setup
    app.add_jproute("/check_components_part1", views.wp_check_components_part1)
    
    # use browser to load page, query, and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/check_components_part1", "wp_check_components_part1")

    # Check if the paragraph is rendered correctly
    p_text = conn.root.get_element_text("/p")
    assert "This is a Paragraph" == p_text

    # Check if the unordered list is rendered correctly
    ul_text = conn.root.get_element_text("/ul")
    assert "Unordered List:" in ul_text

    # Check if the ordered list is rendered correctly
    # ol_text = conn.root.get_element_text("/ol")
    # assert "Ordered List:" in ol_text

    # Check if the list items are rendered correctly
    li1_text = conn.root.get_element_text("/li1")
    assert "List item 1" == li1_text

    li2_text = conn.root.get_element_text("/li2")
    assert "List item 2" == li2_text

    li3_text = conn.root.get_element_text("/li3")
    assert "List item 3" == li3_text


    
    
# def test_test2(session_setup, per_test_setup):
#     print ('run test2')
#     assert True
        
@pytest.mark.skip(reason="Skipping this test for now")    
def test_components_part2(session_setup, per_test_setup):
    # Set up the app
    conn = session_setup 
    app = per_test_setup
    app.add_jproute("/component_part2", views.wp_components_part2)
    
    # Load the webpage
    page_source = conn.root.load_page("http://127.0.0.1:8000/component_part2", "wp_component_part2")

    # Check if the components are rendered correctly
    a_text = conn.root.get_element_text("/a")
    assert "Click me!" == a_text

    label_text = conn.root.get_element_text("/label")
    assert "Enter your name:" == label_text

    circle_text = conn.root.get_element_text("/circle")
    assert "Circle Button" == circle_text

    span_text = conn.root.get_element_text("/span")
    assert "This is a span" == span_text

    # input_change_only_placeholder = conn.root.get_element_attr_value("/input_change_only", "placeholder")
    # assert "Type here" == input_change_only_placeholder

    input_placeholder = conn.root.get_element_attr_value("/input_", "placeholder")
    assert "Another input" == input_placeholder

    td_text = conn.root.get_element_text("/td")
    assert "Table cell" == td_text

    img_src = conn.root.get_element_attr_value("/img", "src")
    assert "https://via.placeholder.com/150" == img_src

    textarea_placeholder = conn.root.get_element_attr_value("/textarea", "placeholder")
    assert "Write your message here" == textarea_placeholder

@pytest.mark.skip(reason="Skipping this test for now")
def test_labeled_input(session_setup, per_test_setup):
    # define an app
    conn = session_setup
    app = per_test_setup
    app.add_jproute("/launcher", views.wp_test_labeled_input)

    # use browser to load page, query, and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/launcher", "oa")


    assert conn.root.element_exists("/my_inp_box") #stack that contains
    assert conn.root.element_exists("/my_inp_box_0") #first label box
    assert conn.root.element_exists("/my_inp_box_0_0") #span in first label box
    assert conn.root.element_exists("/my_inp_box_0_1") #input in first label box
    
    assert conn.root.element_exists("/my_inp_box_1") #first label box
    assert conn.root.element_exists("/my_inp_box_1_0") #span in first label box
    assert conn.root.element_exists("/my_inp_box_1_1") #input in first label box
    
    # Check the label text
    label_text = conn.root.get_element_text("/my_inp_box_0_0")
    assert label_text == "Enter a value"

    # Check the input placeholder
    input_placeholder = conn.root.get_element_attr_value("/my_inp_box_0_1",
                                                         "placeholder")
    assert input_placeholder == "a dummy value"
    label_text = conn.root.get_element_text("/my_inp_box_1_0")
    assert label_text == "Enter a value"

    # Check the input placeholder
    input_placeholder = conn.root.get_element_attr_value("/my_inp_box_1_1",
                                                         "placeholder"
                                                         )
    assert input_placeholder == "dummy value"

    input_text = "New text"
    conn.root.set_element_text("/my_inp_box_1_1",  input_text)
    # doing submit on body element doesn't work
    conn.root.submit_element("/my_inp_box_0_1") 

    # Check if the component on the server side is updated
    wp = views.global_webpage
    inputbox = wp.session_manager.stubStore.my_inp_box_1_1
    updated_value = inputbox.target.value
    assert updated_value == input_text


    # Additional checks can be added for event handling, input change, etc.

@pytest.mark.skip(reason="Skipping this test for now")    
def test_labeled_checkbox_view(session_setup, per_test_setup):
    # define an app
    conn = session_setup
    app = per_test_setup
    app.add_jproute("/labeled_checkbox_view", views.labeled_checkbox_view)

    # use browser to load page, query, and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/labeled_checkbox_view", "oa")

    # Check the label text
    label_text = conn.root.get_element_text("/cbox_0")
    assert label_text == "Got Milk?"

    # Check the checkbox state
    checkbox_checked = conn.root.is_selected("/cbox_1")
    assert checkbox_checked == True

    conn.root.submit_element("/cbox_1")
    checkbox_checked = conn.root.is_selected("/cbox_1")
    assert checkbox_checked == False
    
    
    # Additional checks can be added for event handling, state change, etc.


    

# def test_checkbox_input_view(session_setup, per_test_setup):
#     # define an app
#     conn = session_setup
#     app = per_test_setup
#     app.add_jproute("/checkbox_input_view", views.checkbox_input_view)

#     # use browser to load page, query, and perform checks
#     page_source = conn.root.load_page("http://127.0.0.1:8000/checkbox_input_view", "oa")

#     # Check if the CheckboxInput component is rendered
#     checkbox_input_element = conn.root.get_element("/___myci")
#     assert checkbox_input_element is not None

#     # Check the checkbox state
#     checkbox_checked = conn.root.get_element_property("/___myci/cbox", "checked")
#     assert checkbox_checked == False

#     # Check the input placeholder text
#     placeholder_text = conn.root.get_element_property("/___myci/ibox", "placeholder")
#     assert placeholder_text == "Enter text"

#     # Additional checks can be added for event handling, state change, etc.

# TODO: Fold the global webpage test with labeled input
# @pytest.mark.skip(reason="unable to test inputchangeonly; see demo_via_selenium")
# def test_checkbox_input_view(session_setup, per_test_setup):
#     # Define an app
#     conn = session_setup
#     app = per_test_setup
#     app.add_jproute("/checkbox_input_view", views.checkbox_input_view)

#     # Use browser to load page, query, and perform checks
#     page_source = conn.root.load_page("http://127.0.0.1:8000/checkbox_input_view", "oa")


#     # Check the input placeholder text
#     placeholder_text = conn.root.get_element_attr_value("/___myci/ibox", "placeholder")
#     assert placeholder_text == "Enter text"

#     # Edit the input field
#     input_text = "New text"
#     conn.root.set_element_text("/___myci/ibox",  input_text)
#     conn.root.submit_element("body")

#     # Check if the component on the server side is updated
#     wp = views.global_webpage
#     inputbox = wp.session_manager.stubStore.myci.inputbox
#     updated_value = inputbox.target.value
#     assert updated_value == input_text

#     # Additional checks can be added for event handling, state change, etc.


@pytest.mark.skip(reason="increamentally building test")
def test_subheading_banner_view(session_setup, per_test_setup):
    conn = session_setup
    app = per_test_setup
    app.add_jproute("/subheading_banner_view", views.subheading_banner_view)

    # Use browser to load page, query, and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/subheading_banner_view", "subheading_page")


    # Check the heading text
    heading_text = conn.root.get_element_text("/___myshb/headingL")
    assert heading_text == "Sample Subheading"
    



#@pytest.mark.skip(reason="increamentally building test")
def test_subsubsection_view(session_setup, per_test_setup):
    # define an app
    conn = session_setup
    app = per_test_setup
    app.add_jproute("/subsubsection_view", views.subsubsection_view)

    # use browser to load page, query, and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/subsubsection_view", "oa")
    # Check the heading text
    heading_text = conn.root.get_element_attr_value("/___heading_sss/headingL", "textContent")
    # don't know from where but getting white spaces
    assert heading_text.rstrip() == "Sample Subsubsection"


#@pytest.mark.skip(reason="increamentally building test")    
def test_prose_view(session_setup, per_test_setup):
    # define an app
    conn = session_setup
    app = per_test_setup
    app.add_jproute("/prose_view", views.prose_view)

    # use browser to load page, query, and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/prose_view", "oa")

    # Check if the Prose component is rendered
    prose_element_id = "/my_prose"
    assert conn.root.element_exists(prose_element_id)

    # Check the prose text
    prose_text = conn.root.get_element_text(prose_element_id)
    assert prose_text == "Sample text for prose"

    # Check the class attribute of the prose element
    prose_element_class = conn.root.get_element_attr_value(prose_element_id, "class")

    # Get the server-side class value
    server_prose_element = views.global_webpage.session_manager.stubStore.my_prose

    # Compare the client-side and server-side class values
    assert prose_element_class == server_prose_element.target.classes

    # Additional checks can be added for event handling, state change, etc.



#@pytest.mark.skip(reason="increamentally building test")    
def test_key_value_view(session_setup, per_test_setup):
    # define an app
    conn = session_setup
    app = per_test_setup
    app.add_jproute("/key_value_view", views.key_value_view)

    # use browser to load page, query, and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/key_value_view", "oa")

    # Check if the KeyValue component is rendered
    key_value_element_id = "/my_kv"
    assert conn.root.element_exists(key_value_element_id)

    # Check the key and value text
    key_text = conn.root.get_element_text("/___my_kv/keyt")
    assert key_text == "Key"

    value_text = conn.root.get_element_text("/___my_kv/valuet")
    assert value_text == "Value"

    # Check the classes for key, equals, and value elements
    key_element_classes = conn.root.get_element_attr_value("/___my_kv/keyt", "class")
    eq_element_classes = conn.root.get_element_attr_value("/___my_kv/eqt", "class")
    value_element_classes = conn.root.get_element_attr_value("/___my_kv/valuet", "class")

    # Get the server-side elements from the global_webpage
    server_key_element = views.global_webpage.session_manager.stubStore.___my_kv.keyt
    server_eq_element = views.global_webpage.session_manager.stubStore.___my_kv.eqt
    server_value_element = views.global_webpage.session_manager.stubStore.___my_kv.valuet

    # Compare the classes
    assert key_element_classes == server_key_element.target.classes
    assert eq_element_classes == server_eq_element.target.classes
    assert value_element_classes == server_value_element.target.classes

    # Additional checks can be added for event handling, state change, etc.

    
#@pytest.mark.skip(reason="increamentally building test")    
def test_subtitle_title_view(session_setup, per_test_setup):
    # define an app
    conn = session_setup
    app = per_test_setup
    app.add_jproute("/subtitle_title_view", views.subtitle_title_view)

    # use browser to load page, query, and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/subtitle_title_view", "oa")

    # Check if the SubTitle and Title components are rendered
    subtitle_element_id = "/my_subtitle"
    title_element_id = "/my_title"

    assert conn.root.element_exists(subtitle_element_id)
    assert conn.root.element_exists(title_element_id)

    # Check the subtitle and title text
    subtitle_text = conn.root.get_element_text(subtitle_element_id)
    title_text = conn.root.get_element_text(title_element_id)

    assert subtitle_text == "Subtitle Example"
    assert title_text == "Title Example"

    # Additional checks can be added for event handling, state change, etc.

#@pytest.mark.skip(reason="increamentally building test")        
def test_slider_view(session_setup, per_test_setup):
    # define an app
    conn = session_setup
    app = per_test_setup
    app.add_jproute("/slider_view", views.slider_view)

    # load the page and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/slider_view", "oa")

    # Check if the Slider component is rendered
    slider_element_id = "/my_slider"
    assert conn.root.element_exists(slider_element_id)

    # Check the server-side Slider component
    server_slider_element = views.global_webpage.session_manager.stubStore.my_slider
    assert server_slider_element is not None

    # Simulate clicks on the circles and check server component class
    for i in range(1, 6):
        circle_element_id = f"/___my_slider/c{i}"
        assert conn.root.element_exists(circle_element_id)

        # Simulate the click on the circle element
        conn.root.submit_element(circle_element_id)

        # Wait for a moment to let the server-side code process the click event
        time.sleep(0.5)

        # Check if the server component class matches with that on the browser side
        browser_circle_class = conn.root.get_element_attr_value(circle_element_id, "class")
        server_circle_class = views.global_webpage.session_manager.stubStore.___my_slider[f"c{i}"].target.classes
        assert browser_circle_class == server_circle_class
    


# In test_views.py
#@pytest.mark.skip(reason="increamentally building test")        
def test_color_selector_view(session_setup, per_test_setup):
    # define an app
    conn = session_setup
    app = per_test_setup
    app.add_jproute("/color_selector_view", views.color_selector_view)

    # load the page and perform checks
    page_source = conn.root.load_page("http://127.0.0.1:8000/color_selector_view", "oa")

    # Check if the ColorSelector component is rendered
    color_selector_element_id = "/my_color_selector"
    assert conn.root.element_exists(color_selector_element_id)

    # Check the server-side ColorSelector component
    server_color_selector = views.global_webpage.session_manager.stubStore.my_color_selector.target
    assert server_color_selector is not None

    # Simulate clicks on the mainColorSelector options and the slider circles
    for main_color in twcc2hex.keys():
        main_color_option_element_id = f"/___my_color_selector/opt_{main_color}"
        assert conn.root.element_exists(main_color_option_element_id)

        # Simulate the click on the mainColorSelector option element
        conn.root.submit_element(main_color_option_element_id)

        # Wait for a moment to let the server-side code process the click event
        time.sleep(0.5)

        for i in range(1, 10):
            circle_element_id = f"/___my_color_selector/___shades/c{i}"
            assert conn.root.element_exists(circle_element_id)

            # Simulate the click on the slider circle element
            conn.root.submit_element(circle_element_id)

            # Wait for a moment to let the server-side code process the click event
            time.sleep(0.5)

            # Check if the server-side component's main color and slider value match the clicked elements
            assert server_color_selector.maincolor_value == main_color
            assert server_color_selector.slider_value == i

            # Check if the selected color value is correct
            selected_color_value = twcc2hex[main_color][onetonine[i]]
            assert views.selected_color_value == selected_color_value

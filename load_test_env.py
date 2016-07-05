def get_driver():
    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    profile = FirefoxProfile()
    profile.add_extension('C:/zz_EFG/GitHub/testscript/executables/firebug-2.0.16-fx.xpi')
    d = webdriver.Firefox(firefox_profile=profile)
    d.implicitly_wait(30)
    return d


def igo(d):
    from selenium.webdriver.support.wait import WebDriverWait
    d.get('http://pipepasstoigo-qd3.ipipeline.com/default.aspx?gaid=5752')
    if d.current_url.find("/CossEnterpriseSuite/") == -1:
        elem = d.find_element_by_name("user")
        elem.clear()
        elem.send_keys('tombqd5')

        elem = d.find_element_by_name("password")
        elem.clear()
        elem.send_keys('password1')

        elem = d.find_element_by_name("Submit")
        elem.click()

        WebDriverWait(d,30).until(lambda x: x.find_element_by_id("mycases-button"))

    if d.find_elements_by_id('mycases-button'):
        d.find_element_by_id('mycases-button').click()

    elif d.find_elements_by_id('spanMyCases'):
        d.find_element_by_id('spanMyCases').click()

    WebDriverWait(d, 30).until(lambda x: x.find_element_by_id("btnNewCase"))

#http://pipepasstoigo-qd3.ipipeline.com/default.aspx?gaid=5752
#d.switch_to_frame('CossScreenFrame')

from behave import *

@when('we go to the homepage')
def go_to_homepage(context):
    context.browser.get('http://localhost/')

@then('we will see the homepage text')
def see_homepage_text(context):
    homepage_text = 'Enter a URL to check its SSL.'
    page_text = context.browser.find_element_by_tag_name('body').text
    assert homepage_text in page_text

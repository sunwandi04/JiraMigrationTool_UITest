import time

import allure
from playwright.sync_api import sync_playwright
import os
import pytest
import yaml


# 加载读取配置文件config.yaml
@pytest.fixture(scope="session")
def env(request):
    config_path = os.path.join(request.config.rootdir, "config.yaml")
    with open(config_path) as f:
        env_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    return env_config


@pytest.fixture(scope='session')
def page(env):
    with sync_playwright() as play:
        if os.getenv('DOCKER_RUN') or os.getenv('GITHUB_RUN'):
            browser = play.chromium.launch(headless=True, args=['--no-sandbox'])
        else:
            browser = play.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(env['migration_tool_url'])
        global PAGE
        PAGE = page
        yield page
        context.close()
        browser.close()


PAGE = None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport():
    outcome = yield
    test_result = outcome.get_result()

    if test_result.when in ["setup", "call"]:
        xfail = hasattr(test_result, 'wasxfail')
        if test_result.failed or (test_result.skipped and xfail):
            global PAGE
            if PAGE:
                allure.attach(PAGE.screenshot(), name='screenshot', attachment_type=allure.attachment_type.PNG)
                allure.attach(PAGE.content(), name='html_source', attachment_type=allure.attachment_type.HTML)
                PAGE.reload()
                time.sleep(0.5)

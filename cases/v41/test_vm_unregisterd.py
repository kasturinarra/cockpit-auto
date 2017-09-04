from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.v41.vm_page import VirtualMachinesPage
from fabric.api import run, env, settings
from cases import CONF
import const
from utils.helpers import get_cur_func
import logging

log = logging.getLogger("sherry")

dict1 = dict(zip(const.vm, const.vm_id))

host_ip, host_user, host_password, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('browser')

env.host_string = host_user + '@' + host_ip
env.password = host_password


def init_browser():
    if browser == 'firefox':
        driver = webdriver.Firefox()
        driver.implicitly_wait(20)
        driver.root_uri = "https://{}:9090".format(host_ip)
        return driver
    elif browser == 'chrome':
        driver = webdriver.Chrome()
        driver.implicitly_wait(20)
        driver.root_uri = "https://{}:9090".format(host_ip)
        return driver
        #return None
    else:
        raise NotImplementedError

def test_login(ctx):
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def check_running_vms_unregister_func(ctx):
    """
    RHEVM-18803
        Check running VMs (Unregister to RHEVM) status in virtual machines page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Check running VMs (Unregister to RHEVM) status in virtual machines page...")
        virtual_machines_page = VirtualMachinesPage(ctx)
        virtual_machines_page.basic_check_elements_exists()
        virtual_machines_page.check_running_vms_unregister()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def check_vms_in_cluster_unregister_func(ctx):
    """
    RHEVM-18804
        Check VMs in cluster (Unregister to RHEVM) status in virtual machines page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Check VMs in cluster (Unregister to RHEVM) status in virtual machines page...")
        virtual_machines_page = VirtualMachinesPage(ctx)
        virtual_machines_page.check_vms_in_cluster_unregister()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def runtest():
    ctx = init_browser()
    test_login(ctx)
    check_running_vms_unregister_func(ctx)
    check_vms_in_cluster_unregister_func(ctx)
    ctx.close()

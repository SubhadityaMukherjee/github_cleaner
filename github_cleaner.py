import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

# Please look at the README for more information

# ----------------------------------------------
# CHANGE THESE


"""
comma separated list of position of the organization in list_of_orgs or "D"
eg: list_of_orgs = [
    "backups", "image-process", "old-codes"
]
    1   2   3
sites = '''
algos, dsa, theylia, zeus 
'''

to_put = [
1, 3, "D", 1
]

results:
    algos will go to backups 
    dsa will go to old-codes
    theylia will be deleted
    zeus will go to backups 
"""

browser = "chrome"  # or firefox
user_name = ""  # github username
email = ""  # your login creds
passw = ""  # your password (please please do not push this to github)

list_of_orgs = [

]  # Enter a list of organizations you created


sites = ''' 

'''  # A comma separated list of repository names

to_put = [

]  # put D if you want to delete it or put the list index number . eg : pr-codes, nodejs-helpers

# ----------------------------------------------

# MAIN CODE

if browser.lower() == "chrome":
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    opts = Options()
    browser = Chrome(options=opts)

elif browser.lower() == "firefox":
    from selenium.webdriver import Firefox
    from selenium.webdriver.firefox.options import Options
    opts = Options()
    browser = Firefox(options=opts)


def repeat_keys(actions, key, repeat=2):
    """
    Repeats a key "repeat" number of times
    """
    for _ in range(repeat):
        actions.send_keys(key)


def chain_actions(actions, list_of):
    """
    Executes a chain of actions passed in a list sequentially
    """
    for i in list_of:
        actions.send_keys(i)
    actions.perform()


sites = sites.replace(" ", "")  # Just make sure it works
assert len(sites.split(",")) == len(to_put)

#
actions = ActionChains(browser)

# LOGIN
browser.get('https://github.com/login')
time.sleep(1)
chain_actions(actions, [email, Keys.TAB, passw, Keys.TAB, Keys.ENTER])
time.sleep(1)

for i, site in tqdm(enumerate(sites.split(",")), total=len(sites.split(","))):
    site = f"https://github.com/{user_name}/{site}"

    repo_name = str(site).split("/")[-1].strip()

    # Go to site
    browser.get(site+"/settings")

    # Choose organization
    puts = to_put[i]
    if puts == "D":
        browser.find_element_by_xpath(
            '//*[@id="options_bucket"]/div[10]/ul/li[4]/details/summary').click()
        chain_actions(
            actions, [f"{user_name}/{repo_name}", Keys.TAB, Keys.ENTER])
    else:
        puts -=1
        browser.find_element_by_xpath(
            "/html/body/div[6]/div/main/div[2]/div/div/div[2]/div/div/div/div[10]/ul/li[2]/form/details/summary").click()
        chain_actions(actions, [list_of_orgs[puts], Keys.TAB,
                      f"{user_name}/{repo_name}", Keys.TAB, Keys.ENTER])
    time.sleep(2)

browser.close()

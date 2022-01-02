'''
This script was written by SK4V for the entire sneakers game community !!!

You have to be careful not to overdo it, Zalando could ban the ip.
You can implement proxies using selenium in the codegenerator.py

!showcommands to see the Discord bot commands

'''
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import discord
from discord.ext import commands
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



token='YOUR TOKEN'
PATH = 'CHROME DRIVER PATH'
client = commands.Bot(command_prefix='!')

proxy='' #set proxy here if you need
proxy_information=proxy.split(':')

if proxy!='':
    PROXYMODE=True
    PROXY_HOST = proxy_information[0]  # rotating proxy or host
    PROXY_PORT = proxy_information[1] # port
    PROXY_USER = proxy_information[2] # username
    PROXY_PASS = proxy_information[3] # password
    print(PROXY_HOST,PROXY_PORT,PROXY_USER,PROXY_PASS)


    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
    
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
else: PROXYMODE=False


def get_chromedriver(use_proxy=False,user_agent=None,headless=None):
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)

    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')

    if headless==True:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options, executable_path=PATH)

    return driver

def code(link_newsletter,t):

    driver = get_chromedriver(use_proxy=PROXYMODE)
    link_email = 'https://generator.email/'

    driver.get(link_email)
    email = driver.find_element_by_xpath('//*[@id="email_ch_text"]').text
    print(email)

    # open new chrome tab
    driver.execute_script("window.open('about:blank','tab2');")
    driver._switch_to.window('tab2')
    driver.get(link_newsletter)

    element = WebDriverWait(driver, t).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="uc-btn-accept-banner"]')))
    element.click()

    element = WebDriverWait(driver, t).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email-input"]')))
    element.send_keys(email)

    element = WebDriverWait(driver, t).until(EC.element_to_be_clickable((By.XPATH,
                                                                         '/html/body/div[4]/div/div/div/div/div/div/div[2]/div/div/form/div/div/div[3]/div/div[1]/div/label')))
    element.click()

    element = WebDriverWait(driver, t).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[4]/div/div/div/div/div/div/div[2]/div/div/form/div/div/div[5]/button')))
    element.click()

    # return to the first chrome tab
    driver.switch_to.window(driver.window_handles[0])

    link = 'https://generator.email/' + email
    driver.quit()
    print(link + '\n')
    return link

def fcode(link):
    driver=get_chromedriver(use_proxy=PROXYMODE,headless=True)
    driver.get(link)
    sleep(5)
    code = driver.find_element((By.XPATH,'//*[@id="email-table"]/div[2]/div[4]/div[3]/table[2]/tbody/tr/td/table/tbody/tr/td/table[7]/tbody/tr/td/table[2]/tbody/tr/td/table[4]/tbody/tr/td[1]')).text
    #element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="email-table"]/div[2]/div[4]/div[3]/table[2]/tbody/tr/td/table/tbody/tr/td/table[7]/tbody/tr/td/table[2]/tbody/tr/td/table[4]/tbody/tr/td[1]')))
    #code = element.text
    print(code)
    driver.quit()
    return code

def discordBot():
    @client.event
    async def on_ready():
        print('Bot is ready')

    @client.command()
    @commands.is_owner()
    async def ping(ctx):
        await ctx.send('Bot is online')


    @client.command()
    async def showcommands(ctx):
        mesage = ':flag_it: **!itnow [@username]** send in DM a link for your code \n' \
                 ':flag_fr: **!frnow [@username]** send in DM a link for your code \n' \
                 ':flag_nl: **!nlnow [@username]** send in DM a link for your code \n' \
                 ':flag_es: **!esnow [@username]** send in DM a link for your code \n' \
                 ':flag_be: **!benow [@username]** send in DM a link for your code \n'
        await ctx.send(mesage)


    @client.command()
    async def itnow(ctx, user: discord.Member, *, message=None):
        link_newsletter = 'https://www.zalando.it/zalando-newsletter/'
        print('eseguo codenow')
        await user.send(embed=discord.Embed(title='**YOUR CODE IS COMING**'))
        link_code = code(link_newsletter,2)
        embed=discord.Embed(title='**YOU WILL FIND YOUR CODE HERE** :flag_it:' + link_code)
        await user.send(embed=embed)
        try:
            mes = discord.Embed(title='**YOUR CODE** :flag_it:\n' + fcode(link_code))
            await user.send(embed=mes)
        except:
            mes2 = discord.Embed(title='*Ops I was unable to print the code ... you will find it by clicking the link above*')
            await user.send(embed=mes2)
            pass

    @client.command()
    async def frnow(ctx, user: discord.Member, *, message=None):
        link_newsletter = 'https://www.zalando.fr/zalando-newsletter/'
        print('eseguo codenow')
        await user.send(embed=discord.Embed(title='**YOUR CODE IS COMING**'))
        link_code = code(link_newsletter,2)
        embed = discord.Embed(title='**YOU WILL FIND YOUR CODE HERE** :flag_ifr:' + link_code)
        await user.send(embed=embed)
        try:
            mes = discord.Embed(title='**YOUR CODE** :flag_fr:\n' + fcode(link_code))
            await user.send(embed=mes)
        except:
            mes2 = discord.Embed(title='*Ops I was unable to print the code ... you will find it by clicking the link above*')
            await user.send(embed=mes2)
            pass

    @client.command()
    async def nlnow(ctx, user: discord.Member, *, message=None):
        link_newsletter = 'https://www.zalando.nl/zalando-newsletter/'
        print('eseguo codenow') #log
        await user.send(embed=discord.Embed(title='**YOUR CODE IS COMING**'))
        link_code = code(link_newsletter,2)
        embed = discord.Embed(title='**YOU WILL FIND YOUR CODE HERE** :flag_nl:' + link_code)
        await user.send(embed=embed)
        try:
            mes = discord.Embed(title='**YOUR CODE** :flag_nl:\n' + fcode(link_code))
            await user.send(embed=mes)
        except:
            mes2 = discord.Embed(title='*Ops I was unable to print the code ... you will find it by clicking the link above*')
            await user.send(embed=mes2)
            pass

    @client.command()
    async def esnow(ctx, user: discord.Member, *, message=None):
        link_newsletter = 'https://www.zalando.es/zalando-newsletter/'
        print('eseguo codenow') #log
        await user.send(embed=discord.Embed(title='**YOUR CODE IS COMING**'))
        link_code = code(link_newsletter,2)
        embed = discord.Embed(title='**YOU WILL FIND YOUR CODE HERE** :flag_es:' + link_code)
        await user.send(embed=embed)
        try:
            mes = discord.Embed(title='**YOUR CODE** :flag_es:\n' + fcode(link_code))
            await user.send(embed=mes)
        except:
            mes2 = discord.Embed(title='*Ops I was unable to print the code ... you will find it by clicking the link above*')
            await user.send(embed=mes2)
            pass


    @client.command()
    async def benow(ctx, user: discord.Member, *, message=None):
        link_newsletter = 'https://www.zalando.be/zalando-newsletter/'
        print('eseguo codenow') #log
        await user.send(embed=discord.Embed(title='**YOUR CODE IS COMING**'))
        link_code = code(link_newsletter,2)
        embed = discord.Embed(title='**YOU WILL FIND YOUR CODE HERE** :flag_be:' + link_code)
        await user.send(embed=embed)
        try:
            mes = discord.Embed(title='**YOUR CODE** :flag_be:\n' + fcode(link_code))
            await user.send(embed=mes)
        except:
            mes2 = discord.Embed(title='*Ops I was unable to print the code ... you will find it by clicking the link above*')
            await user.send(embed=mes2)
            pass

    @client.command()
    @commands.is_owner()
    async def shutdown(ctx):
        print('stopBot')
        await ctx.send('Bot shutdown')
        await ctx.bot.logout()

    client.run(token)


if __name__ == '__main__':
    discordBot()

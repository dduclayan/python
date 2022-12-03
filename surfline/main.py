# TODO: Have program check waves for west side and send a text if waves are good or excellent
# TODO: Also have program text user if waves are in user's optimal range E.g. 3-4 feet
# TODO(DONE): Also have program text if the forecast for tomorrow looks good 


# Twilio API for sms messaging
# client = Client(account_sid, auth_token)
from twilio.rest import Client
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

import bs4, requests

# Retrieve Haleiwa surfline report via requests
url = 'https://www.surfline.com/surf-report/haleiwa/5842041f4e65fad6a7708df5'
getPage = requests.get(url)
getPage.raise_for_status()

# Parses surfline html page, assigns to variable surf
surf = bs4.BeautifulSoup(getPage.text, 'html.parser')
forecast = surf.select('.sl-spot-report') # text that says if waves are good or excellent is in div class sl-spot-report

# LEGACY CODE, FOR DOCUMENTATIONAL PURPOSES ONLY
# Variables for "good" and "excellent" waves
# TODO (DONE): Need to make the script so that it matches the text exactly, not just by len of word. Reason being is because 'good' is 
# just as long as 'fair' or 'poor'. As of current state this tool is only good for finding 'excellent' days. 
# gHeight = 'good'
# eHeight = 'excellent'
# gLength = len(gHeight)
# eLength = len(eHeight)

gAvailable = False
eAvailable = False 

# LEGACY CODE, FOR DOCUMENTATIONAL PURPOSES ONLY
# for loop that iterates over text, looks for text length that matches good or excellent, if so changes available variable to True.
# for wave in forecast:
# 	for i in range(len(wave.text)):
# 		chunk = wave.text[i:i+gLength].lower()
# 		if chunk == gHeight:
# 			#gAvailable = True
# for wave in forecast:   
# 	for i in range(len(wave.text)):
# 		chunk = wave.text[i:i+eLength].lower()
# 		if chunk == eHeight:
# 			#eAvailable = True

# test code to see if I can just see if the text 'good' is present in the '.sl-spot-report'
for wave in forecast:
	if 'GOOD' in wave.text:
	    print('Waves are showing as GOOD today.')
	    gAvailable = True
	else:
		print('Waves are less than good today.')
	if 'EXCELLENT' in wave.text:
		print('Waves are showing as excellent.')
		eAvailable = True
	else:
		print('Waves are showing less than excellent.')

print('gAvailable is evaluating as: ', gAvailable)
print('eAvailable is evaluating as: ', eAvailable)


# Send SMS
# LEGACY CODE, FOR DOCUMENTATIONAL PURPOSES ONLY
# if gAvailable or eAvailable == True:
#         client.messages.create(to="+19999999999",
#                        from_="+19999999999", 
#                        body="North shore waves are good/excellent! Go out and surf/shell! \nVisit https://www.surfline.com/surf-report/haleiwa/5842041f4e65fad6a7708df5 for more info.")
#         client.messages.create(to="+19999999999",
#                        from_="+19999999999", 
#                        body="North shore waves are good! Go out and surf/shell! \nVisit https://www.surfline.com/surf-report/haleiwa/5842041f4e65fad6a7708df5 for more info.")
# else:
# 	print('Waves are junk today.')

if gAvailable == True:
	client.messages.create(to="+19999999999",
        from_="19999999999", 
        body="North shore waves are showing as GOOD! Go out and surf/shell! \nVisit https://www.surfline.com/surf-report/haleiwa/5842041f4e65fad6a7708df5 for more info.")
else:
	print('Nothing to report.')
if eAvailable == True:
	client.messages.create(to="+19999999999",
        from_="19999999999", 
        body="North shore waves are showing as EXCELLENT! Go out and surf/shell! \nVisit https://www.surfline.com/surf-report/haleiwa/5842041f4e65fad6a7708df5 for more info.")
else:
	print('Nothing to report.')


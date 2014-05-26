You need to set 3 variables inside the code:

1. MY_API_URL 	
- where do you get your calendar data?
   This should be an JSON feed from API1. Go to the site and select the 
   page of events you want. This can be all events on the site, or just 
   a single group or country or area. Click export and JSON.
   Example URL: http://opentechcalendar.co.uk/api1/events.json

2. MY_SITE_MSG  
- what do you want at the top of the message?

3. MY_GROUP_NAME  or POST_TO_ID
- What's the name of the group on Facebook (needed to find the group-id)
- Use http://lookup-id.com/ to find the ID for a group

and one environment variable:

4. FACEBOOK_ACCESS_TOKEN
- This is what grants you access for your code to post on your behalf.
- The quick'n'dirty way is to login at Facebook, and then in the same
  browser, go to https://developers.facebook.com/tools/explorer and create
  short-term token there by clicking 'get access token'.

  For this code, you need the 'user_groups' from the "User Data Permissions" 
  tab to get the group-id, and the 'publish-actions' from the "Extended 
  Permissions" tab to be able to post. (These tabs come up when you click 
  "Get Access Token")

  By default, the token only lasts an hour, but there is a way to extend it 
  to 60 days. Will see if I can programmatically recreate it.


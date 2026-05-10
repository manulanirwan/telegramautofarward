🚀 The "24/7 Telegram Forwarder" Starter Kit

Step 1: Get API Keys

Tell your friend to go to my.telegram.org, log in, and create an "App." They will get an api_id and api_hash.

Step 2: Generate the "String Session"

They must run this code once in Google Colab to get their login code.

Step 3: Setup Hugging Face (The Server)

Create a New Space on Hugging Face.

SDK: Choose Gradio.

Privacy: Set it to Private (Crucial for safety!).

Secrets: Go to Settings > Secrets and add:

API_ID

API_HASH

STRING_SESSION (The long code from Step 2).

Step 4: The Final Code (app.py)

Tell them to create a file named app.py and paste this exact code. They only need to change the channel names at the top.

Step 5: Add requirements.txt

Add one last file named requirements.txt with these two lines:

Last Step:

The 24/7 "Heartbeat" (Cron-job.org)

This step is essential. It "pings" your bot every few minutes so Hugging Face thinks someone is using it, which prevents it from ever turning off.

Copy your Space URL: * Go to your Hugging Face Space.

Look at the browser address bar. It should look like this: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

However, for the ping to work, you need the Direct URL. Click the three dots (⋮) in the top right -> Embed this Space.

Copy the "Direct URL" (it looks like https://username-spacename.hf.space).

Go to Cron-job.org:

Create a free account and log in.

Click "Create Cronjob".

Title: Telegram Bot Keep Alive

URL: Paste your Direct URL from Step 1.

Execution Schedule: Select "Every 15 minutes".

Save.

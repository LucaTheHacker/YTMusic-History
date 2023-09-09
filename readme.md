# YTMusic History

A nice way to always keep track of what you like to listen - even if copyright laws jump into the matter.

## Requirements

1. Docker
2. Docker Compose
3. A working brain
4. A browser with a logged in Google account 

## Installation

#### Clone the repo

    git clone https://github.com/LucaTheHacker/YTMusic-History

#### CD into the folder

    cd YTMusic-History

#### Copy the example config

    cp .env.example .env

#### Edit the config filling the required fields, use a text editor for that.

Open https://music.youtube.com/library, and open the developer console.  
Developer console > Network tab > filter by XHR.  
Click on the history logo (the clock with the arrow), one request with endpoint starting with "browse" should appear.  
Select the headers tab and scroll to "Request Headers".  
Copy the content of COOKIE and AUTHENTICATION in the .env file.  

`COOKIE` is the cookie you get from your browser.  
`AUTHENTICATION` is the authentication token you get from your browser, starts with `SAPISIDHASH`.  
`DOWNLOAD_DIR` is the directory where the songs will be downloaded.  
`DATABASE_DIR` is the path where the database will be stored.  
`INTERVAL` is the interval between each run, in hours, 24 is recommended.

#### Start the containers

    docker compose up -d

## Why

I lost many remixes due to copyright strikes on YouTube.  
Tired of that, I decided to download every song I listen to, and keep it in a safe place.  
This is the result, and this also records the listening history (max 1 view per day), so that in 10 years I can cringe
at myself for my music taste.

## Workarounds

YouTube, thanks to their asshole-being, does not consent to stream music from two different devices
(Because who thinks I may have left my phone playing music at no volume whilst I'm at my computer!).  
At the same time, downloading all the songs with an account would cause continuous "song paused due to stream on another device" errors.  
Whilst using the same account on two different devices is forbidden, YouTube doesn't allow to download some songs without logging in,
even if they're not 18+ or restricted in any way.  
To work around this pile of garbage, a first try with no account is made, and if the song is not downloadable it's sent to the authenticated queue.  
This should reduce the amount of music stops by a lot.

Thanks Google. 
Spero che domani mattina ve sveja San Pietro.
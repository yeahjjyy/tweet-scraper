# tweet-scraper | twitter followers-scraper | twitter following-scraper

## Description

- Learn how to scrape Twitter tweets using Python and Selenium. Automate data collection with [advanced search](https://github.com/igorbrigadir/twitter-advanced-search) features for precise insights.
- Scrape Twitter Followers with Python and Selenium
- Effortlessly Scrape Twitter Following Data with Python & Selenium

## API
Yout can use APIs from [Apify](https://apify.com/)

## Example of Scraped Tweets Data

```json
{
  "type": "tweet",
  "id": 1843447413824209160,
  "viewCount": "51275823",
  "url": "https://x.com/elonmusk/status/1843447413824209160",
  "twitterUrl": "https://twitter.com/elonmusk/status/1843447413824209160",
  "text": "It is a surefire way for the Dems to turn America into a one-party state, just like California.",
  "isQuote": true,
  "retweetCount": 59493,
  "replyCount": 11090,
  "likeCount": 250068,
  "quoteCount": 1661,
  "createdAt": "Tue Oct 08 00:24:47 +0000 2024",
  "lang": "en",
  "quoteId": "1843379457605939258",
  "bookmarkCount": 11177,
  "isReply": false,
  "source": "Twitter for iPhone",
  "author": {
    "type": "user",
    "username": "elonmusk",
    "url": "https://x.com/elonmusk",
    "twitterUrl": "https://x.com/elonmusk",
    "id": "44196397",
    "name": "Elon Musk",
    "isVerified": false,
    "isBlueVerified": true,
    "profilePicture": "https://pbs.twimg.com/profile_images/1849727333617573888/HBgPUrjG_normal.jpg",
    "description": "Read @America to understand why I’m supporting Trump for President",
    "followers": 202400789,
    "following": 794,
    "mediaCount": 2637,
    "statusesCount": 55447
  },
  "quote": {
    "type": "tweet",
    "id": "1843379457605939258",
    "text": "Elon Musk explains how this will be our last real election if Kamala Harris wins. Everyone must watch this.",
    "retweetCount": 10725,
    "replyCount": 1848,
    "likeCount": 38268,
    "createdAt": "Mon Oct 07 19:54:45 +0000 2024",
    "author": {
      "type": "user",
      "username": "EndWokeness",
      "url": "https://x.com/EndWokeness",
      "id": "1552795969959636992",
      "name": "End Wokeness",
      "followers": 3107102,
      "mediaCount": 7219,
      "statusesCount": 15502
    }
  }
}
```

## Example of Scraped Followers&Following Data

```json

{
  "userId": "95092020",
  "isBlueVerified": true,
  "following": false,
  "canDm": false,
  "canMediaTag": false,
  "createdAt": "Sun Dec 06 23:33:02 +0000 2009",
  "defaultProfile": false,
  "defaultProfileImage": false,
  "description": "Best-Selling Author | Clinical Psychologist | #1 Education Podcast | Enroll to @petersonacademy now:",
  "fastFollowersCount": 0,
  "favouritesCount": 161,
  "followersCount": 5613000,
  "friendCount": 1686,
  "hasCustomTimelines": true,
  "isTranslator": false,
  "listedCount": 14572,
  "location": "",
  "mediaCount": 7318,
  "name": "Dr Jordan B Peterson",
  "normalFollowersCount": 5613000,
  "pinnedTweetIdsStr": ["1849105729438790067"],
  "possiblySensitive": false,
  "profileImageUrlHttps": "https://pbs.twimg.com/profile_images/1407056014776614923/TKBC60e1_normal.jpg",
  "profileInterstitialType": "",
  "username": "jordanbpeterson",
  "statusesCount": 51343,
  "translatorType": "none",
  "verified": false,
  "wantRetweets": false,
  "withheldInCountries": []
}

```

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)


## Installation

### Prerequisites

- Python 3.x installed on your system
- `pip` package manager

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yeahjjyy/tweet-scraper.git
   cd tweet-scraper
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install the dependencies from requirements.txt:
   ```bash
    pip install -r requirements.txt

## Usage
To run the project, simply execute the following command:
   ```bash
    python tweet.py

import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from datetime import datetime, timedelta

async def main():
    api = API("./accounts.db")
    
    start_date = datetime(2015, 12, 31)
    end_date = datetime(2015, 1, 1)
    
    # Define the query base
    base_query = "bitcoin since:{} until:{} lang:es"
    with open("/scrapped_data/file.txt", "a", encoding="utf-8") as f:
        while start_date >= end_date:
            # Format the dates in the query
            since_date_str = start_date.strftime("%Y-%m-%d")
            until_date_str = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")  # Go one day next
            
            # Update the query
            q = base_query.format(since_date_str, until_date_str)
            print(q)
            # Search tweets for the current day
            async for tweet in api.search(q, limit=500, kv={"product": "Top"}):
                tweet_info = f"{tweet.id}|{tweet.user.username}|{tweet.rawContent.replace('\n', '').replace('|', '')}|{tweet.date}|{tweet.likeCount}|{tweet.retweetCount}|{tweet.user.friendsCount}|{tweet.user.followersCount}\n"
                f.write(tweet_info)
            
            # Move to the previous day
            start_date -= timedelta(days=1)

asyncio.run(main())
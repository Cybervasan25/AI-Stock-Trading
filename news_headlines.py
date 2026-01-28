from nltk.sentiment.vader import SentimentIntensityAnalyzer
import feedparser
import csv
from datetime import datetime
import nltk
import re


#Code to give trade suggestions based on news headlines
def get_trade_signals():
    #Setup VADER and sentiment analyzer
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    # Yahoo Finance RSS Feed URL
    rss_url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=UGRO,CGC,PLUG&region=US&lang=en-US"


    #Tickers
    TICKERS = {
    "UGRO": ["UGRO", "urban-gro, Inc.", "Controlled Environment Agriculture & engineering", "NASDAQ penny mover", "Recent volume and 52-week price activity"],  # NASDAQ: UGRO—in the agriculture/environment systems space with recent strong moves & volume :contentReference[oaicite:0]{index=0}
    "VIVK": ["VIVK", "Vivakor, Inc.", "Energy services & logistics", "Nasdaq microcap trading active", "High recent trading activity"],  # NASDAQ: VIVK—energy/transport/logistics with strong volume & diversification news :contentReference[oaicite:1]{index=1}
    "CGC": ["CGC", "Canopy Growth Corporation", "Cannabis sector", "Large microcap with recent gains", "Shows decent intraday action"],  # Canopy Growth—well-known cannabis name under $5 with notable daily % moves
    "PLUG": ["PLUG", "Plug Power Inc.", "Hydrogen energy / fuel cells", "Nasdaq listed under $5 range", "Renewables interest"],  # Plug Power under $5 (per your data) trending with energy interest
    "PAVS": ["PAVS", "Paranovus Entertainment Technology Ltd.", "AI/tech/e-commerce driver", "High speculative volumes", "Nasdaq microcap with strong interim growth news"],  # PAVS—AI/entertainment microcap with reported revenue jumps and volatility :contentReference[oaicite:2]{index=2}
    "ABQQ": ["ABQQ", "AI Era Corp.", "AI / emerging tech penny name", "Microcap speculative", "Heavy intraday % moves"],  # AI Era microcap (per your list)
    "ASST": ["ASST", "Strive Asset Management, LLC", "Bitcoin treasury/asset management", "Nasdaq momentum microcap", "Analyst interest"],  # ASST—Nasdaq listed asset mgmt/bitcoin treasury name with strong buy sentiment and recent action :contentReference[oaicite:3]{index=3}
}

    #TICKERS = ["AAPL"]

    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Limit to 5-10 headlines
    headlines = feed.entries[:100]

    # Filename with date
    filename = f"yahoo_finance_headlines_{datetime.now().strftime('%Y-%m-%d')}.csv"

    #Analyze sentiment for each ticker
    ticker_sentiments = {ticker: [] for ticker in TICKERS}

    #Analyze sentiment for each ticker
    for entry in headlines:
        title = entry.title
        sentiment = sia.polarity_scores(title)['compound']

        #Check the tickers associated with the headlines
        # Replace the mentioned_tickers code with:
        mentioned_tickers = []
        for ticker, keywords in TICKERS.items():
            if any(re.search(rf'\b{re.escape(kw)}\b', title, re.IGNORECASE) for kw in keywords):
                 mentioned_tickers.append(ticker)

        #Calculate sentiment score and divide it by number of tickers mentioned
        #Ensures both tickers get equal impact and avoids double-counting sentiment
        for ticker in mentioned_tickers:
            ticker_sentiments[ticker].append(sentiment/len(mentioned_tickers))

    print(f"\n=== Analyzing {len(headlines)} headlines ===")
    for i, entry in enumerate(headlines[:20]):  # Print first 5 headlines as samples
        print(f"{i+1}. {entry.title}")

    #Generate trade suggestions
    print("\n==Trades to Make==")
    for ticker in TICKERS:
        scores = ticker_sentiments[ticker]
        print(f"Score for Ticker {ticker} is {scores}")

        #Ticker is not in the headline
        if not scores:
            continue

        avg_sentiment= sum(scores) / len(scores)

        if avg_sentiment > 0.05:
            print(f"Buy {ticker}")
        elif avg_sentiment < -0.05:
            print(f"Sell {ticker}")
        else:
            print(f"Hold {ticker}")



    # Save headlines to CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Headline'])

        for entry in headlines:
            title = entry.title
            published = entry.published
            sentiment_scores = sia.polarity_scores(title)
            compound = sentiment_scores['compound']
            if compound >= 0.05:
                sentiment = "Positive" 
            elif compound <= -0.05:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            published = entry.published
            title = entry.title
            writer.writerow([published, title, sentiment, compound])

    trade_signals = []
    for ticker in TICKERS:
        scores = ticker_sentiments[ticker]
        if not scores:
            print(f"No headlines for {ticker}")
            continue
        
        #Calculates average sentiment score of headlines of each ticker
        avg_sentiment = sum(scores) / len(scores)

        #If statment to determine whether to buy or sell stock based on average sentiment score
        if avg_sentiment > 0.05:
            trade_signals.append({"ticker": ticker, "action": "buy", "sentiment": avg_sentiment})
        elif avg_sentiment < -0.05:
            trade_signals.append({"ticker": ticker, "action": "sell", "sentiment": avg_sentiment})

    return trade_signals

    # Lets user know that program has been uploaded
    # print(f"Saved {len(headlines)} headlines to {filename}")

if __name__ == "__main__":
    print("TEST OUTPUT:", get_trade_signals())





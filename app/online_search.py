from duckduckgo_search import DDGS

def search_concert_news(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)

    if not results:
        return "❌ No results found."

    formatted = "\n\n".join(f"{r['title']}\n{r['href']}" for r in results)
    return f"🌍 Online Search Results (DuckDuckGo):\n\n{formatted}"

if __name__ == "__main__":
    user_query = input("Enter your concert-related question: ")
    print(search_concert_news(user_query))

import httpx
import re

def fetch_url(url: str) -> str:
    """Fetches raw text content from a given URL. Useful for reading documentation or articles.
    Args:
        url: The full HTTP/HTTPS URL to fetch.
    """
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            resp = client.get(url)
            resp.raise_for_status()
            
            # Very aggressive HTML strip since we don't have BeautifulSoup installed
            text = re.sub(r'<style.*?</style>', '', resp.text, flags=re.DOTALL)
            text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^<]+?>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text[:10000] + ("\n...[TRUNCATED]" if len(text) > 10000 else "")
    except Exception as e:
        return f"Failed to fetch {url}: {str(e)}"

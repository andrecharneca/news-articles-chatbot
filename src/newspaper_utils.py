import newspaper
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = newspaper.Config()
config.browser_user_agent = user_agent
config.request_timeout = 10

def remove_empty_lines(text: str) -> str:
    """
    Removes empty lines from a string and replaces consecutive
    newline characters with a single newline character.

    Args:
        text (str): The string to remove empty lines from.

    Returns:
        str: The string without empty lines and consecutive newline characters.
    """
    lines = text.splitlines()  # Split the text into individual lines, preserving line endings
    non_empty_lines = [line for line in lines if line.strip() != ""]  # Remove the empty lines
    return "\n".join(non_empty_lines)  # Join the non-empty lines back into a string, using single newline characters

def clean_text(text: str) -> str:
    """
    Cleans the text of an article
    args:
        text (str): text of an article
    returns:
        clean_text(str): cleaned text
    """
    
    # remove empty lines (more than 1 newline)
    clean_text = remove_empty_lines(text)
    
    return clean_text

def get_article(url: str, verbose: bool = False) -> dict:
    """
    Gets the title and text of an article
    args:
        url (str): url of an article
    returns:
        dict: title and text of an article
    """
    article = newspaper.Article(url)#, config=config)
    title, text, date = None, None, None
    
    try:
        article.download()
        article.parse()
        title = article.title
        text = article.text
        text = clean_text(text)
        date = article.publish_date
    except Exception as e:
        if verbose: print(f"Exception {e} with article: ", url)

    return {"title": title, "text": text, "date": date}
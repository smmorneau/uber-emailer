from HTMLParser import HTMLParser
import re


def validate_email(email):
    """ Returns True if email is valid, False otherwise
    Source: http://blog.trojanhunter.com/2012/09/26/the-best-regex-to-validate
            -an-email-address/
    """
    email = email.strip()
    # [-0-9a-zA-Z.+_] 1+x, '@', [-0-9a-zA-Z.+_] 1+x, '.', TLD (2-4 chars)
    email_regex = r"([-0-9a-zA-Z.+_]+)@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}"
    match = re.match(email_regex, email)
    if not match:
        # does not match pattern
        return False
    # emails cannot have 1+ '.' in a row
    if re.search(r"\.\.", email):
        return False
    # local-part of email cannot start or end with '.'
    local = match.group(1)
    if local.startswith(".") or local.endswith("."):
        return False
    return True


def strip_html(text):
    """ Removes html, script, & style tags from text
        Unescapes HTML escape characters and converts to plaintext
        Returns the cleaned text """
    script_regex = r"<[sS][cC][rR][iI][pP][tT](.+?)</[sS][cC][rR][iI][pP][tT]>"
    style_regex = r"<[sS][tT][yY][lL][eE](.+?)</[sS][tT][yY][lL][eE]>"
    tag_regex = r"<[^<>]+?>"  # <(.+?)>

    # converts amp tags (HTML escape characters) to plaintext
    text = HTMLParser().unescape(text)
    # removes script, style, and html tags
    text = re.sub(script_regex, " ", text, flags=re.DOTALL)
    text = re.sub(style_regex, " ", text, flags=re.DOTALL)
    text = re.sub(tag_regex, " ", text)
    # reduce multiple whitespace to single space
    text = re.sub("\s\s+", " ", text).strip()

    return text

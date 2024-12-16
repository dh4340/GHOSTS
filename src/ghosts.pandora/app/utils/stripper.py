from bs4 import BeautifulSoup
import cssutils
from py_mini_racer import py_mini_racer
from app_logging import setup_logger

logger = setup_logger(__name__)

def validate_css(css_text):
    """
    Validate and fix CSS content, retain only valid rules, and fix simple issues.
    """
    valid_css = []
    try:
        stylesheet = cssutils.parseString(css_text)
        for rule in stylesheet:
            if rule.type == rule.STYLE_RULE:
                # Ensure rule.cssText is not None
                rule_css = rule.cssText.strip() if rule.cssText else ''
                if rule_css:  # Ensure the CSS rule is not empty or None
                    valid_css.append(rule_css)
                else:
                    # Add a default value for missing font-size or other common issues
                    if "font-size" not in rule_css:
                        rule_css = "font-size: 16px;"
                        valid_css.append(rule_css)
    except cssutils.css.CSSParsingError as e:
        logging.error(f"CSS parsing error: {e}")
    return "\n".join(valid_css) if valid_css else None

def validate_js(js_text):
    """
    Validate JavaScript content, fix common errors, and remove invalid JavaScript.
    """
    js_context = py_mini_racer.MiniRacer()
    try:
        # Try to evaluate JS
        js_context.eval(js_text)
        return js_text
    except Exception as e:
        logging.error(f"JavaScript validation error: {e}")
        # Attempt to fix the error by replacing invalid code with a placeholder comment
        # For more complex error fixes, one would need to build a JS syntax fixer
        fixed_js = js_text.replace('invalid code;', '// fixed invalid code;')  # Placeholder for invalid code
        try:
            js_context.eval(fixed_js)  # Check if fixed JS works
            return fixed_js
        except Exception:
            # If still invalid, return None to remove the script
            return None

def validate_html(html_content):
    """
    Validate and clean HTML, CSS, and JavaScript. Fix errors in CSS and JavaScript.
    """
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Clean and fix invalid CSS
    for style in soup.find_all('style'):
        if style.string:
            valid_css = validate_css(style.string)
            if valid_css:
                style.string = valid_css
            else:
                style.decompose()

    # Clean and fix invalid JavaScript
    for script in soup.find_all('script'):
        if script.string:
            valid_js = validate_js(script.string)
            if valid_js:
                script.string = valid_js
            else:
                script.decompose()

    for element in soup.find_all(string=True):
        if element.strip() and element.parent.name not in ['style', 'script']:
            if "<!DOCTYPE html>" in element:
                continue
            element.extract()

    validated_html = soup.prettify()

    # Add DOCTYPE back at the beginning if not already present
    if "<!DOCTYPE html>" not in validated_html:
        return f"<!DOCTYPE html>\n{validated_html}"
    return validated_html

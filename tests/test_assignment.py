from pathlib import Path
from bs4 import BeautifulSoup
import re


ROOT = Path(__file__).resolve().parents[1]

HTML_FILE = ROOT / "c07x_sampson.html"
CSS_FILE = ROOT / "c07x_speaker.css"


def read_html():
    return HTML_FILE.read_text(encoding="utf-8")


def read_css():
    return CSS_FILE.read_text(encoding="utf-8")


def css_rule(css, selector):
    """
    Extract a simple CSS rule from the stylesheet.
    """
    pattern = rf"{re.escape(selector)}\s*\{{(.*?)\}}"
    match = re.search(pattern, css, re.S)

    assert match is not None, f"CSS selector '{selector}' was not found."

    return match.group(1)


# ---------------------------------------------------------
# HTML TESTS
# ---------------------------------------------------------

def test_html_file_exists():
    assert HTML_FILE.exists()


def test_css_file_exists():
    assert CSS_FILE.exists()


def test_html_has_correct_title():
    soup = BeautifulSoup(read_html(), "html.parser")

    assert soup.title is not None
    assert soup.title.get_text(strip=True) == \
        "San Joaquin Valley Town Hall"


def test_header_exists():
    soup = BeautifulSoup(read_html(), "html.parser")

    header = soup.find("header")

    assert header is not None


def test_town_hall_logo_exists():
    soup = BeautifulSoup(read_html(), "html.parser")

    image = soup.find(
        "img",
        src=re.compile(r"town_hall_logo\.gif")
    )

    assert image is not None
    assert image.get("alt") == "Town Hall logo"


def test_shadow_class_exists():
    soup = BeautifulSoup(read_html(), "html.parser")

    element = soup.select_one(".shadow")

    assert element is not None
    assert "75" in element.get_text()


def test_section_exists():
    soup = BeautifulSoup(read_html(), "html.parser")

    section = soup.find("section")

    assert section is not None


def test_section_heading():
    soup = BeautifulSoup(read_html(), "html.parser")

    heading = soup.select_one("section h1")

    assert heading is not None
    assert heading.get_text(strip=True) == \
        "Fossil Threads in the Web of Life"


def test_sampson_image_exists():
    soup = BeautifulSoup(read_html(), "html.parser")

    image = soup.find(
        "img",
        src=re.compile(r"sampson_dinosaur\.jpg")
    )

    assert image is not None
    assert image.get("alt") == "Scott Sampson with dinosaur"


def test_guest_speakers_exists():
    soup = BeautifulSoup(read_html(), "html.parser")

    heading = soup.select_one("aside h2")

    assert heading is not None
    assert heading.get_text(strip=True) == "Guest speakers"


def test_four_guest_speakers():
    soup = BeautifulSoup(read_html(), "html.parser")

    items = soup.select("#nav_list ul li")

    assert len(items) == 4


def test_sampson_is_current():
    soup = BeautifulSoup(read_html(), "html.parser")

    current = soup.select_one(
        '#nav_list a.current'
    )

    assert current is not None
    assert "Scott Sampson" in current.get_text()


def test_footer_exists():
    soup = BeautifulSoup(read_html(), "html.parser")

    footer = soup.find("footer")

    assert footer is not None


# ---------------------------------------------------------
# CSS TESTS
# ---------------------------------------------------------

def test_body_width():
    css = read_css()

    rule = css_rule(css, "body")

    assert re.search(
        r"width\s*:\s*850px",
        rule
    )


def test_body_centered():
    css = read_css()

    rule = css_rule(css, "body")

    assert re.search(
        r"margin\s*:\s*0\s+auto",
        rule
    )


def test_body_border():
    css = read_css()

    rule = css_rule(css, "body")

    assert re.search(
        r"border\s*:\s*3px\s+solid\s+#931420",
        rule,
        re.I
    )


def test_body_background():
    css = read_css()

    rule = css_rule(css, "body")

    assert re.search(
        r"background-color\s*:\s*#fffded",
        rule,
        re.I
    )


def test_section_width():
    css = read_css()

    rule = css_rule(css, "section")

    assert re.search(
        r"width\s*:\s*575px",
        rule
    )


def test_section_float():
    css = read_css()

    rule = css_rule(css, "section")

    assert re.search(
        r"float\s*:\s*right",
        rule
    )


def test_aside_width():
    css = read_css()

    rule = css_rule(css, "aside")

    assert re.search(
        r"width\s*:\s*215px",
        rule
    )


def test_aside_float():
    css = read_css()

    rule = css_rule(css, "aside")

    assert re.search(
        r"float\s*:\s*right",
        rule
    )


def test_article_image_float():
    css = read_css()

    rule = css_rule(css, "article img")

    assert re.search(
        r"float\s*:\s*right",
        rule
    )


def test_article_image_border():
    css = read_css()

    rule = css_rule(css, "article img")

    assert re.search(
        r"border\s*:\s*1px\s+solid\s+black",
        rule,
        re.I
    )


def test_navigation_list_has_no_bullets():
    css = read_css()

    rule = css_rule(css, "#nav_list ul")

    assert re.search(
        r"list-style\s*:\s*none",
        rule
    )


def test_navigation_item_width():
    css = read_css()

    rule = css_rule(css, "#nav_list ul li")

    assert re.search(
        r"width\s*:\s*200px",
        rule
    )


def test_navigation_item_border():
    css = read_css()

    rule = css_rule(css, "#nav_list ul li")

    assert re.search(
        r"border\s*:\s*2px\s+double\s+black",
        rule,
        re.I
    )


def test_navigation_border_radius():
    css = read_css()

    rule = css_rule(css, "#nav_list ul li")

    assert re.search(
        r"border-radius\s*:\s*10px",
        rule
    )


def test_navigation_box_shadow():
    css = read_css()

    rule = css_rule(css, "#nav_list ul li")

    assert re.search(
        r"box-shadow\s*:\s*3px\s+3px\s+0\s+0\s+#800000",
        rule,
        re.I
    )


def test_navigation_background_image():
    css = read_css()

    rule = css_rule(css, "#nav_list ul li")

    assert "right.jpg" in rule


def test_current_link_color():
    css = read_css()

    rule = css_rule(css, "#nav_list ul li a.current")

    assert re.search(
        r"color\s*:\s*#800000",
        rule,
        re.I
    )


def test_footer_background():
    css = read_css()

    rule = css_rule(css, "footer")

    assert re.search(
        r"background-color\s*:\s*#931420",
        rule,
        re.I
    )


def test_footer_clears_floats():
    css = read_css()

    rule = css_rule(css, "footer")

    assert re.search(
        r"clear\s*:\s*both",
        rule
    )


def test_footer_text_color():
    css = read_css()

    rule = css_rule(css, "footer p")

    assert re.search(
        r"color\s*:\s*white",
        rule,
        re.I
    )

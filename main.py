import json
from pathlib import Path

from bs4 import BeautifulSoup


def get_sermon_mt_meditation_json() -> dict:
    """
    Get a meditation for each verse in the Sermon on the Mount.

    Currently, this is super-hardcoded to the Spurgeon commentaries I found.
    NOTE: The Spurgeon commentaries have text for most, but not all, verses.
    """
    def get_commentary_verses_from_html(
            path: Path, title: str, link: str
    ) -> dict:
        result = {}
        text = path.read_text(encoding="utf-8", errors="ignore")
        replacements = {
            "“": '"',
            " ”": '"',
            "”": '"',
            '&nbsp;"': '"',
            "&nbsp;": " ",
            "’": "'",
            u"\u2014": "-"
        }
        for key, value in replacements.items():
            text = text.replace(key, value)
        soup = BeautifulSoup(text)

        verse_links = soup.select("a[data-reference]")
        for vl in verse_links:
            reference = f"Matthew {vl.get("data-reference").split(" ")[-1]}".replace(".", ":")
            next_paras = vl.find_all_next("p")
            commentary_text = []
            for p in next_paras:
                if p.get("class") and p["class"][0] == "verse":
                    # assume the ext verse starts and we're done getting the commentary here
                    break
                commentary_text.append(p.text)
            result[reference] = {
                "text": "\n".join(commentary_text),
                "author": "C.H. Spurgeon",
                "sourceTitle": title,
                "sourceLink": link
            }
        return result

    return (
        get_commentary_verses_from_html(
            Path("raw_data/spurgeon-5-commentary.html"),
            "Matthew 5 Commentary",
            "https://www.preceptaustin.org/matthew-5-commentary-spurgeon"
        )
        | get_commentary_verses_from_html(
            Path("raw_data/spurgeon-6-commentary.html"),
            "Matthew 6 Commentary",
            "https://www.preceptaustin.org/matthew-6-commentary-spurgeon"
        )
        | get_commentary_verses_from_html(
            Path("raw_data/spurgeon-7-commentary.html"),
            "Matthew 7 Commentary",
            "https://www.preceptaustin.org/matthew-7-commentary-spurgeon"
        )
    )


def get_sermon_mt_verses_json() -> list:
    """
    Get verses (without meditation) from the ESV source for the Sermon on the Mount.

    Assume each verse is in the ESV API format '[#] Text...' (verse numbers,
    won't include chapter numbers).
    """
    meditations = get_sermon_mt_meditation_json()
    def _chpt(verse: int) -> int:
        if verse >= 82:
            return 7
        if verse >= 48:
            return 6
        return 5

    def _verse_json(i: int, text: str) -> dict:
        ref = f"Matthew {_chpt(i)}:{text.split('] ')[0]}"
        placeholder = {
            "text": "TODO - still looking for something to put here. Sorry!",
            "author": "Admin",
            "sourceTitle": "An Apology",
            "sourceLink": "/"
        }
        return {
            "text": text.split("] ")[1],
            "reference": ref,
            "meditation": meditations.get(ref, placeholder)
        }

    raw_text: str = json.loads(Path("raw_data/esv_text.json").read_text())["passages"][0]
    verses = raw_text.split("[")[1:]
    return [_verse_json(i, text) for i, text in enumerate(verses)]


def get_sermon_mt_sections_json() -> list:
    """
    Get the sections of the Sermon on the Mount as ESV section headings.

    I am hardcoding this because it's faster than trying to automate it (short,
    known list and have to set the section boundaries).

    NOTE: the verse numbers here are 0-indexed, and don't reset between
    chapters (i.e. they correspond to the verse JSON function).
    """
    sections = [
        {
            "name": "The Beatitudes",
            "startVerse": 0,
            "endVerse": 11
        },
        {
            "name": "Salt and Light",
            "startVerse": 12,
            "endVerse": 15
        },
        {
            "name": "Christ Came to Fulfill the Law",
            "startVerse": 16,
            "endVerse": 19
        },
        {
            "name": "Anger",
            "startVerse": 20,
            "endVerse": 25
        },
        {
            "name": "Lust",
            "startVerse": 26,
            "endVerse": 29
        },
        {
            "name": "Divorce",
            "startVerse": 30,
            "endVerse": 31
        },
        {
            "name": "Oaths",
            "startVerse": 32,
            "endVerse": 36
        },
        {
            "name": "Retaliation",
            "startVerse": 37,
            "endVerse": 41
        },
        {
            "name": "Love Your Enemies",
            "startVerse": 42,
            "endVerse": 47
        },
        {
            "name": "Giving to the Needy",
            "startVerse": 48,
            "endVerse": 51
        },
        {
            "name": "The Lord's Prayer",
            "startVerse": 52,
            "endVerse": 62
        },
        {
            "name": "Fasting",
            "startVerse": 63,
            "endVerse": 65
        },
        {
            "name": "Lay Up Treasures in Heaven",
            "startVerse": 66,
            "endVerse": 68
        },
        {
            "name": "Do Not Be Anxious",
            "startVerse": 69,
            "endVerse":81
        },
        {
            "name": "Judging Others",
            "startVerse": 82,
            "endVerse": 87
        },
        {
            "name": "Ask, and It Will Be Given",
            "startVerse": 88,
            "endVerse": 92
        },
        {
            "name": "The Golden Rule",
            "startVerse": 93,
            "endVerse": 95
        },
        {
            "name": "A Tree and Its Fruit",
            "startVerse": 96,
            "endVerse": 101
        },
        {
            "name": "I Never Knew You",
            "startVerse": 102,
            "endVerse": 104
        },
        {
            "name": "Build Your House on the Rock",
            "startVerse": 105,
            "endVerse": 108
        },
        {
            "name": "The Authority of Jesus",
            "startVerse": 109,
            "endVerse": 110
        },
    ]
    return sections


def make_site_data():
    x = {
        "verses": {
            "0": {
                "text": "Seeing the crowds, he went up on the mountain, and when he had sat down, his disciples came to him.",
                "reference": "Matthew 5:1",
                "meditation": {
                    "text": "Spurgeon says things",
                    "author": "C.H. Spurgeon",
                    "sourceTitle": "Matthew 5 Commentary",
                    "sourceLink": "https://stuff.com"
                }
            }
        },
        "sections": {
            "0": {
                "name": "The Beatitudes",
                "startVerse": 0,
                "endVerse": 11
            }
        }
    }
    x["verses"] = get_sermon_mt_verses_json()
    x["sections"] = get_sermon_mt_sections_json()
    return x


def reference(start_verse: dict, end_verse: dict) -> str:
    """Get the verse reference string for the passage."""
    start_ref, end_ref = start_verse["reference"], end_verse["reference"]
    if start_ref == end_ref:
        return start_ref
    chpt_v_1, chpt_v_2 = start_ref.split(" ")[-1], end_ref.split(" ")[-1]
    chpt1, v1 = chpt_v_1.split(":")
    chpt2, v2 = chpt_v_2.split(":")
    if chpt1 == chpt2:
        return f"{start_ref}-{v2}"
    return f"{start_ref}-{chpt_v_2}"


def write_site_data() -> dict:
    site_data = make_site_data()
    file = Path("site_data.json")
    file.write_text(json.dumps(site_data, indent=2))
    return site_data


def build_site(site_data: dict):
    DAY_TEMPLATE_TEXT = Path("template.html").read_text()
    verses = site_data["verses"]

    def _str_to_html(s: str) -> str:
        return "\n".join([f"<p>{x}</p>" for x in s.split("\n")])

    def _verses_html(start: int, end: int) -> str:
        return _str_to_html("".join(
            [v["text"] for v in verses[start:end]]
            # strip the last verse to avoid paragraph breaking the </strong>
            + [f"<strong>{verses[end]["text"].strip()}</strong>"]
        ))

    for i, section in enumerate(site_data["sections"]):
        for verse_i in range(section["startVerse"], section["endVerse"]+1):
            print(verse_i)
            verses_chunk_html = _verses_html(section["startVerse"], verse_i)
            verses_whole_html = _verses_html(0, verse_i)

            html = DAY_TEMPLATE_TEXT[:]
            html = html.replace("TEMPLATE_DAY", str(verse_i+1))
            html = html.replace(
                "TEMPLATE_SECTION_TITLE",
                f"Section {i+1}: {section["name"]} ({reference(verses[section["startVerse"]], verses[section["endVerse"]])})"
            )
            html = html.replace(
                "TEMPLATE_CHUNK_REFERENCE",
                reference(verses[section["startVerse"]], verses[verse_i])
            )
            html = html.replace("TEMPLATE_CHUNK_SCRIPTURE", verses_chunk_html)
            med = verses[verse_i]["meditation"]
            html = html.replace(
                "TEMPLATE_CHUNK_MEDITATION",
                f'{_str_to_html(med["text"])}<p>- {med["author"]}, <a href="{med["sourceLink"]}">{med["sourceTitle"]}</a></p>'
            )
            html = html.replace(
                "TEMPLATE_CUMULATIVE_REFERENCE",
                reference(verses[0], verses[verse_i])
            )
            html = html.replace(
                "TEMPLATE_CUMULATIVE_SCRIPTURE",
                verses_whole_html
            )
            html = html.replace(
                "TEMPLATE_NAVIGATION_HTML",
                # TODO: Refactor this garbage
                "<p>" + (f'<a href="{verse_i}.html">Prev</a>' if verse_i > 0 else "")  + " | " + (f'<a href="{verse_i+2}.html">Next</a>' if verse_i+2 < len(verses) + 1 else "") + "</p>"
            )
            output_path = Path(f"docs/{verse_i+1}.html")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html)
    home_page_text = Path("index.html").read_text()
    home_page_text = home_page_text.replace(
        "TEMPLATE_DAY_LINKS",
        "\n".join([
            f'<li><a href="{i+1}.html">Day {i+1}</a></li>'
            for i in range(len(verses))
        ])
    )
    output_path = Path("docs/index.html")
    output_path.write_text(home_page_text)



def test_crummy_manual(data: dict):
    for i, section in enumerate(data["sections"]):
        start_verse = data["verses"][section["startVerse"]]
        end_verse   = data["verses"][section["endVerse"]]
        print(f"=== Section {i+1}: {section["name"]} ({reference(start_verse, end_verse)}) ===")
        print(''.join(x["text"] for x in data["verses"][section["startVerse"]:section["endVerse"]+1]))

    print(reference(data["verses"][0], data["verses"][1]))
    print(reference(data["verses"][0], data["verses"][100]))


def main():
    site_data = write_site_data()
    test_crummy_manual(site_data)
    build_site(site_data)


if __name__ == "__main__":
    main()

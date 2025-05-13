import json
from pathlib import Path


def get_sermon_mt_verses_json() -> list:
    """
    Get verses (without meditation) from the ESV source for the Sermon on the Mount.

    Assume each verse is in the ESV API format '[#] Text...' (verse numbers,
    won't include chapter numbers).
    """
    def _chpt(verse: int) -> int:
        if verse >= 82:
            return 7
        if verse >= 48:
            return 6
        return 5

    raw_text: str = json.loads(Path("esv_text.json").read_text())["passages"][0]
    verses = raw_text.split("[")[1:]
    return [
        {
            "text": text.split("] ")[1],
            "reference": f"Matthew {_chpt(i)}:{text.split('] ')[0]}"
        }
        for i, text in enumerate(verses)
    ]

def get_sermon_mt_sections_json() -> list:
    """
    Get the sections of the sermon on the mount as ESV section headings.

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
    for i, section in enumerate(site_data["sections"]):
        for verse_i in range(section["startVerse"], section["endVerse"]+1):
            print(verse_i)
            html = DAY_TEMPLATE_TEXT[:]
            html = html.replace("TEMPLATE_DAY", str(verse_i+1))
            html = html.replace(
                "TEMPLATE_SECTION_TITLE",
                f"<u>Section {i+1}: {section["name"]}</u> ({reference(verses[section["startVerse"]], verses[section["endVerse"]])})"
            )
            html = html.replace(
                "TEMPLATE_CHUNK_REFERENCE",
                reference(verses[section["startVerse"]], verses[verse_i])
            )
            html = html.replace(
                "TEMPLATE_CHUNK_SCRIPTURE",
                # TODO: Add newlines properly via <p> tags
                "".join([v["text"] for v in verses[section["startVerse"]:verse_i]] + [f"<strong>{verses[verse_i]["text"]}</strong>"])
            )
            html = html.replace("TEMPLATE_CHUNK_MEDITATION", "TODO")
            html = html.replace(
                "TEMPLATE_CUMULATIVE_REFERENCE",
                reference(verses[0], verses[verse_i])
            )
            html = html.replace(
                "TEMPLATE_CUMULATIVE_SCRIPTURE",
                "".join([v["text"] for v in verses[:verse_i]] + [f"<strong>{verses[verse_i]["text"]}</strong>"])
            )
            html = html.replace(
                "TEMPLATE_NAVIGATION_HTML",
                # TODO: Refactor this garbage
                "<p>" + (f'<a href="{verse_i}.html">Prev</a>' if verse_i > 0 else "")  + " | " + (f'<a href="{verse_i+2}.html">Next</a>' if verse_i+2 < len(verses) + 1 else "") + "</p>"
            )
            output_path = Path(f"build/{verse_i+1}.html")
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
    output_path = Path("build/index.html")
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

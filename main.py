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
    chpt_v_1, chpt_v_2 = start_ref.split(" ")[-1], end_ref.split(" ")[-1]
    chpt1, v1 = chpt_v_1.split(":")
    chpt2, v2 = chpt_v_2.split(":")
    if chpt1 == chpt2:
        return f"{start_ref}-{v2}"
    return f"{start_ref}-{chpt_v_2}"


def main():
    file = Path("site_data.json")
    file.write_text(json.dumps(make_site_data(), indent=2))

    # crummy manual test
    data = json.loads(Path("site_data.json").read_text())
    for i, section in enumerate(data["sections"]):
        start_verse = data["verses"][section["startVerse"]]
        end_verse   = data["verses"][section["endVerse"]]
        print(f"=== Section {i+1}: {section["name"]} ({reference(start_verse, end_verse)}) ===")
        print(''.join(x["text"] for x in data["verses"][section["startVerse"]:section["endVerse"]+1]))

    print(reference(data["verses"][0], data["verses"][1]))
    print(reference(data["verses"][0], data["verses"][100]))


if __name__ == "__main__":
    main()

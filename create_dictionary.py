from yomitandic import DicEntry, Dictionary, create_html_element
import json

def create_dictionary():
    # Create new dictionary
    dictionary = Dictionary("Japanese_Arabic_Dictionary")

    # Read JSON file
    with open('arabicscrapped.json', 'r', encoding='utf-8') as file:
        entries = json.load(file)

    print(f"Found {len(entries)} entries in JSON file")

    # Process entries
    processed = 0
    for entry in entries:
        if 'kanji' in entry and 'meanings' in entry:
            # Split kanji if it contains multiple forms
            kanji_forms = entry['kanji'].split('・')

            # Create definition text
            definition = '\n'.join(entry['meanings'])

            # Create an entry for each kanji form
            for kanji in kanji_forms:
                # Create dictionary entry
                dic_entry = DicEntry(
                    kanji,                    # individual kanji form
                    entry.get('reading', ''), # reading
                    definition=definition     # definition
                )

                # Add examples if available
                if 'examples' in entry and entry['examples']:
                    examples_list = [f"{ex[0]}: {ex[1]}" for ex in entry['examples']]
                    examples_element = create_html_element("div", [
                        create_html_element("div", "例文:"),
                        create_html_element("ul", [
                            create_html_element("li", example) for example in examples_list
                        ])
                    ])
                    dic_entry.add_element(examples_element)

                # Add frequency and JLPT level if available
                meta_info = []
                if 'frequency' in entry:
                    meta_info.append(f"Frequency: {entry['frequency']}")
                if 'jlpt_level' in entry:
                    meta_info.append(f"JLPT: {entry['jlpt_level']}")

                if meta_info:
                    meta_element = create_html_element("div", [
                        create_html_element("span", ' | '.join(meta_info))
                    ])
                    dic_entry.add_element(meta_element)

                # Add entry to dictionary
                dictionary.add_entry(dic_entry)
                processed += 1

            # Print progress every 1000 entries
            if processed % 1000 == 0:
                print(f"Processed {processed} entries...")

    print(f"Processed {processed} entries total")

    # Export and zip the dictionary
    print("Exporting dictionary...")
    dictionary.export()
    print("Zipping dictionary...")
    dictionary.zip()
    print("Dictionary has been created and zipped")

if __name__ == "__main__":
    create_dictionary()

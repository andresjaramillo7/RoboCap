import os
import re
import json
from pathlib import Path
ROOT = Path(os.getcwd()).parents[0]

# Functions to read and process COCO data from .json files

def load_json(path):
    """
    Load a JSON file and return it as a Python dictionary.

    Parameters:
        path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON content.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f) # JSON to Dict

def build_id_to_filename(coco_json):
    """
    Build a dictionary mapping image IDs to their corresponding file names.
    
    Parameters:
        coco_json (dict): Entire COCO annotation JSON.

    Returns:
        dict: Mapping {image_id: file_name}
    """
    # Map id to its filename
    return {img["id"]: img["file_name"] for img in coco_json["images"]}

def group_by_filename(items, id_to_filename, key="image_id"):
    """
    Group a list of annotation items by their image filename.

    Parameters:
        items (list): List of annotation items (dicts).
        id_to_filename (dict): Mapping {image_id: file_name}.
        key (str): The key in each item that holds the image ID. 

    Returns:
        dict: Mapping {file_name: list_of_items}
    """
    grouped = {} # final dict

    for item in items:
        # Extract the image_id from the item
        img_id = item[key]

        # Convert numeric image_id to filename (string)
        filename = id_to_filename[img_id]

        # Create a list if key doesn't exist, then append the item
        grouped.setdefault(filename, []).append(item)

    return grouped

# Function to parse 'captions' from COCO

def parse_captions(json_path):
    """
    Parse a COCO captions annotation file and return a dictionary
    mapping each image filename to its list of captions.

    Parameters:
        json_path (str): Path to COCO captions JSON file.

    Returns:
        dict: {filename: [caption1, caption2, ...]}
    """
    # Load the full COCO JSON
    data = load_json(json_path)

    # Build a helper mapping id to filename
    id_to_filename = build_id_to_filename(data)

    # Extract only the useful fields for captioning
    captions_only = [{"image_id": ann["image_id"], "caption": ann["caption"]} for ann in data["annotations"]]

    # Group captions by image filename
    grouped = group_by_filename(captions_only, id_to_filename)

    # Now convert the grouped structure so each image maps directly
    for filename in grouped:
        grouped[filename] = [x["caption"] for x in grouped[filename]]

    grouped = dict(sorted(grouped.items()))

    # Return the clean final structure
    return grouped

# Function to clean raw captions data

def clean_captions_raw(captions_raw, dedupe=True):
    cleaned = {}
    for fn, caps in captions_raw.items():
        new_caps = []
        seen = set()

        for c in caps:
            c = "" if c is None else str(c)

            # remove \n, \t and normalize spaces
            c = c.replace("\n", " ").replace("\t", " ")
            c = re.sub(r"\s+", " ", c).strip()

            if not c:
                continue

            if dedupe:
                key = c.lower() # basic dedupe
                if key in seen:
                    continue
                seen.add(key)

            new_caps.append(c)

        cleaned[fn] = new_caps
    return cleaned

def load_and_clean_captions(json_path, dedupe=True):
    """
    Load and clean COCO captions from a JSON file.

    Parameters:
        json_path (str): Path to COCO captions JSON file.
        dedupe (bool): Whether to deduplicate captions (case-insensitive).
    Returns:
        dict: {filename: [cleaned_caption1, cleaned_caption2, ...]}
    """
    raw = parse_captions(json_path)
    cleaned = clean_captions_raw(raw, dedupe=dedupe)
    return cleaned
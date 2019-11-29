from pathlib import Path

import argparse
import copy
import extractor
import fontmake.instantiator
import fontTools.designspaceLib
import defcon
import os
import shutil
import ufo2ft
import ufoLib2
import fontTools

# Static vars
BUILD_DIR = Path("build/")
DESIGNSPACE_FILE = "Consolig.designspace"
INPUT_DIR = Path("input/")
INPUT_STYLE_MAP = {
    "Bold": {
        "cascadia_ufo": "CascadiaCode-Regular.ufo",
        "font_file": "consolab.ttf"
    },
    "Bold Italic": {
        "cascadia_ufo": "CascadiaCode-Regular.ufo",
        "font_file": "consolaz.ttf"
    },
    "Italic": {
        "cascadia_ufo": "CascadiaCode-Regular.ufo",
        "font_file": "consolai.ttf"
    },
    "Regular": {
        "cascadia_ufo": "CascadiaCode-Regular.ufo",
        "font_file": "consola.ttf"
    }
}
SOURCES_DIR = Path("sources/")
TEMP_DIR = Path("temp/")


def step_merge_glyphs_from_ufo(path):
    def _merge(instance, added_glyphs):
        ufo = ufoLib2.Font.open(path)
        print(
            f"[{instance.info.familyName} {instance.info.styleName}] Merging glyphs from \"{path}\".")
        for glyph in ufo.glyphOrder:
            if glyph not in instance.glyphOrder and glyph not in added_glyphs:
                instance.addGlyph(ufo[glyph])
                added_glyphs.append(glyph)
    return _merge


def step_set_feature_file(n):
    fea = n.read_text()

    def _set(instance, added_glyphs):
        print(
            f"[{instance.info.familyName} {instance.info.styleName}] Setting feature file from \"{n}\".")
        instance.features.text = fea
    return _set


def build_font_instance(generator, instance_descriptor, *steps):
    instance = generator.generate_instance(instance_descriptor)
    added_glyphs = copy.deepcopy(instance.glyphOrder)
    for step in steps:
        step(instance, added_glyphs)
    setattr(instance.info, "openTypeOS2Panose",
            [2, 11, 6, 9, 2, 0, 0, 2, 0, 4])
    instance.info.openTypeGaspRangeRecords = [
        {
            "rangeMaxPPEM": 9,
            "rangeGaspBehavior": [1, 3]
        },
        {
            "rangeMaxPPEM": 50,
            "rangeGaspBehavior": [0, 1, 2, 3]
        },
        {
            "rangeMaxPPEM": 65535,
            "rangeGaspBehavior": [1, 3]
        },
    ]
    family_name = instance.info.familyName
    style_name = instance.info.styleName
    file_name = f"{family_name}-{style_name}.ttf".replace(" ", "")
    file_path = BUILD_DIR / file_name
    print(f"[{family_name} {style_name}] Compiling font.")
    instance_font = ufo2ft.compileTTF(
        instance, removeOverlaps=False, inplace=True)
    print(f"[{family_name} {style_name}] Saving font.")
    instance_font.save(file_path)
    print(f"[{family_name} {style_name}] Completed font at \"{file_path}\".")


if __name__ == "__main__":
    # Set up temp directory
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCES_DIR / DESIGNSPACE_FILE,
                    TEMP_DIR / DESIGNSPACE_FILE)
    # Load Designspace and filter out instances that are marked as non-exportable.
    designspace = fontTools.designspaceLib.DesignSpaceDocument.fromfile(
        SOURCES_DIR / DESIGNSPACE_FILE)
    designspace.instances = [
        s
        for s in designspace.instances
        if s.lib.get("com.schriftgestaltung.export", True)
    ]
    # Prepare masters.
    generator = fontmake.instantiator.Instantiator.from_designspace(
        designspace)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    step_add_features = step_set_feature_file(SOURCES_DIR / "features.fea")
    for instance_descriptor in designspace.instances:
        print(f"Starting style \"{instance_descriptor.styleName}\".")
        if instance_descriptor.styleName not in INPUT_STYLE_MAP:
            print(
                f"Cannot process instance. Style name \"{instance_descriptor.styleName}\" is not defined in map.")
            continue
        font_file = INPUT_STYLE_MAP[instance_descriptor.styleName]["font_file"]
        print(f"Attempting to extract UFO from \"{font_file}\".")
        if os.path.exists(INPUT_DIR / font_file):
            ufo = defcon.Font()
            extractor.extractUFO(
                (INPUT_DIR / font_file), ufo)
            ufo.save(TEMP_DIR / font_file)
            print(f"UFO extracted successfully.")
        else:
            print(f"Input font file is missing. Skipping.")
            continue
        print(
            f"Beginning build for style \"{instance_descriptor.styleName}\".")
        # Define steps
        step_merge_consolas = step_merge_glyphs_from_ufo(TEMP_DIR / font_file)
        step_merge_cascadia = step_merge_glyphs_from_ufo(
            SOURCES_DIR / INPUT_STYLE_MAP[instance_descriptor.styleName]["cascadia_ufo"])
        # Build font
        build_font_instance(generator, instance_descriptor,
                            step_merge_consolas, step_merge_cascadia, step_add_features)
        print(
            f"Completed build for style \"{instance_descriptor.styleName}\".")
        print("*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***")
    shutil.rmtree(TEMP_DIR)
    print("All build tasks are complete.")

import os
import shutil
import gzip
import pathlib
import json
from bids import layout

def get_versions():
     #collect version from pyproject.toml
    places_to_look = [pathlib.Path(__file__).parent.absolute(), pathlib.Path(__file__).parent.parent.absolute()]

    __version__ = "unable to locate version number in pyproject.toml"
    
    # we use the default version at the time of this writing, but the most current version
    # can be found in the pyproject.toml file under the [tool.bids] section
    __bids_version__ = "1.8.0"
    
    # search for toml file
    for place in places_to_look:
        for root, folders, files in os.walk(place):
            for file in files:
                if file.endswith("pyproject.toml"):
                    toml_file = os.path.join(root, file)

                    with open(toml_file, "r") as f:
                        for line in f.readlines():
                            if "version" in line and len(line.split("=")) > 1 and "bids_version" not in line:
                                __version__ = line.split("=")[1].strip().replace('"', "")
                            if "bids_version" in line and len(line.split("=")) > 1:
                                __bids_version__ = line.split("=")[1].strip().replace('"', "")
                    break
    return {"ingest_pet_version": __version__, "bids_version": __bids_version__}

def zip_nifti(nifti_file):
    """Zips an un-gzipped nifti file and removes the original file."""
    if str(nifti_file).endswith('.gz'):
        return nifti_file
    else:
        with open(nifti_file, 'rb') as infile:
            with gzip.open(nifti_file + '.gz', 'wb') as outfile:
                shutil.copyfileobj(infile, outfile)
        os.remove(nifti_file)
        return nifti_file + '.gz'

def write_out_dataset_description_json(input_bids_dir, output_bids_dir=None):

    # set output dir to input dir if output dir is not specified
    if output_bids_dir is None:
        output_bids_dir = pathlib.Path(os.path.join(input_bids_dir, "derivatives", "petdeface"))
        output_bids_dir.mkdir(parents=True, exist_ok=True)

    # collect name of dataset from input folder
    try:
        with open(os.path.join(input_bids_dir, 'dataset_description.json')) as f:
            source_dataset_description = json.load(f)
    except FileNotFoundError:
        source_dataset_description = {"Name": "Unknown"}

    with open(os.path.join(output_bids_dir, 'dataset_description.json'), 'w') as f:
        dataset_description = {
            "Name": f"petdeface - PET and Anatomical Defacing workflow: "
                    f"PET Defaced Version of BIDS Dataset `{source_dataset_description['Name']}`",
            "BIDSVersion": __bids_version__,
            "GeneratedBy": [
                {"Name": "PET Deface",
                 "Version": __version__,
                 "CodeURL": "https://github.com/bendhouseart/petdeface"}],
            "HowToAcknowledge": "This workflow uses FreeSurfer: `Fischl, B., FreeSurfer. Neuroimage, 2012. 62(2): p. 774-8.`,"
                                "and the MiDeFace package developed by Doug Greve: `https://surfer.nmr.mgh.harvard.edu/fswiki/MiDeFace`",
            "License": "CCBY"
        }

        json.dump(dataset_description, f, indent=4)

def collect_anat(bids_data: pathlib.Path, suffix="T1w"):
    return None

def collect_pet(bids_data: pathlib.Path):
    return None

def 
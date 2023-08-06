# This file is part of the
#   headctools Project (https://gitlab.com/matzkin/headctools).
# Copyright (c) 2021, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/matzkin/headctools/-/blob/master/LICENSE

"""headctools Command Line Interface."""

import warnings
from typing import Optional

import pkg_resources  # part of setuptools
import typer
import typer as t
from ctunet.pytorch.train_test import load_ini_file

from .Preprocessor import preprocess_file_folder
from .antspyregistration import register_file_folder
from .tools.downloader import download_model
from .tools.flap_reconstruction import flap_reconstruction
from .tools.offline_augmentation import simulate_cr_images
from .tools.classic_segmentation import fill_defects

warnings.filterwarnings("ignore")

VERSION = pkg_resources.require("headctools")[0].version

headctools = t.Typer()  # Main CLI

editor = t.Typer()  # Subcommands / Command groups
headctools.add_typer(editor, name="editor")


@headctools.callback()
def headctools_description():
    """headCTools Command Line Interface."""


@headctools.command()
def version():
    """Print headctools version."""
    typer.echo(VERSION)


@headctools.command()
def register(input_ff: str = t.Argument(..., help="File/folder to register"),
             atlas_path: str = t.Argument(..., help="Path of the fixed image"),
             mask_id: Optional[str] = t.Argument(None, help="Mask ID"),
             overwrite: bool = t.Option(False, "--overwrite",
                                        help="Overwrite files in case of "
                                             "existing")):
    """
    Register a single file or the files inside a folder.

    If mask_id is given, it will register the files with that identificator
    with the same transformation as the file without the id.
    """
    register_file_folder(input_ff, atlas_path, mask_id, overwrite)


@headctools.command()
def preprocess(input_ff: str = t.Argument(..., help="Input file or folder"),
               output_folder: Optional[str] = t.Argument(None,
                                                         help="Output folder"),
               prep_type: str = t.Argument('FlapRec', help='Processing tool'),
               image_id: Optional[str] = t.Argument(None),
               mask_id: Optional[str] = t.Argument(None),
               overwrite: bool = t.Option(False, "--overwrite",
                                          help="Overwrite preprocessed images "
                                               "in case they exist")):
    """
    Preprocess a single file or folder.

    It currently supports Flap Reconstruction and Segmentation preprocessing
    types, setting the prep_type option with 'FlapRec' or 'Segmentation'
    respectively (Flap Reconstruction is set by default).

    If the output folder path is not provided, it will create a subfolder in
    the input folder.

    Available preprocessing tools are 'FlapRec' (default) and 'Segmentation'.

    If image_id is set, it will only preprocess the images that match this
    parameter. The same with mask_id: it will apply the same resampling and/or
    registration than the image differing the image and mask ids.
    Example subj001_image.nii.gz and subj001_mask.nii.gz
    """

    preprocess_file_folder(input_ff, output_folder, prep_type, image_id,
                           mask_id, overwrite)


@headctools.command()
def model(ini_file: str = t.Argument(..., help="ini file with the train/test"
                                               "parameters")):
    """
    Run CT-UNet with the configuration set in the ini file.
    """
    load_ini_file(ini_file)


@headctools.command()
def flaprec(input_ff: str = t.Argument(..., help="Input file or folder"),
            out_path: Optional[str] = t.Argument(None, help="Output path"),
            model: str = t.Argument('UNetSP', help="Trained model name"),
            show_intermediate: bool = t.Option(False, "--show_intermediate",
                                               help="Display the images"),
            skip_prepr: bool = t.Option(False, "--skip_prepr",
                                        help="Skip preprocessing"),
            keep_all: bool = t.Option(False, "--keep_all",
                                      help="Omit taking the largest CC")):
    """
    Preprocess the image, predict the bone flap and sum the flap to
    the preprocessed skull.

    The show_intermediate option uses SimpleITK for displaying the images of
    the pipeline. Make sure to set the SITK_SHOW_COMMAND environment variable
    pointing to a CT image viewer program such as itksnap.

    If the images in the folder are already preprocessed, run the command with
    the skip_prepr option, otherwise it will preprocess the CT scan.

    By default, it will take the largest connected component of the
    predicted images. For keeping the entire prediction, use the option
    --keep_all.
    """
    flap_reconstruction(input_ff, out_path, model, show_intermediate,
                        skip_prepr, keep_all)


@headctools.command()
def download(model_name: str = t.Argument(..., help="Trained model name"),
             workspace_path: Optional[str] = t.Argument('~/headctools')):
    """
    Downlaod a previously trained model.

    Download one of the built-in trained models. Currently, the UNetSP
    model for flap/skull reconstruction is available.

    If the headCTools workspace is different than the default, set the
    workspace_path argument.
    """
    download_model(model_name, workspace_path)


@editor.callback()  # Editor subcommands start here
def editor_description():
    """
    Image editor. It contains tools for augmentation/postprocessing.

    Available tools are defgen (Defect Generator) and filldef (Fill Defects).
    See each respective help for more info.
    """


@editor.command()
def defgen(input_ff: str = t.Argument(..., help="Input file or folder"),
           out_folder: str = t.Argument(..., help="Output path"),
           n_reps: int = t.Argument(10, help="Number of generated images"),
           image_id: str = t.Argument('image', help="Image identificator")):
    """
    Generate defects of the input file/folder.

    n_reps controls how many virtual craniectomies will be generated for
    each image.
    If the images have an id in the name, it can be provided in the image_id
    argument.
    """
    simulate_cr_images(input_ff, n_reps, image_id, out_folder)


@editor.command()
def filldef(input_ff: str = t.Argument(..., help="Input file or folder")):
    """
    Fill defects on images.
    It calculates the convex hull on binary masks and then fills the holes
    inside them.
    """
    fill_defects(input_ff)


@editor.command()
def retaincc(input_ff: str = t.Argument(..., help="Input file or folder")):
    """
    Retain the largest connected component of the file(s).
    """
    largest_cc(input_ff)


if __name__ == "__main__":
    headctools()

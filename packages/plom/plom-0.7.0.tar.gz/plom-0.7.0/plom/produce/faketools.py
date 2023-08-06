# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2019-2021 Colin B. Macdonald
# Copyright (C) 2020 Andrew Rechnitzer
# Copyright (C) 2020 Vala Vakilian
# Copyright (C) 2020 Dryden Wiebe

"""Plom tools for scribbling fake answers on PDF files"""

__copyright__ = "Copyright (C) 2019-2021 Andrew Rechnitzer, Colin B. Macdonald, et al"
__credits__ = "The Plom Project Developers"
__license__ = "AGPL-3.0-or-later"

import os
import random
from pathlib import Path
from glob import glob
import argparse
import json
import base64
import sys

if sys.version_info >= (3, 7):
    import importlib.resources as resources
else:
    import importlib_resources as resources

import fitz
from stdiomask import getpass

import plom.produce
from plom.produce import paperdir as _paperdir
from plom import __version__
from plom.messenger import ManagerMessenger
from plom.plom_exceptions import PlomExistingLoginException


# load the digit images
digit_array = json.loads(resources.read_text(plom.produce, "digits.json"))
# how many of each digit were collected
number_of_digits = len(digit_array) // 10
assert len(digit_array) % 10 == 0


possible_answers = [
    "I am so sorry, I really did study this... :(",
    "I know this, I just can't explain it",
    "Hey, at least its not in Comic Sans",
    "Life moves pretty fast. If you don't stop and look around once in a while, "
    "you could miss it.  -- Ferris Bueler",
    "Stupid is as stupid does.  -- Forrest Gump",
    "Of course, it is very important to be sober when you take an exam.  "
    "Many worthwhile careers in the street-cleansing, fruit-picking and "
    "subway-guitar-playing industries have been founded on a lack of "
    "understanding of this simple fact.  -- Terry Pratchett",
    "The fundamental cause of the trouble in the modern world today is that "
    "the stupid are cocksure while the intelligent are full of doubt.  "
    "-- Bertrand Russell",
    "Numbers is hardly real and they never have feelings\n"
    "But you push too hard, even numbers got limits.  -- Mos Def",
    "I was doin' 150 miles an hour sideways\n"
    "And 500 feet down at the same time\n"
    "I was lookin' for the cops, 'cuz you know\n"
    "I knew that it, it was illegal  -- Arlo Guthrie",
    "But there will always be science, engineering, and technology.  "
    "And there will always, always be mathematics.  -- Katherine Johnson",
    "Is 5 = 1?  Let's see... multiply both sides by 0.  "
    "Now 0 = 0 so therefore 5 = 1.",
    "I mean, you could claim that anything's real if the only basis for "
    "believing in it is that nobody's proved it doesn't exist!  -- Hermione Granger",
]


def fill_in_fake_data_on_exams(paper_dir_path, classlist, outfile, which=None):
    """Fill-in exams with fake data for demo or testing.

    Arguments:
        paper_dir_path (str/pathlib.Path): Directory containing the blank exams.
        classlist (list): ordered list of (sid, sname) pairs.
        outfile (str/pathlib.Path): write results into this concatenated PDF file.

    Keyword Arguments:
        which: by default ("`which=None`") scribble on all exams or specify
            something like `which=range(10, 16)` to scribble on a subset.
    """

    # Customizable data
    blue = [0, 0, 0.75]
    student_number_length = 8
    extra_page_probability = 0.2
    digit_font_size = 24
    answer_font_size = 13
    extra_page_font_size = 18

    # We create the path objects
    paper_dir_path = Path(paper_dir_path)
    out_file_path = Path(outfile)

    print("Annotating papers with fake student data and scribbling on pages...")
    if not which:
        named_papers_paths = glob(
            str(paper_dir_path / "exam_*_*.pdf")
        )  # those with an ID number
        papers_paths = sorted(glob(str(paper_dir_path / "exam_*.pdf")))  # everything
    else:
        papers_paths = sorted(
            [
                paper_dir_path / "exam_{}.pdf".format(str(index).zfill(4))
                for index in which
            ]
        )

    used_id_list = []
    # need to avoid any student numbers already used to name papers - look at file names
    for index, file_name in enumerate(named_papers_paths):
        used_id_list.append(os.path.split(file_name)[1].split(".")[0].split("_")[-1])
    # now load in the student names and numbers -only those not used to prename
    clean_id_dict = {}  # not used
    for sid, sname in classlist:
        if sid not in used_id_list:
            clean_id_dict[sid] = sname

    # now grab a random selection of IDs from the dict.
    # we need len(papers_paths) - len(named_papers_paths) of them
    id_sample = random.sample(
        list(clean_id_dict.keys()), len(papers_paths) - len(named_papers_paths)
    )

    # A complete collection of the pdfs created
    all_pdf_documents = fitz.open()

    clean_count = 0
    for index, file_name in enumerate(papers_paths):
        if file_name in named_papers_paths:
            print("{} - prenamed paper - scribbled".format(os.path.basename(file_name)))
        else:
            student_number = id_sample[clean_count]
            student_name = clean_id_dict[student_number]
            clean_count += 1
            print(
                "{} - scribbled using {} {}".format(
                    os.path.basename(file_name), student_number, student_name
                )
            )

        # TODO: could do `with fitz.open(file_name) as pdf_document:`
        pdf_document = fitz.open(file_name)
        front_page = pdf_document[0]

        # First we input the student names
        if file_name not in named_papers_paths:  # can draw on front page
            # insert digit images into rectangles - some hackery required to get correct positions.
            width = 28
            border = 8
            for digit_index in range(student_number_length):
                rect1 = fitz.Rect(
                    220 + border * digit_index + width * digit_index,
                    265,
                    220 + border * digit_index + width * (digit_index + 1),
                    265 + width,
                )
                uuImg = digit_array[
                    int(student_number[digit_index]) * number_of_digits
                    + random.randrange(number_of_digits)
                ]  # uu-encoded png
                img_BString = base64.b64decode(uuImg)
                front_page.insert_image(rect1, stream=img_BString, keep_proportion=True)
                # TODO - there should be an assert or something here?

            digit_rectangle = fitz.Rect(228, 335, 550, 450)
            excess = front_page.insert_textbox(
                digit_rectangle,
                student_name,
                fontsize=digit_font_size,
                color=blue,
                fontname="Helvetica",
                fontfile=None,
                align=0,
            )
            assert excess > 0

        # Write some random answers on the pages
        for page_index, pdf_page in enumerate(pdf_document):
            random_answer_rect = fitz.Rect(
                100 + 30 * random.random(), 150 + 20 * random.random(), 500, 500
            )
            random_answer_text = random.choice(possible_answers)

            # TODO: "helv" vs "Helvetica"
            if page_index >= 1:
                excess = pdf_page.insert_textbox(
                    random_answer_rect,
                    random_answer_text,
                    fontsize=answer_font_size,
                    color=blue,
                    fontname="helv",
                    fontfile=None,
                    align=0,
                )
                assert excess > 0

        # delete last page from the zeroth test.
        if index == 0:
            pdf_document.delete_page(-1)
            print("Deleting last page of test {}".format(file_name))

        # We then add the pdfs into the document collection
        all_pdf_documents.insert_pdf(pdf_document)

        # For a comprehensive test, we will add some extrapages with the probability of 0.2 percent
        if random.random() < extra_page_probability:
            # folder_name/exam_XXXX.pdf or folder_name/exam_XXXX_YYYYYYY.pdf,
            # file_pdf_name drops the folder name and the .pdf parts
            file_pdf_name = os.path.splitext(os.path.basename(file_name))[0]

            # Then we get the test number and student_number from file_pdf_name
            test_number = file_pdf_name.split("_")[1]
            if (
                file_name in named_papers_paths
            ):  # file_pdf_name is exam_XXXX_YYYYYYY.pdf
                student_number = file_pdf_name.split("_")[2]

            print(
                "  making an extra page for test {} and sid {}".format(
                    test_number, student_number
                )
            )
            all_pdf_documents.insert_page(
                -1,
                text="EXTRA PAGE - t{} Q1 - {}".format(test_number, student_number),
                fontsize=extra_page_font_size,
                color=blue,
            )

    all_pdf_documents.save(out_file_path)
    print('Assembled in "{}"'.format(out_file_path))


def make_garbage_pages(out_file_path, number_of_garbage_pages=2):
    """Randomly generates and inserts garbage pages into a PDF document.

    Used for testing.

    Arguments:
        out_file_path (pathlib.Path/str): a pdf file we add pages to.

    Keyword Arguments:
        number_of_garbage_pages (int): how many junk pages to add (default: 2)
    """
    green = [0, 0.75, 0]

    all_pdf_documents = fitz.open(out_file_path)
    print("Doc has {} pages".format(len(all_pdf_documents)))
    for _ in range(number_of_garbage_pages):
        garbage_page_index = random.randint(-1, len(all_pdf_documents))
        print("Insert garbage page at garbage_page_index={}".format(garbage_page_index))
        all_pdf_documents.insert_page(
            garbage_page_index, text="This is a garbage page", fontsize=18, color=green
        )
    all_pdf_documents.saveIncr()


def make_colliding_pages(paper_dir_path, outfile):
    """Build two colliding pages - last pages of papers 2 and 3.

    Arguments:
        paper_dir_path (str/pathlib.Path): Directory containing the blank exams.
        out_file_path (str/pathlib.Path): write results into this concatenated PDF file.

    Purely used for testing.
    """
    paper_dir_path = Path(paper_dir_path)
    out_file_path = Path(outfile)

    all_pdf_documents = fitz.open(out_file_path)
    # Customizable data
    blue = [0, 0, 0.75]
    colliding_page_font_size = 18

    papers_paths = sorted(glob(str(paper_dir_path / "exam_*.pdf")))
    for file_name in papers_paths[1:3]:  # just grab papers 2 and 3.
        pdf_document = fitz.open(file_name)
        test_length = len(pdf_document)
        colliding_page_index = random.randint(-1, len(all_pdf_documents))
        print(
            "Insert colliding page at colliding_page_index={}".format(
                colliding_page_index
            )
        )
        all_pdf_documents.insert_pdf(
            pdf_document,
            from_page=test_length - 1,
            to_page=test_length - 1,
            start_at=colliding_page_index,
        )
        excess = all_pdf_documents[colliding_page_index].insert_textbox(
            fitz.Rect(100, 100, 500, 500),
            "I was dropped on the floor and rescanned.",
            fontsize=colliding_page_font_size,
            color=blue,
            fontname="helv",
            fontfile=None,
            align=0,
        )
        assert excess > 0

    all_pdf_documents.saveIncr()


def splitFakeFile(out_file_path):
    """Split the scribble pdf into three files"""

    print("Splitting PDF into 3 in order to test bundles.")
    originalPDF = fitz.open(out_file_path)
    newPDFName = os.path.splitext(out_file_path)[0]
    length = len(originalPDF) // 3

    doc1 = fitz.open()
    doc2 = fitz.open()
    doc3 = fitz.open()

    doc1.insert_pdf(originalPDF, from_page=0, to_page=length)
    doc2.insert_pdf(originalPDF, from_page=length + 1, to_page=2 * length)
    doc3.insert_pdf(originalPDF, from_page=2 * length + 1)

    doc1.save(newPDFName + "1.pdf")
    doc2.save(newPDFName + "2.pdf")
    doc3.save(newPDFName + "3.pdf")

    os.unlink(out_file_path)


def download_classlist(server=None, password=None):
    """Download list of student IDs/names from server."""
    if server and ":" in server:
        s, p = server.split(":")
        msgr = ManagerMessenger(s, port=p)
    else:
        msgr = ManagerMessenger(server)
    msgr.start()

    if not password:
        password = getpass('Please enter the "manager" password: ')

    try:
        msgr.requestAndSaveToken("manager", password)
    except PlomExistingLoginException:
        print(
            "You appear to be already logged in!\n\n"
            "  * Perhaps a previous session crashed?\n"
            "  * Do you have another management tool running,\n"
            "    e.g., on another computer?\n\n"
            'In order to force-logout the existing authorisation run "plom-build clear"'
        )
        raise
    try:
        classlist = msgr.IDrequestClasslist()
    finally:
        msgr.closeUser()
        msgr.stop()
    return classlist


def main():
    """Main function used for running.

    1. Generates the files.
    2. Creates the fake data filled pdfs using fill_in_fake_data_on_exams.
    3. Deletes from the pdf file using delete_one_page.
    4. We also add some garbage pages using delete_one_page.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument("-s", "--server", metavar="SERVER[:PORT]", action="store")
    parser.add_argument("-w", "--password", type=str, help='for the "manager" user')
    args = parser.parse_args()

    if not hasattr(args, "server") or not args.server:
        try:
            args.server = os.environ["PLOM_SERVER"]
        except KeyError:
            pass
    if not hasattr(args, "password") or not args.password:
        try:
            args.password = os.environ["PLOM_MANAGER_PASSWORD"]
        except KeyError:
            pass

    out_file_path = "fake_scribbled_exams.pdf"
    classlist = download_classlist(args.server, args.password)

    fill_in_fake_data_on_exams(_paperdir, classlist, out_file_path)
    make_garbage_pages(out_file_path)
    make_colliding_pages(_paperdir, out_file_path)
    splitFakeFile(out_file_path)


if __name__ == "__main__":
    main()

import os
import filetype
import matplotlib.pyplot as plt
import difflib
import textract
from docx import Document
from difflib import SequenceMatcher
from datetime import datetime
import subprocess

desktop_path = os.path.expanduser("~/Desktop")

# Plotting visualisation
def plot_pie_chart(file_types, title):
    labels = file_types.keys()
    sizes = [count for count in file_types.values()]
    explode = [0.1] * len(labels)

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(title)
    plt.show()


# Classify files by extension
def classify_files_by_extension(path):
    file_types = {}
    total_files = 0
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            kind = filetype.guess(item_path)
            if kind:
                ext = kind.extension.lower()
                file_types[ext] = file_types.get(ext, 0) + 1
                total_files += 1
    return file_types, total_files


def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = " ".join(para.text for para in doc.paragraphs)
    return text


def extract_text_from_pdf(pdf_path):
    try:
        text = textract.process(pdf_path).decode('utf-8')
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def calculate_similarity(text1, text2):
    return difflib.SequenceMatcher(None, text1, text2).ratio()


def should_ignore_file(file_name):
    ignored_extensions = ['.lnk']
    ignored_filenames = ['Adobe Media Encoder']
    file_ext = os.path.splitext(file_name)[1].lower()
    if file_ext in ignored_extensions or any(filename in file_name for filename in ignored_filenames):
        return True
    return False


file_type_counts, total_files = classify_files_by_extension(desktop_path)
labels = file_type_counts.keys()
sizes = [count for count in file_type_counts.values()]
explode = [0.1] * len(labels)

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title("File Type Distribution on Desktop Before Removal")
plt.show()

def find_similar_files(file_list):
    similar_files = []
    for i in range(len(file_list)):
        for j in range(i + 1, len(file_list)):
            path1 = os.path.join(desktop_path, file_list[i])
            path2 = os.path.join(desktop_path, file_list[j])
            similarity_ratio = SequenceMatcher(None, path1, path2).ratio()
            if similarity_ratio >= 0.7:
                similar_files.append((file_list[i], file_list[j]))
    return similar_files


desktop_files = [item for item in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, item))]
similar_files = find_similar_files(desktop_files)

print("Similar File Pairs:")
for pair in similar_files:
    file1, file2 = pair
    path1 = os.path.join(desktop_path, file1)
    path2 = os.path.join(desktop_path, file2)

    if should_ignore_file(file1) or should_ignore_file(file2):
        print(f"Ignoring files: {file1} or {file2}")
        continue

    if not os.path.exists(path1) or not os.path.exists(path2):
        print(f"File does not exist: {file1} or {file2}")
        continue

    last_modified1 = datetime.fromtimestamp(os.path.getmtime(path1))
    last_modified2 = datetime.fromtimestamp(os.path.getmtime(path2))

    print(f"Similar Pair: {pair}")
    print(f"First Modified Date: {min(last_modified1, last_modified2)}")
    print(f"Last Modified Date: {max(last_modified1, last_modified2)}")
    print()

user_opt = int(input("Do you want to move the older duplicates to a folder? Yes = 1 and No = 2: "))
if user_opt == 1:
    foldername = input("Enter the folder name: ").strip()
    misc_folder = os.path.join(desktop_path, foldername)
    if not os.path.exists(misc_folder):
        os.makedirs(misc_folder)
    else:
        print(f"Folder '{foldername}' already exists. Overwriting...")

    moved_files = []

    for pair in similar_files:
        file1, file2 = pair
        path1 = os.path.join(desktop_path, file1)
        path2 = os.path.join(desktop_path, file2)

        if should_ignore_file(file1) or should_ignore_file(file2):
            print(f"Ignoring files: {file1} or {file2}")
            continue

        if not os.path.exists(path1) or not os.path.exists(path2):
            print(f"File does not exist: {file1} or {file2}")
            continue

        last_modified1 = datetime.fromtimestamp(os.path.getmtime(path1))
        last_modified2 = datetime.fromtimestamp(os.path.getmtime(path2))

        source_path = path1 if last_modified1 < last_modified2 else path2
        destination_path = os.path.join(misc_folder, os.path.basename(source_path))

        if os.path.basename(source_path) not in moved_files:
            os.rename(source_path, destination_path)
            print(f"Moved to 'misc' folder: {destination_path}")
            moved_files.append(os.path.basename(source_path))
        else:
            print(f"File '{os.path.basename(source_path)}' already moved. Skipping...")

    subprocess.run(["explorer", os.path.abspath(misc_folder)])
else:
    print("Not removing")

if len(similar_files) == 0:
    print("No similar files found")

updated_file_type_counts, _ = classify_files_by_extension(desktop_path)
plot_pie_chart(updated_file_type_counts, "File Type Distribution on Desktop After Removal")



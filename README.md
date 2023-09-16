# PyDeskTidy
This project focuses on duplicate files that have been created by us daily user for any file type. The theory is simple as it focuses on naming scheme of each file as well as its last date modeified (recent edition). Logically `HERISH_RESUME_FINALE.docx (22/01/2023)` is the latest edition compared to `HERISH_RESUME_FINAL.docx (01/01/23)`. The problem arises with the name scheme used `FINALE/FINAL` ; to sort this I have implemnted a preset score to detect similiarty (70% as tested). This score will return true if both files are having simliar names to 70%. 

## Features:

- **Duplicate Detection:** PyDeskTidy intelligently detects duplicates based on file names and modification dates. It uses a preset similarity score threshold of 70% to determine similarity.

- **Supported File Types:** PyDeskTidy currently supports several common file types, including docx, jpeg, jpg, pdf, img, pptx, and zip.

- **Customizable Exclusions:** You can customize the script to exclude specific file types like shortcuts (lnk) to avoid accidental removal.

- **File Movement:** PyDeskTidy offers the option to move all detected miscellaneous files to a folder of your choice, helping you keep your desktop clutter-free.

## Screenshots:

### Exclusions Config:
![Exclusions Configuration](https://github.com/herish23/PyDeskTidy/assets/87555721/c2614d1b-755f-48f3-9092-03f3a79621fe)

### File Mv:
![File Movement](https://github.com/herish23/PyDeskTidy/assets/87555721/62e12037-513c-4228-a13e-4a77f787a0fc)

## File Distribution Insights :

Before and after using PyDeskTidy, you can visualize the distribution of file types on your desktop.

![File Type Distribution](https://github.com/herish23/PyDeskTidy/assets/87555721/1c46239c-bd12-4079-8b5e-12dacc4f6a92)

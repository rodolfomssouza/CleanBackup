# CleanDupFiles

Remove duplicated and hidden files.

The goal of this algorithm is to check duplicated files and
remove duplicates across multiple directories. It is recommended to
run in a backup folder. This algorithm comes with **NO WARRANTY**.

A list of files checksum a directory will be created.
After that, python will check by duplicated checksums and export
a list of files to be deleted. Finally, the hidden files and empty
directores will also be deleted.

# Requirements
- Python 3.90 or greater;
- pandas;
- rharsh.

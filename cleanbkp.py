"""
Check and remove duplicated and hidden files
"""

# %% Packages
import pandas as pd
import os


# %% Class

class RemoveDups:

    def __init__(self, dir):
        self.df2del = None
        self.dfall = None
        self.dfhidden = None
        self.dir = dir
        self.get_dup_list()
        self.read_results()
        self.get_files_difference()
        pass

    def delete_hidden_files(self):
        os.system(
            f"find {self.dir}/ -name '.*' > results_hidden_files.txt")
        try:
            df1 = pd.read_table("results_hidden_files.txt", header=None)
            self.dfhidden = df1
            for i in range(len(self.dfhidden)):
                r = self.dfhidden.loc[i].to_list()[0]
                r = r.replace("//", "/")
                if os.path.exists(r):
                    os.remove(r)
                    print(f"Deleted: {r}")
                else:
                    print("File does not exists")
                pass
        except:
            pass
        
        pass

    def delete_empty_dir(self):
        self.delete_hidden_files()
        n = 1
        while n > 0:
            os.system(
                f"find {self.dir}/ -type d -empty > results_empty_dir.txt")
            try:
                df1 = pd.read_table("results_empty_dir.txt", header=None)
                if len(df1) > 0:
                    for i in range(len(df1)):
                        r = df1.loc[i].to_list()
                        r = r[0].replace("//", "/")
                        if os.path.exists(r):
                            os.rmdir(r)
                        else:
                            pass
                        pass
                    pass
                else:
                    n = 0
                pass
            except:
                break
            pass
        pass

    def get_dup_list(self):
        """
        Runs rhash command to get list of checksums
        """
        if os.path.exists("results_checksum.txt"):
            print("Checksum list exists. Please verify and remove or rename the file.")
            self.read_results()
            print(self.dfall.head())
        else:
            os.system(
                f"rhash --md5 -p '%h,%p\n' -r {self.dir}/ > results_checksum.txt")
        pass

    def read_results(self):
        """
        Creates a list of files to be deleted
        """
        df1 = pd.read_table("results_checksum.txt", sep=",", header=None)
        df1.columns = ["checksum", "file"]
        self.dfall = df1
        pass

    def get_files_difference(self):
        df1 = self.dfall.drop_duplicates(subset="checksum")
        df2 = pd.concat([self.dfall, df1]).drop_duplicates(keep=False)
        df2 = df2.reset_index(drop=True)
        df1.to_csv("list_files_to_keep.csv", index=False)
        df2.to_csv("list_files_to_be_deleted.csv", index=False)
        self.df2del = df2
        pass

    def delete_files(self):
        for i in range(len(self.df2del)):
            r = str(self.df2del.loc[i].file)
            if os.path.exists(r):
                os.remove(r)
                print(f"Deleted: {r}")
            else:
                print("File does not exists")
            pass
        pass

    # End class
    pass


# %% Main
if __name__ == "__main__":
    g = RemoveDups("Downloads")
    g.delete_files()
    g.delete_empty_dir()
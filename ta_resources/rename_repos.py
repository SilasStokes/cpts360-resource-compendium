
from email import header
import os
import sys
import csv

def main():
    cwd = os.getcwd()
    if (len(sys.argv) < 2):
        print('Pass a roster file, downloaded from GitHub Classroom')

    if (len(sys.argv) == 3):
        cwd += '/'
        if ".csv" in sys.argv[1]:
            cwd += sys.argv[2]
            roster_file = sys.argv[1];
        else:
            cwd += sys.argv[1]
            roster_file = sys.argv[2]
        os.chdir(cwd);
    else:
        roster_file = sys.argv[1];

    directories = os.listdir(cwd)
    
    missing_dir = open("missing_students.txt", "w+")
    with open(roster_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            name = row[0]
            name= name.replace("'", '')
            name= name.replace(" ", '')
            github_usr = row[1] # os.rename(src, dst)
            if github_usr in directories:
                os.rename(github_usr, name)
            else:
                missing_dir.write("missing student: {} \t\t github username: {}\n".format(name, github_usr));


if __name__ == "__main__":
    main()






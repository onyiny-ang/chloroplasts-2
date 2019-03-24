#!/usr/bin/python3
import pytest
from pytest_postgresql import factories

import sys
import os
import psycopg2
import tkinter as tk

from tkinter import messagebox
from os import listdir
from os.path import join


postgresql_my_proc = factories.postgresql_proc( host="localhost", database="clientserver", user="user", password="password", port = None, logsdir='/tmp')
postgresql_my = factories.postgresql('postgresql_my_proc')

def test_scrub(postgresql_my):
    destinationFolder='fake-data/tmp'
    if not os.path.exists('fake-data/tmp'):
        xfail("fake-data/tmp is not present in your current folder but should be")

    unScrubbedFolders = ""
    numOfUnscrubbedFolders = 0

    for section in listdir('fake-data'):
        os.mkdir(join(destinationFolder, section))
        if section == "Current Year" or section == "Previous Years":
        for studentSubmission in listdir(join(folder, section)):
            try:
                #take note of each folder you are going into
                studentSubmissionFolder = join(join(folder, section), studentSubmission)

                #get the names in plain english, and save them to variables
                firstName, lastName, stdNum = studentSubmission.split("_")

                #save the hash vaules of the 3 variables from above
                hashFirstName = str(hash(firstName))
                hashLastName = str(hash(lastName))
                hashStdNum = str(hash(stdNum))

                #create directory to save the scrubbed data to
                scrubbedStudentFolder = join(join(destinationFolder, section), hashFirstName+"_"+hashLastName+"_"+hashStdNum)

                #Create the folder so the files have somewhere to go
                os.mkdir(scrubbedStudentFolder)

                # save hash in the database HERE
                try:
                    cur.execute("INSERT INTO \"StudentHashMapping\" (\"Hash_Firstname\", \"Hash_Lastname\", " +
                                "\"Hash_StudentNumber\", \"Firstname\", \"Lastname\", \"StudentNumber\") VALUES " +
                                "(%s, %s, %s, %s, %s, %s);", (hashFirstName, hashLastName, hashStdNum, firstName, lastName, str(stdNum)))
                except:
                    #does not exit the program, we want to process all the student submissions that we can
                    sys.exit("Unable to insert into database")

                #Loop through each file in the student submission folder and replace identifying info
                for root, directory, files in os.walk(studentSubmissionFolder):
                    for filename in files:
                        if filename.endswith(".java") or filename.endswith(".cpp") or filename.endswith(".c") \
                                or filename.endswith(".hpp") or filename.endswith(".h"):
                            #scrub data
                            f = open(join(root, filename)).read()
                            replace = f.replace(firstName, hashFirstName).replace(lastName, hashLastName)\
                                .replace(stdNum, hashStdNum)
                            #write to scrubbed file
                            newFolder = join(scrubbedStudentFolder, "Scrubbed-"+filename)
                            newF = open(newFolder, 'w')
                            newF.write(replace)
                            newF.close()
            except:
                #this code will be executed if the folder is not named properly
                unScrubbedFolders = "\t" + studentSubmission + "\n"
                numOfUnscrubbedFolders = numOfUnscrubbedFolders + 1

#if any folder causes an exception, then show an alert at the end with the summary
if numOfUnscrubbedFolders == 1:
    alertMessage = "A submission was not able to be scrubbed. It is listed below:\n"
    alertMessage = alertMessage + unScrubbedFolders
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning('ALERT', alertMessage)
elif numOfUnscrubbedFolders > 1:
    alertMessage = str(numOfUnscrubbedFolders)+" submissions were not able to be scrubbed. They are listed below:\n"
    alertMessage = alertMessage + unScrubbedFolders
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning('ALERT', alertMessage)

conn.commit()

#close the database connection
if conn is not None:
    conn.close()

#completed successfully
sys.exit(None)


#Loop through each file in the student submission folder and replace identifying info
                for filename in listdir(studentSubmissionFolder):
                    if filename.endswith(".java") or filename.endswith(".cpp") or filename.endswith(".c") \
                            or filename.endswith(".hpp") or filename.endswith(".h"):
                        #scrub data
                        f = open(join(studentSubmissionFolder, filename)).read()
                        replace = f.replace(firstName, hashFirstName).replace(lastName, hashLastName)\
                            .replace(stdNum, hashStdNum)
                        #write to scrubbed file
                        newFolder = join(scrubbedStudentFolder, "Scrubbed-"+filename)
                        newF = open(newFolder, 'w')
                        newF.write(replace)
                        newF.close()
            except:
                #this code will be executed if the folder is not named properly
                unScrubbedFolders = "\t" + studentSubmission + "\n"
                numOfUnscrubbedFolders = numOfUnscrubbedFolders + 1

#if any folder causes an exception, then show an alert at the end with the summary
if numOfUnscrubbedFolders == 1:
    alertMessage = "A submission was not able to be scrubbed. It is listed below:\n"
    alertMessage = alertMessage + unScrubbedFolders
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning('ALERT', alertMessage)
elif numOfUnscrubbedFolders > 1:
    alertMessage = str(numOfUnscrubbedFolders)+" submissions were not able to be scrubbed. They are listed below:\n"
    alertMessage = alertMessage + unScrubbedFolders
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning('ALERT', alertMessage)

conn.commit()

#close the database connection
if conn is not None:
    conn.close()

#completed successfully
sys.exit(None)

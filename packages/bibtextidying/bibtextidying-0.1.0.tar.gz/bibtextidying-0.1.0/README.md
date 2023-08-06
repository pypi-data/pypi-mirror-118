#-- bibtextidying 0.1.0 --

Author: Jian Ding and ShiBo Xu and Kun Chen
Email: 937207118@qq.com
Mentor: X. Fu and TingYu Luo

##[Purpose]
This software is trying to help users to tidy up their bibtex files.

##[Prerequisite]
- Python3
- MySQL

##[Requires Projects]
- bibtexparser
- mysqlclient

##[Github]
https://gitee.com/chen-kun19/summer-program

##[Manual]
- **How to install it?**
  - use command following.
    - For Windows 
    ```PowerShell
    pip install bibtextidying
    ```
    - For Linux
    ```PowerShell
    sudo apt-get update
    sudo apt-get install libmysqlclient-dev
    sudo pip install mysqlclient
    pip install bibtextidying
    ```
- **How to use it?**
  - Type following code in your python files:
    ```PowerShell
    from finalbib import bibtextidying
    ```
- **Then you can use all the function in module bibcopy!**
  - this function give you an interface to use all the eight functions
    ```PowerShell
    bibtextidying.comprehensive()
    ```
  - and maybe you will use a specific function, we have:
    ```PowerShell
    bibtextidying.pythonlist("filename")
    bibtextidying.checkintegrity("filename")
    bibtextidying.checkconflicts("filename")
    bibtextidying.merge("filename1","filename2")
    bibtextidying.formating("filename")
    bibtextidying.keyword("filename")
    bibtextidying.database_storage("filename","host","username","password","database")
    bibtextidying.database_query("bib_filename","entry","fields","host","user_name","passward","database")
    ```
##[Function]
```PowerShell
1. Resolves the bib_file to a list form.Give it a filename, then it tells you the information about the bibfile.
2. Checks whether the field provided by the file entry is complete.Give it a filename, it can check the field depends on the type of each entry.
3. Checks the same article whether there are more than the same items, remove the same items, if there are conflicts prompted conflict information.Just fill the filename, you can use it.
4. Synthesizes the two files into a single file, outputting is filename1_filename2.bib.
5. Formats the file.Make the file looks more tidy.
6. Uniform file keyword style.Like name2000articlename.
7. Stores a database of the specified type.7 and 8 function need users have database account or access.
8. Outputs domain information of the specified type for the specified type entry in the database, and generates bib_file.
```
##[Bug Report]:
Any bug or documentation error you found , please submit an issue on github parge: https://gitee.com/chen-kun19/summer-program
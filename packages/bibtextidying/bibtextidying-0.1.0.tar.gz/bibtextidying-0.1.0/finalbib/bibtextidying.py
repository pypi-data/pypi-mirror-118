import bibtexparser as bp
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode, author
import operator
import MySQLdb

# 参考 http://blog.sina.com.cn/s/blog_4fa8810401013gpw.html
# 必要域
RequiredFields = {
    "article": ["author", "title", "journal", "year"],
    "book": ["author/editor", "title", "publisher", "year"],
    "booklet": ["title"],
    "conference": ["author", "title", "booktitle", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "inbook": ["author/editor", "title", "chapter/pages", "publisher", "year"],
    "incollection": ["author", "title", "booktitle", "publisher", "year"],
    "manual": ["title"],
    "mastersthesis": ["author", "title", "school", "year"],
    "misc": [],
    "phdthesis": ["author", "title", "year", "school"],
    "proceedings": ["title", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "unpublished": ["author", "title", "note"]}

# 限制域
LimitedFields = {
    "article": ["author", "title", "journal", "year", "volume", "number", "pages", "month", "note", "ENTRYTYPE", "ID"],
    "book": ["author", "editor", "title", "publisher", "year", "volume", "number", "series", "address", "edition", "month", "note", "ENTRYTYPE", "ID"],
    "booklet": ["title", "author", "howpublished", "address", "month", "year", "note"],
    "conference": ["author", "title", "booktitle", "year", "editor", "volume", "number", "series", "pages", "address", "month", "organization", "publisher", "note", "ENTRYTYPE", "ID"],
    "inproceedings": ["author", "title", "booktitle", "year", "editor", "volume", "number", "series", "pages", "address", "month", "organization", "publisher", "note", "ENTRYTYPE", "ID"],
    "inbook": ["author", "editor", "title", "chapter", "pages", "publisher", "year", "volume", "number", "series", "type", "address", "edition", "month", "note", "ENTRYTYPE", "ID"],
    "incollection": ["author", "title", "booktitle", "publisher", "year", "editor", "volume", "number", "series", "type", "chapter", "pages", "address", "edition", "month", "note", "ENTRYTYPE", "ID"],
    "manual": ["title", "author", "organization", "address", "edition", "month", "year", "note", "ENTRYTYPE", "ID"],
    "mastersthesis": ["author", "title", "school", "year", "type", "address", "month", "note", "ENTRYTYPE", "ID"],
    "misc": ["author", "title", "howpublished", "month", "year", "note", "ENTRYTYPE", "ID"],
    "phdthesis": ["author", "title", "year", "school", "address", "month", "keywords", "note", "ENTRYTYPE", "ID"],
    "proceedings": ["title", "year", "editor", "volume", "number", "series", "address", "month", "organization", "publisher", "note", "ENTRYTYPE", "ID"],
    "techreport": ["author", "title", "institution", "year", "type", "number", "address", "month", "note", "ENTRYTYPE", "ID"],
    "unpublished": ["author", "title", "note", "month", "year", "ENTRYTYPE", "ID"]}

# 初步格式化
def pretreatment(record):
    """
    该函数实现了两个功能（可根据需要自由添加）：
    1、将'author'种的'and'，'\n'，'\\'去除；
    2、进行了各个条目的预处理
    """
    # 'author' 格式化
    if 'author' in record:
        if record['author']:
            record['author'] = record['author'].replace('\n', ' ')
        else:
            record['author'] = ''
    return record

# 将record letex 编码转换为 unicode 编码并且修改 'author' 格式
def convert_pretreatment(record):
    """
    1、将 record letex 编码转换为 unicode 编码；
    2、执行了 author_pretreatment 函数的功能。
    """
    record = convert_to_unicode(record)
    record = pretreatment(record)
    record = author(record)
    return record

# 判断两个作者是否相同
def author_eq(author_1, author_2):
    pre_1 = author_1.lower().split(',')
    pre_2 = author_2.lower().split(',')
    if len(pre_1[1].split()) == len(pre_2[1].split()):
        flag = 1
        for i in range(len(pre_1[1].split())):
            if pre_1[1].split()[i][0] != pre_2[1].split()[i][0]:
                flag = 0
            else:
                if not '.' in pre_1[1].split()[i] and not '.' in pre_2[1].split()[i] and not operator.eq(pre_1[1].split()[i], pre_2[1].split()[i]):
                    flag = 0
        if flag and operator.eq(pre_1[0], pre_2[0]):
            return True
    return False

# 判断两个类的作者是否存在包含关系
def author_compare(record_1, record_2):
    record_1_store = record_1['author']
    record_2_store = record_2['author']
    authors_1 = author(record_1)
    authors_2 = author(record_2)
    record_1['author'] = record_1_store
    record_2['author'] = record_2_store
    if set(authors_1["author"]) >= set(authors_2["author"]) or set(authors_1["author"]) < set(authors_2["author"]):
        return True
    if len(authors_1["author"]) < len(authors_2["author"]):
        for i in authors_1["author"]:
            flag = 1
            for j in authors_2["author"]:
                if author_eq(i, j):
                    flag = 0
                    break
            if flag:
                return False
    else:
        for i in authors_2["author"]:
            flag = 1
            for j in authors_1["author"]:
                if author_eq(i, j):
                    flag = 0
                    break
            if flag:
                return False
    return True

# 输出name
def name(record):
    try:
        name = record['author'].split("and")[0].split(',')[0].split()[0]
    except:
        name = ""
    str = ""
    str = str.join(x for x in name if x.isalpha())
    return str

# 必须基本功能1：
def pythonlist(bib_filename):
    """
    将.bib文件解析为Python list

    :bib_filename: 文件名
    :return: python list
    """
    bib_filename=bib_filename.replace('.bib','')
    with open(bib_filename + '.bib', encoding='utf-8') as bib_file:
        parser = BibTexParser()
        parser.customization = convert_pretreatment
        bib_database = bp.load(bib_file, parser=parser)
    for key in bib_database.entries:
        print(key)

# 必须基本功能2：
def checkintegrity(bib_filename):
    """
    检测bib文件条目提供的域是否完全，输出缺少的域以及未收录的条目

    :bib_filename: 文件名
    """
    bib_filename=bib_filename.replace('.bib','')
    with open(bib_filename + '.bib', encoding='utf-8') as bib_file:
        parser = BibTexParser()
        parser.customization = pretreatment
        bib_database = bp.load(bib_file, parser=parser)
    requiredkeys = RequiredFields.keys()
    error = 0
    for key in bib_database.entries:
        if key['ENTRYTYPE'] in requiredkeys:
            for entry in RequiredFields[key['ENTRYTYPE']]:
                flag = 0
                for etype in key.keys():
                    if operator.eq(entry, etype) or etype in entry.split('/'):
                        flag = 1
                        break
                if flag == 0:
                    error = error + 1
                    print("{}：{} 条目缺少 {} 域\n".format(
                        key['ID'], key['ENTRYTYPE'], entry))
        else:
            error = error + 1
            print("“{}” 类型条目未收录\n".format(key['ENTRYTYPE']))
    print("共发现{}处错误".format(error))

# 必须基本功能3：
def checkconflicts(bib_filename):
    """
    检测同一文章是否存在多个条目，去掉相同项，并提示冲突信息

    :bib_filename: 文件名
    """
    bib_filename=bib_filename.replace('.bib','')
    with open(bib_filename + '.bib', encoding='utf-8') as bib_file:
        parser = BibTexParser()
        parser.customization = pretreatment
        bib_database = bp.load(bib_file, parser=parser)
    entrylen = len(bib_database.entries)
    dellist = []
    database = []
    for i in range(0, entrylen-1):
        for j in range(i+1, entrylen):
            if operator.eq(bib_database.entries[i]['title'], bib_database.entries[j]['title']) and operator.eq(bib_database.entries[i]['ENTRYTYPE'], bib_database.entries[j]['ENTRYTYPE']) and author_compare(bib_database.entries[i], bib_database.entries[j]):
                dellist.append(j)
                for entry in bib_database.entries[j].keys():
                    if not entry in bib_database.entries[i].keys():
                        bib_database.entries[i][entry] = bib_database.entries[j][entry]
                    else:
                        if not operator.eq(bib_database.entries[i][entry], bib_database.entries[j][entry]):
                            print("{}--{}：题目均为“{}”，“{}”内容存在冲突".format(
                                bib_database.entries[i]['ID'], bib_database.entries[j]['ID'], bib_database.entries[i]['title'], entry))
        if not i in dellist:
            database.append(bib_database.entries[i])
    bib_checked_database = BibDatabase()
    bib_checked_database.entries = database
    with open(bib_filename + '.bib', 'w', encoding='utf-8') as bib_file:
        bp.dump(bib_checked_database, bib_file)

# 必须基本功能4：
def merge(bib_filename_1, bib_filename_2):
    """
    将两个.bib文件综合为一个.bib文件，生成新文件 '{bib_filename_1}_{bib_filename_2}.bib'

    :bib_filename: 文件名
    """
    bib_filename_1=bib_filename_1.replace('.bib','')
    bib_filename_2=bib_filename_2.replace('.bib','')
    with open(bib_filename_1 + '.bib', encoding='utf-8') as bib_file_1:
        bib_parser_1 = BibTexParser()
        bib_parser_1.customization = pretreatment
        bib_database_1 = bp.load(bib_file_1, parser=bib_parser_1)
    with open(bib_filename_2 + '.bib', encoding='utf-8') as bib_file_2:
        bib_parser_2 = BibTexParser()
        bib_parser_2.customization = pretreatment
        bib_database_2 = bp.load(bib_file_2, parser=bib_parser_2)
    bib_database_merge = BibDatabase()
    for key in bib_database_1.entries + bib_database_2.entries:
        if not key in bib_database_merge.entries:
            bib_database_merge.entries.append(key)
    with open(bib_filename_1 + '_' + bib_filename_2 + '.bib', 'w', encoding='utf-8') as bib_file:
        bp.dump(bib_database_merge, bib_file)
    print("文件“{}.bib”和文件“{}.bib”已合并为文件“{}.bib”".format(
        bib_filename_1, bib_filename_2, bib_filename_1 + '_' + bib_filename_2))

# 必须基本功能5：
def formating(bib_filename):
    """
    将.bib文件格式化，生成新文件 '{filename}_format.bib'
    bibtexparser.bwriter 中的 _entry_to_bibtex 函数规定了输出格式，可自由修改

    :bib_filename: 文件名
    """
    bib_filename=bib_filename.replace('.bib','')
    with open(bib_filename + '.bib', encoding='utf-8') as bib_file:
        bib_parser = BibTexParser()
        bib_parser.customization = pretreatment
        bib_database = bp.load(bib_file, parser=bib_parser)
    limitedkeys = LimitedFields.keys()
    for key in bib_database.entries:
        if key['ENTRYTYPE'] in limitedkeys:
            if not set(key.keys()).issubset(set(LimitedFields[key['ENTRYTYPE']])):
                for field in LimitedFields[key['ENTRYTYPE']]:
                    if not field in key.keys():
                        print("“{}” 条目缺少内容 “{}”".format(key['ID'], field))
        else:
            print("“{}” 条目未收录".format(key['ENTRYTYPE']))
    with open(bib_filename + '_format.bib', 'w', encoding='utf-8') as bib_file_w:
        bp.dump(bib_database, bib_file_w)
    print("已将文件{}.bib格式化，生成文件{}_format.bib。".format(bib_filename))

# 介词列表：
preposition = ['in','on', 'with', 'by', 'for', 'at', 'about', 'under', 'of',  'into', 'within', 'throughout', 'inside', 'outside', 'without']

# 可选高阶功能1：
def keyword(bib_filename):
    """
    统一bib文件关键字格式，修改源文件

    :bib_filename: 文件名
    """
    bib_filename=bib_filename.replace('.bib','')
    with open(bib_filename + '.bib', encoding='utf-8') as bib_file:
        bib_parser = BibTexParser()
        bib_parser.customization = pretreatment
        bib_database = bp.load(bib_file, parser=bib_parser)
    for key in bib_database.entries:
        try:
            for word in key['title'].split():
                if not word.lower() in preposition:
                    key['ID'] = (name(key) + key['year'] + ''.join(x for x in word if x.isalpha())).lower()
                    break
        except:
            continue
    with open(bib_filename + '.bib', 'w', encoding='utf-8') as bib_file_w:
        bp.dump(bib_database, bib_file_w)
    print("文件{}.bib中的关键字已统一。".format(bib_filename))


# 可选高阶功能2：
# 可自主添加所需域
fields_id = ["ID", "ENTRYTYPE", "author", "title", "year",
             "journal", "volume", "number", "pages", "month", "organization", "publisher"]
fields_len = {"ID": "varchar(64)", "ENTRYTYPE": "varchar(32)", "author": "varchar(4096)", "title": "varchar(1024)", "year": "int(4)",
              "journal": "varchar(1024)", "volume": "int(5)", "number": "varchar(16)", "pages": "varchar(16)", "month": "varchar(32)", "organization": "varchar(1024)", "publisher": "varchar(1024)"}


def database_storage(bib_filename, host, user_name, passward, database):
    """
    创建不同类型条目的数据库表，并存储各类条目至不同数据库表
    注：当前只录入5种条目，可自行拓展

    :bib_filename: 文件名
    :host: 主机名，默认为 "localhost"
    :user_name: 用户名
    :passward: 密码
    :database: 数据库名    
    """
    # 打开.bib文件得到记录列表
    bib_filename=bib_filename.replace('.bib','')
    with open(bib_filename + '.bib', encoding='utf-8') as bib_file:
        parser = BibTexParser()
        parser.customization = pretreatment
        bib_database = bp.load(bib_file, parser=parser)
    # 打开数据库连接
    db = MySQLdb.connect(host, user_name, passward, database, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 创建 bib 库
    sql_create = "CREATE TABLE bib_database("
    for i in range(len(fields_id)):
        if i == len(fields_id)-1:
            sql_create = sql_create + \
                fields_id[i] + " %s" % (fields_len[fields_id[i]])
        else:
            sql_create = sql_create + \
                fields_id[i] + " %s, " % (fields_len[fields_id[i]])
    sql_create = sql_create + ");"
    try:
        cursor.execute(sql_create)
        db.commit()
    except:
        db.rollback()
    try:
        cursor.execute("ALTER TABLE `bib_database` ADD unique(`ID`);")
        db.commit()
    except:
        db.rollback()
    # 创建索引库
    try:
        cursor.execute(
            "CREATE TABLE `indexes_author`(`index` int(8), `author` varchar(32));")
        db.commit()
    except:
        db.rollback()
    try:
        cursor.execute("ALTER TABLE `indexes_author` ADD unique(`author`);")
        db.commit()
    except:
        db.rollback()
    # 插入索引库
    try:
        # 执行SQL语句
        cursor.execute("SELECT * FROM indexes_author;")
        db.commit()
    except:
        db.rollback()
    # 获取所有记录列表
    results = cursor.fetchall()
    index = len(results)
    for key in bib_database.entries:
        if 'author' in key:
            author_list = key['author'].split(' and ')
            key['author'] = key['author'].replace(' and ', ',')
            for author in author_list:
                index = index + 1
                sql_index = "insert into `indexes_author`(`index`,`author`)values(%d, \"%s\");" % (
                    index, author)
                flag = 0
                try:
                    cursor.execute(sql_index)
                    db.commit()
                except:
                    index = index - 1
                    flag = 1
                    db.rollback()
                if flag:
                    try:
                        # 执行SQL语句
                        cursor.execute("SELECT * FROM indexes_author;")
                        db.commit()
                    except:
                        db.rollback()
                    # 获取所有记录列表
                    results = cursor.fetchall()
                    for row in results:
                        if operator.eq(row[1], author):
                            true_index = row[0]
                else:
                    true_index = index
                key['author'] = key['author'].replace(author, str(true_index))
    # 插入 bib 库
    sql_insert_init = "insert into bib_database("
    for i in range(len(fields_id)):
        if i == len(fields_id)-1:
            sql_insert_init = sql_insert_init + fields_id[i]
        else:
            sql_insert_init = sql_insert_init + fields_id[i] + ", "
    sql_insert_init = sql_insert_init + ")values("
    for key in bib_database.entries:
        sql_insert = sql_insert_init
        for i in range(len(fields_id)):
            if i == len(fields_id)-1:
                try:
                    sql_insert = sql_insert + "\"" + \
                        key[fields_id[i]] + "\"" + ");"
                except:
                    sql_insert = sql_insert + "null" + ");"
            else:
                try:
                    sql_insert = sql_insert + "\"" + \
                        key[fields_id[i]] + "\"" + ", "
                except:
                    sql_insert = sql_insert + "null" + ", "
        try:
            # 执行sql语句
            cursor.execute(sql_insert)
            # 提交到数据库执行
            db.commit()
        except:
            db.rollback()
    print("已成功录入！")


def database_query(bib_filename, entry, fields, host, user_name, passward, database):
    """
    读取数据库的规定条目的规定域，并产生相应的.bib文件

    :bib_filename: 文件名
    :entry: 条目类型
    :field: 域类型
    :host: 主机名，默认为 "localhost"
    :user_name: 用户名
    :passward: 密码
    :database: 数据库名  
    """
    # 打开数据库连接
    db = MySQLdb.connect(host, user_name, passward, database, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    bib_mysql = []
    # 构建所需要的域的列表
    fields_list = fields.split(",")
    for i in fields_list:
        if not i in fields_id:
            print("“{}”域未收录，无法导出该域".format(i))
            fields_list.remove(i)
    fields_list.append("ID")
    fields_list.append("ENTRYTYPE")
    try:
        # 执行SQL语句
        cursor.execute("SELECT * FROM bib_database;")
        db.commit()
    except:
        db.rollback()
    # 获取所有记录列表
    results_bib = cursor.fetchall()
    try:
        # 执行SQL语句
        cursor.execute("SELECT * FROM indexes_author;")
        db.commit()
    except:
        db.rollback()
    # 获取所有记录列表
    results_index = cursor.fetchall()
    # 将记录存入到列表中，进而转化为 BibDatabase 对象
    for row in results_bib:
        key = {}
        if operator.eq(row[fields_id.index("ENTRYTYPE")], entry):
            for field in fields_list:
                if row[fields_id.index(field)]:
                    key[field] = str(row[fields_id.index(field)])
                if operator.eq("author", field):
                    index_list = key[field].split(',')
                    key[field] = key[field].replace(',', ' and ')
                    for index in index_list:
                        key[field] = key[field].replace(
                            index, results_index[int(index)-1][1])
            bib_mysql.append(key)
    bib_mysql_database = BibDatabase()
    bib_mysql_database.entries = bib_mysql
    # 将 BibDatabase 对象转化为.bib文件
    with open(bib_filename + '.bib', 'w', encoding='utf-8') as bib_file:
        bp.dump(bib_mysql_database, bib_file)
    # 关闭数据库连接
    db.close()
    print("已生成{}.bib文件。".format(bib_filename))


# 综合功能函数
def comprehensive():
    """
    可应用该库的所有功能函数

    :bib_filename: 操作文件名称
    """
    # 功能选择界面
    print("请选择功能如下：\n"
          "必须基本功能：\n"
          "1：将.bib文件解析为Python list；\n"
          "2：检测bib文件条目提供的域是否完全；\n"
          "3：检测同一文章是否存在多个条目，去掉相同项，并提示冲突信息；\n"
          "4：将两个.bib文件综合为一个.bib文件；\n"
          "5：将.bib文件格式化。\n"
          "可选高阶功能：\n"
          "6：统一bib文件关键字格式；\n"
          "7：存储指定类型数据库；\n"
          "8：输出数据库中指定类型条目的指定类型的域信息，并生成.bib文件。"
          )
    try:
        function = int(input())
    except:
        print("请输入正确格式的指令！\n")
    if function == 1:
        print("请输入文件名：")
        bib_filename = str(input())
        pythonlist(bib_filename)
    elif function == 2:
        print("请输入文件名：")
        bib_filename = str(input())
        checkintegrity(bib_filename)
    elif function == 3:
        print("请输入文件名：")
        bib_filename = str(input())
        checkconflicts(bib_filename)
    elif function == 4:
        print("请输入文件名1：")
        bib_filename_1 = str(input())
        print("请输入文件名2：")
        bib_filename_2 = str(input())
        merge(bib_filename_1,bib_filename_2)    
    elif function == 5:
        print("请输入文件名：")
        bib_filename = str(input())
        formating(bib_filename)
    elif function == 6:
        print("请输入文件名：")
        bib_filename = str(input())
        keyword(bib_filename)      
    elif function == 7:
        print("请输入文件名：")
        bib_filename = str(input())
        print("请输入主机名：")
        host = str(input())
        print("请输入用户名：")
        user_name = str(input())
        print("请输入密码：")
        passward = str(input())
        print("请输入数据库名称：")
        database = str(input())
        database_storage(bib_filename, host, user_name, passward, database)
    elif function == 8:
        print("请输入文件名：")
        bib_filename = str(input())
        print("请输入需要的条目：")
        entry = str(input())
        print("请输入需要的域（用逗号隔开）：")
        fields = str(input())
        print("请输入主机名：")
        host = str(input())
        print("请输入用户名：")
        user_name = str(input())
        print("请输入密码：")
        passward = str(input())
        print("请输入数据库名称：")
        database = str(input())
        database_query(bib_filename, entry, fields, host, user_name, passward, database)
    else:
        print("无此功能！")

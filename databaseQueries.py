import psycopg2


def requestErrors():
    database = psycopg2.connect(database="news")
    crsr = database.cursor()
    crsr.execute("""create or replace view countDates as select
    time::timestamp::date as Date, count(*) from
    log group by Date order by count(*) desc""")
    crsr.execute("""create or replace view countErrors as select
    time::timestamp::date as Date, count(*) from
    log where status like '40%'
    group by Date order by count(*) desc""")
    crsr.execute("""select countDates.Date,
    round((countErrors.count * 100.0) / (countDates.count), 2) as percentage
    from countDates join countErrors on
    countDates.Date = countErrors.Date where
    round((countErrors.count * 100.0) / (countDates.count), 2) > 1.00""")

    res = crsr.fetchall()
    database.close()
    return res


def favAuthorsInDesc():
    database = psycopg2.connect(database="news")

    crsr = database.cursor()
    crsr.execute("""create or replace view selectPath as select
    substring(path, 10) as path from log where
    path like '/article/%' """)
    crsr.execute("""create or replace view createJoin as select
    articles.author, count(*) from articles join
    selectPath on articles.slug = selectPath.path
    group by articles.author order by count(*) desc""")
    crsr.execute("""create or replace view favAuthors as select
    authors.name, authors.id from authors
    join articles on articles.author = authors.id
    group by authors.id""")
    crsr.execute("""select name, count from favAuthors, createJoin where
    favAuthors.id = createJoin.author""")
    res = crsr.fetchall()
    database.close()
    return res


def topThreeArticles():
    database = psycopg2.connect(database="news")
    crsr = database.cursor()
    crsr.execute("""create or replace view topArticles as select path,
    COUNT(*) as count from (select substring(path, 10) as path from
    log where path like '/article/%') log
    GROUP BY path ORDER BY COUNT(*) desc limit 3""")
    crsr.execute("""select title, count from topArticles join
    articles on articles.slug = topArticles.path ORDER BY count desc""")

    res = crsr.fetchall()
    database.close()
    return res

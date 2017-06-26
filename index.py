from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import psycopg2

from databaseQueries import requestErrors, favAuthorsInDesc, topThreeArticles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            output = '''\
            <!DOCTYPE html>
            <html>
            <head>
            <title>LOG ANALYSIS Project</title>
            </head>
            <table>
            <tr>
            <td colspan = '2'>
            <h3>
            Click on button for getting three most popular Articles!!
            </h3>
            </td>
            <td>
            &nbsp;
            <td>
            <td>
            <form action="/top_articles">
            <button type="submit">
            Check me out for most popular Articles! :D
            </button>
            </form>
            </td>
            </tr>
            <tr>
            <td colspan = '2'>
            <h3>
            Click on the button to get the list
            of the favourite authors from top to bottom!!
            </h3>
            </td>
            <td>
            &nbsp;
            </td>
            <td>
            <form action="/famous_authors">
            <button type="submit">
            Yes, Click me and I'll show you the list of authors!
            </button>
            </form>
            </td>
            <tr>
            <tr>
            <td colspan = '2'>
            <h3>
            Click on the button to get the days having request errors!!
            </h3>
            </td>
            <td>
            &nbsp;
            </td>
            <td>
            <form action="/request_errors">
            <button type="submit">
            Click me to get the days!
            </button>
            </form>
            </td>
            <tr>
            </table>
            </html>'''
            if self.path.endswith("/log_analysis"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(output)
            return
            if self.path.endswith("/top_articles?"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                res_article = topThreeArticles()
                out = ""
                out += '''<html>
                <head>
                Top 3 articles
                </head>'''
                out = '''<body><center><h3>The three most popular articles are :</h3><br />
                %s<br /><br />
                <a href = "/log_analysis">Back</a></center></body></html>'''
                some_list = '''<table border=1>
                <tr> <td>&nbsp;<b>Name</b>&nbsp;
                </td> <td>&nbsp;<b>Count</b>&nbsp;</td></tr>'''
                some_list += "".join([
                    "<tr> <td>&nbsp;{p1}&nbsp;"
                    "</td> <td>&nbsp;{p2}&nbsp;</td>"
                    "</tr>".format(p1=t1, p2=t2) for t1, t2 in res_article])
                some_list += "</table>"
                out = out % some_list
                self.wfile.write(out)
            return
            if self.path.endswith("/famous_authors?"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                res_authors = favAuthorsInDesc()
                out = ""
                out += '''<html>
                <head>
                Famous Authors
                </head>'''
                out = '''<body><center><h3>
                The famous authors
                (top -> most famous and bottom -> least famous)
                are :</h3><br />
                %s<br /><br />
                <a href = "/log_analysis">Back</a></center></body></html>'''
                some_list = '''<table border=1>
                <tr> <td>&nbsp;<b>Name</b>&nbsp;
                </td> <td>&nbsp;<b>Count</b>&nbsp;</td></tr>'''
                some_list += "".join([
                    "<tr> <td>&nbsp;{p1}&nbsp;"
                    "</td> <td>&nbsp;{p2}&nbsp;</td>"
                    "</tr>".format(p1=t1, p2=t2) for t1, t2 in res_authors])
                some_list += "</table>"
                out = out % some_list
                self.wfile.write(out)
            return
            if self.path.endswith("/request_errors?"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                res_errors = requestErrors()
                out = ""
                out += '''<html>
                <head>
                Request Errors
                </head>'''
                out = '''<body><center><h3>The days where requests lead to errors are:</h3><br />
                %s<br /><br />
                <a href = "/log_analysis">Back</a></center></body></html>'''
                some_list = '''<table border=1>
                <tr> <td>&nbsp;<b>Date</b>&nbsp;
                </td> <td>&nbsp;<b>Percentage of Errors</b>&nbsp;</td></tr>'''
                some_list += "".join([
                    "<tr> <td>&nbsp;{p1}&nbsp;"
                    "</td> <td>&nbsp;{p2}&nbsp;</td>"
                    "</tr>".format(p1=t1, p2=t2) for t1, t2 in res_errors])
                some_list += "</table>"
                out = out % some_list
                self.wfile.write(out)
            return
        except IOError:
                self.send_error(404, "File Not Found %s" % self.path)

    def main():
        try:
            server = HTTPServer(('', 8080), webServerHandler)
            print "Web server running... " +
            "Open localhost:8080/log_analysis in your browser"
            server.serve_forever()
        except KeyboardInterrupt:
            print "^C entered, stopping web server..."
            server.socket.close()
        if __name__ == '__main__':
            main()

# -*- coding: utf-8 -*-

# 使用 CGI 为基于 Python 的 Web 服务器编写一个留言板（处理程序）

# Import modules for CGI handling 
import cgi
import cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
name = form.getvalue('Name')
comment  = form.getvalue('Comment')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>CGI Program Example </title>"
print "</head>"
print "<body>"
print "<h2> %s sends a comment: %s</h2>" % (name, comment)
print "</body>"
print "</html>"
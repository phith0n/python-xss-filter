#!/usr/bin/env python
#coding=utf-8
__author__ = 'Phtih0n'
import web, os, pxfilter

urls = (
    '.*', 'router'
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    web.config.debug = False
    app.run()

class su:
    def other(self):
        raise web.seeother('main')

class router(su):
    def __init__(self):
        self.tplData = {}
        self.globalsTplFuncs = {}
        web.header("X-XSS-Protection", "0")

    def GET(self):
        self.assign("html", "")
        return self.display("xsshtml")

    def POST(self):
        html = web.input(xsscode = "").xsscode
        parser = pxfilter.XssHtml()
        parser.feed(html)
        parser.close()
        html = parser.getHtml()
        self.assign("html", html)
        return self.display("xsshtml")

    def assign(self,key,value = ''):
        if type(key) == dict:
            self.tplData = dict(self.tplData, **key)
        else:
            self.tplData[key] = value

    def display(self, tplName):
        self.tplData['render'] = web.template.render('html', globals = self.globalsTplFuncs)
        return getattr(self.tplData['render'], tplName)(self.tplData)
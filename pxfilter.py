# -*- coding: utf-8 -*-
"""
Python 富文本XSS过滤类
@package XssHtml
@version 0.1
@link http://phith0n.github.io/python-xss-filter
@since 20150407
@copyright (c) Phithon All Rights Reserved

Based on native Python module HTMLParser purifier of HTML, To Clear all javascript in html
You can use it in all python web framework
Written by Phithon <root@leavesongs.com> in 2015 and placed in the public domain.
phithon <root@leavesongs.com> 编写于20150407
From: XDSEC <www.xdsec.org> & 离别歌 <www.leavesongs.com>
GitHub Pages: https://github.com/phith0n/python-xss-filter
Usage:
	parser = XssHtml()
	parser.feed('<html code>')
	parser.close()
	html = parser.getHtml()
	print html

Requirements
Python 2.6+ or 3.2+
Cannot defense xss in browser which is belowed IE7
浏览器版本：IE7+ 或其他浏览器，无法防御IE6及以下版本浏览器中的XSS
"""
import re
try:
	from html.parser import HTMLParser
except:
	from HTMLParser import HTMLParser

class XssHtml(HTMLParser):
	allow_tags = ['a', 'img', 'br', 'strong', 'b', 'code', 'pre',
				  'p', 'div', 'em', 'span', 'h1', 'h2', 'h3', 'h4',
				  'h5', 'h6', 'blockquote', 'ul', 'ol', 'tr', 'th', 'td',
				  'hr', 'li', 'u', 'embed', 's', 'table', 'thead', 'tbody',
				  'caption', 'small', 'q']
	allow_attrs = ['title', 'src', 'href', 'id', 'class', 'style',
	               'width', 'height', 'alt', 'target', 'align', 'rel',
					'border', 'cellpadding', 'cellspacing']
	common_attrs = ["id", "style", "class", "name"]
	nonend_tags = ["img", "hr", "br"]

	def __init__(self, allows = []):
		HTMLParser.__init__(self)
		self.allow_tags = allows if allows else self.allow_tags
		self.result = []
		self.start = []
		self.data = []

	def getHtml(self):
		"""
		Get the safe html code
		"""
		for i in range(0, len(self.result)):
			tmp = self.result[i].rstrip('\n')
			tmp = tmp.lstrip('\n')
			if tmp:
				self.data.append(tmp)
		return ''.join(self.data)

	def handle_startendtag(self, tag, attrs):
		self.handle_starttag(tag, attrs)

	def handle_starttag(self, tag, attrs):
		if tag not in self.allow_tags:
			return
		end_diagonal = ' /' if tag in self.nonend_tags else ''
		if not end_diagonal:
			self.start.append(tag)
		attdict = {}
		for attr in attrs:
			attdict[attr[0]] = attr[1]

		if hasattr(self, "node_%s" % tag):
			attdict = getattr(self, "node_%s" % tag)(attdict)
		else:
			attdict = self.node_default(attdict)

		attrs = []
		for (key, value) in attdict.items():
			attrs.append('%s="%s"' % (key, self.__htmlspecialchars(value)))
		attrs = (' ' + ' '.join(attrs)) if attrs else ''
		self.result.append('<' + tag + attrs + end_diagonal + '>')

	def handle_endtag(self, tag):
		if self.start and tag == self.start[len(self.start) - 1]:
			self.result.append('</' + tag + '>')
			self.start.pop()

	def handle_data(self, data):
		self.result.append(self.__htmlspecialchars(data))

	def handle_entityref(self, name):
		if name.isalpha():
			self.result.append("&%s;" % name)

	def handle_charref(self, name):
		if name.isdigit():
			self.result.append("&#%s;" % name)

	def node_default(self, attrs):
		attrs = self.__common_attr(attrs)
		attrs = self.__wash_attr(attrs, self.common_attrs)
		return attrs

	def node_img(self, attrs):
		attrs = self.__common_attr(attrs)
		attrs = self.__wash_attr(attrs, self.common_attrs + ["src", "width", "height", "alt", "align"])
		return attrs

	def node_a(self, attrs):
		attrs = self.__common_attr(attrs)
		attrs = self.__wash_attr(attrs, self.common_attrs + ["href", "target", "rel"])
		attrs = self.__get_link(attrs, "href")
		attrs = self.__set_attr_default(attrs, "target", "_blank")
		return attrs

	def node_embed(self, attrs):
		attrs = self.__common_attr(attrs)
		attrs = self.__wash_attr(attrs, self.common_attrs + ["src", "width", "height"])
		attrs = self.__get_link(attrs, "src")
		attrs["allowscriptaccess"]="never";
		return attrs

	def node_table(self, attrs):
		attrs = self.__common_attr(attrs)
		attrs = self.__wash_attr(attrs, self.common_attrs + ["border", "cellpadding", "cellspacing"])
		return attrs

	def __true_url(self, url):
		prog = re.compile(r"^(http|https|ftp)://.+", re.I | re.S)
		if prog.match(url):
			return url
		else:
			return "http://%s" % url

	def __true_style(self, style):
		if style:
			style = re.sub(r"(\\|&#|/\*|\*/)", "_", style)
			style = re.sub(r"e.*x.*p.*r.*e.*s.*s.*i.*o.*n", "_", style)
		return style

	def __get_style(self, attrs):
		if attrs.has_key("style"):
			attrs["style"] = self.__true_style(attrs.get("style"))
		return attrs

	def __get_link(self, attrs, name):
		if attrs.has_key(name):
			attrs[name] = self.__true_url(attrs[name])
		return attrs

	def __wash_attr(self, attrs, allows):
		if attrs:
			for (key, value) in attrs.items():
				if key not in allows:
					del attrs[key]
		return attrs

	def __common_attr(self, attrs):
		attrs = self.__wash_attr(attrs, self.allow_attrs)
		attrs = self.__get_style(attrs)
		return attrs

	def __set_attr_default(self, attrs, name, default = ''):
		if not attrs.has_key(name):
			attrs[name] = default
		return attrs

	def __htmlspecialchars(self, html):
		return html.replace("<", "&lt;")\
			.replace(">", "&gt;")\
			.replace('"', "&quot;")\
			.replace("'", "&#039;")


if "__main__" == __name__:
	parser = XssHtml()
	parser.feed("""<p><img src=1 onerror=alert(/xss/)></p><div class="left"><a href='javascript:prompt(
	1)'><br />hehe</a></div><p id="test" onmouseover="alert(1)">&gt;M<svg><a href="https://www.baidu.com" target="self"
	>MM</a></p>""")
	parser.close()
	print(parser.getHtml())
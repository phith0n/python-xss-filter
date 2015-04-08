# python-xss-filter
Based on native Python module HTMLParser purifier of HTML, To Clear all javascript in html

## Python 富文本XSS过滤类
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


### Requirements
Python 2.6+ or 3.2+
Cannot defense xss in browser which is belowed IE7
浏览器版本：IE7+ 或其他浏览器，无法防御IE6及以下版本浏览器中的XSS

# python-xss-filter
Based on native Python module HTMLParser purifier of HTML, To Clear all javascript in html  

## Python 富文本XSS过滤类
@package XssHtml  
@version 0.1  
@link https://github.com/phith0n/python-xss-filter
@since 20150407  
@copyright (c) Phithon All Rights Reserved  

Based on native Python module HTMLParser purifier of HTML, To Clear all javascript in html  
You can use it in all python web framework  
Written by Phithon <root@leavesongs.com> in 2015 and placed in the public domain.  
phithon <root@leavesongs.com> 编写于20150407  
From: XDSEC <www.xdsec.org> & 离别歌 <www.leavesongs.com>  
Demo: http://python-xss-filter.leavesongs.com  
Usage:
	
	import pxfilter
	parser = pxfilter.XssHtml()
	parser.feed('<html code>')
	parser.close()
	html = parser.getHtml()
	print html


### Requirements
Python 2.6+ or 3.2+  
Cannot defense xss in browser which is belowed IE7  
浏览器版本：IE7+ 或其他浏览器，无法防御IE6及以下版本浏览器中的XSS  

### Other
**pxfilter.py** 是过滤类所在的文件，其他文件是测试网站 http://python-xss-filter.leavesongs.com 的源代码。  
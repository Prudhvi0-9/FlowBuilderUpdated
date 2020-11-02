import json

from lxml import etree

XSL = '''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
  <html>
  <body>
    <h2>My CD Collection</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>Title</th>
        <th>Artist</th>
      </tr>
      <xsl:for-each select="catalog/cd">
      <tr>
        <td><xsl:value-of select="title" /></td>
        <td><xsl:value-of select="artist" /></td>
      </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>'''



# load input
dom = etree.parse('new.xml')
# load XSLT
transform = etree.XSLT(etree.fromstring(XSL))

# apply XSLT on loaded dom
json_text = str(transform(dom))

# json_text contains the data converted to JSON format.
# you can use it with the JSON API. Example:
data = json.loads(json_text)
print(data)
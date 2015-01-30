## Minimized version of a bug that appeared in 21lines.py
import xml.etree.ElementTree as etree
print etree.fromstring("<html></html>").tag

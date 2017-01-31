#!/usr/bin/env python
# coding:utf-8


import unittest
import xml.etree.cElementTree as ElementTree


class XmlTest(unittest.TestCase):
    def test_default(self):
        root = ElementTree.fromstring("<root><a hello='world'>123</a></root>")

        for child in root:
            print "text:%s, tag:%s, attr:%s" % (child.text, child.tag, child.attrib)

        print root


    def test_children(self):
        root = ElementTree.fromstring("<root><a hello='world'>123</a></root>")
        children = root.getchildren()
        print len(children)



if __name__ == "__main__":
    unittest.main()


import unittest
import sys
import os

# get the code path in a cross platform way
code_path = os.path.abspath(os.pardir)
sys.path.insert(0,code_path)
from src import PTwikitextCleaner

class TestPTwikitextCleaner(unittest.TestCase):

    def test_amp_sub(self):
        wikitext = '1&amp;nbsp;2'
        correct = "1 2"
        out = PTwikitextCleaner(wikitext).clean()
        self.assertTrue(out == correct)

    def test_section_removal(self):
        wikitext = 'keep this\n== Ligações externas ==\ndelete this'
        correct = "keep this"
        out = PTwikitextCleaner(wikitext).clean()
        
        self.assertTrue(out == correct)

    def test_template_removal(self):
        wikitext = """keep {{unbulleted list
        |first item|second item|third item|...
        |class     = class
        |style     = style
        |list_style  = style for ul tag
        |item_style  = style for all li tags
        |item1_style = style for first li tag |item2_style = style for second li tag |...
        }}this"""
       
        correct = "keep this"
        out = PTwikitextCleaner(wikitext).clean()
        self.assertTrue(out == correct)

    def test_tag_removal(self):
        wikitext = 'keep<math>remove this</math> this'
        correct = 'keep this'
        out = PTwikitextCleaner(wikitext).clean()
        self.assertTrue(out == correct)

if __name__ == '__main__':
    unittest.main()

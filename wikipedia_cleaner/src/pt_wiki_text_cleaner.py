import mwparserfromhell
import re


class PTwikitextCleaner(object):
    # Static definition of the filtered elements

    # detalhes: 
    # https://en.wikipedia.org/wiki/Template:Plainlist
    # https://en.wikipedia.org/wiki/Template:Unbulleted_list
    # https://en.wikipedia.org/wiki/Template:Bulleted_list
    # https://en.wikipedia.org/wiki/Template:Flatlist
    # https://en.wikipedia.org/wiki/Template:Ordered_list
    filter_template = ['unbulleted list', 'flatlist', 'hlist', 'bulleted list', 'ordered list', 'plainlist', 'defn',
                       'term', 'glossary', 'glossary end', 'outdent', 'outdent2', 'fake heading', 'col-begin',
                       'col-end', 'columns-list']

    # detalhes: 
    # https://en.wikipedia.org/wiki/Help:Wikitext
    # https://en.wikipedia.org/wiki/Help:HTML_in_wikitext
    filter_tags_and_templates = ['chem', 'chem2', 'graph', 'hiero', 'indicator', 'math', 'score', 'syntaxhighlight',
                                 'source', 'code', 'templatedata', 'timeline', 'gallery', 'categorytree', 'table',
                                 'tr', 'td', 'ul', 'li', 'ol', 'dl', 'dt', 'dd', 'ref']

    # detalhes:
    # https://pt.wikipedia.org/wiki/Ajuda:Guia_de_edi%C3%A7%C3%A3o/
    # Como_usar_imagens#Sintaxe_para_multim%C3%ADdias
    # Os prefixos "Imagem:", "Arquivo:", "File:" e "Image:"
    # são reconhecidos pelo MediaWiki e apontam todos para o domínio "Ficheiro:"
    filter_wikilinks = ['file:', 'imagem:', 'image:', 'arquivo:', 'media:']

    # detalhes:
    # https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:Livro_de_estilo
    # Quando certas seções-padrão são usadas, estas devem ficar no final do artigo,
    # respeitando a terminologia das seções, e uma das duas sequências seguinte:[2]
    # Notas, Referências, Ver também, Bibliografia, Ligações externas
    sections_headers = ['Referências', 'Ver também', 'Bibliografia', 'Ligações externas']

    def __init__(self, wikitext):
        self._wikitext = wikitext

    def clean(self):
        wiki_text = self._sub_amp(self._wikitext)
        wiki_text = self._filter_identation_and_lists(wiki_text)
        wiki_text = self._filter_images_wikilinks(wiki_text)
        wiki_text = self._fix_foreign(wiki_text)

        mw_parser = mwparserfromhell.parse(wiki_text)

        mw_parser = self._fix_categories(mw_parser)
        mw_parser = self._filter_specific_pt_elements(mw_parser)
        mw_parser = self._filter_headings(mw_parser)  # must be last otherwise the section will not be

        plain_text = mw_parser.strip_code()
        plain_text = self._remove_tags(plain_text)
        plain_text = self._remove_non_identation_space(plain_text)

        return plain_text

    def _fix_foreign(self, wikitext):
        return re.sub(r'\{\{lang-[a-z]+\|([^}]*)\}\}', r"\1", wikitext)

    def _sub_amp(self, wikitext):
        return wikitext.replace('&amp;', '&')

    def _filter_headings(self, prs):
        for heading in prs.filter_headings():
            prs.remove(heading)
        return prs

    def _filter_identation_and_lists(self, wikitext):
        # https://en.wikipedia.org/wiki/Help:Wikitext
        # : -> idented
        # ; -> description lists
        # * -> list
        # # -> ordered list

        # regex = r'^[\\t|\s]*[\*|\#|:|\;]+.+$'
        regex = r'^[\\t\s]*[\*\#:\;]+.+$'
        return re.sub(regex, '', wikitext, flags=re.MULTILINE)

    def _filter_images_wikilinks(self, wikitext):
        regex = r'^\[\[(imagem|image|arquivo|file|media).+\]\]$'
        return re.sub(regex, '', wikitext, flags=re.MULTILINE | re.IGNORECASE)

    def _fix_categories(self, prs):
        for l in prs.filter_wikilinks():
            if 'categoria:' in l.title.lower() or 'category:' in l.title.lower():
                if not l.text or not l.text.strip(' ').strip('\t'):
                    text = re.sub(r'^[^\:]+\:', '', str(l.title))
                    l.text = text
        return prs

    def _remove_tags(self, plain_text):
        # Specific issue with mwparserfrom hell
        regex = r'<[\w]*[^>]*>[^<]*<\/[\w]*>|<[\w]*[^>]*[\/]?>'
        return re.sub(regex, '', plain_text)

    def _remove_non_identation_space(self, plain_text):
        return plain_text.replace("\xa0", " ")

    def _filter_specific_pt_elements(self, prs):

        return self._filter_elements(prs,
                                     tags=self.filter_tags_and_templates,
                                     templates=self.filter_tags_and_templates + self.filter_template,
                                     wikilinks=self.filter_wikilinks,
                                     sections=self.sections_headers)

    def _filter_elements(self, prs, tags, templates, wikilinks, sections):
        remove_elements = []

        # find sections
        for section in prs.get_sections():
            section_headings = [str(h.title).strip() for h in section.filter_headings()]
            if any(heading for heading in section_headings if heading in sections):
                remove_elements.append(section)

        remove_elements = []

        # find nodes
        for i, node in enumerate(list(prs.nodes)):
            # filter tags
            if type(node) == mwparserfromhell.nodes.Tag:
                if node.tag.lower() in tags:
                    remove_elements.append(node)
            # filter templates
            elif type(node) == mwparserfromhell.nodes.Template:
                if node.name.lower() in templates:
                    remove_elements.append(node)
            # filter wikilinks
            elif type(node) == mwparserfromhell.nodes.Wikilink:
                title = node.title.lower()
                if any(link for link in wikilinks if link in title):
                    remove_elements.append(node)

        # Here the problem is the order of deletion or poorly structured wikitext due
        # to malformation by the user or the manipulations performed by this code
        for element in remove_elements:
            try:
                prs.remove(element)
            except:
                pass

        return prs

import mwparserfromhell
import sys
import os
import re

# get the code path in a cross platform way
code_path = os.path.abspath(os.pardir)
sys.path.insert(0,code_path)
import src
import tst_string
txt = """{{Info/Território geográfico
 |nome                = América Latina
 |preposicao          = da
 |localizacao         = Latin America (orthographic projection).svg
 |vizinhos            = [[Ásia]], [[África]], [[América Anglo-Saxônica]], [[Antártida]], [[Europa]] e [[Oceania]]
 |numero_paises       = 21
 |numero_territorios  = 10
 |area_total          = 21&nbsp;069&nbsp;501&nbsp;
 |maior_pais          = {{BRAb}} [[Brasil]] (8.514.876,599&nbsp;km²)
 |menor_pais          = {{ELSb}} [[El Salvador]] (21.041&nbsp;km²)
 |populacao           = 569 milhões
 |demog_densidade     = 27 hab/km²
 |pais_mais_populoso  = [[Brasil]] (191&nbsp;480&nbsp;630 hab.<ref name="IBGE_Pop_2009">{{citar web | url = http://www.ibge.gov.br/home/estatistica/populacao/estimativa2009/POP2009_DOU.pdf | titulo = Estimativas da população para 1º de julho de 2009|data= 14 de agosto de 2008 | publicado = Instituto Brasileiro de Geografia e Estatística (IBGE) |data= 14 de agosto de 2008 |acessodata= 14 de setembro de 2008 | formato = [[PDF]] }}</ref>)
 |pais_menos_populoso =
 |pais_mais_povoado   =
 |pais_menos_povoado  =
 |linguas             = [[Língua castelhana|Espanhol]], [[Língua portuguesa|português]], [[Língua francesa|francês]], [[Língua quíchua|quíchua]], [[Língua aimará|aimará]], [[Língua náuatle|náuatle]], [[Línguas maias]], [[Língua guarani|guarani]], [[Crioulo haitiano]], [[papiamento]], [[Línguas tupis]].
 |ponto_mais_alto     = [[Aconcágua]], [[Argentina]], 6962 m
 |ponto_mais_baixo    = [[Laguna del Carbón]], [[Argentina]], -105 m
 |maior_lago          = [[Lago Titicaca]] (8300 km²)
 |ponto_extremo_norte =
 |ponto_extremo_sul   = [[Cabo Horn]]
 |ponto_extremo_leste = [[Ponta do Seixas]] (continental)
 |ponto_extremo_oeste =
 |maior_ilha          = {{CUBb}} [[Cuba]] (105 806 km²)
 |maior_vulcao        = [[Ojos del Salado]], [[Argentina]] e [[Chile]]
 |pais_mais_rico      = {{BRA}}<small>[[Brasil]] (US$ 2,100 trilhão)</small>
 |pais_mais_pobre     = {{HTI}}<small>[[Haiti]] (US$ 15,8 bilhões)</small>
}}
A '''América Latina''' ({{lang-es|''América Latina'' ou ''Latinoamérica''}}; {{lang-fr|''Amérique latine''}}) é uma região do [[continente americano]] que engloba os países onde são faladas, primordialmente, [[línguas românicas]] (derivadas do [[latim]]) — no caso, o [[Língua castelhana|espanhol]], o [[Língua portuguesa|português]] e o [[Língua francesa|francês]] — visto que, historicamente, a região foi maioritariamente dominada pelos [[impérios coloniais]] europeus [[Império Espanhol|Espanhol]] e [[Império Português|Português]].<ref name=Colburn>{{Citar livro
 | sobrenome   = Colburn
 | nome        = Forrest D
 | título      = Latin America at the End of Politics
 | editora     = Princeton University Press
 | ano         = 2002
 | isbn        = 0-691-09181-1
 | URL         = http://books.google.com/books?id=qBCVB3mxCK8C&pg=PP1
}}</ref> A América Latina tem uma área de cerca de {{formatnum:21069501}} km², o equivalente a cerca de 3,9% da superfície da [[Terra]] (ou 14,1% de sua superfície emersa terrestre).<ref name="area e populacao">{{citar web|url=http://www.bvmemorial.fapesp.br/php/level.php?lang=pt&component=19&item=3|título=Sobre a América Latina|autor=Biblioteca Virtual da América Latina|data=2011|publicado=Biblioteca Virtual da América Latina|língua=português|acessodata=12 de dezembro de 2011}}</ref> Em 2008, a sua população foi estimada em mais de 569 milhões de pessoas.<ref name="area e populacao"/> Os países do restante do continente americano tiveram uma colonização majoritariamente realizada por povos [[europeus]] de cultura [[Anglo-saxões|anglo-saxônica]] ou [[Império Colonial Neerlandês|neerlandesa]] (ver [[América Anglo-Saxônica]]).<ref>{{citar web|url=http://www.historyworld.net/wrldhis/PlainTextHistories.asp?historyid=aa80|título=HISTORY OF BRITISH COLONIAL AMERICA|autor=History World|data=2011|publicado=History World|língua=português|acessodata=12 de dezembro de 2011}}</ref> Vale ressaltar algumas exceções, como [[Québec]], que não é um país independente, mas uma província de maioria [[Francofonia|francófona]] que pertence ao [[Canadá]];<ref>{{citar web|url=http://www.republiquelibre.org/cousture/NVFR2.HTM|título=NEW FRANCE: 1524-1763|autor=Repúblique Libre|data=2011|publicado=Repúblique Libre|língua=inglês|acessodata=12 de dezembro de 2011}}</ref> o estado da [[Luisiana]], que também foi [[Império colonial francês|colonizado por franceses]], mas pertence aos [[Estados Unidos]]<ref>{{citar web|url=http://www.republiquelibre.org/cousture/LASALLE.HTM|título=René-Robert Cavelier de La Salle|autor=Repúblique Libre|data=2011|publicado=Repúblique Libre|língua=francês|acessodata=12 de dezembro de 2011}}</ref> e os estados do [[Região Sudoeste dos Estados Unidos|sudoeste estadunidense]], que tiveram [[Colonização espanhola da América|colonização espanhola]].<ref>{{citar web|url=http://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/America/United_States/_Topics/history/_Texts/BOUSIA/11*.html|título=Exploration of the Interior of North America (1517‑1541)|autor=Edward Gaylord Bourne|data=1º de fevereiro de 2008|publicado=Universidade de Chicago|língua=inglês|acessodata=12 de dezembro de 2011}}</ref>

A América Latina compreende a quase totalidade das Américas do [[América do Sul|Sul]] e [[América Central|Central]]: as exceções são os países sul-americanos da [[Guiana]] e do [[Suriname]] e a nação centro-americana de [[Belize]], que são países de [[línguas germânicas]]. Também engloba alguns países da [[América Central Insular]] (países compostos de [[ilha]]s e [[arquipélago]]s banhados pelo [[Mar do Caribe]]), como [[Cuba]], [[Haiti]] e [[República Dominicana]]. Da [[América do Norte]], apenas o [[México]] é considerado como parte da América Latina.<ref name="America Latina">{{citar web|url=http://www.infoescola.com/geografia/america-latina/|título=América Latina|autor=Caroline Faria|data=19 de outubro de 2008|publicado=Info Escola|língua=português|acessodata=12 de dezembro de 2011}}</ref> A região engloba 20 [[país]]es: [[Argentina]], [[Bolívia]], [[Brasil]], [[Chile]], [[Colômbia]], [[Costa Rica]], [[Cuba]], [[Equador]], [[El Salvador]], [[Guatemala]], [[Haiti]], [[Honduras]], [[México]], [[Nicarágua]], [[Panamá]], [[Paraguai]], [[Peru]], [[República Dominicana]], [[Uruguai]] e [[Venezuela]].<ref name="paises">{{citar web|url=http://www.portalbrasil.net/americas.htm|título=Países das Américas|autor=Fernando Toscano|data=2011|publicado=Portal Brasil|língua=português|acessodata=12 de dezembro de 2011}}</ref>

A expressão "América Latina" foi utilizada pela primeira vez em 1856 pelo filósofo chileno Francisco Bilbao<ref name="Francisco Bilbao">{{Citar web |url=http://www.clarin.com/diario/2005/05/16/opinion/o-01901.htm |título=América Latina o Sudamérica?'', por Luiz Alberto Moniz Bandeira, Clarín, 16 de mayo de 2005 |língua=espanhol |autor= |obra= |data= |acessodata=}}</ref> e, no mesmo ano, pelo escritor colombiano José María Torres Caicedo;<ref name="José María Torres Caicedo">{{citar web|url=http://www.filosofia.org/hem/185/18570215.htm|título=Las dos Américas (poema)|autor=TORRES CAICEDO, José María|data=|publicado=Cola da Web|língua=espanhol|acessodata=29 de maio de 2012}}</ref> e aproveitada pelo imperador francês [[Napoleão III]] durante sua invasão francesa no México como forma de incluir a França — e excluir os anglo-saxões — entre os países com influência na América, citando também a [[Indochina]] como área de expansão da [[França]] na segunda metade do [[século XIX]].<ref>{{citar web|url=http://www.languagehat.com/archives/001218.php|título=LATIN AMERICA|autor=Language Hat|data=21 de março de 2004|publicado=Language Hat|língua=inglês|acessodata=12 de dezembro de 2011}}</ref> Deve-se também observar que na mesma época foi criado o conceito de [[Europa latina|Europa Latina]], que englobaria as regiões de predomínio de [[línguas românicas]].<ref>A Europa Latina, por sua vez, engloba [[Portugal]], [[Espanha]], [[Andorra]], [[França]], [[Mônaco]], [[Itália]], [[San Marino]], [[Vaticano]] e [[Romênia]]</ref> Pesquisas sobre a origem da expressão conduzem, ainda, a [[Michel Chevalier]], que mencionou o termo "América Latina" em 1836, durante uma [[missão diplomática]] feita aos Estados Unidos e ao México.<ref>{{citar web|url=http://netviagens.sapo.pt/Ferias/CircuitosDetalhe.aspx?channelId=9D2140A0-A388-41E8-A6EB-51BEEF686FFF|título=América Latina|autor=Net Viagens|data=2011|publicado=Net Viagens|língua=português|acessodata=12 de dezembro de 2011}}</ref> Nos Estados Unidos, o termo não foi usado até o final do século XIX tornando-se comum para designar a região ao sul daquele país já no início do século XX.<ref name="Enciclopédia Canção Nova">{{citar web|url=http://wiki.cancaonova.com/index.php/América_Latina|título=América Latina|autor=Enciclopédia Canção Nova|data=2011|publicado=Enciclopédia Canção Nova|língua=português|acessodata=12 de dezembro de 2011}}</ref> Ao final da [[Segunda Guerra Mundial]], a criação da [[Comissão Econômica para a América Latina e o Caribe]] consolidou o uso da expressão como sinônimo dos países menos desenvolvidos dos continentes americanos, e tem, em consequência, um significado mais próximo da economia e dos assuntos sociais.<ref name="Enciclopédia Canção Nova"/>

Convém observar que a [[Organização das Nações Unidas]] reconhece a existência de dois [[continente]]s: [[América do Sul]] e [[América do Norte]], sendo que esta última se subdivide em [[Caribe]], América Central e América do Norte propriamente dita, englobando México, Estados Unidos e Canadá, além das ilhas de [[Saint Pierre et Miquelon]], [[Bermudas]] e a [[Groenlândia]].<ref name="Enciclopédia Canção Nova"/> As antigas colônias neerlandesas (e, atualmente, países constituintes do [[Reino dos Países Baixos]]) [[Curaçao]], [[Aruba]] e [[São Martinho (Caraíbas)|São Martinho]] não são habitualmente consideradas partes da América Latina, embora sua língua mais falada seja o [[papiamento]], língua de influência ibérica (embora não considerada latina).<ref name="Enciclopédia Canção Nova"/>

== Etimologia ==
O termo foi utilizado pela primeira vez em [[1856]], numa conferência do filósofo chileno [[Francisco Bilbao]]<ref name="Francisco Bilbao" /> e, no mesmo ano, pelo escritor colombiano [[José María Torres Caicedo]] em seu poema ''Las dos Américas'' ("As duas Américas", em português)<ref name="José María Torres Caicedo" />.

O termo "América Latina" foi usado pelo Império Francês de [[Napoleão III da França]] durante sua [[Segunda intervenção francesa no México|invasão francesa no México]] (1863-1867) como forma de incluir a [[França]] entre os países com influência na América e excluir os [[anglo-saxões]]. Desde sua aparição, o termo evoluiu para designar e compreender um conjunto de características culturais, étnicas, políticas, sociais e econômicas.<ref>{{Citar web |url=http://milenio.com/monterrey/milenio/notaanterior.asp?id=912184 |titulo=El nombre de América Latina |publicado= Ediciones Impresas Milenio|acessodata= [[9 de Novembro]] de [[2009]]}}</ref>

== História ==
{{Artigo principal|História da América Latina}}
{{Vertambém|História da América do Norte|História da América do Sul|História da América Central|História do Caribe}}

=== Primeiros povos ===
{{Artigo principal|Povoamento da América|História demográfica dos povos indígenas das Américas|Era pré-colombiana}}

[[Imagem:Mexico SunMoonPyramid.jpg|thumb|esquerda|[[Teotihuacan]], atual [[México]], vista da via de entrada dos mortos a partir da [[pirâmide da Lua]].]]

A chegada à [[América]] dos primeiros [[humano]]s oriundos da [[Ásia]] ocorreu cerca de 20 mil anos antes da chegada de [[Cristóvão Colombo]] ao [[hemisfério ocidental]].<ref>{{citar web|url=http://www.coladaweb.com/historia/chegada-do-homem-na-america|título=Chegada do Homem na América|autor=FERREIRA, José|data=|publicado=Cola da Web|língua=português|acessodata=27 de junho de 2011}}</ref> É possível que os primeiros colonos tenham vindo da Ásia para a América, fazendo a travessia de uma ponte feita de terra, chamado de [[Beríngia]], no tempo da [[era glacial]], ou fazendo a travessia de barca pelo [[estreito de Bering]], ou ainda, passando de uma ilha para outra, nas [[Aleutas]].<ref name="www.historiamais.com">{{citar web|url=http://www.historiamais.com/homemamericano.htm|título=A Origem do Homem Americano|autor=|data=|publicado=História Mais|língua=português|acessodata=27 de junho de 2011}}</ref> Dirigindo-se do sul, foram, gradualmente, sendo espalhados pelas Américas.<ref name="www.historiamais.com"/>

Essas [[População|populações]] que se originaram da [[Ásia]], a quem são chamados pelos ocidentais de [[povos indígenas das Américas]], ou ameríndios, tiveram perambulação pela terra, praticando a [[caça]] e a [[pesca]].<ref>{{citar web|url=http://www.pime.org.br/missaojovem/mjregtradicind.htm|título=O mundo religioso dos indígenas “primitivos|autor=BESEN, José Artulino|data=|publicado=Pontifício Instituto Missões Exteriores|língua=português|acessodata=27 de junho de 2011}}</ref> Depois de uma grande quantidade de gerações na [[América]], certas tribos foram desenvolvedoras de novos modos de vida.<ref name="Enciclopédia Delta Universal 421">{{cite encyclopedia |encyclopedia=Enciclopédia Delta Universal |title=América Latina: História |edition=volume 1 |year=1982 |publisher=Delta |language=português |location=São Paulo |id= |doi= |pages=pp. 421 |quote= }}</ref> Ao invés de continuarem perambulantes, foram construtores de comunidades agrícolas e de civilizações.<ref name="Enciclopédia Delta Universal 421"/> Foram os mais antigos povos plantadores de [[cacau]], [[milho]], [[feijão]], [[fava]]s, [[batata]]s, [[abóbora]] e [[tabaco]].<ref>{{citar web|url=http://www.klickeducacao.com.br/conteudo/pagina/0,6313,POR-1376-10971-,00.html|título=A agricultura da América|autor=|data=|publicado=Klick Educação|língua=português|acessodata=27 de junho de 2011}}</ref> Nas regiões onde foram conseguidas boas [[Agricultura|colheitas]] e com a possibilidade de viver tranquilamente, a população teve crescimento rápido.<ref name="Enciclopédia Delta Universal 421"/>

A [[cultura maia]] foi a mais antiga [[civilização]] de alto desenvolvimento no [[hemisfério ocidental]].<ref>{{citar web|url=http://pt.shvoong.com/humanities/475076-civilização-maia/|título=A Civilização Maia|autor=Jesus e Oscar Aquino|data=|publicado=Shvoong|língua=português|acessodata=27 de junho de 2011}}</ref> Teve início na [[América Central]] mais de cem anos antes da época em que nasceu [[Jesus Cristo]].<ref>{{citar web|url=http://www.historiadomundo.com.br/maia/maias.htm|título=Civilização Maia - História dos Maias|autor=|data=|publicado=História do Mundo|língua=português|acessodata=27 de junho de 2011}}</ref> Por volta do ano [[600 a.C.]], os [[maias]] haviam sido os criadores de um [[calendário]] e de um [[alfabeto]] de [[ideogramas]].<ref>{{citar web|url=http://www.espiritualismo.hostmach.com.br/maias.htm|título=Maias: Ascensão e Queda|autor=FIGUEIREDO, Beraldo|data=|publicado=Espiritualismo|língua=português|acessodata=27 de junho de 2011}}</ref> Foram criadores, também, de estilos [[Arquitetura|arquitetônicos]], [[escultura]]is e de trabalhos [[Metalurgia|metalúrgicos]].<ref>{{citar web|url=http://www.historiadomundo.com.br/maia/arte-e-arquitetura-maia.htm|título=Arte e Arquitetura Maia - História da Arte e Arquitetura Maia|autor=|data=|publicado=História do Mundo|língua=português|acessodata=31 de agosto de 2011}}</ref> Eram possuidores de um governo de boa organização<ref>{{citar web|url=http://www.doismiledoze.com/maias-organizacao-politica-e-social/|título=Maias: Organização política e social|autor=Fenrir|data=2011|publicado=Dois Mil e Doze|língua=português|acessodata=31 de agosto de 2011}}</ref> e conheciam bastante [[astronomia]]<ref>{{citar web|url=http://super.abril.com.br/revista/240a/materia_especial_261510.shtml?pagina=1|título=Como os maias sabiam tanto sobre astronomia?|autor=Tiago Cordeiron|data=|publicado=Superinteressante|língua=português|acessodata=31 de agosto de 2011}}</ref> e [[agricultura]].<ref>{{citar web|url=http://www.doismiledoze.com/maias-a-economia/|título=Maias: Economia e Agricultura|autor=Fenrir|data=2011|publicado=Dois Mil e Doze|língua=português|acessodata=31 de agosto de 2011}}</ref>

Na época em que os [[espanhóis]] invadiram a [[América Central]], no [[século XVI]], ali ocorria o florescimento das três grandes civilizações ameríndias: a [[civilização maia]], na América Central (influenciada pela [[Toltecas|civilização tolteca]], do [[México]], a partir do [[século X]] d.C.); a [[civilização asteca]], no México; e a [[civilização inca]], no [[Equador]], no [[Peru]] e da [[Bolívia]].<ref>{{citar web|url=http://www.suapesquisa.com/astecas/|título=História dos Maias, História dos Astecas e História dos Incas|autor=|data=2011|publicado=Suapesquisa.com|língua=português|acessodata=31 de agosto de 2011}}</ref> Essas civilizações tiveram grande influência para que fosse desenvolvida posteriormente a América Latina.<ref name="Enciclopédia Delta Universal 421" /> O [[ouro]] e a [[prata]] que existiram em suas minas fizeram com que os espanhóis fossem os conquistadores dos [[Povo indígena|povos indígenas]] na maior rapidez possível.<ref name="Enciclopédia Delta Universal 421" /> {{panorama|95 - Machu Picchu - Juin 2009.jpg|810px|[[Panorama]] de [[Machu Picchu]], uma antiga cidade do [[Império Inca]] em meio aos [[Andes]] [[peru]]anos, na [[América do Sul]].}}"""

prs = mwparserfromhell.parse(tst_string.tst_str)


#print(prs.filter_headings())
# #print(prs.get_sections())
# for section in prs.get_sections():
#     print(section.filter_headings())
#     for sec in section.filter_headings():
#         print('->'+str(sec.title))

# for link in prs.filter_wikilinks():
#     print(link.title.lower())

cleaner = src.PTwikitextCleaner(txt)
cleaner = src.PTwikitextCleaner(tst_string.tst_str)



regex = r'\[\[Categoria:[] ]]'

print(cleaner.clean())
#print(prs.strip_code())


#coord_re = re.sub(r'\{\{lang-[a-z]+\|([^}]*)\}\}', r"\1", """{{lang-es|''América Latina'' ou ''Latinoamérica''}}; {{lang-fr|''Amérique latine''}}""")
#print(coord_re)
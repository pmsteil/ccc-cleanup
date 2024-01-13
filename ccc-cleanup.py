"""
    This script will cleanup the text of the CCC text file
"""
import sys
import re

DEBUG_100 = 0
DEBUG_110 = 0
DEBUG_120 = 0
DEBUG_130 = 0
DEBUG_140 = 0
DEBUG_150 = 0
DEBUG_160 = 0
DEBUG_200 = 0
DEBUG_300 = 0
DEBUG_310 = 0
DEBUG_320 = 0
DEBUG_330 = 0
DEBUG_340 = 0
DEBUG_350 = 0
DEBUG_360 = 0
DEBUG_370 = 0
DEBUG_380 = 0
DEBUG_400 = 0


# TODOS:
#   - replace 'Sng and music' with 'Song and music'
#   - replace 'Is_this' with 'Is this'
#   - check to see why we needed this: cleanupLastFootnotes_400


# the books as they appeared in the original ccc text
original_ot_books = ['Gen', 'Ex', 'Lev', 'Num', 'Dt', 'Josh', 'Judg', 'Ruth',
                     'I Sam', 'II Sam', 'I Kgs', 'II Kgs', 'I Chr', 'II Chr',
                     'Ezra', 'Neh', 'Tob', 'Jdt', 'Esth', 'I Macc', 'II Macc',
                     'Job', 'Ps', 'Prov', 'Eccl', 'Song', 'Wis', 'Sir', 'Is', 'Jer',
                     'Lam', 'Bar', 'Ezek', 'Dan', 'Hos', 'Joel', 'Amos', 'Obad',
                     'Jon', 'Mic', 'Nah', 'Hab', 'Zeph', 'Hag', 'Zech', 'Mal']
original_nt_books = ['Mt', 'Mk', 'Lk', 'Jn', 'Acts', 'Rom', 'I Cor', 'II Cor', '1 Cor', '2 Cor',
                     'Gal', 'Eph', 'Phil', 'Col', 'I Thess', 'II Thess', '1 Thess', '2 Thess',
                     'I Tim', 'II Tim',
                     '1 Tim', '2 Tim', 'Titus', 'Phlm', 'Heb', 'Jas', 'I Pt', 'II Pt',
                     'I Jn', 'II Jn', 'III Jn', 'Jude', 'Rev']

# spell out ot book names
new_ot_books = [ 'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges',
                'Ruth', 'I Samuel', 'II Samuel', 'I Kings', 'II Kings', 'I Chronicles',
                'II Chronicles', 'Ezra', 'Nehemiah', 'Tobit', 'Judith', 'Esther', 'I Maccabees',
                'II Maccabees', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Songs',
                'Wisdom', 'Sirach', 'Isaiah', 'Jeremiah', 'Lamentations', 'Baruch', 'Ezekiel',
                'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum',
                'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi' ]
new_nt_books = [ 'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', 'I Corinthians',
                'II Corinthians', 'I Corinthians', 'II Corinthians', 'Galatians', 'Ephesians',
                'Philippians', 'Colossians', 'I Thessalonians', 'II Thessalonians', 'I Thessalonians', 'II Thessalonians',
                'I Timothy',
                'II Timothy', 'I Timothy', 'II Timothy', 'Titus', 'Philemon', 'Hebrews', 'James',
                'I Peter', 'II Peter', 'III John', 'II John', 'I John', 'Jude', 'Revelation']



# must be global, used by cleanupFootnotes1_110 and 2
other_books = [ 'Roman', 'CD', 'CT', 'Cf.', 'Extraordinary Synod of Bishops',
               'John Paul II, Discourse', 'GS', 'St. Augustine,', 'St. Thomas Aquinas,',
               'Vatican Council', 'Pius', 'ZZZLiturgy', 'Lateran Council', 'DV', 'St. Irenaeus,',
               'St. John of the Cross,', 'UR', 'LG', 'St. Gregory the Great,', 'St. Bernard,',
               'Origen,', 'Lettera gesta docet,','St. Caesaria the Younger',
               'St. Therese of Lisieux,', 'Dei', 'John Henry Cardinal Newman,',
               'St. Anselm,', 'DH', 'St. Basil De Spiritu Sancto', 'Faustus of Riez,',
               'St. Cyril of Jerusalem,', 'Paul', 'St. Ambrose,', 'EX', 'St. Joan of',
               'St. Nicholas of', 'St. Teresa', 'St. Caesarius of Arles,', 'GCD',
               'The English phrases', 'Niceno-Constantinopolitan Creed;', 'Nicene Creed;',
               'Council of', 'Fides', 'St. Basil,', 'St. Francis', 'St. Benedict,', 'LH,', 'LH',
               'Prayer of Blessed Elizabeth', 'AG', 'DS', 'LC', 'John', 'Byzantine', 'OC',
               'B Rituale per', 'CIC,', 'SC', 'PO', 'Congregation of Rites,', 'ZZZApostolic',
               'B Cf.', 'OE', 'GIRM', 'Fanqith,', 'Didache', 'EP', 'OP', 'Tertullian,',
               'Indulgentiarum', 'BCIC,', 'OT', 'St. Peter', 'St. Catherine',
               'St. John of the Cross,', 'St. John Chrysostom,', 'St. John Damascene,',
               'St. John Eudes:', 'St. John Eudes,','St. John of the Cross,',
               'St. John Vianney,', 'St. Maximus', 'St. Leo', 'St. Gregory of Nazianzus, Oratio',
               'St. Bonaventure,', 'St. Theophilus of Antioch,', '2 Macc',
               'The Correspondence of Sir Thomas More,', 'Julian of Norwich,',
               'St. Fulgentius of Ruspe,', 'St. Ignatius of Antioch,', 'St. Justin,', 'St. Monica,',
               'St. Thomas Aquinas', 'FC', 'CELAM,', 'Niceno-Constantinopolitan Creed.', 'OCF',
               'St. Simeon of Thessalonica,', 'St. Gregory of Nyssa,', 'St.Teresa of Avila,',
               'RP', 'cf. Mt', 'CA', 'St. Clement of Rome,', 'Ep. Barnabae,', 'CS', 'Leo XIII,',
               'Cicero,', 'St. Athanasius,', 'St.Therese of Lisieux,', 'AA', 'NA',
               'Sermo de die dominica', 'GE', 'Ad Diognetum 5,', 'CDF,', 'Cf.Tob', 'MD', 'Cf.Titus',
               'HV', 'SRS', 'P. Hansen,', 'Martyrium Polycarpi', 'St. Ignatius of Loyola,',
               'IM', 'St. Gregory the Great Moralia', 'Pastor Hermae,', 'Evagrius Ponticus,',
               'St. Alphonsus Liguori,', 'Tertullian De orat.', 'St. Cyprian,',
               'St. Ambrose De Sacr.', 'St. Cyprian,', 'Ad Diognetum', 'St. Cyprian De',
               'Attributed to St. Ignatius Loyola,', 'St. Bernard of Clairvaux,',
               'Clement of Alex.,', 'Kontakion of Romanos', 'St. Hilary of Poitiers,',
               'St. Rose of Lima:', 'Ancient Homily for Holy Saturday:', 'St. John Cassian,',
               'Liturgy of St. John']
footnote_books = other_books + original_ot_books + original_nt_books

# eccliastical books referenced in CCC footnotes
# Common ecclesiastical document references in the CCC
# Abbreviations used in the Catechism of the Catholic Church with full names
ecclesiastical_documents_full = [
    ('AA', 'Apostolicam actositatem'),
    ('AAS', 'Acta Apostolicae Sedis'),
    ('AF', 'J.B. Lightfoot, ed., The Apostolic Fathers (New York: Macmillan, 1889-1890)'),
    ('AG', 'Ad gentes'),
    ('Ben', 'de Benedictionibus'),
    ('CA', 'Centesimus annus'),
    ('Catech. R.', 'Catechismus Romanus'),
    ('CCEO', 'Corpus Canonum Ecclesiarum Orientalium'),
    ('CCL', 'Corpus Christianorum, Series Latina (Turhout, 1953- )'),
    ('CD', 'Christus Dominus'),
    ('CDF', 'Congregation for the Doctrine of the faith'),
    ('CELAM', 'Consejo Episcopal Latinoamericano'),
    ('CIC', 'Codex Iuris Canonici'),
    ('CL', 'Christifideles laici'),
    ('COD', 'Conciliorum oecumenicorum decreta'),
    ('CPG', 'Solemn Profession of faith: Credo of the People of God'),
    ('CSEL', 'Corpus Scriptorum Ecclesiasticorum Latinorum (Vineea, 1866- )'),
    ('CT', 'Catechesi tradendae'),
    ('DeV', 'Dominum et Vivificanum'),
    ('DH', 'Dignitatis humanae'),
    ('DM', 'Dives in misericordia'),
    ('DS', 'Denzinger-Schonmetzer, Enchiridion Symbolorum, definitionum et declarationum de rebus fidei et morum (1965)'),
    ('DV', 'Dei Verbum'),
    ('EN', 'Evangelii nuntiandi'),
    ('EP', 'Eucharistic Prayer'),
    ('FC', 'Familiaris consortio'),
    ('GCD', 'General Catechetical Directory'),
    ('GE', 'Gravissimum educationis'),
    ('GILH', 'General Introduction to LH'),
    ('GIRM', 'General Instruction to RomM'),
    ('GS', 'Gaudium et spes'),
    ('HV', 'Humanae vitae'),
    ('ICEL', 'International Commission on English in the Liturgy'),
    ('IM', 'Inter mirifica'),
    ('LE', 'Laborem exercens'),
    ('LG', 'Lumen gentium'),
    ('LH', 'Liturgy of the Hours'),
    ('LXX', 'Septuagint'),
    ('MC', 'Marialis cultus'),
    ('MD', 'Mulieris dignitatem'),
    ('MF', 'Mysterium fidei'),
    ('MM', 'Mater et magistra'),
    ('NA', 'Nostra aetate'),
    ('NCCB', 'National Conference of Catholic Bishops (U.S.A.)'),
    ('ND', 'Neuner-Dupuis, The Christian Faith in the Doctrinal Documents of the Catholic Church'),
    ('OBA', 'Ordo baptismi adultorum'),
    ('OC', 'Ordo confirmarionis'),
    ('OCF', 'Order of Christian Funerals'),
    ('OCM', 'Ordo celebrandi Matrimonium'),
    ('OCV', 'Ordo consecrarionis virginum'),
    ('OE', 'Orientalium ecclesiarum'),
    ('OP', 'Ordo paenitantiae'),
    ('OR', 'Office of Readings'),
    ('OT', 'Optatam totius'),
    ('PC', 'Perfectae caritatis'),
    ('PG', 'J.P. Migne, ed., Patroligia Greaca (Paris, 1867-1866)'),
    ('PL', 'J.P. Migne, ed., Patroligia Latina (Paris, 1841-1855)'),
    ('PLS', 'J.P. Migne, ed., Patroligia Latina Supplement'),
    ('PO', 'Presbyterorum ordinis'),
    ('PP', 'Populorum progressio'),
    ('PT', 'Pacem in terris'),
    ('RBC', 'Rite of Baptism of Children'),
    ('RCIA', 'Rite of christian initiation of adults'),
    ('RH', 'Redemptor hominis'),
    ('RomM', 'Roman Missal'),
    ('RMat', 'Redemptoris Mater'),
    ('RMiss', 'Redemptoris Missio'),
    ('RP', 'Reconciliatio et paenitentia'),
    ('SC', 'Sacrosanctum concilium'),
    ('SCG', 'Summa Contra Gentiles'),
    ('SCh', 'Sources Chretiennes (Paris: 1942- )'),
    ('SRS', 'Sollicitudo rei socialis'),
    ('STh', 'Summa Theologiae'),
    ('UR', 'Unitatis redintegratio')
]







def cleanupFootnotes0_100( text, debug_level ):
    """
        Cleanup more footnotes
    """
    footnote_search     = [  '“', ' ', ' Cf ', 'Cf.Wis', 'DV10# ', 'Cf.Vatican Council', 'cf. Jn', 'Cf Jn', '1 Tim ', 'DV8', 'St.Thomas Aquinas,', 'St. Caesaria theYounger', '1 Cor ', 'l Cor', ' 2 Sam ', 'Cf Wis', 'Cf Ps', 'l Jn', '67Niceno-Constantinopolitan', 'Pss ', ' 1 Th ', ' 2 Th ', ' 1 Jn ', ' Cf Mt ', ' 2 Pt ', '116 Cal 2:20.', ' Cf Rev ', ' Cf Mk ', 'SL Ambrose', '160 In 6', '2452 Pet 3:13.', '7 ? Cor ', '11 1Jn1', ' 1 Pet ', '123T Cf. CCEO, can. 828.', '182 Niceno-Constantinopolitan Creed.', ' 2 Pet ', '1802TheWord', '661 Pet 4:7.', '901 Thess ', ' PS ', ' Deut ', '? Sir', '67B John Paul II, Evangelium vitae 56.', '73?s', '99 Isa ', ' Philem ', ' 2 Thess ', 'Deut ', '250 Am ', '1 Sam ', ' 1 Kings ', '1Thess5', '114PS', '124 Am', '? Cor 15:24-28', '469Bis Acts 2:24.', '461Mt ' ]
    footnote_replace    = [  '"', '', ' Cf. ', 'Cf. Wis', 'DV 10 # ', 'Cf. Vatican Council', 'Cf. Jn', 'Cf. Jn', 'I Tim ', 'DV 8', 'St. Thomas Aquinas,', 'St. Caesaria the Younger', 'I Cor ', 'I Cor', ' II Sam ', 'Cf. Wis', 'Cf. Ps', 'I Jn', '67 Niceno-Constantinopolitan', 'Ps ', ' I Thess ', ' II Thess ', ' I Jn ', ' Cf. Mt ', ' II Pt ', '116 Gal 2:20.', ' Cf. Rev ', ' Cf. Mk ', 'St. Ambrose', '160 Jn 6', '245 II Pt 3:13.', '7 II Cor ', '11 I Jn 1', ' I Pt ', '{footnote #123T: Cf. CCEO, can. 828.}', '182 Niceno-Constantinopolitan Creed. ', ' II Pt ', '1802 The Word', '66 I Pt 4:7.', '90 I Thess ', ' Ps ', ' Dt ', 'Sir', '{footnote #67B: John Paul II, Evangelium vitae 56.}', '73 Ps', '99 Is ', ' Phlm ', ' II Thess ', 'Dt ', '250 Amos ', 'I Sam ', ' I Kgs ', 'I Thess 5', '114 Ps', '124 Amos', '1 Cor 15:24-28', '{footnote #469B: Acts 2:24.}', '461 Mt ']
    # search for footnote_search and replace with footnote_replace
    for i in range( len( footnote_search ) ):
        text = text.replace( footnote_search[i], footnote_replace[i] )

    return text







def cleanupFootnotes1_110( text, debug_level ):
    """
    cleanup ones like this:
    1Rev 1:1
    2Jn 1:1
    """
    # use footnote_books in the pattern
    # the regex pattern matches any line that starts with a number and
    # is immediately followed by a book name
    # and then followed by a space and then anything else
    pattern = r"^(\d+)(%s) (.*)" % "|".join(footnote_books)

    def footnote_format(match):
        num, abbr, line = match.groups()
        # print (f">>>footnote: {num}, abbr: {abbr}, line: {line} returning: [^{num}]:{abbr} {line}")
        if num == '':
            raise ValueError( f"footnote num is empty, abbr: {abbr}, line: {line}")
        return f"111[^{num}]:{abbr} {line}"

    text = re.sub(pattern, footnote_format, text, flags=re.MULTILINE)

    return text





# other typos, fixes
def cleanupInlineFootnotes_120( text, debug_level ):
    """
        Cleanup other typos, fixes
    """
    str_search     = [  '"into all the truth".68',    'returned to the Father.69',    'glorification70 reveals',    'from the Father."71',    '"72 "For', '74 On the mountain',       'him!"75 Jesus', 'you."76 This',       'Creator.240 Man',    'him."242 None',    'partner.243 The',    'flesh."244',    'flesh",245 they',    'earth."246 ',    'work.247',    'the earth248',    'exists",249',    'justice".250',    'life".251',    'die.252',    'woman,253',    'concupiscence254',    'garden.255', 'burden,256',       'Augustine,257',    'religion".258',    'grace.259',    'conqueror.260', '190Heb 9:24.'        ]
    str_replace    = [  '"into all the truth".[^68]', 'returned to the Father.[^69]', 'glorification[^70] reveals', 'from the Father."[^71]', '"[^72] "For', '[^74] On the mountain', 'him!"[^75] Jesus', 'you."[^76] This', 'Creator.[^240] Man', 'him."[^242] None', 'partner.[^243] The', 'flesh."[^244]', 'flesh",[^245] they', 'earth."[^246] ', 'work.[^247]', 'the earth[^248]', 'exists",[^249]', 'justice".[^250]', 'life".[^251]', 'die.[^252]', 'woman,[^253]', 'concupiscence[^254]', 'garden.[^255]', 'burden,[^256]', 'Augustine,[^257]', 'religion".[^258]', 'grace.[^259]', 'conqueror.[^260]', '190 Heb 9:24.' ]
    # str_search for str_search and replace with str_replace
    for i in range( len( str_search ) ):
        text = text.replace( str_search[i], str_replace[i] )

    return text







def formatFootnote_130( text, debug_level ):
    """
        Looking for a footnote to format like these:
            1 Jn 17 3
            2 1 Tim 2:3-4.
            3 Acts 4:12
        and convert to:
            [^1]: 1 Jn 17 3
            [^2]: 1 Tim 2:3-4.
            [^3]: Acts 4:12
    """
    # regex pattern: ^ matches the beginning of the line
    # \d+ matches one or more digits
    # %s matches any of the footnote_books
    # followed by a space, followed by any other text
    pattern = r"^(\d+) (%s) (.*)" % "|".join(footnote_books)

    def footnote_format(match):
        num, abbr, line = match.groups()
        # strip num, abbr, line

        # return "[^%s]:%s %s" % (num, abbr, line)
        return f"[^{num}]:{abbr} {line}"

    text = re.sub(pattern, footnote_format, text, flags=re.MULTILINE)

    return text






# create function to search through the text looking for any line that starts with "[^9]:" and replace any book names using the replace_ecclesiastical_abbreviations function
def replaceScriptureBooksInFootnotes_140( text, debug_level ):
    """
        Replace the scripture books in the footnotes
    """

    def _renameScriptureBooks( text ):
        """
        Rename the scripture books in the footnotes
        from the original abbreviated names to the full names
        """

        footnote_search     = original_ot_books + original_nt_books
        footnote_replace    = new_ot_books + new_nt_books
        # search for footnote_search and replace with footnote_replace
        for i in range( len( footnote_search ) ):
            text = text.replace( footnote_search[i], footnote_replace[i] )

        return text



    # find the footnote markers and replace the book names
    pattern = r"(\[\^\d+\]):(.*)"

    def footnote_format(match):
        footnote, line = match.groups()
        return "%s: %s" % ( footnote, _renameScriptureBooks( line ) )

    text = re.sub(pattern, footnote_format, text, flags=re.MULTILINE)

    return text







# create function to search through the text looking for any line that starts with "[^9]:" and replace any book names using the replace_ecclesiastical_abbreviations function
def replaceEccliasticBooksInFootnotes_150( text, debug_level ):
    """
        Replace the ecclesiastical books in the footnotes
    """
    # create function to search through only the footnotes and call the replace_ecclesiastical_abbreviations function on each one
    def _replace_ecclesiastical_abbreviations(text, replacements):
        for abbreviation, full_name in replacements:
            full_name_with_quotes = f'"{full_name}"'  # Enclose the full name in double quotes
            text = text.replace(abbreviation, full_name_with_quotes)
        return text

    # find the footnote markers and replace the book names
    pattern = r"(\[\^\d+\]):(.*)"

    def footnote_format(match):
        footnote, line = match.groups()
        return "%s: %s" % ( footnote, _replace_ecclesiastical_abbreviations( line, ecclesiastical_documents_full ) )

    text = re.sub(pattern, footnote_format, text, flags=re.MULTILINE)


    return text













def formatFootnoteMarker_160( text, debug_level ):
    """
        Find any lines that are NOT a footnote and
        end with a number and format it as a footnote marker
        like this:
            "FATHER,... this is eternal life, that they may know you, the only true God, and Jesus Christ whom you have sent."1
            "God our Saviour desires all men to be saved and to come to the knowledge of the truth."2
            "There is no other name under heaven given among men by which we must be saved"3 - than the name of JESUS.
    """
    # need an RE pattern that matches any line that does NOT begin with
    # [^\d+] and ends with a number of any length but at least 1 digit
    pattern = r"^(?![\^\d+]:)(.*)(\d+)$"

    print( f"1debug_level: {debug_level}" )

    def footnote_format(match):
        line, num = match.groups()
        # print( f"\n>>>footnote marker: {line}, {num}")
        debug( f"\n>>> footnote marker: {line}, {num}", debug_level )

        if "[^" not in line:
            # return "%s [^%s]" % (line, num)
            return f"{line} [^{num}]"
        else:
            return f"{line} {num}"

    text = re.sub(pattern, footnote_format, text, flags=re.MULTILINE)

    return text

def debug( text, debug_level ):
    """
        Debug function
    """
    if debug_level > 0:
        print( f"{text}" )
    # return text


# other typos, fixes, anywhere in the text
def cleanupOther_200( text, debug_level ):
    """
        Cleanup other typos, fixes
    """
    str_search     = [  'Article 9THE NINTH', 'The Interpretation of the Heritage of FaithThe heritage of faith entrusted to the whole of the Church', '348The sabbath ',      '460TheWord became flesh',    '408 I John ',         '."488',    'life.489I.',      '503 1 Lk 24:17;',    '512 O vere beata',    '518I Th',       '540 Missale Romanum,',    '547 Nicene Creed.', '4 In 17:3.', '17 In 3:5-8.',           '18 In 14:16,',     '20 In 16:13.',     '261 Pet 4:14.',     '42 1 Thess 5:19.',     '67 Cf.Jn 1:14; Phil 2:7.',     '78Isa 43:19.',     '81Isa 11:1-2.', '84Isa 61:',         '[^718]:  ',   '[^719]:  ',     '133 St. Cyril of Alexandria,',      '137 St. Hippolytus,',     '2021 Pet 2:9.',     '231 Pope St. Gregory',        '262 St. Clement ', '305 CL 17, 3.',         '458 PC 1.' , '460CIC,', '460BCf. ', '460T Cf. ','Matthew19:12', '463 Ordo Consecrationis', '477 Nicetas', '497 Martyrium', '494 St. Dominic', '556 1 Thess 4', '587 The Imitation', '589 OCF', '597 Benedict', '6302 Pet 3', '645 Isa', '4 eu-logia,','45 Ep. 8.', '35 St. Hippolytus', '39 St. Jerome,', '43 St. Athanasius', '150 Apostolic Constitutions','12 St. Gregory of Nazianzus', '5 Guigo the Carthusian', '7 GILH', '22 St. Gregory', '1 St. Gregory', '469 Bis Acts 2:24.', '518 I Th 4:14.', '78 Isa 43:19.', '81 Isa 11:1-2.', '84 Isa 61:1-2; cf. Lk 4:18-19.', '460 T Cf. John Paul II,Vita Consecrata 7.' ]
    str_replace     = [  'Article 9THE NINTH', 'The Interpretation of the Heritage of FaithThe heritage of faith entrusted to the whole of the Church', '348 The sabbath ',      '460 TheWord became flesh', '[^408]: I John ', '."[^488]', 'life.[^489]\nI.', '[^503]:1 Lk 24:17;', '[^512]:O vere beata', '[^518]   I Th', '[^540]:Missale Romanum,', '[^547]:Nicene Creed.', '[^4]:In 17:3.', '[^17]: In 3:5-8.', '[^18]: In 14:16,', '[^20]: In 16:13.', '[^26]:1 Pet 4:14.', '[^42]: 1 Thess 5:19.', '[^67]: Cf.Jn 1:14; Phil 2:7.', '[^78]:Isa 43:19.', '[^81]:Isa 11:1-2.', '[^84]:Isa 61:', '\nCCC 718\n', '\nCCC 719\n',   '[^133]:  St. Cyril of Alexandria,', '[^137]: St. Hippolytus,', '[^202]:1 Pet 2:9.', '[^231]: Pope St. Gregory',    '[^262]: St. Clement ', '[^305]: CL 17, 3.', '[^458]: PC 1.' , '460 CIC,', '[^460B] Cf. ', '[^460T] Cf. ','Matthew 19:12','[^463] Ordo Consecrationis','[^477] Nicetas','[^497] Martyrium','[^494] St. Dominic','[^556] 1 Thess 4','[^587] The Imitation', '[^589] OCF','[^597] Benedict','[^630] 2 Pet 3','[^645] Isa','[^4] eu-logia,','[^45] Ep. 8.','[^35] St. Hippolytus','[^39] St. Jerome,','[^43] St. Athanasius','[^150] Apostolic Constitutions','[^12] St. Gregory of Nazianzus','[^5] Guigo the Carthusian','[^7] GILH','[^22] St. Gregory','[^1] St. Gregory','[^469Bis] Acts 2:24.','[^518] I Th 4:14.','[^78] Isa 43:19.','[^81] Isa 11:1-2.','[^84] Isa 61:1-2; cf. Lk 4:18-19.','[^460T] Cf. John Paul II,Vita Consecrata 7.' ]
    # search for str_search and replace with str_replace
    for i in range( len( str_search ) ):
        text = text.replace( str_search[i], str_replace[i] )

    return text





def handleCCCParagraphs_300( text, debug_level ):

    # regex pattern matches any line that starts with a number
    pattern = r"^(\d+) (.*)"

    def footnote_format(match):
        num, line = match.groups()
        # print (f"found CCC paragraph: {num}, line: {line} returning: CCC {num}\n{line}")
        return "\nCCC %s\n%s" % (num, line)

    text = re.sub(pattern, footnote_format, text, flags=re.MULTILINE)

    return text



def handlePrologueHeader_310( text, debug_level ):

    pattern = r"^(PROLOGUE)"

    def search_format(match):
        line = match.groups()
        return "%s" % (line)

    text = re.sub(pattern, search_format, text, flags=re.MULTILINE)

    return text




def handlePartsHeader_320( text, debug_level ):

    pattern = r"^(Part .*:)(.*)"

    def search_format(match):
        part, line = match.groups()
        return "%s %s" % (part, line)

    text = re.sub(pattern, search_format, text, flags=re.IGNORECASE | re.MULTILINE)


    return text



def handleSectionHeader_330( text, debug_level ):

    pattern = r"^(Section .*:)(.*)"

    def search_format(match):
        part, line = match.groups()
        return "%s %s" % (part, line)

    text = re.sub(pattern, search_format, text, flags=re.IGNORECASE | re.MULTILINE)


    return text



def handleChapterHeader_340( text, debug_level ):

    pattern = r"^(Chapter .*:)(.*)"

    def search_format(match):
        part, line = match.groups()
        return "%s %s" % (part, line)

    text = re.sub(pattern, search_format, text, flags=re.IGNORECASE | re.MULTILINE)


    return text




def handleArticleHeader_350( text, debug_level ):

    pattern = r"^Article (\d+)(.*)"

    def search_format(match):
        part, line = match.groups()
        return "Article %s: %s" % (part, line)

    text = re.sub(pattern, search_format, text, flags=re.IGNORECASE | re.MULTILINE)


    return text







def handleRomanNumeralHeader_360( text, debug_level ):

    # I. heading...
    pattern = r"(^[iv]+\.)(.*)"

    def search_format(match):
        part, line = match.groups()
        return "%s %s" % (part, line)

    text = re.sub(pattern, search_format, text, flags=re.IGNORECASE | re.MULTILINE)


    return text



def handleParagraphHeader_370( text, debug_level ):

    # Paragraph 1. ...
    pattern = r"(^Paragraph \d\.)(.*)"

    def search_format(match):
        para, line = match.groups()
        return "%s %s" % (para, line)

    text = re.sub(pattern, search_format, text, flags=re.IGNORECASE | re.MULTILINE)


    return text




def handleInBrief_380( text, debug_level ):

    # I. heading...
    pattern = r"(^IN BRIEF)"

    def search_format(match):
        line = match.groups()
        return "IN BRIEF:"

    text = re.sub(pattern, search_format, text, flags=re.IGNORECASE | re.MULTILINE)


    return text





def cleanupLastFootnotes_400( text, debug_level ):
    """
        Cleanup other typos, fixes
        Hmm, why did we need to do this?
    """
    #   - replace 'Sng and music' with 'Song and music'
    #   - replace 'Is_this' with 'Is this'

    str_search     = [ '[^]:   ', 'Sng and music', 'Is_this' ]
    str_replace    = [ '', 'Song and music', 'Is this' ]
    # str_search for str_search and replace with str_replace
    for i in range( len( str_search ) ):
        text = text.replace( str_search[i], str_replace[i] )

    return text










# function that will find each CCC paragraph and print it out with the CCC number
def validateCCCParagraphs( text ):
    """
        Validate that all CCC paragraphs are present and in order
    """
    expected_ccc_paragraphs = 2865

    pattern = r"^CCC (\d+)"

    # def search_format(match):
    #     num = match.groups()
    #     return "%s" % (num)

    ccc_paragraphs = []
    count_warnings = 0

    # loop over text looking for pattern
    for match in re.finditer(pattern, text, flags=re.MULTILINE):
        # print( f"Found CCC #{match.group(0)}" )
        #add found CCC paragraph to list
        ccc_paragraphs.append( match.group(1) )

    print( f"Found {len(ccc_paragraphs)} CCC Paragraphs")

    last_good_paragrah = "-1"
    last_bad_paragraph = "-1"

    #enumerate over list of found CCC paragraphs and make sure the number matches the index
    for i, number_found in enumerate( ccc_paragraphs ):
        # print( f"CCC Paragraph #{i+1} is {ccc_paragraphs[i]} number_found is {number_found}")

        # if the number does not match the index, print a warning
        if (ccc_paragraphs[i].isdigit() is False) or (int( ccc_paragraphs[i] ) != i+1):
            # print( f"\n[Warning]CCC #{i+1} does not validate, the number is {ccc_paragraphs[i]}")
            last_bad_paragraph = ccc_paragraphs[i]
            count_warnings += 1
        else:
            last_good_paragrah = ccc_paragraphs[i]

        if count_warnings > 0:
            print( "1 warnings found, exiting" )
            # print( f"last good paragraph: {last_good_paragrah}, last bad: {last_bad_paragraph}" )
            # print( f"Warning, CCC {last_bad_paragraph} found under CCC {last_good_paragrah} looking for CCC {i+1}")
            print( f"Warning, after CCC {last_good_paragrah} expecting CCC {i+1}, but found CCC {last_bad_paragraph}")
            exit()

        if i+1 == expected_ccc_paragraphs:
            print( f"All {expected_ccc_paragraphs} CCC paragraphs found and verified" )

    # return text






def main():
    """
        Entrypoint for the script
    """

    in_filename = 'ccc-raw.txt'
    out_filename = 'ccc.md'

    print( f"DEBUG_160: {DEBUG_160}" )


    # load the text of the file
    with open( in_filename, 'r', encoding='utf-8') as myfile:
        print( "processing file: " + in_filename )
        text = myfile.read()

    text = cleanupFootnotes0_100( text, DEBUG_100 )
    text = cleanupFootnotes1_110( text, DEBUG_110 )
    text = cleanupInlineFootnotes_120( text, DEBUG_120 )
    text = formatFootnote_130( text, DEBUG_130 )
    text = replaceScriptureBooksInFootnotes_140( text, DEBUG_140 )
    text = replaceEccliasticBooksInFootnotes_150( text, DEBUG_150 )
    text = formatFootnoteMarker_160( text, DEBUG_160 )

    text = cleanupOther_200( text, DEBUG_200 )

    text = handleCCCParagraphs_300( text, DEBUG_300 )
    text = handlePrologueHeader_310( text, DEBUG_310 )
    text = handlePartsHeader_320( text, DEBUG_320 )
    text = handleSectionHeader_330( text, DEBUG_330 )
    text = handleChapterHeader_340( text, DEBUG_340 )
    text = handleArticleHeader_350( text, DEBUG_350 )
    text = handleRomanNumeralHeader_360( text, DEBUG_360 )
    text = handleParagraphHeader_370( text, DEBUG_370 )
    text = handleInBrief_380( text, DEBUG_380 )

    text = cleanupLastFootnotes_400( text, DEBUG_400 )







    # print( text )

    #save file
    with open(out_filename, 'w', encoding='utf-8') as myfile:
        myfile.write(text)
        print( f"Markdown file saved: {out_filename}")


    validateCCCParagraphs( text )


if __name__ == '__main__':

    # process any debug vars passed on command line
    for arg in sys.argv:
        if arg.startswith("DEBUG_"):
            print( f"setting {arg} to 1")
            globals()[arg] = 1

    main()

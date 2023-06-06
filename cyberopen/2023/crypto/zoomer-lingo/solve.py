from pwn import *

def check_same(arr, p1, p2):
    '''
    Check that two blocks are the same 
    p1: first pointer
    p2: second pointer
    returns length of the block
    '''
    ret = 0
    while (arr[p1] == arr[p2]):
        print(p1, p2, arr[p1], arr[p2])
        ret += 1
        p1 += 1
        p2 += 1
    return ret


'''
Should only be 28 characters -> ascii_lowercase + ' ' + ?
'''
char_list = {
    '🍿🍥': 'a',
    '🛀🍸⛩🌖': 'b',
    '🕷🍝🙃🈸🥒🔖🧉👻': 'c',
    '🏙🚞😽🔕🦪🎢': 'd',
    '👦🦴💏': 'e',
    '🐥😂👭🛫📈👚': 'f',
    '🛋🪐🦕🗃🌹🚵📮🤘': 'g',
    '💅🟠👳👷🎬💶': 'h',
    '🧿🚶😆🤒🚩🎟': 'i',
    '🦔🟥✋🧜🚪🤍📒💖🌩': 'j',
    '🐜🕉🌓🍊🤐🏦🎧😋🔍': 'k',
    '⌛🧓🚭🌰🏪😅🎳': 'l',
    '🍭🦜💑😴🍰💮🍼': 'm',
    '🦸🍮🤔': 'n',
    '🥺🆑🕢🛐🧫🟤💙🎤': 'o',
    '🚹🎋🕝🔋': 'p',
    '👀🦼☔🗒': 'q',
    '🔆㊗🎪⌨🍀☀🏭🖐🐔': 'r',
    '👵🚷☎🆕👧🎿🤺': 's',
    '🤿🛅🛬◼🍎🚥🦮💵🤴': 't',
    '🌅🧸🍻🚙😵🦋📚⏲': 'u',
    '🎺🧃😝🙍🍾👗': 'v',
    '🚾🧧⛴♦💳🗼🐒🌕': 'w',
    '🔶🌙': 'x',
    '🎆🦖': 'y',
    '🥗🏵☄◾🚡': 'z',
    '😩🛑🙄😎🙆🧷🍚🔁': '?',
    '📅🐏h🔻': '*'
}


def sandbox():
    f = open('zoomer.emoji', 'r').read()
    print(len(f))
    for k in char_list.keys():
        f = f.replace(k, char_list[k])
    
    new_text = ''
    for i,v in enumerate(f):
        if v not in char_list.values():
            continue
        new_text += v
        

    f2 = open('letters.txt', 'w').write(new_text)
    

    dec = 'zoomerslingowsasnejsvernacularsphakingsgenerationalscommunicationwwlanguagesipsaslivingsentitysthatscontinuouplysevolvepstosreflectsthesekeriencepsandsculturesofsitpspkeaxerpwsapsthesbatonsofscommunicationskappepsfromsonesgenerationstosanotherwsnejslinguipticsptylepsemergewsphakingsthesjaysjesinteractsandsekreppsourpelvepwsinsrecentsyearpwsasdiptinctsvernacularsxnojnsapswzoomerslingowshapstaxenscentersptagewscakturingsthesattentionsofslinguiptpsandspocialsobperverpsalixewsthipseppayseklorepsthescharacteripticpwsoriginpwsandsimkactsofszoomerslingowspheddingslightsonsitpspignificancesapsasformsofsgenerationalsekreppionwwwzoomerslingosreferpstosthesuniqueslinguipticsptylesandsvocabularysemkloyedsbysgenerationszwsalposxnojnsapszoomerpwsbornsbetjeenstheslateswwwwpsandsearlyswwwwpwszupcgwunderptandingtaxepfrequentptudiepwoomerpshavesgrojnsuksinsanserasofsrakidstechnologicalsadvancementwsinptantsconnectivitywsandsglobalizedsculturewsthipsuniquescontetshapsgivensripestosaslanguagesthatsipsheavilysinfluencedsbysdigitalsmediawsmemepwsandsthesfaptwkacedsnaturesofsonlinescommunicationwwwonesofsthesdefiningsfeaturepsofszoomerslingosipsitpsbrevitysandsconcipeneppwszoomerpshavesembracedsthesjorldsofsacronympwsabbreviationpwsandsphortenedsjordpstosconveystheirsthoughtpsquicxlysandsefficientlywsforsinptancewskhrapepslixeswlolwswlaughsoutsloudwwswtbhwswtosbeshoneptwwsandswomgwswohsmysgodwshavesbecomesubiquitoupsinstheirsonlinesconverpationpwsthepesabbreviatedsekreppionpshavesnotsonlysbecomesasphorthandsjaysofscommunicationsbutshavesalposcreatedsaspenpesofscamaraderiesandspharedsunderptandingsamongszoomerpwwwinsadditionstosacronympwszoomerslingosipscharacterizedsbysthesupesofsplangwsjhichsoftensoriginatepsfromskokularsculturewspocialsmediawsandsmemepwsjordpslixeswlitwwswpavagewwswfamwwsandswcloutwshavesenteredsthesmainptreamsleiconsthroughstheslanguagesofszoomerpwsthepestermpscarrysnuancedsmeaningpsandscansbesupedstosconveysasjidesrangesofsemotionpwsekeriencepwsandspocialsdynamicpwstheyspervesapsmarxerpsofsbelongingsandsidentitysjithinstheszoomerscommunitysandscontributestosthesformationsofsasdiptinctsculturalsekreppionwwwzoomerslingosalposthrivepsonsthesupesofsmemepsandsinternetshumorwsmemepwsjhichsareshumoroupsandsoftenspatiricalsimagepwsvideopwsorstetsthatsaresrakidlyspharedsandsreklicatedsonlinewshavesbecomesansintegralskartsofszoomerscommunicationwsmemepsoftensemkloysvipualsandstetualselementpsinscombinationwsrequiringsascertainslevelsofsculturalsliteracystosunderptandsthesreferencepwstheysallojszoomerpstosekreppscomklesideapsandsemotionpsinsaslightheartedsandsrelatablesmannerwsmemepshavestranpcendedsthesdigitalsrealmsandshavesinfiltratedseverydaysconverpationpwsmaxingszoomerslingosnotsonlysasjrittenslanguagesbutsalposaspkoxensonewwwthesoriginpsofszoomerslingoscansbestracedsbacxstosthesemergencesofsonlinescommunicationsklatformpsandspocialsmediawsjithsthesripesofspmartkhonepsandstheskroliferationsofsklatformpslixesinptagramwspnakchatwsandstixtoxwszoomerpshaveshadsunkrecedentedsacceppstosasglobalsnetjorxsofskeerpwstheyshavesleveragedsthipsconnectivitystoscreatesaspharedslanguagesthatspkanpsgeograkhicsandsculturalsboundariepwszoomerslingosactpsapsaslinguipticscodesthatsbindpsthipsgenerationstogetherwsfopteringsaspenpesofscommunitysandsenablingsthemstosnavigatesthescomkleitiepsofsthesdigitalsagewwwzoomerslingowslixesanysformsofslanguagewshapsitpscriticpsandspxekticpwspomesarguesthatsthesupesofsacronympsandsplangsleadpstosasdeclinesinsgrammaticalsandslinguipticsptandardpwstheysfearsthatsthesbrevitysandsinformalitysofszoomerslingosmightshinderseffectivescommunicationsandsunderminestraditionalslanguagespxillpwshojeverwsotherpsarguesthatszoomerslingosipsasnaturalsadaktationstosthesfaptwkacedsandsevolvingsnaturesofsmodernscommunicationwsitsreflectpsthesabilitystosquicxlysdecikhersandskroceppsinformationwsmaxingsitsasvaluablespxillsinsthesdigitalsagewwwfurthermorewszoomerslingosphouldsnotsbesdipmippedsapsmeresfrivolitysorsaskappingstrendwsitspervepsapsaskojerfulstoolsforspelfwekreppionwscreativitywsandsculturalsidentityws?uptsapskrevioupsgenerationpsdevelokedstheirsuniqueslinguipticsptylepwszoomerpshavesembracedstheirsojnsformsofscommunicationwsphakingsitstospuitstheirsneedpsandsapkirationpwszoomerslingosallojpsthemstosekreppstheirsthoughtpwsemotionpwsandsekeriencepsinsasjaysthatsreponatepsjithstheirskeerpwscreatingsaspenpesofsbelongingsandspharedsunderptandingwwwmoreoverwszoomerslingoshapstranpcendedsitpsgenerationalsboundariepsandshapsinfluencedsmainptreamslanguagesandsculturewsmanyszoomersekreppionpsandsplangstermpshavesenteredsthesleiconsofsoldersgenerationpwsleadingstosintergenerationalslinguipticsechangewsthipscroppwkollinationsofslanguagesunderpcorepstheskojersandsinfluencesofszoomerslingosapsasculturalsforcewwwinsconclupionwszoomerslingosipsasvibrantsandsdynamicsformsofscommunicationsthatsreflectpsthesekeriencepwsculturewsandsapkirationpsofsgenerationszwsitsipscharacterizedsbysbrevitywsacronympwsplangwsmemepwsandsansinherentsunderptandingsofsthesdigitalslandpcakewsjhilespomesmaysviejsitsapsasdekarturesfromstraditionalslanguagesnormpwszoomerslingosipsansekreppionsofslinguipticsadaktationstosthesrealitiepsofsthesdigitalsagewsitsfopterpsaspenpesofscommunitywsallojpsforspelfwekreppionwsandsinfluencepsmainptreamslanguagesandsculturewsapszoomerpscontinuestosphakesthesjorldsaroundsthemwstheirsuniquesvernacularsjillsundoubtedlysevolvesandsleavesaslaptingsimkactsonstheslinguipt*cslandpcakesofsthesfuturew'

    # dec = dec.replace('s', ' '),
    f3 = open('dec.txt', 'w').write(dec)
    
    # flag: uscg{understandingtakesfrequentstudies}

                



def main():
    sandbox()

if __name__ == '__main__':
    main()
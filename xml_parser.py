from xml.dom import minidom


def get_config_xml(cfg_file):
    xml_doc = minidom.parse(cfg_file)
    keyword_list = xml_doc.getElementsByTagName('command')
    dns_list = xml_doc.getElementsByTagName('dns')

    dns = []
    words = []
    for i, s in enumerate(keyword_list):
        tmp = s.attributes['name'].value
        words.append(tmp)
        print("keyword{} : {}".format(i+1, tmp))

    for i, s in enumerate(dns_list):
        tmp = s.attributes['address'].value
        dns.append(tmp)
        print("dns address{} : {}".format(i+1, tmp))
    
    return dns, words


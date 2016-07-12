from igo.igo_xml import createXML, createXMLException

try:
    carrier = 'bankers'
    product = 'medsupp'
    plan = 'CPL-GR-A830'
    state = 'WI'

    full_path = createXML(carrier, product, state, plan, verbose=True)

    print('full_path:', full_path)
except createXMLException as e:
    print(e)

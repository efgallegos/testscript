from igo.igo_xml import createXML, createXMLException

try:
    carrier = 'bankers'
    product = 'fuwl'
    plan = '19E'
    state = 'AK'

    full_path = createXML(carrier, product, state, plan, verbose=True)

    print('full_path:', full_path)
except createXMLException as e:
    print(e)

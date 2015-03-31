from igo.igo_xml import createXML, createXMLException

try:

    product = 'cb'
    plan = 'GR-G220'
    state = 'AL'

    full_path = createXML(product, state, plan, verbose=True)

    print('full_path:', full_path)
except createXMLException as e:
    print(e)

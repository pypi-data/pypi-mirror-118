import re

def fn_gstin(gstin=None):
    try:
        if gstin is None:
            return ('No GSTIN provided')
        else:
            pattern = re.compile(r'(\d{2})([a-zA-Z]{5}\d{4}[a-zA-Z]{1})[1-9a-zA-Z]{1}[zZ]{1}[a-zA-Z\d]{1}')
            gst = re.search(pattern, gstin)
            if gst:
                return gst.group(2)
            else:
                return ('Check input GSTIN format')
    except Exception as e:
        raise Exception("Something went wrong while getting gstin details\n" + str(e))


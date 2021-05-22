from .utils import seqIdtoDict

def createDocument(elements, sequence):
    document = ""
    for seq_id in sequence:
        for element in elements: 
            if seq_id == element.seq_id:
                seq_id_parsed = seqIdtoDict(seq_id)
                if seq_id_parsed['seq_tag_role'] == "1":
                    document += element.with_attributes
                elif seq_id_parsed['seq_tag_role'] == "2":
                    pass
                else: 
                    pass
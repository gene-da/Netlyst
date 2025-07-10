from Netlist.Classes.Base.SpiceElement import*
"""
.model mname type(pname1=pval1 pname2=pval2 ... )
"""
class MODEL(SpiceElement):
    def __init__(self, name: str, type: str, mod: str):
        self.name = name
        self.type = type
        self.mod = mod
    
    def to_string(self):
        return f'.model {self.name} {self.type} {self.mod}'
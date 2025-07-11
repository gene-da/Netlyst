from Netlist.Classes.Base.SpiceElement import*
"""
.model mname type(pname1=pval1 pname2=pval2 ... )
"""
class MODEL(SpiceElement):
    def __init__(self, name: str, type: str, mod: str):
        self.name = name
        self.type = type
        self.mod = mod  # raw model string

    def to_string(self):
        cmd = '.model'
        header = f'{cmd:<8} {self.name:<8} {self.type:<8}'
        lines = [header]
        current_line = "+"

        for token in self.mod.split():
            # wrap once we exceed 40 characters on a line
            if len(current_line) + len(token) + 1 > 40:
                lines.append(current_line)
                current_line = "+"
            current_line += f" {token}"

        if current_line.strip() != "+":
            lines.append(current_line)

        return "\n".join(lines)

           
class CModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
        
class DModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)

class FModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
        
class GModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
        
class IModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
        
class JModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
        
class LModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
        
class MModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
        
class QModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
        

        
class XModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
        
class ZModel(MODEL):
    def __init__(self, name, type, mod):
        super().__init__(name, type, mod)
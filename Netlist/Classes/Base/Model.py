from Netlist.Classes.Base.SpiceElement import*
"""
.model mname type(pname1=pval1 pname2=pval2 ... )
"""
class MODEL(SpiceElement):
    def __init__(self, name: str, type: str, mod: str, doc: Optional[str] = None) -> None:
        self.name = name
        self.type = type
        self.mod = mod  # raw model string
        self._doc = doc
        super().__init__()

    def to_string(self):
        doc_line = f"* {self._doc}" if self._doc else ""
        cmd = '.model'
        header = f'{cmd:<8} {self.name:<8} {self.type:<8}'
        lines = [header]
        current_line = "+"

        for token in self.mod.split():
            if len(current_line) + len(token) + 1 > 40:
                lines.append(current_line)
                current_line = "+"
            current_line += f" {token}"

        if current_line.strip() != "+":
            lines.append(current_line)

        model_block = "\n".join(lines)
        return f"{doc_line}\n{model_block}" if doc_line else model_block

    def to_line(self):
        doc_line = f"* {self._doc}" if self._doc else ""
        model_line = f".MODEL {self.name} {self.type} ({self.mod})"
        return f"{doc_line}\n{model_line}" if doc_line else model_line

           
# class CModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
        
# class DModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)

# class FModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
        
# class GModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
        
# class IModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
        
# class JModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
        
# class LModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
        
# class MModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
        
# class QModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
        

        
# class XModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
        
# class ZModel(MODEL):
#     def __init__(self, name, type, mod):
#         super().__init__(name, type, mod)
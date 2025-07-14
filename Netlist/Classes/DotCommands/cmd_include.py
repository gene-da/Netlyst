from Netlist.Components import SpiceElement

class INCLUDE(SpiceElement):
    """
    Represents an INCLUDE directive in a SPICE netlist.
    This is used to include external files or libraries in the netlist.
    """
    
    def __init__(self, filename, doc=None):
        super().__init__(doc=doc)
        self.filename = filename

    def to_string(self):
        return f".INCLUDE '{self.filename}'" + (f" ; {self.doc}" if self.doc else "")
    
    def to_line(self):
        return self.to_string()
    
class INCPSLT(SpiceElement):
    """
    Represents an INCLUDE directive for a SPICE library.
    This is used to include a specific SPICE library file.
    """
    
    def __init__(self, filename, doc=None):
        super().__init__(doc=doc)
        self.filename = filename

    def to_string(self):
        return f".INCPSLT '{self.filename}'" + (f" ; {self.doc}" if self.doc else "")
    
    def to_line(self):
        return self.to_string()
    
class LIB(SpiceElement):
    """
    Represents a LIB directive in a SPICE netlist.
    This is used to include a library of models or components.
    """
    
    def __init__(self, filename, doc=None):
        super().__init__(doc=doc)
        self.filename = filename

    def to_string(self):
        return f".LIB '{self.filename}'" + (f" ; {self.doc}" if self.doc else "")
    
    def to_line(self):
        return self.to_string()